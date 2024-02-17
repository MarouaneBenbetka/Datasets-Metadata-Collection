from fastapi import APIRouter, Request, HTTPException
from app.etl.data_collectors import *
router = APIRouter()


def extract_datasets(source):
    if source == "uci":
        return get_datasets_metadata_uci()
    elif source == "kaggle":
        return get_datasets_metadata_kaggle()
    elif source == "github":
        return get_datasets_metadata_github()
    elif source == "hugging-face":
        return get_datasets_metadata_hugging_face()
    else:
        return None


@router.get("/extract/{source}")
async def get_data_kaggle(source: str, limit=100, start=0):
    if not source:
        raise HTTPException(
            status_code=400, detail="Invalid source")
    if source not in ["kaggle", "github", "uci", "hugging-face"]:
        raise HTTPException(
            status_code=400, detail="Invalid source")

    return extract_datasets(source)


@router.get("/extract/kaggle/scrap-descussions")
async def get_kaggle_descussion():
    return scrap_kaggle_descussions()


@router.get("/extract/kaggle/download-notebooks")
async def get_kaggle_notebooks():
    return add_notebooks_as_json()
