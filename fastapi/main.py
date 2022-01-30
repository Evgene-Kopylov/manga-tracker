from fastapi import FastAPI, Request
import uvicorn
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from db.models import Page
from db.session import SessionLocal
from routers.page import router as page_router
from routers.list_all import router as list_all_router

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


app.include_router(page_router)
app.include_router(list_all_router)

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


class ChatConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, obj: List):
        for connection in self.active_connections:
            await connection.send_json(obj)


websocket_manager = ChatConnectionManager()


@app.websocket("/ws/list_all")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    try:
        while True:
            await websocket.receive()
            await websocket_manager.broadcast(get_pages())
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        reload=True)
