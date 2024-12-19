"""
Модульные тесты для CQRS-адаптера.
"""

from unittest.mock import MagicMock

import pytest

from core.result import Result


def test_success_result():
    """Проверяем успешное создание результата."""

    result = Result.success(data={"id": 1}, meta={"info": "test"})

    assert result.is_success is True
    assert result.data == {"id": 1}
    assert result.meta == {"info": "test"}
    assert result.errors == []


def test_failure_result():
    """Проверяем создание результата с ошибкой."""

    result = Result.failure(errors="Something went wrong")

    assert result.is_success is False
    assert result.data == {}
    assert result.errors == ["Something went wrong"]
    assert result.meta == {}


def test_to_dict_method():
    """Проверяем преобразование объекта в словарь."""

    result = Result.success(data={"key": "value"}, meta={"info": "debug"})

    result_dict = result.to_dict()
    assert result_dict == {
        "is_success": True,
        "data": {"key": "value"},
        "errors": [],
        "meta": {"info": "debug"},
    }


def test_adapt_exception():
    """Проверяем обработку исключения в Result."""

    try:
        raise ValueError("Test exception")
    except ValueError as e:
        result = Result.failure(errors=str(e))

    assert result.is_success is False
    assert result.errors == ["Test exception"]
    assert "traceback" not in result.meta or isinstance(result.meta["traceback"], list)


def test_adapt_list():
    """Проверяем преобразование списка."""

    result = Result()
    result._adapt_source([1, 2, 3])
    assert result.is_success is True
    assert result.data == [1, 2, 3]
    assert result.errors == []


def test_adapt_dict():
    """Проверяем преобразование словаря."""

    source = {
        "is_success": True,
        "data": {"id": 1},
        "errors": [],
        "meta": {"info": "test"},
    }

    result = Result()
    result._adapt_source(source)
    assert result.is_success is True
    assert result.data == {"id": 1}
    assert result.meta == {"info": "test"}
    assert result.errors == []


def test_adapt_unsupported_source():
    """Проверяем обработку неподдерживаемого источника."""

    result = Result()
    result._adapt_source(123)  # Неподдерживаемый тип

    assert result.is_success is False
    assert "Unsupported source type" in result.errors


def test_adapt_queryset():
    """Проверяем обработку QuerySet."""

    mock_queryset = MagicMock()
    mock_queryset.all.return_value.values.return_value = [{"id": 1}, {"id": 2}]
    result = Result()
    result._adapt_source(mock_queryset)

    assert result.is_success is True
    assert result.data == [{"id": 1}, {"id": 2}]
    assert result.errors == []
