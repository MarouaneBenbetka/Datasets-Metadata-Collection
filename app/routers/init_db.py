from fastapi import APIRouter, Request, Depends
from ..db_schema import create_schema, create_loading_procedure
from ..utils.jwt import verify_token


router = APIRouter()


@router.get("/init-db")
async def init_db(user: str = Depends(verify_token)):
    await create_schema()
    await create_loading_procedure()
    return {"message": "Schema created successfully"}
