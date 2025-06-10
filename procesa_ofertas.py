import os
# django project name is adleads, replace adleads with your project name
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Libreria.settings")

import django
django.setup()

from Ofertas.models import Oferta

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
from decimal import Decimal

# Configura el driver de Chrome
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Opcional: ejecuta sin abrir el navegador

service = Service('chromedriver')  # Cambia esto si el chromedriver no está en el PATH
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 30)

print("......................................................................................................................")

try:
    # Paso 1: Ir al sitio principal
    driver.get("https://www.elvirrey.com")

    # Paso 2: Denegar cookies
    try:
        denegar_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Denegar')]")))
        denegar_btn.click()
    except Exception as e:
        print("No se encontró el botón de cookies o ya fue cerrado:", e)

    # Paso 3: Navegar a la sección de Ofertas
    ofertas_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Ofertas")))
    ofertas_link.click()

    # Paso 4: Esperar a que cargue la página
    # wait.until(EC.presence_of_element_located((By.CLASS_NAME, "book-item")))
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "block")))

    # Paso 5: Ver todos
    # ofertas_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Ver todos")))
    url = "/categoria/9-9_G2004"
    ofertas_link = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="'+url+'"]')))
    ofertas_link.click()

    hayLibros = True
    numeroPagina = 0
    librosOferta = []

    print("Leyendo de la página web")

    while (hayLibros):

        # Paso 6: Esperar a que cargue la página
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "row")))
        numeroPagina+=1
        print(f"------ numeroPagina={numeroPagina} ---------------")

        # Paso 7: Extraer títulos y precios
        librosEnPagina = []
        secuenciaEnPagina = 0
        # book_elements = driver.find_elements(By.CLASS_NAME, "book-item")
        book_elements = driver.find_elements(By.CLASS_NAME, "item")

        for book in book_elements:
            secuenciaEnPagina+=1
            try:
                titulo = book.find_element(By.CLASS_NAME, "title").text
                autor = book.find_element(By.CLASS_NAME, "creator").text
                precio = book.find_element(By.CLASS_NAME, "precio").text
                disponibilidad = None
                # Obtener el atributo href de un enlace específico
                # enlace_especifico = driver.find_element(By.LINK_TEXT, "Nombre del enlace")
                enlace_especifico = book.find_element(By.CLASS_NAME, "productClick")
                url_enlace = enlace_especifico.get_attribute("href")
                print(url_enlace)
    
                try:
                    disponibilidad = book.find_element(By.CLASS_NAME, "green").text
                except Exception as e:
                    try:
                        disponibilidad = book.find_element(By.CLASS_NAME, "orange").text
                    except Exception as e:
                        print(f"No se obtuvo disponibilidad")
                disponibilidad = disponibilidad.replace("\n", " ")
                librosEnPagina.append((titulo, autor, precio, secuenciaEnPagina, disponibilidad, url_enlace))
            except Exception as e:
                print(f"Error extrayendo datos de un libro: {e}")

        # Mostrar resultados
        print("\nLibros en oferta:")
        for titulo, autor, precio, secuencia, disponibilidad, url_enlace in librosEnPagina:
            librosOferta.append((titulo, autor, precio, numeroPagina, secuencia, disponibilidad, url_enlace))
            print(f"{titulo} - {autor} - {precio} - {secuencia} - {disponibilidad}")

        try:
            # Paso 6: Ver todos
            paginador = driver.find_element(By.CLASS_NAME, "paginador")
            # print(f"paginador={paginador}")
            siguiente = paginador.find_element(By.CLASS_NAME, "fa-angle-right")
            # print(f"siguiente={siguiente}")
            # siguiente = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "fas fa-angle-right")))
            siguiente.click()
        except Exception as e:
            hayLibros = False

    print("Revisa los actuales")    
    for oferta in Oferta.objects.filter(fecha_salida = None):
        encontrado = False
        for titulo, autor, precio, pagina, secuencia, disponibilidad, url_enlace in librosOferta:
            if oferta.titulo == titulo and oferta.autor == autor:
                encontrado = True
        if not encontrado:
            print(f"oferta={oferta} no encontrado")
            oferta.estado = "Baja"
            oferta.fecha_salida = datetime.date.today()
            oferta.save(update_fields=["estado", "fecha_salida"])
        

    print("Proceso las ofertas")
    for titulo, autor, precio, pagina, secuencia, disponibilidad, url_enlace in librosOferta:
        try:
            oferta = Oferta.objects.get(titulo=titulo, autor=autor)
            oferta.pagina = pagina
            oferta.secuencia = secuencia
            oferta.disponibilidad_anterior = oferta.disponibilidad
            oferta.disponibilidad = disponibilidad
            oferta.estado = "Activo"
            oferta.save()
        except Exception as e:
            oferta = Oferta(titulo = titulo, 
                            autor= autor, 
                            precio_en_texto = precio,
                            fecha_ingreso = datetime.date.today(), 
                            fecha_salida = None, 
                            pagina = pagina, 
                            secuencia = secuencia, 
                            disponibilidad = disponibilidad,
                            estado = "Nuevo", 
                            disponibilidad_anterior= None,
                            enlace = url_enlace )
            oferta.save()
            print(f"Nuevo, oferta={oferta}")

finally:
    driver.quit()

