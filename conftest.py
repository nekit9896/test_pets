from dataclasses import asdict

import allure
import pytest

from data.pet_objects import Category, Pet, Tag
from request_logic.logic import client


@pytest.fixture
def custom_pet_object(request):
    """
    Фикстура получает значение из параметризованного списка в автотесте через объект request, предоставленный pytest.
    """
    with allure.step("Формирование объекта с атрибутами питомца"):
        params = request.param
        pet = Pet(
            id=params.get("pet_id"),
            category=Category(
                id=params.get("category_id"), name=params.get("category_name")
            ),
            name=params.get("pet_name"),
            photoUrls=params.get("photo_urls"),
            tags=[Tag(id=params.get("tag_id"), name=params.get("tag_name"))],
            status=params.get("status"),
        )

    yield asdict(pet)

    with allure.step("Удаление питомца после каждого запуска тестов"):
        pet_id = params.get("pet_id")
        try:
            response = client.delete_pets(pet_id, need_check_status_code=False)
            if response.status_code == 404:
                # Логирование о том, что питомец не найден
                allure.attach(
                    f"Питомец с ID {pet_id} не найден: {response.text}",
                    name="INFO",
                    attachment_type=allure.attachment_type.TEXT,
                )
        except Exception as e:
            # Обработка исключения без использования переменной response
            error_message = str(e)  # Получаем текст ошибки из исключения
            allure.attach(
                f"Ошибка при удалении питомца: {error_message}",
                name="ERROR",
                attachment_type=allure.attachment_type.TEXT,
            )
