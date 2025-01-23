import allure
from assertpy import assert_that, soft_assertions


def response_body_validator(testing_object, comparison_object):
    with allure.step("Извлечение сущностей для проверки"):
        requested_tag_ids = [tag["id"] for tag in testing_object["tags"]]
        requested_tag_names = [tag["name"] for tag in testing_object["tags"]]
        tag_ids = [tag["id"] for tag in testing_object["tags"]]
        tag_names = [tag["name"] for tag in testing_object["tags"]]

    with soft_assertions():  # позволяет выполнять последующие проверки полей при фейле любого ассерта
        assert_that(
            testing_object["name"],
            "Питомец не создан с корректным именем",
        ).contains(comparison_object["name"])
        assert_that(testing_object["id"], "ID питомца не совпадает").is_equal_to(
            comparison_object["id"]
        )
        assert_that(
            testing_object["category"]["id"], "ID категории питомца не совпадает"
        ).is_equal_to(comparison_object["category"]["id"])
        assert_that(
            testing_object["category"]["name"],
            "Название категории питомца не совпадает",
        ).contains(comparison_object["category"]["name"])
        assert_that(
            len(testing_object["photoUrls"]),
            "Количество фотографий питомца не совпадает с кол-вом добавленных",
        ).is_equal_to(len(comparison_object["photoUrls"]))
        assert_that(tag_ids, "ID тега питомца не совпадает").is_subset_of(
            requested_tag_ids
        )
        assert_that(tag_names, "Название тега питомца не совпадает").is_subset_of(
            requested_tag_names
        )
        assert_that(testing_object["status"], "Статус питомца не совпадает").contains(
            comparison_object["status"]
        )
