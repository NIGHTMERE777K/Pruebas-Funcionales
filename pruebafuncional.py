from selenium import webdriver 
from selenium.webdriver.common.by import By  
from selenium.webdriver.common.keys import Keys   
from selenium.webdriver.support.ui import Select
import time
import os
from datetime import datetime 

# Función para crear carpeta numerada
def crear_carpeta_prueba():
    contador = 1
    while True:
        nombre_carpeta = f"prueba_{contador}"
        if not os.path.exists(nombre_carpeta):
            os.makedirs(nombre_carpeta)
            return nombre_carpeta
        contador += 1

# Función para tomar captura de pantalla
def tomar_captura(driver, carpeta, nombre_archivo):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta_archivo = os.path.join(carpeta, f"{nombre_archivo}_{timestamp}.png")
    driver.save_screenshot(ruta_archivo)
    print(f"Captura guardada: {ruta_archivo}")
    return ruta_archivo

# Función para realizar una operación
def realizar_operacion(driver, carpeta, operacion, num1, num2, descripcion):
    try:
        print(f"\n=== {descripcion} ===")
        
        # Limpiar campos
        print("Limpiando campos...")
        driver.find_element(By.ID, "clearButton").click()
        time.sleep(2)
        
        # Captura ANTES de la operación
        print("Tomando captura ANTES...")
        tomar_captura(driver, carpeta, f"before_{operacion}")
        
        # Ingresar números
        print(f"Ingresando números: {num1} y {num2}")
        input_first = driver.find_element(By.ID, "number1Field")
        input_second = driver.find_element(By.ID, "number2Field")
        
        input_first.clear()
        input_second.clear()
        input_first.send_keys(str(num1))
        input_second.send_keys(str(num2))
        
        # Seleccionar operación usando Select
        print(f"Seleccionando operación: {operacion}")
        operation_dropdown = Select(driver.find_element(By.ID, "selectOperationDropdown"))
        
        # Seleccionar la operación específica
        if operacion == "add":
            operation_dropdown.select_by_value("0")  # Add
        elif operacion == "subtract":
            operation_dropdown.select_by_value("1")  # Subtract
        elif operacion == "multiply":
            operation_dropdown.select_by_value("2")  # Multiply
        elif operacion == "divide":
            operation_dropdown.select_by_value("3")  # Divide
        elif operacion == "concatenate":
            operation_dropdown.select_by_value("4")  # Concatenate
        
        time.sleep(2)
        
        # Hacer clic en calcular
        print("Haciendo clic en calcular...")
        calculate_button = driver.find_element(By.ID, "calculateButton")
        calculate_button.click()
        time.sleep(3)
        
        # Captura DESPUÉS de la operación
        print("Tomando captura DESPUÉS...")
        tomar_captura(driver, carpeta, f"after_{operacion}")
        
        # Obtener y mostrar resultado
        result_text = driver.find_element(By.ID, "displayValue")
        resultado = result_text.text
        print(f"Resultado de {descripcion}: {resultado}")
        
        return resultado
        
    except Exception as e:
        print(f"ERROR en {descripcion}: {str(e)}")
        return f"ERROR: {str(e)}"

# Crear carpeta para esta prueba
carpeta_prueba = crear_carpeta_prueba()
print(f"Carpeta de prueba creada: {carpeta_prueba}")

# Inicializar el navegador
driver = webdriver.Chrome()
driver.get("https://testsheepnz.github.io/BasicCalculator.html")
time.sleep(2)

print("=== INICIANDO PRUEBAS DE CALCULADORA ===")

# Realizar todas las operaciones
resultados = {}

# 1. SUMA
print("\n🔄 INICIANDO OPERACIÓN 1: SUMA")
resultados['suma'] = realizar_operacion(driver, carpeta_prueba, "add", 10, 5, "SUMA: 10 + 5")
print("✅ SUMA COMPLETADA")
time.sleep(2)

# 2. RESTA  
print("\n🔄 INICIANDO OPERACIÓN 2: RESTA")
resultados['resta'] = realizar_operacion(driver, carpeta_prueba, "subtract", -4, 8, "RESTA: -4 - 8")
print("✅ RESTA COMPLETADA")
time.sleep(2)

# 3. MULTIPLICACIÓN
print("\n🔄 INICIANDO OPERACIÓN 3: MULTIPLICACIÓN")
resultados['multiplicacion'] = realizar_operacion(driver, carpeta_prueba, "multiply",-6, 7, "MULTIPLICACIÓN:-6 × 7")
print("✅ MULTIPLICACIÓN COMPLETADA")
time.sleep(2)

# 4. DIVISIÓN
print("\n🔄 INICIANDO OPERACIÓN 4: DIVISIÓN")
resultados['division'] = realizar_operacion(driver, carpeta_prueba, "divide", 3, 4, "DIVISIÓN: 3 ÷ 4")
print("✅ DIVISIÓN COMPLETADA")
time.sleep(2)

# 5. CONCATENACIÓN
print("\n🔄 INICIANDO OPERACIÓN 5: CONCATENACIÓN")
resultados['concatenacion'] = realizar_operacion(driver, carpeta_prueba, "concatenate", 123, 456, "CONCATENACIÓN: 123 + 456")
print("✅ CONCATENACIÓN COMPLETADA")

# Mostrar resumen de resultados
print("\n=== RESUMEN DE RESULTADOS ===")
for operacion, resultado in resultados.items():
    print(f"{operacion.upper()}: {resultado}")

print(f"\nTodas las capturas se guardaron en la carpeta: {carpeta_prueba}")

time.sleep(3)
driver.quit()
