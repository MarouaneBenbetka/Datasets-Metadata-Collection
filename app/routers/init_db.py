from fastapi import APIRouter, Request, Depends
from ..db_schema import create_schema, create_loading_procedure, create_indexes, create_views
from ..utils.jwt import verify_token


router = APIRouter()


@router.get("/init-db")
async def init_db(user: str = Depends(verify_token)):
    print("Tables Creation")
    await create_schema()

    print("Indexes Creation")
    await create_indexes()

    print("Loading Procedure Creation")
    await create_loading_procedure()

    print("Views/Materielized Views Creation")
    await create_views()

    return {"message": "Schema created successfully"}
