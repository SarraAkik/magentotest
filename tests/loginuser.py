import time
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configurer les options pour Edge
options = Options()
options.add_argument('--headless')  # Lancer le navigateur en mode sans tête
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Définir le chemin vers le driver Edge
service = EdgeService(executable_path='msedgedriver.exe')

@allure.feature("Magento Admin Login/Logout Tests")
class TestMagentoChangeActionAndLogout:

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

    @allure.story("Interagir avec le bouton Change et se déconnecter")
    def test_change_action_and_logout(self, driver):
        try:
            self.click_change_button(driver)
            self.logout_of_magento(driver)
        except Exception as e:
            self.handle_error(driver, e)

    def click_change_button(self, driver):
        with allure.step("Accéder à la page"):
            driver.get("http://mage2rock.magento.com/customer/account/login/")

        with allure.step("Connexion au compte"):
            # Remplir l'email
            driver.find_element(By.ID, "email").send_keys("noursene.gabsi@ensi-uma.tn")
            # Remplir le mot de passe
            driver.find_element(By.ID, "password").send_keys("Noursene1234@.")
            # Clic sur le bouton Sign In
            driver.find_element(By.CSS_SELECTOR, ".action.login.primary").click()

        with allure.step("Cliquer sur le bouton Change"):
            # Attendre que le bouton apparaisse
            change_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "action.switch"))
            )
            # Cliquer sur le bouton Change
            change_button.click()

        with allure.step("Prendre une capture d'écran après le clic sur Change"):
            time.sleep(5)  # Attendre un moment pour l'effet
            self.take_screenshot(driver, "change_button_screenshot.png")

    def logout_of_magento(self, driver):
        with allure.step("Cliquer sur Sign Out pour se déconnecter"):
            # Localiser le lien de déconnexion "Sign Out"
            logout_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Sign Out"))
            )
            # Cliquer sur le lien de déconnexion
            logout_link.click()

        with allure.step("Prendre une capture d'écran après la déconnexion"):
            # Attendre un moment pour s'assurer que la déconnexion est effective
            time.sleep(5)
            self.take_screenshot(driver, "logout_screenshot.png")

    def handle_error(self, driver, exception):
        print(f"Error occurred: {exception}")
        self.take_screenshot(driver, "error_screenshot.png")
        raise exception
