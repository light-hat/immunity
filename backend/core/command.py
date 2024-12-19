"""
CQRS команда.
"""

import logging

from django.db import models, transaction
from django.forms.models import model_to_dict

from core.result import Result

logger = logging.getLogger(__name__)


class Command:
    """
    Универсальная команда для выполнения CUD-операций над любой
    моделью Django с поддержкой Foreign Key.
    """

    def __init__(
        self,
        model: models.Model,
        entity_id: int = None,
        data: dict = None,
        foreign_keys: dict = None,
    ):
        """
        Конструктор команды.

        :param model: Django модель, с которой будет работать команда.
        :param entity_id: ID сущности (для Update/Delete операций).
        :param data: Данные для создания или обновления сущности.
        :param foreign_keys: Словарь внешних ключей, где ключ — поле модели,
        а значение — ID связанной модели.
        """
        self.model = model
        self.entity_id = entity_id
        self.data = data or {}
        self.foreign_keys = foreign_keys or {}

    def _resolve_foreign_keys(self):
        """
        Резолвинг внешних ключей.

        :return: Обновленные данные с привязанными внешними объектами.
        """
        resolved_data = self.data.copy()
        for field, related_id in self.foreign_keys.items():
            try:
                related_model = self.model._meta.get_field(
                    field
                ).remote_field.model  # pytest: ignore-protected-access
                related_instance = related_model.objects.get(id=related_id)
                resolved_data[field] = related_instance
            except Exception as e:
                raise ValueError(
                    f"Ошибка внешнего ключа {field} объекта с идентификатором {related_id}: {e}"
                )
        return resolved_data

    def create(self):
        """
        Создание новой сущности с поддержкой внешних ключей.

        :return: Result с данными о созданной сущности.
        """
        try:
            with transaction.atomic():
                resolved_data = self._resolve_foreign_keys()
                entity = self.model.objects.create(**resolved_data)
                return Result.success(
                    data={"id": str(entity.id), "details": model_to_dict(entity)}
                )
        except Exception as e:
            return Result.failure(errors=str(e))

    def update(self):
        """
        Обновление существующей сущности с поддержкой внешних ключей.

        :return: Result с данными об обновленной сущности.
        """
        if not self.entity_id:
            return Result.failure(errors="Требуется указать ID сущности.")

        try:
            with transaction.atomic():
                entity = self.model.objects.get(id=self.entity_id)
                resolved_data = self._resolve_foreign_keys()
                for field, value in resolved_data.items():
                    setattr(entity, field, value)
                entity.save()
                return Result.success(
                    data={"id": str(entity.id), "details": model_to_dict(entity)}
                )
        except self.model.DoesNotExist:
            return Result.failure(
                errors=f"Сущности с ID {self.entity_id} не существует."
            )
        except Exception as e:
            return Result.failure(errors=str(e))

    def delete(self):
        """
        Удаление существующей сущности.
        :return: Result с данными об удаленной сущности.
        """
        if not self.entity_id:
            return Result.failure(errors="Требуется указать ID сущности.")

        try:
            with transaction.atomic():
                entity = self.model.objects.get(id=self.entity_id)
                entity.delete()
                return Result.success()
        except self.model.DoesNotExist:
            return Result.failure(
                errors=f"Сущности с ID {self.entity_id} не существует."
            )
        except Exception as e:
            return Result.failure(errors=str(e))
