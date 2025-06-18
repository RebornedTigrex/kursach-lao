from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pytest
import subprocess

# URL вашей страницы (замените на нужный порт и путь)
BASE_URL = "http://127.0.0.1:3000/pages/subjects.html"


@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Без открытия окна браузера
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_subjects_add_and_delete(driver):
    driver.get(BASE_URL)
    time.sleep(1)  # Ждём загрузки страницы

    # Проверяем, что контейнер для предметов есть
    container = driver.find_element(By.ID, 'subjects-list-container')
    assert container is not None

    # Добавляем предмет
    input_elem = driver.find_element(By.ID, 'subject-input')
    input_elem.clear()
    input_elem.send_keys('SeleniumTest')
    form = driver.find_element(By.ID, 'add-subject-form')
    form.submit()
    time.sleep(1)

    # Проверяем, что предмет появился в списке
    assert 'SeleniumTest' in container.text

    # Удаляем предмет
    del_btns = container.find_elements(By.TAG_NAME, 'button')
    for btn in del_btns:
        if btn.text == 'Удалить':
            btn.click()
            break
    time.sleep(1)
    assert 'SeleniumTest' not in container.text
