import kaggle
from kaggle.api.kaggle_api_extended import KaggleApi
import json


def fetch_competitions_details():
    # Initialize API
    api = KaggleApi()
    api.authenticate()

    # Fetch competitions list
    competitions = api.competitions_list()
    result = []
    for competition in competitions:
        competition_dict = competition.__dict__

        print(
            f"Discussion URL: {competition.ref}/discussion")

        try:
            datasets = api.competitions_data_list_files(competition.ref)
            for dataset in datasets:
                print(dataset)
                competition_dict["Datasets"].append(dataset.name)
        except Exception as e:
            print("nope")

        result += [competition.__dict__]
    with open('kaggle_competitions.json', 'w', encoding='utf8') as file:
        json.dump(result, file, indent=4, default=str, )

        # Break after one competition for brevity


if __name__ == "__main__":
    fetch_competitions_details()
