"""
Модуль для унифицированного представления результатов операций.

Класс `Result` используется для преобразования различных источников данных
(например, исключений, ORM-запросов, списков) в стандартизированный формат.

Основные возможности:
- Единый формат ответа с атрибутами `is_success`, `data`, `errors`, `meta`.
- Автоматическое логирование ошибок.
- Поддержка ORM QuerySet, списков, словарей и исключений.

Пример использования:
    >>> result = Result.success(data={"id": 1}, meta={"info": "test"})
    >>> print(result.to_dict())
    {'is_success': True, 'data': {'id': 1}, 'errors': [], 'meta': {'info': 'test'}}

    >>> result = Result.failure(errors="Something went wrong")
    >>> print(result.to_dict())
    {'is_success': False, 'data': {}, 'errors': ['Something went wrong'], 'meta': {}}
"""

import traceback
from typing import Any, Dict, List, Optional, Union

from django.conf import settings


class Result:
    """
    Унифицированный класс для представления результата выполнения операции.

    Основная задача: преобразовать исходные данные (исключения, ORM-запросы, списки и т.д.)
    в стандартизированный формат с атрибутами `is_success`, `data`, `errors`, и `meta`.

    Attributes:
        is_success (bool): Флаг успешности операции.
        data (Union[Dict, List]): Данные результата (если операция успешна).
        errors (List[str]): Список ошибок (если операция завершилась неудачей).
        meta (Dict): Дополнительные метаданные (например, отладочная информация).
    """

    def __init__(self, source: Optional[Any] = None) -> None:
        """
        Инициализация объекта Result. Если передан источник данных (`source`),
        преобразует его в формат Result.

        Args:
            source (Any): Исходный объект для преобразования в Result.
                          Может быть словарём, исключением, QuerySet, списком и т.д.
        """
        self.is_success: bool = False
        self.data: Union[Dict, List] = {}
        self.errors: List[str] = []
        self.meta: Dict[str, Any] = {}

        if source:
            self._adapt_source(source)

    def _adapt_source(self, source: Any) -> None:
        """
        Преобразование исходного объекта в формат Result.

        Args:
            source (Any): Исходный объект для обработки.
        """
        if isinstance(source, dict):
            self._from_dict(source)
        elif isinstance(source, Exception):
            self._from_exception(source)
        elif hasattr(source, "all"):  # Предполагаем, что это QuerySet
            self._from_queryset(source)
        elif isinstance(source, list):
            self._from_list(source)
        else:
            self.errors.append("Unsupported source type")

    def _from_dict(self, source: Dict[str, Any]) -> None:
        """
        Преобразование словаря в формат Result.

        Ожидается, что словарь содержит ключи `is_success`, `data`, `errors` и `meta`.

        Args:
            source (Dict[str, Any]): Словарь с данными результата.
        """
        self.is_success = source.get("is_success", False)
        self.data = source.get("data", {})
        self.errors = source.get("errors", [])
        self.meta = source.get("meta", {})

    def _from_exception(self, source: Exception) -> None:
        """
        Преобразование исключения в формат Result.

        Args:
            source (Exception): Объект исключения.
        """
        self.is_success = False
        self.errors.append(str(source))
        self.meta = {
            "exception_type": source.__class__.__name__,
        }

        tb = traceback.format_exc().splitlines() if settings.DEBUG else []
        self.meta["traceback"] = tb

    def _from_queryset(self, source: Any) -> None:
        """
        Преобразование QuerySet (или Manager) в формат Result.

        Args:
            source (QuerySet): Django QuerySet или Manager.
        """
        try:
            self.is_success = True
            self.data = list(source.all().values())
        except Exception as e:
            self.is_success = False
            self.errors.append(str(e))

    def _from_list(self, source: List[Any]) -> None:
        """
        Преобразование списка в формат Result.

        Args:
            source (List[Any]): Список данных.
        """
        self.is_success = True
        self.data = source

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразование объекта Result в словарь.

        Returns:
            Dict[str, Any]: Словарь с атрибутами `is_success`, `data`, `errors` и `meta`.
        """
        return {
            "is_success": self.is_success,
            "data": self.data,
            "errors": self.errors,
            "meta": self.meta,
        }

    @classmethod
    def success(
        cls, data: Optional[Any] = None, meta: Optional[Dict[str, Any]] = None
    ) -> "Result":
        """
        Статический метод для создания успешного результата.

        Args:
            data (Any): Данные результата.
            meta (Dict[str, Any]): Дополнительные метаданные.

        Returns:
            Result: Объект Result с is_success=True.
        """
        instance = cls()
        instance.is_success = True
        instance.data = data or {}
        instance.meta = meta or {}
        return instance

    @classmethod
    def failure(
        cls, errors: Union[str, List[str]], meta: Optional[Dict[str, Any]] = None
    ) -> "Result":
        """
        Статический метод для создания результата с ошибками.

        Args:
            errors (Union[str, List[str]]): Ошибка или список ошибок.
            meta (Dict[str, Any]): Дополнительные метаданные.

        Returns:
            Result: Объект Result с is_success=False.
        """
        instance = cls()
        instance.is_success = False
        instance.errors = errors if isinstance(errors, list) else [errors]
        instance.meta = meta or {}
        return instance
