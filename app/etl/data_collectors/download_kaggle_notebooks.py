import json
import os
from kaggle.api.kaggle_api_extended import KaggleApi
import shutil
from app.utils.extract import read_raw_data_from_json, save_raw_data_to_json


# credentials
os.environ['KAGGLE_USERNAME'] = os.getenv("KAGGLE_USERNAME")
os.environ['KAGGLE_KEY'] = os.getenv("KAGGLE_KEY")


def clear_directory(folder_path):
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)  # Removes files and symbolic links
            elif os.path.isdir(item_path):
                # Removes directories and their contents
                shutil.rmtree(item_path)
        except Exception as e:
            print(f'Failed to delete {item_path}. Reason: {e}')


def add_notebooks_as_json():

    # Load slugs from JSON file
    data = read_raw_data_from_json("kaggle")

    # Initialize and authenticate Kaggle API
    api = KaggleApi()
    api.authenticate()

    # Download path
    # Update this to your desired download path
    download_path = '/app/static/temp_notebooks/'

    for dataset in data:
        for notebook in dataset["notebooks"]:
            slug = notebook["ref"]
            try:
                # Attempt to download the notebook
                api.kernels_pull(slug, path=download_path)
                ipynb_files = [f for f in os.listdir(
                    download_path) if f.endswith('.ipynb')]
                with open(download_path+ipynb_files[0], 'r', encoding='utf-8') as file:
                    notebook_json = json.load(file)

                notebook["content"] = notebook_json

                print(f"Downloaded notebook for slug: {slug}")
            except Exception as e:
                print(
                    f"Error downloading notebook for slug: {slug}. Error: {e}")

            save_raw_data_to_json(data, "kaggle")

            clear_directory(download_path)
