import allure
from pages.payment_page import PaymentPage
from helpers.db_helper import get_payment_status, get_payment_count, clear_database


@allure.feature("Оплата тура")
@allure.story("Успешная оплата валидной картой")
def test_success_payment(browser):
    clear_database()

    page = PaymentPage(browser)

    with allure.step("Открыть форму оплаты"):
        page.open_payment()
        page.wait_form()

    with allure.step("Заполнить форму валидной картой"):
        page.fill_form(
            "1111 2222 3333 4444",
            "12",
            "26",
            "IVAN IVANOV",
            "123"
        )

    with allure.step("Отправить форму"):
        page.submit_form()

    with allure.step("Проверить успешное уведомление"):
        page.wait_success()

    with allure.step("Проверить статус в БД"):
        status = get_payment_status()
        assert status == "APPROVED"


@allure.feature("Оплата тура")
@allure.story("Отклонённая карта")
def test_declined_payment(browser):
    clear_database()

    page = PaymentPage(browser)

    with allure.step("Открыть форму оплаты"):
        page.open_payment()
        page.wait_form()

    with allure.step("Заполнить форму отклонённой картой"):
        page.fill_form(
            "5555 6666 7777 8888",
            "12",
            "26",
            "IVAN IVANOV",
            "123"
        )

    with allure.step("Отправить форму"):
        page.submit_form()

    with allure.step("Проверить уведомление об ошибке"):
        page.wait_error()

    with allure.step("Проверить статус в БД"):
        status = get_payment_status()
        assert status == "DECLINED"


@allure.feature("Валидация формы")
@allure.story("Месяц 00")
def test_00_month(browser):
    clear_database()

    page = PaymentPage(browser)

    with allure.step("Открыть форму оплаты"):
        page.open_payment()
        page.wait_form()

    with allure.step("Ввести месяц 00"):
        page.fill_form(
            "1111 2222 3333 4444",
            "00",
            "26",
            "IVAN IVANOV",
            "123"
        )

    with allure.step("Отправить форму"):
        page.submit_form()

    with allure.step("Проверить ошибку валидации месяца"):
        page.invalid_month()

    with allure.step("Проверить, что запись в БД не создана"):
        count = get_payment_count()
        assert count == 0


@allure.feature("Валидация формы")
@allure.story("Прошедший год")
def test_past_year(browser):
    clear_database()

    page = PaymentPage(browser)

    with allure.step("Открыть форму оплаты"):
        page.open_payment()
        page.wait_form()

    with allure.step("Ввести прошедший год"):
        page.fill_form(
            "1111 2222 3333 4444",
            "12",
            "25",
            "IVAN IVANOV",
            "123"
        )

    with allure.step("Отправить форму"):
        page.submit_form()

    with allure.step("Проверить ошибку года"):
        page.invalid_year()

    with allure.step("Проверить, что запись в БД не создана"):
        count = get_payment_count()
        assert count == 0


@allure.feature("Валидация формы")
@allure.story("Имя содержит цифры")
def test_name_numbers(browser):
    clear_database()

    page = PaymentPage(browser)

    with allure.step("Открыть форму оплаты"):
        page.open_payment()
        page.wait_form()

    with allure.step("Ввести имя с цифрами"):
        page.fill_form(
            "1111 2222 3333 4444",
            "12",
            "26",
            "IVAN123456",
            "123"
        )

    with allure.step("Отправить форму"):
        page.submit_form()

    with allure.step("Проверить ошибку имени"):
        page.invalid_name()

    with allure.step("Проверить, что запись в БД не создана"):
        count = get_payment_count()
        assert count == 0


@allure.feature("Валидация формы")
@allure.story("Неверный CVC")
def test_invalid_cvc(browser):
    clear_database()

    page = PaymentPage(browser)

    with allure.step("Открыть форму оплаты"):
        page.open_payment()
        page.wait_form()

    with allure.step("Ввести неверный CVC"):
        page.fill_form(
            "1111 2222 3333 4444",
            "12",
            "26",
            "IVAN IVANOV",
            "00"
        )

    with allure.step("Отправить форму"):
        page.submit_form()

    with allure.step("Проверить ошибку CVC"):
        page.invalid_cvc()

    with allure.step("Проверить, что запись в БД не создана"):
        count = get_payment_count()
        assert count == 0