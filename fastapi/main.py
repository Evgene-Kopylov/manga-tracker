from fastapi import FastAPI, Request
import uvicorn
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from db.models import Page
from db.session import SessionLocal
from routers.page import router as page_router

from typing import List

from fastapi import WebSocket, WebSocketDisconnect

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.include_router(page_router)

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


def get_pages() -> List:
    pages = session.query(Page).all()
    collection = [
        {
            'id': page.id,
            'url': page.url,
            'name': page.name,
            'last_chapters': [ch for ch in page.chapters.split(', ')][:5],
            'chapters_total': len([ch for ch in page.chapters.split(', ')]),
            'last_check': str(page.last_check),
            'last_update': str(page.last_update)
        } for page in pages
    ]
    collection.sort(key=lambda x: x['last_update'])
    return collection


@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse(
        "list_all.html", {"request": request})


class ChatConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast_obj(self, obj: List):
        for connection in self.active_connections:
            await connection.send_json(obj)


chat_manager = ChatConnectionManager()


@app.get("/chat")
async def get(request: Request):
    pages = session.query(Page).all()
    return templates.TemplateResponse(
        "chat.html",
        {
            "request": request,
            'pages': pages
        }
    )


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket):
    await chat_manager.connect(websocket)
    try:
        while True:
            await websocket.receive()
            await chat_manager.broadcast_obj(get_pages())
    except WebSocketDisconnect:
        chat_manager.disconnect(websocket)
        # await chat_manager.broadcast(f"Client #{client_id} left the chat")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        reload=True)
