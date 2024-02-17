import json


metadata_path = "app/static/temp_meta_data/raw/"


def save_raw_data_to_json(data, source):
    with open(f"{metadata_path}{source}.json", 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print(f"{source} data saved to '{metadata_path}{source}.json' successfully.")


def read_raw_data_from_json(source):
    with open(f"{metadata_path}{source}.json", 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data
