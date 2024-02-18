from fastapi import APIRouter, Request, HTTPException, Depends
import json
from ..etl.data_loaders import load_multiple_json
from ..utils.jwt import verify_token
from enum import Enum

router = APIRouter()


metadata_path = "app/static/temp_meta_data/"


class Source(str, Enum):
    kaggle = "kaggle"
    github = "github"
    uci = "uci"
    hugging_face = "hugging-face"


@router.get("/fill-db")
async def fill_db(source: Source = None):

    if not source:
        raise HTTPException(
            status_code=400, detail="Source is required pick one from kaggle, github, uci, hugging-face.")
    if source not in ["kaggle", "github", "uci", "hugging-face"]:
        raise HTTPException(
            status_code=400, detail="Invalid source")

    try:

        with open(f'{metadata_path}clean/{source.value}.json', 'r') as file:
            data = json.load(file)

        # Execute your query
        await load_multiple_json(json.dumps(data))

        return {"message": f"{source.value} data inserted successfully."}

    except Exception as e:
        # Log the error or send it to an error tracking system
        print(f"An error occurred: {e}")

        # Return an error response
        raise HTTPException(
            status_code=500, detail="An error occurred while inserting data.")
