from selenium import webdriver 
from selenium.webdriver.common.by import By  
from selenium.webdriver.common.keys import Keys   
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from datetime import datetime 
 
 
# Crear carpeta numerada para cada ejecución de la prueba
def get_next_test_folder():
    test_number = 1
    while True:
        folder_name = f"prueba_{test_number}"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            print(f"Carpeta '{folder_name}' creada para esta ejecución de la prueba")
            return folder_name
        test_number += 1

screenshots_folder = get_next_test_folder()

driver = webdriver.Chrome()
driver.get("https://the-internet.herokuapp.com/login") 
time.sleep(2)

# Tomar captura de pantalla antes del login
timestamp_before = datetime.now().strftime("%Y%m%d_%H%M%S")
screenshot_before = os.path.join(screenshots_folder, f"before_login_{timestamp_before}.png")
driver.save_screenshot(screenshot_before)
print(f"Captura de pantalla antes del login guardada como: {screenshot_before}")

user_input = driver.find_element(By.ID, "username") 
passw_input = driver.find_element(By.ID, "password") 

user_input.send_keys("tomsmith")
passw_input.send_keys("SuperSecretPassword!")

login_button = driver.find_element(By.CSS_SELECTOR, "button.radius")
login_button.click()

time.sleep(2)

# Tomar captura de pantalla después del login
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
screenshot_filename = os.path.join(screenshots_folder, f"login_screenshot_{timestamp}.png")
driver.save_screenshot(screenshot_filename)
print(f"Captura de pantalla guardada como: {screenshot_filename}")

try:
    success_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".flash.success"))
    ).text
    print("Login exitoso", success_message)
except:
    error_message = driver.find_element(By.CSS_SELECTOR, ".flash").text
    print("No se encontró el mensaje de éxito", error_message)
