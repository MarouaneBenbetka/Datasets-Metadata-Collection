from fastapi import FastAPI, Depends
from app.routers import datasetes, extract, init_db, transform, auth, load
# Connect to the database


app = FastAPI()


app.include_router(datasetes.router)
app.include_router(extract.router)
app.include_router(load.router)
app.include_router(init_db.router)
app.include_router(transform.router)
app.include_router(auth.router)
