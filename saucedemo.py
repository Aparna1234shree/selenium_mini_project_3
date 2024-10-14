from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class SauceDemoAutomation:
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get("https://www.saucedemo.com/")

    def print_cookies(self, message):
        cookies = self.driver.get_cookies()
        print(f"{message}: {cookies}")

    def login(self, username, password):
        username_input = self.driver.find_element(By.ID, "user-name")
        password_input = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.ID, "login-button")

        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button.click()

        # Wait for the login process to complete
        time.sleep(2)

    def logout(self):
        wait = WebDriverWait(self.driver, 10)

        # Click on the menu button
        menu_button = wait.until(EC.element_to_be_clickable((By.ID, "react-burger-menu-btn")))
        menu_button.click()

        # Click on the logout button
        logout_button = wait.until(EC.element_to_be_clickable((By.ID, "logout_sidebar_link")))
        logout_button.click()

        # Wait for the logout process to complete
        time.sleep(2)

    def close_browser(self):
        self.driver.quit()

