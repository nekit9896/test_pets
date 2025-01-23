from data.constants import BASE_URL
from request_logic.request_pets import RequestPets


class Logic(RequestPets):
    """
    Logic расширяет RequestPets и реализует конкретные методы API для работы с "pets"
    Ручек, как правило, больше чем рестовых методов, поэтому вынесено в Logic
    """

    def create_pets(
        self,
        data: dict,
        need_check_status_code: bool = True,
        expected_status_code: int = 200,
    ):
        response = self.modify_post(
            "/pet", data, need_check_status_code, expected_status_code
        )
        return response.json()

    def get_pets(
        self,
        pet_id: int,
        need_check_status_code: bool = True,
        expected_status_code: int = 200,
    ):
        response = self.modify_get(
            f"/pet/{pet_id}", need_check_status_code, expected_status_code
        )
        return response.json()

    def update_pets(
        self,
        data: dict,
        need_check_status_code: bool = True,
        expected_status_code: int = 200,
    ):
        response = self.modify_put(
            "/pet", data, need_check_status_code, expected_status_code
        )
        return response.json()

    def delete_pets(
        self,
        pet_id: int,
        need_check_status_code: bool = True,
        expected_status_code: int = 200,
    ):
        response = self.modify_delete(
            "/pet", pet_id, need_check_status_code, expected_status_code
        )
        return response.json()


client = Logic(BASE_URL)
