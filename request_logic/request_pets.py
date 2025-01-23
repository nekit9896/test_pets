import logging

import requests

logger = logging.getLogger(__name__)


class RequestPets:
    """
    RequestPets - базовый класс для выполнения HTTP-запросов с проверкой статуса в методах запроса,
    т к ручек может быть много и для каждой ручки делать проверку статус кода = много дублирования.
    Плюс сюда можно добавлять обертки для подсчета покрытия
    """

    def __init__(self, base_url: str):
        self.base_url = base_url

    def modify_post(
        self,
        handler: str,
        data: dict,
        need_check_status_code: bool = True,
        expected_status_code: int = 200,
    ):
        """
        Метод принимает конечный path, делает post запрос и проверяет статус код
        """
        response = requests.post(f"{self.base_url}{handler}", json=data)
        # Сделаем проверку статус кода опциональной, чтобы в определенных случаях можно было выключить
        if need_check_status_code:
            # Чтобы АТ помечались broken - желтым в аллюре, т к до проверки в тесте мы так и не дошли, если упали тут:
            if response.status_code != expected_status_code:
                raise ValueError(
                    f"Ожидался статус код {expected_status_code}, но получен {response.status_code}"
                )
            # Добавим логирование запроса в stdout для комфорта
            logger.info(
                f"Отправка POST запроса на {self.base_url}{handler} с данными {data}"
            )

        return response

    def modify_get(
        self,
        handler: str,
        need_check_status_code: bool = True,
        expected_status_code: int = 200,
    ):
        """
        Метод принимает конечный path, делает гет запрос и проверяет статус код
        """
        response = requests.get(f"{self.base_url}{handler}")
        # Сделаем проверку статус кода опциональной, чтобы в определенных случаях можно было выключить
        if need_check_status_code:
            # Чтобы АТ помечались broken - желтым в аллюре, т к до проверки в тесте мы так и не дошли, если упали тут:
            if response.status_code != expected_status_code:
                raise ValueError(
                    f"Ожидался статус код {expected_status_code}, но получен {response.status_code}"
                )
            # Добавим логирование запроса в stdout для комфорта
            logger.info(
                f"Отправка GET запроса на {self.base_url}{handler} по айди животного"
            )
        return response

    def modify_put(
        self,
        handler: str,
        data: dict,
        need_check_status_code: bool = True,
        expected_status_code: int = 200,
    ):
        """
        Метод принимает конечный path, делает put запрос и проверяет статус код
        """
        response = requests.put(f"{self.base_url}{handler}", json=data)
        # Сделаем проверку статус кода опциональной, чтобы в определенных случаях можно было выключить
        if need_check_status_code:
            # Чтобы АТ помечались broken - желтым в аллюре, т к до проверки в тесте мы так и не дошли, если упали тут:
            if response.status_code != expected_status_code:
                raise ValueError(
                    f"Ожидался статус код {expected_status_code}, но получен {response.status_code}"
                )
            # Добавим логирование запроса в stdout для комфорта
            logger.info(
                f"Отправка PUT запроса на {self.base_url}{handler} с данными {data}"
            )
        return response

    def modify_delete(
        self,
        handler: str,
        pet_id: int,
        need_check_status_code: bool = True,
        expected_status_code: int = 200,
    ):
        """
        Метод принимает конечный path, делает delete запрос и проверяет статус код
        """
        response = requests.delete(f"{self.base_url}{handler}/{pet_id}")
        # Сделаем проверку статус кода опциональной, чтобы в определенных случаях можно было выключить
        if need_check_status_code:
            # Чтобы АТ помечались broken - желтым в аллюре, т к до проверки в тесте мы так и не дошли, если упали тут:
            if response.status_code != expected_status_code:
                raise ValueError(
                    f"Ожидался статус код {expected_status_code}, но получен {response.status_code}"
                )
            # Добавим логирование запроса в stdout для комфорта
            logger.info(
                f"Отправка DELETE запроса на {self.base_url}{handler} по айди животного"
            )
        return response
