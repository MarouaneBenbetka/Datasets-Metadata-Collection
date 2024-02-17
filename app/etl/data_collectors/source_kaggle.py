import kaggle
import json
from app.utils.extract import save_raw_data_to_json
import os

max_pages = 10
base_url = "https://www.kaggle.com"
metadata_temp_path = r'app/static/temp_meta_data/raw/kaggle_temp'

os.environ['KAGGLE_USERNAME'] = os.getenv("KAGGLE_USERNAME")
os.environ['KAGGLE_KEY'] = os.getenv("KAGGLE_KEY")


def get_datasets_metadata_kaggle(max_pages=max_pages):
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
        "ref": dataset.get("ref", ""),
        "title": dataset.get("title", ""),
        "creator": dataset.get("creatorName", ""),
        "totalBytes": dataset.get("totalBytes", ""),
        "lastUpdated": dataset.get("lastUpdated", ""),
        "stats": {"downloadCount": dataset.get("downloadCount", None),
                  "voteCount": dataset.get("voteCount", None),
                  "viewCount": dataset.get("viewCount", None),
                  },
        "owner": {"ref": dataset.get("ownerRef", None), "name": dataset.get("ownerName", None)},
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
                    "lastRunTime": str(kernel_dict.get("lastRunTime", "")),
                    "totalVotes": kernel_dict.get("totalVotes"),
                    "language": kernel_dict.get("language"),
                }
                notebooks.append(notebook)

            dataset['notebooks'] = notebooks
        except:
            dataset['notebooks'] = []

        print("=========")
    save_raw_data_to_json(datasets_dict, "kaggle")

    return datasets_dict
