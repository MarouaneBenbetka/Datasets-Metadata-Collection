from datetime import datetime
from app.utils.cleaning import generate_tags

current_datetime = datetime.utcnow()
formatted_date = current_datetime.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

source = {
    "name": "UCI-ML-Repo",
    "url": "https://archive.ics.uci.edu/",
    "description": "The UCI Machine Learning Repository is a collection of databases, domain theories, and data generators widely used by the machine learning community, providing a diverse range of datasets for research and experimentation in various fields of artificial intelligence and data science."
}


license = {
    "name": "Creative Commons Attribution 4.0 International License (CC-BY-4.0)",
    "url": "https://creativecommons.org/licenses/by/4.0/",
    "description": "This license lets others remix, tweak, and build upon your work, even commercially, as long as they credit you for the original creation. This is the most flexible of the licenses offered, in terms of what others can do with your works."
}


base_url = "https://archive.ics.uci.edu/datasets"


def clean_uci_dataset(dataset):

    clean_dataset = {}

    clean_dataset["title"] = dataset.get("title", "")
    clean_dataset["url"] = base_url+dataset.get("dataset_rul", "")
    clean_dataset["description"] = f'{dataset.get("description","")} \n\n {dataset.get("summary","")} \n\n doi code : {dataset.get("doi","")}'
    clean_dataset["totalBytes"] = 0
    year = int(dataset.get("creation_date", None))
    if year:
        clean_dataset["creation_date"] = datetime(
            year=year, month=1, day=1).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "X"
    else:
        clean_dataset["creation_date"] = formatted_date
    clean_dataset["source"] = source
    clean_dataset["stats"] = None
    creators = dataset.get("creators", [])

    owners_list = []
    for creator in creators:
        owners_list += [{
            "name": creator,
            "ref": f'https://www.linkedin.com/search/results/all/?keywords={creator.replace(" ","+")}'
        }]
    clean_dataset["owners"] = owners_list

    clean_dataset["license"] = license

    clean_dataset["notebooks"] = []
    clean_dataset["descussions"] = []

    features = []
    for feature in dataset.get("variables", []):
        features += [{
            "name": feature["name"],
            "type": feature["type"],
            "description": f'This is a {feature["role"]} variable. described as {feature["description"]}.'
        }]
    clean_dataset["features"] = features

    tasks = dataset.get("tasks", [])
    tags = generate_tags(clean_dataset["title"])
    clean_dataset["tags"] = tasks + tags
    clean_dataset["useCases"] = tasks
    clean_dataset["issues"] = []

    return clean_dataset


# result = []
# with open('./datasets/uci/uci.json', 'r') as file:
#     data = json.load(file)
#     for dataset in data:
#         try:
#             result += [clean_dataset(dataset)]
#         except Exception as e:
#             print(f'Error in this dataset: {dataset.get("title", "")}')
#             print(e)


# with open('./datasets/uci/uci-cleaned.json', 'w') as file:
#     json.dump(result, file)
