from ucimlrepo import fetch_ucirepo, list_available_datasets
import json

result = []

# datasets = list_available_datasets()
# for i in datasets:
#     print(i)
#     print("---")
# exit()
datasets_ids = [1, 2, 9, 10, 14, 15, 16, 17, 19, 20, 27, 29, 31, 42, 45, 46, 50, 52, 53, 59, 60, 62, 73, 76, 80, 81, 94, 101, 105, 109, 110, 111, 143, 144, 151, 159, 162, 186, 189,
                222, 225, 235, 242, 275, 277, 292, 296, 320, 329, 350, 352, 360, 468, 471, 477, 519, 544, 545, 560, 565, 571, 579, 602, 697, 759, 827, 850, 878, 880, 887, 890, 891, 925, 936, 938]
for id in datasets_ids:
    try:

        print(f"-->Fetching dataset {id}")
        iris = fetch_ucirepo(id=id)
        variables = []
        for variable in iris.variables.iterrows():
            variables += [variable[1].to_dict()]

        result += [{
            "id": id,
            'doi': iris.metadata.get("dataset_doi"),
            "title": iris.metadata.get("name"),
            "dataset_rul": iris.metadata.get("data_url"),
            'description': iris.metadata.get("abstract"),
            'area': iris.metadata.get("area"),
            'tasks': iris.metadata.get("tasks"),
            'characteristics': iris.metadata.get("characteristics"),
            'nb_rows': iris.metadata.get("num_instances"),
            'num_features': iris.metadata.get("num_features"),
            'feature_types': iris.metadata.get("feature_types", []),
            'target_col': iris.metadata.get("target_col"),
            'creation_date': iris.metadata.get("year_of_dataset_creation"),
            'last_update': iris.metadata.get("last_update"),
            'creators': iris.metadata.get("creators", []),
            'intro_paper': iris.metadata.get("intro_paper"),
            'summary': iris.metadata.get("additional_info", {}).get("summary", ""),
            'variables': variables,
            'license': {"name ": 'CC BY 4.0', "description": "This dataset is licensed under a Creative Commons Attribution 4.0 International (CC BY 4.0) license.\n\nThis allows for the sharing and adaptation of the datasets for any purpose, provided that the appropriate credit is given."},

        }]

        print(f"Dataset {iris.metadata.get('name')} fetched")
    except Exception as e:
        print(f"An error occurred for dataset id {id}")
        pass

with open('uci.json', 'w', encoding='utf8') as file:
    json.dump(result, file, indent=4, default=str, )
