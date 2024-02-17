from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from app.utils.extract import read_raw_data_from_json, save_raw_data_to_json
import time

base_url = "https://www.kaggle.com"


def init_chrome():
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver


def get_descussions(driver, dataset_ref):

    driver.get(f"{base_url}/{dataset_ref}/discussion")
    time.sleep(1)
    descussions_container = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".km-list--avatar-list")))

    html = descussions_container.get_attribute('innerHTML')
    soup = BeautifulSoup(html, 'html.parser')

    descussions_links = soup.select(
        'li > div:nth-child(1) > a:nth-child(2)', href=True)

    links = [link.get("href", None) for link in descussions_links]

    return links


def get_descussion_content(driver, link):

    descussion = {"url": "", "title": "",
                  "user": "", "content": "", "comments": []}

    descussion_url = f"{base_url}{link}"
    descussion["url"] = descussion_url
    driver.get(descussion_url)
    time.sleep(1)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".sc-eTNRI ")))

    print("checkpoint")
    content_container = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="discussion-detail-render-tid"]')))

    html = content_container.get_attribute('innerHTML')
    soup = BeautifulSoup(html, 'html.parser')

    user_soup = soup.select_one("a.sc-jQuReu")
    descussion["user"] = user_soup.get("href", None) if user_soup else None

    descussion_title_soup = soup.select_one(".sc-eTNRI")

    descussion["title"] = descussion_title_soup.text if descussion_title_soup else ""

    descussion_content_soup = soup.select_one(".sc-kClXGk")

    descussion["content"] = descussion_content_soup.text if descussion_content_soup else ""
    print(">descussion_found")
    print(descussion)
    try:
        comments_container_soup = soup.select_one(".sc-bOcqSQ")
        comments_list_soup = comments_container_soup.select("div.sc-jxvlqV")
        print(f">comments found : {len(comments_list_soup)}")
        for comment in comments_list_soup:
            comment_content = {"content": "", "user": "", "replies": ""}
            try:
                comment_soup = comment.select_one(".sc-ktWtzy")
                comment_user_soup = comment_soup.select_one(
                    "a.sc-hsaIUA.beCozw.sc-gMQCKe.dWKKTq")
                comment_content["user"] = comment_user_soup.get(
                    "href", None) if user_soup else None

                comment_text_soup = comment_soup.select_one(".sc-jIYCZY.krFte")

                comment_content["content"] = comment_text_soup.text if comment_text_soup else ""

                comments_replies_soup = comment_soup.select_one(
                    ".sc-dUVpZY.dRLOPq")

                replies = ""
                if comments_replies_soup:
                    replies = "\n".join(block.text if block.text.strip().lower() not in ["quote", "copy permalink"] and block.text.lower().strip().startswith("posted") else "---" for block in comments_replies_soup.select(
                        " p , .uc-code-block code "))

                comment_content["replies"] = replies
                descussion["comments"] = descussion.get(
                    "comments", []) + [comment_content]
                print("--------")
            except Exception as e:

                pass

    except Exception as e:
        print(">No comments")
        pass
    return descussion


def scrap_kaggle_descussions():
    datasets = read_raw_data_from_json("kaggle")
    driver = init_chrome()
    for dataset in datasets:
        try:
            descussions_links = get_descussions(
                driver, dataset["ref"])

            # descussions_links = ['/datasets/nelgiriyewithana/apple-quality/discussion/473469',
            #                      '/datasets/nelgiriyewithana/apple-quality/discussion/471663', '/datasets/nelgiriyewithana/apple-quality/discussion/470940']

            dataset["descussion"] = []
            for descussion_link in descussions_links:
                descussion = get_descussion_content(driver, descussion_link)
                dataset["descussion"] = dataset.get(
                    "descussion", []) + [descussion]

            save_raw_data_to_json(datasets, "kaggle")
        except Exception as e:
            print(e)
            continue

    return datasets
