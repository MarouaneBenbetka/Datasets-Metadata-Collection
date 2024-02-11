from datasets import load_dataset, get_dataset_config_names
from huggingface_hub import list_datasets
import concurrent.futures

import json
import os

result = []
save_each = 5


cpt = 0
for dataset in list_datasets():

    try:
        print(f"Dataset: {dataset.id}")

        config_names = get_dataset_config_names(dataset.id)
        config = config_names[0] if config_names else None

        dataset_dict = {
            "author": dataset.author,
            "createdAt": dataset.created_at,
            "downloads": dataset.downloads,
            "id": dataset.id,
            "lastModified": dataset.lastModified,
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
            os.makedirs(
                dataset_dir, exist_ok=True)
            datasets_split.to_csv(dataset_file)

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

    if cpt % save_each == 0:
        with open(f'hugging-face-{cpt}.json', 'w', encoding='utf8') as file:
            json.dump(result, file, indent=4, default=str, )
        result = []
