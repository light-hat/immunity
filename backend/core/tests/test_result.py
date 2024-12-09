"""
Модульные тесты для CQRS-адаптера.
"""

import pytest
from core.result import Result


@pytest.mark.django_db
def test_init_with_dict_success():
    """Проверка успешной инициализации с источником-словарём."""

    source = {
        "is_success": True,
        "data": {"key": "value"},
        "errors": [],
        "meta": {"info": "test"},
    }
    result = Result(source)

    assert result.is_success is True
    assert result.data == {"key": "value"}
    assert result.errors == []
    assert result.meta == {"info": "test"}


@pytest.mark.django_db
def test_init_with_dict_failure():
    """Проверка инициализации с ошибочным словарём."""

    source = {
        "is_success": False,
        "data": {},
        "errors": ["Something went wrong"],
        "meta": {},
    }
    result = Result(source)

    assert result.is_success is False
    assert result.errors == ["Something went wrong"]
    assert result.data == {}
    assert result.meta == {}


@pytest.mark.django_db
def test_init_with_exception():
    """Проверка инициализации с объектом исключения."""

    exception = ValueError("Test exception")
    result = Result(exception)

    assert result.is_success is False
    assert "Test exception" in result.errors
    assert result.meta["exception_type"] == "ValueError"


@pytest.mark.django_db
def test_init_with_queryset_success(mocker):
    """Проверка преобразования QuerySet в Result."""

    mock_queryset = mocker.MagicMock()
    mock_queryset.all.return_value.values.return_value = [{"id": 1, "name": "Test"}]

    result = Result(mock_queryset)

    assert result.is_success is True
    assert result.data == [{"id": 1, "name": "Test"}]
    mock_queryset.all.assert_called_once()


@pytest.mark.django_db
def test_init_with_queryset_failure(mocker):
    """Проверка обработки исключения при работе с QuerySet."""

    mock_queryset = mocker.MagicMock()
    mock_queryset.all.side_effect = Exception("Database error")

    result = Result(mock_queryset)

    assert result.is_success is False
    assert "Database error" in result.errors


@pytest.mark.django_db
def test_init_with_list():
    """Проверка преобразования списка в Result."""

    source = [{"id": 1, "name": "Item1"}, {"id": 2, "name": "Item2"}]
    result = Result(source)

    assert result.is_success is True
    assert result.data == source


@pytest.mark.django_db
def test_unsupported_source():
    """Проверка обработки неподдерживаемого типа источника."""

    source = 12345  # Неподдерживаемый тип
    result = Result(source)

    assert result.is_success is False
    assert "Unsupported source type" in result.errors


@pytest.mark.django_db
def test_to_dict():
    """Проверка преобразования Result в словарь."""

    result = Result.success(data={"key": "value"}, meta={"info": "test"})

    result_dict = result.to_dict()
    expected_dict = {
        "is_success": True,
        "data": {"key": "value"},
        "errors": [],
        "meta": {"info": "test"},
    }

    assert result_dict == expected_dict


@pytest.mark.django_db
def test_success_static_method():
    """Проверка статического метода success."""

    result = Result.success(data={"key": "value"}, meta={"info": "test"})

    assert result.is_success is True
    assert result.data == {"key": "value"}
    assert result.meta == {"info": "test"}


@pytest.mark.django_db
def test_failure_static_method():
    """Проверка статического метода failure."""

    result = Result.failure(errors=["Something went wrong"], meta={"info": "test"})

    assert result.is_success is False
    assert result.errors == ["Something went wrong"]
    assert result.meta == {"info": "test"}
