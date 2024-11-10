# test_magento.py

import pytest
from selenium import webdriver
from allure_commons.types import AttachmentType
import allure

@allure.title("Vérifier le titre de la page Magento")
def test_magento_homepage():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Initialiser le WebDriver
    driver = webdriver.Chrome(options=options)
    driver.get("http://mage2rock.magento.com")  # URL Magento

    # Vérification du titre
    assert "Magento" in driver.title

    # Capture d'écran en cas de succès
    allure.attach(driver.get_screenshot_as_png(), name="Homepage Screenshot", attachment_type=AttachmentType.PNG)

    driver.quit()
