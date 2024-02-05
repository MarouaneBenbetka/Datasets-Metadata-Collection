import kaggle
import json

max_pages = 10


def list_datasets():
    kaggle.api.authenticate()

    page = 1
    total_datasets = []
    while page < max_pages:
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

    # for dataset in total_datasets:
    #     print(dataset)
    #     print(f"Dataset Name: {dataset.name}")

    datasets_dict = [dataset for dataset in total_datasets]

    for dataset in datasets_dict:
        try:
            print(f"Dataset Name: {dataset['title']}")
            kernels = kaggle.api.kernels_list(
                search=dataset['ref'].split('/')[1])
            dataset['Kernels'] = [kernel.__dict__ for kernel in kernels]
        except:
            dataset['Kernels'] = []

    with open('kaggle_datasets.json', 'w', encoding='utf8') as file:
        json.dump(datasets_dict, file, indent=4, default=str, )

    print("Datasets have been saved to 'kaggle_datasets.json'")


if __name__ == "__main__":
    list_datasets()
