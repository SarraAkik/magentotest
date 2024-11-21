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

# Définir le chemin vers le driver Edge
service = EdgeService(executable_path='msedgedriver.exe')

@allure.feature("Magento Admin LOgin/Logout Tests")
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

    def handle_error(self, driver, error):
        self.take_screenshot(driver, "error.png")
        print(f"Erreur rencontrée : {error}")
        raise error

    @allure.story("Connexion à Magento")
    def test_magento_login(self, driver):
        try:
            self.login_to_magento(driver)
        except Exception as e:
            self.handle_error(driver, e)

    def login_to_magento(self, driver):
        with allure.step("Accéder à la page de connexion de Magento"):
            driver.get("http://mage2rock.magento.com/admin/")
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "username"))
            )

        with allure.step("Saisir les informations d'identification"):
            driver.find_element(By.ID, "username").send_keys("rockadmin")
            driver.find_element(By.ID, "login").send_keys("sarra1234")
            self.take_screenshot(driver, "before_click_login.png")

        with allure.step("Cliquer sur le bouton de connexion"):
            login_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".action-login"))
            )
            login_button.click()

        with allure.step("Vérifier que la connexion est réussie"):
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "admin__action-dropdown"))
            )
            self.take_screenshot(driver, "sign_in_success.png")
            
            # Assertion pour vérifier la connexion
            assert driver.find_element(By.CLASS_NAME, "admin__action-dropdown").is_displayed(), "Échec de la connexion"

    def logout_from_magento(self, driver):
        with allure.step("Naviguer vers le menu utilisateur"):
            user_menu = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@title='My Account']"))
            )
            user_menu.click()  # Clic sur le menu
            self.take_screenshot(driver, "user_menu_opened.png")

        with allure.step("Attendre que le menu déroulant soit visible"):
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "admin__action-dropdown-menu"))
            )

        with allure.step("Cliquer sur le bouton de déconnexion"):
            logout_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@title='Sign Out']"))
            )
            logout_button.click()

        with allure.step("Prendre une capture d'écran après la déconnexion"):
            # Capture d'écran après la déconnexion (page de connexion ou état après logout)
            self.take_screenshot(driver, "after_sign_out.png")

    @allure.story("Déconnexion de Magento")
    def test_magento_logout(self, driver):
        try:
            self.login_to_magento(driver)  # Connexion pour préparer la déconnexion
            self.logout_from_magento(driver)  # Effectuer la déconnexion
        except Exception as e:
            self.handle_error(driver, e)
