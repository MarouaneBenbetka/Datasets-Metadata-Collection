from datasets import load_dataset, get_dataset_config_names
from huggingface_hub import list_datasets
from app.utils.extract import save_raw_data_to_json

import json
import os


def get_dataset_list(limit=100, start=0):
    print("1-Collecting dataset list :")
    datasets = list(list_datasets())[start:limit+1]
    print(f"> {len(datasets)} datasets collected")
    return datasets


def get_datasets_metadata_hugging_face(limit=100, start=0, fast=True):
    result = []
    datasets = get_dataset_list(limit)
    for dataset in datasets:
        try:
            print(f"Dataset: {dataset.id}")

            config_names = get_dataset_config_names(dataset.id)
            config = config_names[0] if config_names else None

            dataset_dict = {
                "author": dataset.author,
                "createdAt": str(dataset.created_at),
                "downloads": dataset.downloads,
                "id": dataset.id,
                "lastModified": str(dataset.lastModified),
                "likes": dataset.likes,
                "sha": dataset.sha,
                "siblings": dataset.siblings,
                "infos": {}
            }

            if "big_patent" in dataset.id:
                continue

            for tag in dataset.tags:
                if ":" not in tag:
                    continue

                key, *value = tag.split(":")
                if key in dataset_dict["infos"]:
                    dataset_dict["infos"][key] = dataset_dict["infos"][key] + \
                        "," + "".join(value)

                dataset_dict["infos"][key] = "".join(value)

            # if fast option is selected there is no need to downlaod the datafile of the dataset cause it will take time
            if fast:
                result.append(dataset_dict)
                continue

            try:
                dataset_name = dataset_dict["id"]
                if config:
                    datasets_split = load_dataset(
                        dataset_name, config, split=None, trust_remote_code=True)
                else:
                    datasets_split = load_dataset(
                        dataset_name, split=None, trust_remote_code=True)

                dataset_dir = f"./datasets_hugging_face/{dataset_name.replace('/','-')}"
                dataset_file = f"{dataset_dir}/train.csv"

                try:
                    os.makedirs(
                        dataset_dir, exist_ok=True)
                    datasets_split.to_csv(dataset_file)
                except Exception as e:
                    print(">no dataset file")

                # Accessing the dataset metadata

                dataset_dict["features"] = datasets_split.__getattribute__(
                    "features")
                dataset_dict["version"] = datasets_split.__getattribute__(
                    "version")
                dataset_dict["download_size"] = datasets_split.__getattribute__(
                    "download_size")
                dataset_dict["dataset_size"] = datasets_split.__getattribute__(
                    "dataset_size")
                dataset_dict["info"] = datasets_split.__getattribute__(
                    "info")
                dataset_dict["license"] = datasets_split.__getattribute__(
                    "license")
                dataset_dict["nb_rows"] = datasets_split.shape[0]
                dataset_dict["local_link"] = dataset_file
            except Exception as e:
                print(e)

            cpt += 1
            result.append(dataset_dict)

        except Exception as e:
            print(e)

    save_raw_data_to_json(result, 'hugging_face2')
    return result
