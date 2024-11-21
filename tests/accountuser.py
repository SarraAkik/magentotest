import time
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuration du navigateur Edge
options = Options()
options.add_argument('--headless')  # Mode sans tête
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Définir le chemin vers le driver Edge
service = EdgeService(executable_path='msedgedriver.exe')

@allure.feature("Magento Account Creation Test")
class TestMagentoAccountCreation:

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

    @allure.story("Création d'un compte Magento")
    def test_magento_account_creation(self, driver):
        try:
            self.create_account(driver)
        except Exception as e:
            self.handle_error(driver, e)

    def create_account(self, driver):
        with allure.step("Accéder à la page de création de compte"):
            driver.get("http://mage2rock.magento.com/customer/account/create/")
            time.sleep(3)  # Pause pour charger la page
            self.take_screenshot(driver, "step_1_access_page.png")

        with allure.step("Remplir les champs du formulaire"):
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "firstname"))).send_keys("Noursene")
            self.take_screenshot(driver, "step_2_firstname.png")
            
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "lastname"))).send_keys("Gabsi")
            self.take_screenshot(driver, "step_3_lastname.png")
            
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "email_address"))).send_keys("noursene.gabsi@ensi-uma.tn")
            self.take_screenshot(driver, "step_4_email.png")
            
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "password"))).send_keys("Noursene1234@.")
            self.take_screenshot(driver, "step_5_password.png")
            
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "password-confirmation"))).send_keys("Noursene1234@.")
            time.sleep(30)
            self.take_screenshot(driver, "step_6_password_confirmation.png")

        with allure.step("Soumettre le formulaire"):
            time.sleep(10)  # Pause avant de cliquer sur le bouton
            submit_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".action.submit.primary"))
            )
            submit_button.click()
            self.take_screenshot(driver, "step_7_form_submitted.png")

        with allure.step("Attendre et vérifier les résultats"):
            time.sleep(120)  # Attendre pour observer les résultats (peut être réduit si besoin)
            self.take_screenshot(driver, "step_8_account_creation_result.png")

    def handle_error(self, driver, exception):
        print(f"Erreur rencontrée : {exception}")
        self.take_screenshot(driver, "error_screenshot.png")
        raise exception
