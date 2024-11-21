import time
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

# Configuration du navigateur Edge
options = Options()
options.add_argument('--headless')  # Mode sans tête
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Chemin vers le driver Edge
service = EdgeService(executable_path='msedgedriver.exe')

@allure.feature("Magento Admin Order Creation Test")
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

    @allure.story("Création d'une nouvelle commande dans Magento")
    def test_create_order(self, driver):
        try:
            self.login_to_magento(driver)
            self.navigate_to_sales(driver)
            self.create_new_order(driver)
            self.fill_billing_address(driver)
            self.submit_order(driver)
        except Exception as e:
            self.handle_error(driver, e)

    def login_to_magento(self, driver):
        with allure.step("Accéder à la page de connexion de Magento"):
            driver.get("http://mage2rock.magento.com/admin/")
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "username")))

        with allure.step("Saisir les informations d'identification"):
            driver.find_element(By.ID, "username").send_keys("rockadmin")
            driver.find_element(By.ID, "login").send_keys("sarra1234")
            self.take_screenshot(driver, "before_click_login.png")

        with allure.step("Cliquer sur le bouton de connexion"):
            login_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".action-login"))
            )
            login_button.click()
            time.sleep(3)  # Assurer le chargement après la connexion
            self.take_screenshot(driver, "sign_in_success.png")

    def navigate_to_sales(self, driver):
        with allure.step("Accéder au menu 'Sales'"):
            sales_menu = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "menu-magento-sales-sales"))
            )
            sales_menu.click()
            time.sleep(20)
            self.take_screenshot(driver, "sales_menu_opened.png")
            time.sleep(2)

        with allure.step("Accéder à 'Orders' dans le menu Sales"):
            orders_submenu = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/sales/order/index')]"))
            )
            orders_submenu.click()
            time.sleep(10)
            self.take_screenshot(driver, "orders_page_opened.png")
            time.sleep(2)

        with allure.step("Cliquer sur 'Create New Order'"):
            create_order_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "add"))
            )
            create_order_button.click()
            time.sleep(10)  # Temps pour charger la page
            self.take_screenshot(driver, "create_order_page_opened.png")

    def create_new_order(self, driver):
        with allure.step("Sélectionner un client pour la commande"):
            select_customer_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//tr[@data-role='row' and @title='2']"))
            )
            select_customer_button.click()
            time.sleep(50)  # Temps pour charger les informations du client
            self.take_screenshot(driver, "customer_selected.png")

    def fill_billing_address(self, driver):
        with allure.step("Remplir les informations de facturation"):
            driver.find_element(By.NAME, "order[billing_address][firstname]").send_keys("Sarra")
            driver.find_element(By.NAME, "order[billing_address][lastname]").send_keys("Noursene")
            driver.find_element(By.NAME, "order[billing_address][street][0]").send_keys("1234 Elm Street")
            driver.find_element(By.NAME, "order[billing_address][city]").send_keys("monastir")
            driver.find_element(By.NAME, "order[billing_address][postcode]").send_keys("90001")
            driver.find_element(By.NAME, "order[billing_address][telephone]").send_keys("99408311")
            self.take_screenshot(driver, "billing_address_filled.png")

        with allure.step("Sélectionner le pays"):
            country_dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "order[billing_address][country_id]"))
            )
            select_country = Select(country_dropdown)
            select_country.select_by_value("TN")  # Assurez-vous que la valeur correspond exactement
            self.take_screenshot(driver, "billing_country_selected.png")
            time.sleep(2)

        
    def submit_order(self, driver):
        with allure.step("Soumettre la commande"):
            submit_order_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "submit_order_top_button"))
            )
            submit_order_button.click()
            self.take_screenshot(driver, "order_submitted.png")
            print("Commande soumise avec succès.")

    def handle_error(self, driver, exception):
        self.take_screenshot(driver, "error.png")
        allure.attach(str(exception), name="Erreur", attachment_type=allure.attachment_type.TEXT)
        allure.attach(driver.page_source, name="Page Source", attachment_type=allure.attachment_type.TEXT)
        pytest.fail(f"Erreur rencontrée : {exception}")
