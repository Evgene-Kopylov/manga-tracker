from fastapi import FastAPI
import uvicorn
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

from tests.materials.db_list import db_list

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")


class PageScenario(BaseModel):
    url: str
    element: str
    block: str


@app.get("/add_title")
def add_title(url: str, element: str, block: str):
    scenario = PageScenario(
        url=url,
        element=element,
        block=block)
    return scenario


@app.get('/')
def main():
    return db_list


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        reload=True)
