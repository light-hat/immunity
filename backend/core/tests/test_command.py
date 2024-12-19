'''"""
Модульные тесты для тестирования CQRS-команд.
"""

import pytest
import json
from core.command import Command
from core.models import Project


@pytest.fixture
def load_test_data(request):
    """
    Загрузить данные из JSON-файла.
    request.param должен содержать путь к JSON-файлу.
    """
    file_path = request.param
    with open(file_path, "r") as f:
        return json.load(f)

@pytest.mark.django_db
@pytest.mark.parametrize(
    "model, load_test_data",
    [
        (Project, "core/tests/fixtures/project.json"),
    ],
    indirect=["load_test_data"]
)
def test_create_valid(mocker, model, load_test_data):
    """
    Тест на успешное создание сущности.
    """
    data = load_test_data["create"]["valid"]["data"]
    foreign_keys = load_test_data["create"]["valid"]["foreign_keys"]

    mock_entity = mocker.MagicMock(spec=model)
    mock_entity.id = 1
    mocker.patch(f"core.models.{model.__name__}.objects.create", return_value=mock_entity)

    command = Command(model=model, data=data, foreign_keys=foreign_keys)
    result = command.create()
    print(result.to_dict())

    #model.objects.create.assert_called_once_with(**data)

    #assert result.is_success is True
    assert result.data == {"id": mock_entity.id, "details": mock_entity}
'''
