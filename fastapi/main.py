from fastapi import FastAPI
from fastapi import Request
import uvicorn
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")


class TextArea(BaseModel):
    content: str


db = [
    {
        "id": 0,
        "name": "Go to the gym",
        "done": False
    },
    {
        "id": 1,
        "name": "Walk the dog",
        "done": False
    },
    {
        "id": 2,
        "name": "Get some pizza",
        "done": False
    },
    {
        "name": "Finish this project",
        "id": 3,
        "done": False
    }
]


@app.post("/add")
async def post_textarea(data: TextArea):
    print(data.dict())
    return {**data.dict()}


@app.get("/")
async def serve_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get('/todos')
def fetch_users():
    return db


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        reload=True)
