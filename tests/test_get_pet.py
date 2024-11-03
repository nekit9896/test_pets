import allure
import pytest

from PetsTests.data.constants import FAKE_PET_ID
from PetsTests.helpers.validators import response_body_validator
from PetsTests.request_logic.logic import client


@allure.suite("GetPet")
@allure.feature("positive")
@allure.title("Получение питомца по id")
@allure.description("Тестирование успешного получения питомца по id")
@pytest.mark.parametrize(
    "custom_pet_object",
    [
        {
            "pet_id": 333333,
            "category_id": 10,
            "category_name": "Dogs",
            "pet_name": "Dry Joe",
            "photo_urls": ["http://example.com/photo1"],
            "tag_id": 10,
            "tag_name": "favorite_pet",
            "status": "active",
        }
    ],
    indirect=True,
)
def test_get_pet_success(custom_pet_object):
    with allure.step("Создание питомца"):
        created_pet = client.create_pets(custom_pet_object)

    with allure.step("Получение питомца по айди"):
        pet_id = created_pet["id"]
        got_pet = client.get_pets(pet_id)

    with allure.step("Проверка атрибутов найденного питомца"):
        response_body_validator(got_pet, custom_pet_object)


@allure.suite("GetPet")
@allure.feature("negative")
@allure.title("Получение питомца по несуществующему id")
@allure.description("Тестирование получения питомца по несуществующему id")
def test_fail_get_pet():
    """
    Попробуем удалить питомца, если он существует, а потом попробуем получить его по айди после удаления
    """
    with allure.step("Удаление питомца"):
        pet_id = FAKE_PET_ID
        try:
            response = client.delete_pets(pet_id, need_check_status_code=False)
            if response["code"] == 404:
                # Логирование о том, что питомец не найден, может быть полезным
                allure.attach(
                    f"Питомец с ID {pet_id} не найден: {response['message']}. Нечего удалять",
                    name="INFO",
                    attachment_type=allure.attachment_type.TEXT,
                )
        except Exception as e:
            # Логирование ошибки, если что-то пошло не так
            allure.attach(
                f"Ошибка при удалении питомца: {response['message'], str(e)}",
                name="ERROR",
                attachment_type=allure.attachment_type.TEXT,
            )

    with allure.step("Попытка получения питомца по удаленному айди"):
        client.get_pets(pet_id, expected_status_code=404)
