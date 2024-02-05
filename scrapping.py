from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import re
from bs4 import BeautifulSoup
import concurrent.futures
import os
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


BASE_URL = "https://www.kaggle.com"
NB_PAGES = 10

options = webdriver.ChromeOptions()
options.add_argument("--incognito")
driver = webdriver.Chrome(options=options)
driver.maximize_window()


results = []
for page in range(1, NB_PAGES+1):

    driver.get(f"{BASE_URL}/competitions?listOption=completed&page={page}")

    # wait until laoding finished
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".sc-gSXJRe")))

    competition_container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".km-list--three-line")))
    html = competition_container.get_attribute("innerHTML")
    soup = BeautifulSoup(html, "html.parser")
    competitions = soup.find_all(
        class_="sc-jPQKUW jbWedR".split())

    competition_links = []
    for competition in competitions:
        try:

            link = competition.find("a").get("href", "")
            competition_links += [f"{BASE_URL}{link}"]
            print(f"Link: {link}")

            print("------")
        except Exception as e:
            print(e)

    for competition_link in competition_links:
        driver.get(competition_link)
        time.sleep(5)

        # wait until laoding finished
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".sc-eEPhau")))

        # with open("index.html", "w", encoding="utf-8") as file:
        #     file.write(driver.page_source)
        # exit()
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # 1.extracting title
        title_soup = soup.select_one(".sc-irLvIq")
        TITLE = title_soup and title_soup.text.strip() or ""
        print(f"Title: {TITLE}")

        # 2.extracting overview

        description_soup = soup.select_one("#abstract .sc-eEPhau")
        OVERVIEW = ""
        if description_soup:
            paragraphs = description_soup.find_all("p")
            OVERVIEW = " \n".join(f"{p.text.strip()} \n" for p in paragraphs)
        # print(f"OVERVIEW:\n {OVERVIEW}")

        # 3.extracting description

        description_soup = soup.select_one("#description ")
        DESCRIPTION = ""
        if description_soup:
            paragraphs = description_soup.select("p, h2")
            DESCRIPTION = " \n".join(
                f"{p.text.strip()} \n" for p in paragraphs)
        print(f"DESCRIPTION:\n {DESCRIPTION}")

        evaluation_soup = soup.select_one("#evaluation")
        EVALUATION = ""
        if evaluation_soup:
            paragraphs = evaluation_soup.select("p, h2 , .uc-code-block code")
            EVALUATION = " \n".join(
                f"{p.text.strip()}" for p in paragraphs)
        print(f"EVALUATION:\n {EVALUATION}")


exit()

magasin_button.click()
time.sleep(3)

print(">Start Scrapping each category :")
for url in url_category_mapping:
    print(f">>>{url}")
    CATEGORIE = url_category_mapping.get(url, "divers")
    try:
        driver.get(url)
        try:
            driver.maximize_window()
        except:
            pass
        time.sleep(1)
        cookies_list = driver.get_cookies()
        cookies = {cookie["name"]: cookie["value"] for cookie in cookies_list}

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'product-price')))

        for i in range(3):
            ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(.15)

        while True:
            try:
                button_next = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "nav.pagination-main__container a.pagination-adjacent__link i.icon-arrowRight")))

                footer = driver.find_element(By.ID, "cms-slot-footerSlot")
                driver.execute_script(
                    "window.scrollTo(0, {0})".format(footer.location["y"]-600))
                time.sleep(.5)

                if "?page=" in driver.current_url:
                    page_number = int(
                        driver.current_url.split('?page=', 1)[1])
                else:
                    page_number = 1
            except:
                break

        # with open("index.html", "r", encoding="utf-8") as file:
        #     html = file.read()
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        promotions_cards = soup.find_all(
            class_="product-thumbnail list__item shadow--light product-thumbnail--column")

        links = []
        # with open("index.html", "w", encoding="utf-8") as file:
        #     file.write(html)
        main_info_result = []
        for card in promotions_cards:
            try:
                URL = f'https://www.auchan.fr{card.find(class_="product-thumbnail__details-wrapper")["href"]}'
                links += [URL]
                IMAGE = card.find(
                    class_="product-thumbnail__picture").find("img")["src"].replace("110x110", "1024x1024")

                designation_soup = card.find(
                    class_='product-thumbnail__description')

                try:
                    MARQUE = designation_soup.find(
                        'strong').extract().text.strip()
                except:
                    MARQUE = ""

                DESIGNATION = designation_soup.text.replace(
                    "\n", " ").replace("\t", " ").strip().replace("   ", " ").replace("  ", " ")

                if MARQUE.strip():
                    DESIGNATION = f"{MARQUE} : {DESIGNATION}"

                labels_soup = card.find(
                    "div", class_="product-thumbnail__attributes")
                try:
                    PRIX_INFOS = " ".join(label.text for label in labels_soup.select(
                        ".product-attribute"))

                except Exception as e:
                    PRIX_INFOS = ""

                try:
                    PRIX_INFOS += " " + labels_soup.find(
                        "span", {"data-seller-type": "GROCERY"}).text
                except:
                    PRIX_INFOS += ""

                SOUSCATEGORIE = CATEGORIE + "-divers" if CATEGORIE != "divers" else "divers"

                tag_text = DESIGNATION + \
                    (f" {CATEGORIE}" if CATEGORIE != "divers" else "")
                TAG = ",".join([x for x in tag_text.split() if len(
                    x) > 2 and x.isalpha() and x.lower() not in mots_inutiles])

                new_price = card.find(
                    "div", class_="product-price").text.replace("€", "").strip().replace(",", ".")
                try:
                    PRIX = card.select_one(
                        ".product-price.product-price--old").text.replace("€", "").replace(",", ".")
                except Exception as e:
                    PRIX = new_price

                try:
                    NUM_PRODUIT = "1"
                    try:
                        promo = re.sub(
                            r'\s+', ' ', card.find(class_='product-discount-label').text.strip())
                    except:
                        promo = re.sub(
                            r'\s+', ' ', card.select_one('.discount-markups > .product-discount').text.strip())

                    if ("%" in promo):
                        if ("-" in promo):
                            TYPE_PROMOTION = "reduction"
                            if ("dès" in promo):
                                NUM_PRODUIT = promo.split()[-2][0]
                            elif ("sur" in promo):
                                NUM_PRODUIT = promo.split()[-1][0]
                            REDUCTION = promo.split()[0][1:]

                        elif ("cagnotté" in promo):
                            TYPE_PROMOTION = "economie"
                            if ("dès" in promo):
                                NUM_PRODUIT = promo.split()[-2][0]
                            if ("sur" in promo):
                                NUM_PRODUIT = promo.split()[-1][0]
                            REDUCTION = promo.split()[0]
                    elif ("€" in promo):
                        TYPE_PROMOTION = "iRemise"
                        if ("-" in promo):
                            REDUCTION = promo.split()[0][1:]
                        elif ("si"):
                            NUM_PRODUIT = promo.split()[5]
                            REDUCTION = promo.split()[0]
                    elif ("=" in promo):
                        TYPE_PROMOTION = "combinaison"
                        NUM_PRODUIT = promo.split()[0]
                        REDUCTION = str(
                            (int(NUM_PRODUIT) - int(promo.split()[3]))*100)
                    elif ("Offre spéciale" in promo):
                        TYPE_PROMOTION = "catalogue"
                except Exception as e:
                    TYPE_PROMOTION = 'catalogue'
                    NUM_PRODUIT = "1"
                    REDUCTION = "0"

                try:
                    REDUCTION = REDUCTION.replace(",", ".")
                except:
                    pass

                if any(marque_special.lower() in f"{DESIGNATION} {MARQUE}".lower().split() for marque_special in marques_special_auchan):
                    enseigne = ENSEIGNE_ID
                else:
                    enseigne = ""

                main_info_result += [[
                    DESIGNATION, MARQUE, PRIX,	TYPE_PROMOTION,	NUM_PRODUIT,	REDUCTION, 	CATEGORIE,	SOUSCATEGORIE,	TAG,	PRIX_INFOS,	enseigne, MAGASIN_ID, URL]]
                promo = ""
            except Exception as e:
                print(e)
                pass

        with concurrent.futures.ThreadPoolExecutor() as executor:
            meta_data_result = executor.map(scrap_meta_data, links)

        final_result = []
        for i, meta_data in enumerate(meta_data_result):
            final_result += [[meta_data["CODE_BAR"], meta_data["IMAGE"]] + main_info_result[i] +
                             [meta_data["DESCRIPTION"], meta_data["DATE_EXPIRATION"]]]

        if not os.path.exists(f'Promotions/Auchan/{ENSEIGNE_ID}'):
            os.makedirs(f'Promotions/Auchan/{ENSEIGNE_ID}')
        workbook = xlsxwriter.Workbook(
            f'Promotions/Auchan/{ENSEIGNE_ID}/Auchan_Promotion_{CATEGORIE}.xlsx')

        worksheet = workbook.add_worksheet("Listing")
        worksheet.add_table(f'A1:{"ABCDEFGHIJKLMNOPQRSTUVWXYZ"[len(final_result[0])-1]}{len(final_result)}', {'data': final_result,
                                                                                                              'columns': [
                                                                                                                  {'header': 'CODE_BAR'},
                                                                                                                  {'header': 'IMAGE'},
                                                                                                                  {'header': 'DESIGNATION'},
                                                                                                                  {'header': 'MARQUE'},
                                                                                                                  {'header': 'PRIX'},
                                                                                                                  {'header': 'TYPE_PROMOTION'},
                                                                                                                  {'header': 'NUM_PRODUIT'},
                                                                                                                  {'header': 'REDUCTION'},
                                                                                                                  {'header': 'CATEGORIE'},
                                                                                                                  {'header': 'SOUSCATEGORIE'},
                                                                                                                  {'header': 'TAG'},
                                                                                                                  {'header': 'PRIX_INFOS'},
                                                                                                                  {'header': 'ENSEIGNES'},
                                                                                                                  {'header': 'MAGASIN_ID'},
                                                                                                                  {'header': 'URL'},
                                                                                                                  {'header': 'DESCRIPTION'},
                                                                                                                  {'header': 'DATE_EXPIRATION'},


                                                                                                              ]})

        workbook.close()
        print(f"Categorie {CATEGORIE}  finshed and saved")
    except Exception as e:
        print(e)
        print(f"Erreur dans cette categorie {CATEGORIE}")
