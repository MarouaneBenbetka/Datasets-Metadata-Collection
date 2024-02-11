import kaggle
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from bs4 import BeautifulSoup
import concurrent.futures
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

max_pages = 2
base_url = "https://www.kaggle.com"
metadata_temp_path = r'./metadata'


def get_list_datasets():
    kaggle.api.authenticate()

    page = 1
    total_datasets = []
    print("1-Collecting dataset basic infos :")
    while page < max_pages+1:
        print(f"\t>page {page}")
        try:
            datasets = kaggle.api.datasets_list(search="", page=page)
            if datasets:
                total_datasets.extend(datasets)
                page += 1
            else:
                break
        except Exception as e:
            print(f"An error occurred: {e}")
            break
    print("-------")

    datasets_dict = [{
        "ref": dataset.get("ref"),
        "title": dataset.get("title"),
        "creator": dataset.get("creatorName"),
        "totalBytes": dataset.get("totalBytes"),
        "lastUpdated": dataset.get("lastUpdated"),
        "stats": {"downloadCount": dataset.get("downloadCount"),
                  "voteCount": dataset.get("voteCount"),
                  "viewCount": dataset.get("viewCount"),
                  },
        "owner": {"ref": dataset.get("ownerRef"), "name": dataset.get("ownerName")},
        "usability": dataset.get("usabilityRating"),
    } for dataset in datasets]

    print("2-Collecting dataset meta infos :")
    # collecting meta data for each dataset
    for dataset in datasets_dict:
        # meta data file :
        print(f"\t>dataset : {dataset.get('ref')}")
        try:
            kaggle.api.dataset_metadata(
                dataset['ref'], path=metadata_temp_path)
            with open(f"{metadata_temp_path}/dataset-metadata.json", 'r') as file:
                metadata = json.load(file)
                dataset["keywords"] = metadata.get("keywords")
                dataset["licenses"] = metadata.get("licenses")
                dataset["description"] = metadata.get("description")
                dataset["subtitle"] = metadata.get("subtitle")

        except:
            dataset["keywords"] = []
            dataset["licenses"] = []
            dataset["description"] = ""
            dataset["subtitle"] = ""

        print("\tCollecting associated notebooks")

        # notebooks for each dataset
        try:
            kaggle.api.dataset_metadata(dataset['ref'], path='./metadata')
            kernels = kaggle.api.kernels_list(
                search=dataset['ref'].split('/')[1])

            notebooks = []

            for kernel in kernels:
                kernel_dict = kernel.__dict__
                notebook = {
                    "ref": kernel_dict.get("ref"),
                    "title": kernel_dict.get("title"),
                    "author": kernel_dict.get("author"),
                    "lastRunTime": kernel_dict.get("lastRunTime"),
                    "totalVotes": kernel_dict.get("totalVotes"),
                    "language": kernel_dict.get("language"),
                }
                notebooks.append(notebook)

            dataset['notebooks'] = notebooks
        except:
            dataset['notebooks'] = []

        print("=========")

    with open('kaggle_datasets_api.json', 'w', encoding='utf8') as file:
        json.dump(datasets_dict, file, indent=4, default=str, )

    return datasets_dict


def init_chrome():
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver


def get_descussions(driver, dataset_ref):
    print(f"{base_url}/{dataset_ref}/discussion")
    driver.get(f"{base_url}/{dataset_ref}/discussion")

    descussions_container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".km-list--avatar-list")))

    html = descussions_container.get_attribute('innerHTML')
    soup = BeautifulSoup(html, 'html.parser')
    descussions_links = soup.select(
        ' li > div:nth-child(1) > a:nth-child(2)', href=True)

    return [link.get("href", None) for link in descussions_links]


def get_descussion_content(driver, link):

    descussion = {"url": "", "title": "",
                  "user": "", "content": "", "comments": []}

    descussion_url = f"{base_url}{link}"
    descussion["url"] = descussion_url
    driver.get(descussion_url)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".sc-eTNRI ")))

    content_container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".sc-iiqfCt")))

    html = content_container.get_attribute('innerHTML')
    soup = BeautifulSoup(html, 'html.parser')

    user_soup = soup.select_one("a.sc-jQuReu")
    descussion["user"] = user_soup.get("href", None) if user_soup else None

    descussion_title_soup = soup.select_one(".sc-eTNRI")

    descussion["title"] = descussion_title_soup.text if descussion_title_soup else ""

    descussion_content_soup = soup.select_one(".sc-bihjUw.cWVrVx")

    descussion["content"] = descussion_content_soup.text if descussion_content_soup else ""

    try:
        comments_container_soup = soup.select_one(".sc-bOcqSQ")
        comments_list_soup = comments_container_soup.select("div.sc-jxvlqV")
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
        pass
    return descussion


if __name__ == "__main__":
    datasets = get_list_datasets()
    driver = init_chrome()
    for dataset in datasets:
        try:
            print(f"Start scrapping {dataset['ref']}")
            descussions_links = get_descussions(
                driver, dataset["ref"])
            # descussions_links = ['/datasets/nelgiriyewithana/apple-quality/discussion/473469',
            #                      '/datasets/nelgiriyewithana/apple-quality/discussion/471663', '/datasets/nelgiriyewithana/apple-quality/discussion/470940']
            dataset["descussion"] = []
            for descussion_link in descussions_links:
                descussion = get_descussion_content(driver, descussion_link)
                dataset["descussion"] = dataset.get(
                    "descussion", []) + [descussion]
        except Exception as e:
            pass
    with open('kaggle_datasets.json', 'w', encoding='utf8') as file:
        json.dump(datasets, file, indent=4, default=str, )
