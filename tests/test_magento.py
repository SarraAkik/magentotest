import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configurer les options pour Edge
options = Options()
options.add_argument('--headless')  # Lancer le navigateur en mode sans tête (pas d'interface graphique)
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Définir le chemin vers le driver Edge
service = EdgeService(executable_path='/usr/local/bin/msedgedriver')  # Ajustez le chemin selon votre configuration

# Initialiser le WebDriver pour Edge
driver = webdriver.Edge(service=service, options=options)

@pytest.fixture(scope='class')
def driver():
    # Initialisation du driver Selenium
    driver = webdriver.Edge(service=service, options=options)
    yield driver
    driver.quit()

def take_screenshot(driver, filename):
    # Prendre une capture d'écran et la sauvegarder
    driver.save_screenshot(filename)
    print(f"Capture d'écran prise : {filename}")

class TestMagentoAdmin:

    def test_magento_login(self, driver):
        try:
            # Accéder à la page de connexion de Magento
            driver.get("http://mage2rock.magento.com/admin/")  # L'URL de la page de connexion de Magento
            time.sleep(500)  

            # Attendre que le formulaire de connexion soit visible
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "username")))

            # Remplir le formulaire de connexion avec les informations d'identification
            driver.find_element(By.ID, "username").send_keys("rockadmin")  # Remplacez par ton nom d'utilisateur
            driver.find_element(By.ID, "login").send_keys("sarra123")  # Remplacez par ton mot de passe

            # Attendre que le bouton de connexion soit cliquable et cliquer
            login_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".action-login"))
            )
            login_button.click()

            # Capture d'écran après la connexion
            take_screenshot(driver, "sign_in_success.png")

            # Cliquer sur le menu "Catalog"
            catalog_menu = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "menu-magento-catalog-catalog"))
            )
            catalog_menu.click()

            # Attendre que le sous-menu apparaisse
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "submenu"))
            )

            # Capture d'écran après avoir cliqué sur le menu "Catalog" et vu le sous-menu
            take_screenshot(driver, "catalog_opened.png")

            print("Test terminé avec succès.")

        except Exception as e:
            print(f"Erreur rencontrée : {e}")
            # Capture d'écran en cas d'erreur
            take_screenshot(driver, "error.png")
            pytest.fail(f"Erreur rencontrée : {e}")
