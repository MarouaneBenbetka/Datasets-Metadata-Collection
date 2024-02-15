from fastapi import APIRouter, Request, HTTPException
import json
from ..etl.data_cleaners import clean_uci_dataset, clean_github_dataset, clean_hugging_face_dataset, clean_kaggle_dataset


router = APIRouter()


metadata_path = "app/static/temp_meta_data/"
clean_relative_path = "clean/"
raw_relative_path = "raw/"


def clean_dataset(dataset, source):
    if source == "uci":
        return clean_uci_dataset(dataset)
    elif source == "kaggle":
        return clean_kaggle_dataset(dataset)
    elif source == "github":
        return clean_github_dataset(dataset)
    elif source == "hugging-face":
        return clean_hugging_face_dataset(dataset)
    else:
        return None


@router.get("/clean")
async def clean_handler(source: str = "kaggle"):
    if source not in ["kaggle", "github", "uci", "hugging-face"]:
        raise HTTPException(
            status_code=400, detail="Invalid source")

    try:
        result = []
        with open(f'{metadata_path}{raw_relative_path}{source}.json', 'r') as file:
            data = json.load(file)
            for dataset in data:
                print("cleaning dataset")
                try:
                    result += [clean_dataset(dataset, source)]
                except Exception as e:
                    print(
                        f"Error in this dataset: {dataset.get('ref', 'unknown')}")
                    print(e)

        with open(f'{metadata_path}{clean_relative_path}{source}.json', 'w') as file:
            json.dump(result, file)
        return {"message": f"{source} data  cleaned successfully.",
                "location": f"{metadata_path}{clean_relative_path}{source}.json"
                }
    except Exception as e:
        # Log the error or send it to an error tracking system
        print(f"An error occurred: {e}")

        # Return an error response
        raise HTTPException(
            status_code=500, detail="An error occurred while inserting data.")
