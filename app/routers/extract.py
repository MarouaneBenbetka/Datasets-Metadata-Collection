from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/extract/kaggle")
async def get_data_kaggle(request: Request):
    request.app.cursor.execute("""
        select * from datasets;
        """)
    return request.app.cursor.fetchall()


@router.get("/extract/github")
async def get_data_github(request: Request):
    request.app.cursor.execute("""
        select * from datasets;
        """)
    return request.app.cursor.fetchall()


@router.get("/extract/huggingface")
async def get_data_huggingface(request: Request):
    request.app.cursor.execute("""
        select * from datasets;
        """)
    return request.app.cursor.fetchall()


@router.get("/extract/uci")
async def get_data_uci(request: Request):
    request.app.cursor.execute("""
        select * from datasets;
        """)
    return request.app.cursor.fetchall()
