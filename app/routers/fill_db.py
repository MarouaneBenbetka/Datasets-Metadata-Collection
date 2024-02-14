from fastapi import APIRouter, Request, HTTPException
import json
from ..etl.data_loaders import load_multiple_json


router = APIRouter()


@router.get("/fill-db")
async def fill_db(request: Request):
    try:
        # Assuming `request.app.db` is your database connection object
        # and `request.app.db` has a cursor attribute you can use.
        with open('app/static/data.json', 'r') as file:
            data = json.load(file)

        # Execute your query
        await load_multiple_json(json.dumps(data))

        return {"message": "Data inserted successfully."}

    except Exception as e:
        # Log the error or send it to an error tracking system
        print(f"An error occurred: {e}")

        # Return an error response
        raise HTTPException(
            status_code=500, detail="An error occurred while inserting data.")
