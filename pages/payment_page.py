from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class PaymentPage:

    buy_button = (By.XPATH, "//span[text()='Купить']/..")

    card_number = (By.XPATH, "//span[text()='Номер карты']/..//input")
    month = (By.XPATH, "//span[text()='Месяц']/..//input")
    year = (By.XPATH, "//span[text()='Год']/..//input")
    owner = (By.XPATH, "//span[text()='Владелец']/..//input")
    cvc = (By.XPATH, "//span[contains(text(),'CVC')]/..//input")

    submit = (By.XPATH, "//span[text()='Продолжить']/..")

    success_notification = (
        By.XPATH,
        "//div[contains(@class,'notification_status_ok')]//div[contains(text(),'Операция одобрена')]"
    )

    error_notification = (
        By.XPATH,
        "//div[contains(@class,'notification_status_error')]//div[contains(text(),'Банк отказал')]"
    )

    invalid_month_error = (
        By.XPATH,
        "//span[text()='Неверно указан срок действия карты']"
    )

    invalid_year_error = (
        By.XPATH,
        "//span[text()='Истёк срок действия карты']"
    )

    invalid_name_error = (
        By.XPATH,
        "//span[text()='Имя не может содержать цифры']"
    )

    invalid_cvc_error = (
        By.XPATH,
        "//span[text()='Неверный формат']"
    )

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def open_payment(self):
        self.driver.find_element(*self.buy_button).click()

    def wait_form(self):
        self.wait.until(
            EC.visibility_of_element_located(self.card_number)
        )

    def fill_form(self, number, month, year, owner, cvc):

        def clear_and_type(locator, value):
            field = self.driver.find_element(*locator)
            field.send_keys(Keys.CONTROL + "a")
            field.send_keys(Keys.DELETE)
            field.send_keys(value)

        clear_and_type(self.card_number, number)
        clear_and_type(self.month, month)
        clear_and_type(self.year, year)
        clear_and_type(self.owner, owner)
        clear_and_type(self.cvc, cvc)

    def submit_form(self):
        self.driver.find_element(*self.submit).click()

    def wait_success(self):
        self.wait.until(
            EC.visibility_of_element_located(self.success_notification)
        )

    def wait_error(self):
        self.wait.until(
            EC.visibility_of_element_located(self.error_notification)
        )

    def invalid_month(self):
        self.wait.until(
            EC.visibility_of_element_located(self.invalid_month_error)
        )

    def invalid_year(self):
        self.wait.until(
            EC.visibility_of_element_located(self.invalid_year_error)
        )

    def invalid_name(self):
        self.wait.until(
            EC.visibility_of_element_located(self.invalid_name_error)
        )

    def invalid_cvc(self):
        self.wait.until(
            EC.visibility_of_element_located(self.invalid_cvc_error)
        )