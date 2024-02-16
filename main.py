from fastapi import FastAPI, Depends
from app.routers import datasetes, extract, fill_db, init_db, clean_datasets, auth
# Connect to the database


app = FastAPI()


app.include_router(datasetes.router)
app.include_router(extract.router)
app.include_router(fill_db.router)
app.include_router(init_db.router)
app.include_router(clean_datasets.router)
app.include_router(auth.router)
