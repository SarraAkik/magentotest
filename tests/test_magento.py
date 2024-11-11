import time
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Configurer les options pour Edge
options = Options()
options.add_argument('--headless')  # Lancer le navigateur en mode sans tête
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Définir le chemin vers le driver Edge (vérifier que ce chemin est correct)
service = EdgeService(executable_path='/usr/local/bin/msedgedriver.exe')

@allure.feature("Magento Admin Login Test")
class TestMagentoAdmin:

    @pytest.fixture(scope='class')
    def driver(self):
        driver = webdriver.Edge(service=service, options=options)
        yield driver
        driver.quit()

    @allure.step("Prendre une capture d'écran")
    def take_screenshot(self, driver, filename):
        driver.save_screenshot(filename)
        allure.attach.file(filename, attachment_type=allure.attachment_type.PNG)
        print(f"Capture d'écran prise : {filename}")

    @allure.story("Connexion à Magento")
    def test_magento_login(self, driver):
        try:
            with allure.step("Accéder à la page de connexion de Magento"):
                driver.get("http://mage2rock.magento.com/admin/")
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, "username"))
                )

            with allure.step("Saisir les informations d'identification"):
                driver.find_element(By.ID, "username").send_keys("rockadmin")
                driver.find_element(By.ID, "login").send_keys("sarra123")

            with allure.step("Cliquer sur le bouton de connexion"):
                login_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".action-login"))
                )
                login_button.click()
                self.take_screenshot(driver, "sign_in_success.png")

            with allure.step("Ouvrir le menu 'Catalog'"):
                catalog_menu = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "menu-magento-catalog-catalog"))
                )
                catalog_menu.click()
                # Remplacer le time.sleep() par un WebDriverWait pour attendre la visibilité d'un élément
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "submenu"))
                )
                self.take_screenshot(driver, "catalog_opened.png")

            with allure.step("Vérifier la visibilité du sous-menu"):
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "submenu"))
                )

            print("Test terminé avec succès.")

        except Exception as e:
            self.take_screenshot(driver, "error.png")
            allure.attach(str(e), name="Erreur", attachment_type=allure.attachment_type.TEXT)
            pytest.fail(f"Erreur rencontrée : {e}")
