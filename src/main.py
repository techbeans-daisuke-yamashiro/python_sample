from typing import Union

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database import create_db_and_tables, create_seed_data
from errors import ApiError

from routers import APIRoot

#initialize FastAPI
app = FastAPI()
app.mount("/assets", StaticFiles(directory="assets"), name="static")
app.include_router(APIRoot)

@app.get("/")
def read_root():
    return {"Hello": "World!"}


@app.on_event("startup")
def init_app():
    pass

@app.exception_handler(ApiError)
async def api_error_handler(request, err: ApiError):
    raise HTTPException(status_code=err.status_code, detail=f'{err.detail}')
