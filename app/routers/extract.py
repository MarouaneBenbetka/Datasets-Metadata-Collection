from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/extract/kaggle")
async def get_users(request: Request):
    request.app.cursor.execute("""
        select * from datasets;
        """)
    return request.app.cursor.fetchall()
