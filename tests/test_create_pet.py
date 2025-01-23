import allure
import pytest

from helpers.validators import response_body_validator
from request_logic.logic import client


@allure.suite("CreatePet")
@allure.feature("positive")
@allure.title("Создание питомца")
@allure.description("Тест успешного создания питомца с валидными данными")
@pytest.mark.parametrize(
    "custom_pet_object",
    [
        {
            "pet_id": 111111,
            "category_id": 10,
            "category_name": "Dogs",
            "pet_name": "Dry Joe",
            "photo_urls": ["http://example.com/photo1"],
            "tag_id": 10,
            "tag_name": "favorite_pet",
            "status": "active",
        },
        {
            "pet_id": 222222,
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
def test_create_pet_success(custom_pet_object):
    with allure.step("Создание питомца"):
        created_pet = client.create_pets(custom_pet_object)

    with allure.step("Проверка атрибутов созданного питомца"):
        response_body_validator(created_pet, custom_pet_object)


@allure.suite("CreatePet")
@allure.feature("negative")
@allure.title("Создание питомца с невалидными данными")
@allure.description("Негативный тест создания питомца с невалидными данными")
@pytest.mark.parametrize(
    "custom_pet_object",
    [
        {
            "pet_id": "-1",
            "category_id": None,
            "category_name": None,
            "pet_name": None,
            "photo_urls": [],
            "tag_id": None,
            "tag_name": None,
            "status": None,
        },
        {
            "pet_id": "invalid",
            "category_id": None,
            "category_name": None,
            "pet_name": None,
            "photo_urls": [],
            "tag_id": None,
            "tag_name": None,
            "status": None,
        },
    ],
    indirect=True,
)
def test_create_pet_invalid_data(custom_pet_object):
    """
    1) Тест падает в первом случае, т к сервер возвращает 200(бага), по идее ожидается 400 Bad Request, айдишники всегда
    делают от 0 и так далее до бесконечности
    2) Тест падает во втором случае, т к сервер возвращает 500(бага), по идее ожидается 400 Bad Request
    3) В документации ошибка: "405	Invalid input" - на самом деле это Method Not Allowed
    4) При создании зверька с pet_id = 0 в ответе возвращается pet_id != 0 (бага), ожидается pet_id = 0
    """
    with allure.step("Создание питомца c невалидными данными"):
        client.create_pets(custom_pet_object, expected_status_code=400)
