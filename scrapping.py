import csv
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def clean_price(price_str):
    cleaned_str = re.sub(r'[^\d\s]', '', price_str)
    cleaned_str = re.sub(r'\s', '', cleaned_str)
    try:
        return int(cleaned_str)
    except ValueError:
        # Return 0 if conversion fails
        return 0

def scrape_data(url, nb_pages):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    all_data = []

    for page in range(1, nb_pages + 1):
        full_url = f"{url}?page={page}"
        driver.get(full_url)
        time.sleep(4)

        try:
            cards = driver.find_elements(By.CSS_SELECTOR, "div.cars-listing-card")
        except:
            continue

        for card in cards:
            try:
                details = card.find_element(By.CSS_SELECTOR, ".cars-listing-card__header__title").text.strip()
                prix_text = card.find_element(By.CSS_SELECTOR, ".cars-listing-card__price__value").text.strip()
                prix = clean_price(prix_text)
                image = card.find_element(By.CSS_SELECTOR, "img.listing-card__image__resource").get_attribute("src")
                lien = card.find_element(By.CSS_SELECTOR, "a.cars-listing-card__inner").get_attribute("href")
            except:
                continue

            # Aller à la page de détails
            try:
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(lien)
                time.sleep(3)

                # Propriétés (état, marque, etc.)
                try:
                    props = driver.find_elements(By.CSS_SELECTOR, ".listing-item__properties dt")
                    values = driver.find_elements(By.CSS_SELECTOR, ".listing-item__properties dd")
                    props_map = {p.text.strip(): v.text.strip() for p, v in zip(props, values)}
                except:
                    props_map = {}

                etat = props_map.get("Etat", "N/A")
                marque = props_map.get("Marque", "N/A")

                # Adresse
                try:
                    lieu = driver.find_element(By.CSS_SELECTOR, ".listing-item__address-location").text.strip()
                    region = driver.find_element(By.CSS_SELECTOR, ".listing-item__address-region").text.strip()
                    adresse = f"{lieu}, {region}"
                except:
                    adresse = "N/A"

                driver.close()
                driver.switch_to.window(driver.window_handles[0])

                all_data.append([details, etat, marque, adresse, prix, image])

            except:
                # Fermer l'onglet détail s'il a été ouvert
                if len(driver.window_handles) > 1:
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                continue

    driver.quit()
    return all_data

def save_to_csv(filename, data):
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["détails", "état", "marque", "adresse", "prix", "image_lien"])
        writer.writerows(data)
    print(f"[✅] Fichier '{filename}' enregistré.")
