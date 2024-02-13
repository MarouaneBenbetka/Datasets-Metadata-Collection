import os
import kaggle
import pandas as pd
import json


kaggle_datasets_path = r"C:\Users\ASUS ROG\OneDrive\Desktop\ESI\Current\S1\BDA\Dataset-Quality-Checker\Kaggle-API\kaggle_datasets.json"


def download_and_process_dataset(dataset_name, download_path='./', rows=1000):
    # Ensure Kaggle API is configured
    if not os.path.exists(os.path.join(os.path.expanduser('~'), '.kaggle/kaggle.json')):
        raise ValueError(
            "Kaggle API credentials not found. Please configure your Kaggle API key.")

    # Create download path if it does not exist
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # Use the Kaggle API to download the dataset
    # Note: This does not unzip by default

    kaggle.api.dataset_download_files(
        dataset_name, path=download_path, unzip=True)

    # extract_zip_with_shutil(dataset_file_path, dataset_name)

    # Assuming CSV files are directly in download_path now, either from unzip or direct download
    csv_files = [f for f in os.listdir(download_path) if f.endswith('.csv')]
    if not csv_files:
        raise ValueError("No CSV files found in the dataset.")
    first_csv_file = csv_files[0]

    # Read the first 1000 rows of the CSV file
    csv_path = os.path.join(download_path, first_csv_file)
    df = pd.read_csv(csv_path, nrows=rows)

    for file in csv_files:
        os.remove(os.path.join(download_path, file))

    # Optionally, save the processed DataFrame to a new CSV file
    output_csv_path = os.path.join(
        download_path, f"processed_{dataset_name.replace('/', '_')}.csv")
    df.to_csv(output_csv_path, index=False)

    print(f"Dataset processed and saved to {output_csv_path}")


def read_dataset_refs(json_file_path):

    with open(json_file_path, 'r') as file:
        data = json.load(file)
        return [dataset["ref"] for dataset in data]


for ref in read_dataset_refs(kaggle_datasets_path):
    try:
        print(">Downloading dataset: ", ref)
        dataset_name = ref
        download_path = "datasets/" + dataset_name+"/data/"
        os.makedirs(download_path, exist_ok=True)
        download_and_process_dataset(
            dataset_name,  rows=1000, download_path=download_path)
    except Exception as e:
        print("----")
        print(f"Error with {ref}")
        print(e)
        print("----")
        continue
