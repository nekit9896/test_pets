from dataclasses import asdict

import allure
import pytest

from data.pet_objects import Category, Pet, Tag
from helpers.validators import response_body_validator
from request_logic.logic import client


@allure.suite("UpdatePet")
@allure.feature("positive")
@allure.title("Обновление данных питомца")
@allure.description(
    "Тестирование успешного обновления данных питомца с валидными значениями"
)
@pytest.mark.parametrize(
    "custom_pet_object",
    [
        {
            "pet_id": 444444,
            "category_id": 20,
            "category_name": "Birds",
            "pet_name": "Spy Popug",
            "photo_urls": ["http://example.com/photo2", "http://example.com/photo3"],
            "tag_id": 20,
            "tag_name": "not_favorite_pet",
            "status": "silent-aggressive",
        },
    ],
    indirect=True,
)
def test_update_pet_success(custom_pet_object):
    with allure.step("Создание питомца"):
        client.create_pets(custom_pet_object)

    with allure.step("Обновление данных питомца"):
        # Подготовим новый объект измененными category_id и pet_name
        prepare_pet_object = Pet(
            id=444444,
            category=Category(id=30, name="Birds"),
            name="Spy Popug Hot Gorilla",
            photoUrls=["http://example.com/photo2", "http://example.com/photo3"],
            tags=[Tag(id=20, name="not_favorite_pet")],
            status="silent-aggressive",
        )
        pet = asdict(prepare_pet_object)

        updated_pet = client.update_pets(pet, need_check_status_code=False)

    with allure.step("Поиск питомца с обновленными данными"):
        get_updated_pet = client.get_pets(pet["id"])

    with allure.step("Проверка ответа ручки при обновлении данных методом PUT"):
        response_body_validator(updated_pet, pet)

    with allure.step(
        "Проверка, что тестируемый питомец находится в бд с обновленными данными"
    ):
        response_body_validator(get_updated_pet, pet)


@allure.suite("UpdatePet")
@allure.feature("positive")
@allure.title("Ошибка при обновлении данных")
@allure.description("Тестирование обновления данных питомца с некорректными данными")
@pytest.mark.parametrize(
    "custom_pet_object",
    [
        {
            "pet_id": 444444,
            "category_id": 20,
            "category_name": "Birds",
            "pet_name": "Spy Popug",
            "photo_urls": ["http://example.com/photo2", "http://example.com/photo3"],
            "tag_id": 20,
            "tag_name": "not_favorite_pet",
            "status": "silent-aggressive",
        },
    ],
    indirect=True,
)
def test_update_pet_fail(custom_pet_object):
    """
    400	Invalid ID supplied - этот ответ должен быть отправлен сервером, если передаваемый ID имеет неверный формат.
    Если API ожидает число (например 444444), а мы пеередаем его списком со строкой ['444444'], но в ответ прилетает 500
    В результате тест ожидаемо падает из-за бага
    """
    with allure.step("Создание питомца"):
        client.create_pets(custom_pet_object)

    with allure.step(
        "Обновление данных питомца с некорректными данными и проверка статус кода"
    ):
        # Подготовим новый объект измененными category_id и pet_name
        prepare_pet_object = Pet(
            id=444444,
            category=Category(id=30, name="Birds"),
            name="Spy Popug Hot Gorilla",
            photoUrls=["http://example.com/photo2", "http://example.com/photo3"],
            tags=[Tag(id=20, name="not_favorite_pet")],
            status="silent-aggressive",
        )

        pet = asdict(prepare_pet_object)
        pet["id"] = ["444444"]
        client.update_pets(pet, expected_status_code=400)
