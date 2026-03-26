from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pytest


@pytest.fixture
def browser():
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install())
    )
    driver.maximize_window()
    driver.get("http://localhost:8080")

    yield driver

    driver.quit()