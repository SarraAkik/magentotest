# test_magento.py

import pytest
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from allure_commons.types import AttachmentType
import allure

@allure.title("Vérifier le titre de la page d'accueil Magento")
def test_magento_homepage():
    # Configuration des options Edge
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Définir le chemin du driver (assuré d'être en PATH par l'image Docker)
    # Utiliser le chemin complet du driver
    service = EdgeService(executable_path='/usr/local/bin/msedgedriver.exe')

    # Initialiser le WebDriver Edge
    driver = webdriver.Edge(service=service, options=options)

    try:
        # Accéder à l'URL Magento
        driver.get("http://mage2rock.magento.com")
        
        # Vérifier que le titre contient "Magento"
        assert "Magento" in driver.title, "Le titre de la page ne contient pas 'Magento'"
        
        # Capture d'écran
        allure.attach(driver.get_screenshot_as_png(), 
                      name="Homepage Screenshot", 
                      attachment_type=AttachmentType.PNG)

        # Vérification d'un élément clé pour s'assurer que la page est chargée correctement
        assert driver.find_element(By.CSS_SELECTOR, "body"), "Le corps de la page n'est pas présent"

    except Exception as e:
        allure.attach(driver.get_screenshot_as_png(), 
                      name="Erreur Screenshot", 
                      attachment_type=AttachmentType.PNG)
        raise e
    finally:
        driver.quit()
