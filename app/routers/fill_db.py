from fastapi import APIRouter, Request, HTTPException
import json
from ..etl.data_loaders import load_multiple_json


router = APIRouter()


metadata_path = "app/static/temp_meta_data/"


@router.get("/fill-db")
async def fill_db(source: str = "kaggle"):
    if source not in ["kaggle", "github", "uci", "hugging-face"]:
        raise HTTPException(
            status_code=400, detail="Invalid source")

    try:

        with open(f'{metadata_path}clean/{source}.json', 'r') as file:
            data = json.load(file)

        # Execute your query
        await load_multiple_json(json.dumps(data))

        return {"message": f"{source} data inserted successfully."}

    except Exception as e:
        # Log the error or send it to an error tracking system
        print(f"An error occurred: {e}")

        # Return an error response
        raise HTTPException(
            status_code=500, detail="An error occurred while inserting data.")
