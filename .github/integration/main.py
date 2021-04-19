import os

from pydantic import BaseModel
from fastapi import FastAPI
from fastapi_crudrouter import MemoryCRUDRouter
import uvicorn

API_HOST = os.environ.get("API_HOST", "0.0.0.0")
API_PORT = os.environ.get("API_PORT", 5000)


class Potato(BaseModel):
    id: int
    color: str
    mass: float


app = FastAPI()
app.include_router(MemoryCRUDRouter(schema=Potato))


if __name__ == '__main__':
    uvicorn.run(app, host=API_HOST, port=API_PORT, debug=False)
