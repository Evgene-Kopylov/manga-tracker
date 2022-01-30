from typing import List

from fastapi import APIRouter, Request
from fastapi import WebSocket, WebSocketDisconnect

from db.session import SessionLocal
from fastapi.templating import Jinja2Templates

from routers.list_all_utils import get_pages

session = SessionLocal()
router = APIRouter()
templates = Jinja2Templates(directory="templates")


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


manager = ChatConnectionManager()


@router.get("/")
async def get(request: Request):
    return templates.TemplateResponse(
        "list_all.html", {"request": request})


@router.websocket("/ws/list_all")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive()
            await manager.broadcast(get_pages())
    except WebSocketDisconnect:
        manager.disconnect(websocket)
