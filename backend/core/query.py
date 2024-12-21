"""
CQRS запрос.
"""

import math
from functools import reduce
from operator import or_
from typing import Any, Dict, List, Optional, Union

from django.db.models import F, Q
from django.forms.models import model_to_dict

from core.result import Result


class Query:
    """
    Универсальный CQRS-запрос для работы с любой Django-моделью.
    """

    def __init__(self, model):
        """
        Инициализация универсального запроса.

        :param model: Django-модель, с которой работает запрос.
        """
        self.model = model

    def get_by_id(self, entity_id: Any) -> Result:
        """
        Получить одну запись по ID.

        :param entity_id: ID сущности.
        :return: Result с объектом или ошибкой.
        """
        try:
            entity = self.model.objects.get(id=entity_id)
            return Result.success(data=model_to_dict(entity))
        except self.model.DoesNotExist:
            return Result.failure(errors=f"Entity with ID {entity_id} does not exist.")
        except Exception as e:
            return Result.failure(errors=str(e))

    def convert_queryset_to_list(self, queryset: List[Any]) -> List[Dict[str, Any]]:
        """
        Преобразовать QuerySet в список словарей.
        """
        return [model_to_dict(entity) for entity in queryset]

    def filter(
        self,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[List[str]] = None,
        pagination: Optional[Dict[str, int]] = None,
    ) -> Result:
        """
        Получить список записей с фильтрацией, сортировкой и пагинацией.

        :param filters: Словарь фильтров для QuerySet.
        :param order_by: Список полей для сортировки.
        :param pagination: Параметры пагинации: {"page": int, "page_size": int}.
        :return: Result с QuerySet или ошибкой.
        """
        try:
            conditions = [Q(**{k: v}) for k, v in filters.items()]

            if conditions:
                qs = self.model.objects.filter(reduce(or_, conditions))
            else:
                qs = self.model.objects.all()

            # Сортировка
            if order_by:
                qs = qs.order_by(*order_by)

            # Пагинация
            if pagination:
                page = pagination.get("page", 1)
                page_size = pagination.get("page_size", 10)
                start = (page - 1) * page_size
                end = start + page_size
                qs = qs[start:end]
                count = qs.count()
                pagination_count = math.ceil(count / page_size)

            return Result.success(
                data=list(qs.values()),
                meta={
                    "page": page,
                    "page_size": page_size,
                    "pages_count": pagination_count,
                    "objects_count": count,
                },
            )
        except Exception as e:
            return Result.failure(errors=str(e))

    def all(self, order_by: Optional[List[str]] = None) -> Result:
        """
        Получить все записи.

        :param order_by: Список полей для сортировки.
        :return: Result с QuerySet.
        """
        try:
            qs = self.model.objects.all()
            if order_by:
                qs = qs.order_by(*order_by)
            return Result.success(data=list(qs.values()))
        except Exception as e:
            return Result.failure(errors=str(e))
