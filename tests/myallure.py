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
from selenium.webdriver.support.ui import Select

# Configurer les options pour Edge
options = Options()
options.add_argument('--headless')  # Lancer le navigateur en mode sans tête
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Définir le chemin vers le driver Edge
service = EdgeService(executable_path='msedgedriver.exe')

@allure.feature("Magento Admin Add product Test")
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
            self.login_to_magento(driver)
            self.navigate_to_catalog(driver)
            self.add_simple_product(driver)
            self.add_simple_product_details(driver)
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
            self.take_screenshot(driver, "sign_in_success.png")

    def navigate_to_catalog(self, driver):
        with allure.step("Ouvrir le menu 'Catalog'"):
            catalog_menu = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "menu-magento-catalog-catalog"))
            )
            catalog_menu.click()
            time.sleep(2)  # Petit délai pour s'assurer que le menu se déploie
            self.take_screenshot(driver, "catalog_menu_opened.png")

        with allure.step("Vérifier la visibilité du sous-menu 'Products'"):
            products_submenu = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "li.item-catalog-products.level-2"))
            )
            actions = ActionChains(driver)
            actions.move_to_element(products_submenu).perform()
            self.take_screenshot(driver, "hover_on_catalog_products_submenu.png")
            products_submenu.find_element(By.TAG_NAME, "a").click()
            time.sleep(40)
            self.take_screenshot(driver, "products_page.png")

    def add_simple_product(self, driver):
        with allure.step("Ajouter un produit - Sélectionner 'Simple Product'"):
            add_product_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.action-toggle.primary.add"))
            )
            add_product_button.click()
            time.sleep(10)
            self.take_screenshot(driver, "add_product_button.png")

            simple_product_option = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "span[title='Simple Product']"))
            )
            simple_product_option.click()
            time.sleep(60)
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".page-title"))
            )
            self.take_screenshot(driver, "simple_product_page.png")
            print("Produit 'Simple Product' sélectionné avec succès.")

    def add_simple_product_details(self, driver):
        with allure.step("Remplir les détails du produit"):
            driver.find_element(By.NAME, "product[name]").send_keys("sac")
            self.take_screenshot(driver, "product_name_filled.png")

            driver.find_element(By.NAME, "product[sku]").send_keys("SKU1")
            self.take_screenshot(driver, "product_sku_filled.png")

            driver.find_element(By.NAME, "product[price]").send_keys("400")
            self.take_screenshot(driver, "product_price_filled.png")

            driver.find_element(By.NAME, "product[quantity_and_stock_status][qty]").send_keys("100")
            self.take_screenshot(driver, "product_quantity_filled.png")

            driver.find_element(By.NAME, "product[weight]").send_keys("5")
            self.take_screenshot(driver, "product_weight_filled.png")

            driver.find_element(By.NAME, "product[news_from_date]").send_keys("11/26/2024")
            self.take_screenshot(driver, "product_news_from_date_filled.png")

            driver.find_element(By.NAME, "product[news_to_date]").send_keys("12/10/2024")
            self.take_screenshot(driver, "product_news_to_date_filled.png")

            # Sélectionner le pays de fabrication (Tunisie)
            country_dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "product[country_of_manufacture]"))
            )
            select_country = Select(country_dropdown)  # Utilisation de Select pour gérer le menu déroulant
            select_country.select_by_value("TN")  # Sélectionner la Tunisie
            self.take_screenshot(driver, "product_country_filled.png")

        with allure.step("Enregistrer le produit avec l'option 'Save and New'"):
            save_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".action-toggle.primary.save"))
            )
            save_button.click()
            time.sleep(5)
            save_and_new_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "save_and_new"))
            )
            save_and_new_button.click()
            time.sleep(120)
            self.take_screenshot(driver, "product_saved_and_new.png")
            print("Produit enregistré avec succès avec l'option 'Save and New'.")

        with allure.step("Revenir à la page des produits"):
            back_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "back"))
            )
            back_button.click()
            time.sleep(120)
            self.take_screenshot(driver, "returned_to_products_page.png")
            print("Retour à la page des produits effectué avec succès.")

    def handle_error(self, driver, exception):
        self.take_screenshot(driver, "error.png")
        allure.attach(str(exception), name="Erreur", attachment_type=allure.attachment_type.TEXT)
        allure.attach(driver.page_source, name="Page Source", attachment_type=allure.attachment_type.TEXT)
        pytest.fail(f"Erreur rencontrée : {exception}")
