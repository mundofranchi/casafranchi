import os
import time
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from PIL import Image
from io import BytesIO

# ---------- CONFIGURACIÓN ----------
EXCEL_FILE = "ListaDeProductos.xlsx"  # Reemplazar con tu archivo Excel real
SHEET_NAME = "Lista Lusqtoff"
OUTPUT_FOLDER = "imagenes_productos"

# ---------- FUNCIONES ----------
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def buscar_y_descargar_imagen(driver, query, filename):
    from PIL import Image
    from io import BytesIO

    driver.get(f"https://www.bing.com/images/search?q={query.replace(' ', '+')}")
    time.sleep(2)

    try:
        images = driver.find_elements(By.CSS_SELECTOR, "img.mimg")

        for img in images:
            src = img.get_attribute("src")
            if src and src.startswith("http"):
                try:
                    r = requests.get(src, timeout=10)
                    if r.status_code == 200:
                        image = Image.open(BytesIO(r.content))
                        image.save(filename)
                        print(f"✅ Imagen guardada: {filename}")
                        return
                except Exception as e:
                    print(f"⚠️ Error al descargar {src} - {e}")
                    continue

        print(f"⚠️ No se encontró imagen útil para {query}")

    except Exception as e:
        print(f"❌ Error general con {query}: {e}")



# ---------- PROCESO PRINCIPAL ----------
def main():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)

    # Buscar desde qué índice empezar
    start_index = df[df["Codigo"] == "MPS-2"].index[0]

    # Filtrar desde esa fila
    df = df.iloc[start_index:]

    driver = setup_driver()

    for _, row in df.iterrows():
        codigo = str(row["Codigo"]).strip()
        producto = str(row["Producto"]).strip()
        query = f"{codigo} {producto}"
        filename = os.path.join(OUTPUT_FOLDER, f"{codigo}.jpg")

        if not os.path.exists(filename):  # Evita repetir si ya lo bajaste
            buscar_y_descargar_imagen(driver, query, filename)

    driver.quit()
    print("🎉 Proceso completado.")

if __name__ == "__main__":
    main()
