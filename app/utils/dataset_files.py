
import os


dataset_path = "app/static/datasets_storage/"


def find_csv_in_folder(slug: str, source: str) -> str:
    prefix = "/data/" if source == "kaggle" else ""
    try:
        path = f"{dataset_path}{source}/{slug}{prefix}"
        print(path)
        print(os.listdir(path))
        for file in os.listdir(path):
            print(file)
            if file.endswith(".csv"):
                print(os.path.join(path, file))
                return os.path.join(path, file)
        return ""
    except Exception as e:
        print(e)


def get_dataset(slug, source):
    path = f"{dataset_path}{source}/{slug}"
