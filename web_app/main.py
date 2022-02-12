import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.staticfiles import StaticFiles

from db.session import SessionLocal
from routers.page import router as page_router
from routers.test_page import router as test_page_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(page_router)
app.include_router(test_page_router)

session = SessionLocal()


class PageScenario(BaseModel):
    url: str
    element: str
    block: str


@app.get('/current_user')
def show_user():
    return 'current_user'


@app.get("/add_title")
def add_title(url: str, element: str, block: str):
    scenario = PageScenario(
        url=url,
        element=element,
        block=block)
    return scenario


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        reload=True)
