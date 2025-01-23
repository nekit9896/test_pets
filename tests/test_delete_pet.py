import allure
import pytest
from assertpy import assert_that

from data.constants import FAKE_PET_ID
from request_logic.logic import client


@allure.suite("DeletePet")
@allure.feature("positive")
@allure.title("Удаление питомца по id")
@allure.description("Тестирование успешного удаления питомца по id")
@pytest.mark.parametrize(
    "custom_pet_object",
    [
        {
            "pet_id": 777777,
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
def test_delete_pet_success(custom_pet_object):
    with allure.step("Создание питомца"):
        client.create_pets(custom_pet_object)

    with allure.step("Удаление питомца"):
        pet_id = custom_pet_object["id"]
        deleted_pet = client.delete_pets(pet_id, need_check_status_code=False)

    with allure.step("Проверка удаления питомца"):
        assert_that(
            int(deleted_pet["message"]),
            "Питомец не создан с корректным именем",
        ).is_equal_to(pet_id)


@allure.suite("DeletePet")
@allure.feature("negative")
@allure.title("Удаление питомца по несуществующему id")
@allure.description("Тестирование удаления питомца, которого нет в базе")
def test_delete_pet_fail():
    """
    Попробуем мягко удалить питомца, если он вдруг существует.
    Далее когда мы точно уверены, что питомца нет в базе, проверим код ответа 404 при удалении несуществующего питомца
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

    with allure.step("Удаление питомца по ненастоящему айди"):
        client.delete_pets(pet_id, expected_status_code=404)
