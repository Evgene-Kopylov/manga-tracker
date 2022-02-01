import json
from typing import List, MutableMapping, Any

from fastapi import APIRouter, Request
from fastapi import WebSocket, WebSocketDisconnect

from db.models import Page
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


def event_action(ws_msg: MutableMapping[str, Any]) -> None:
    """

    @param ws_msg: websocket msg
    """
    if not ws_msg.get('text'):
        return
    msg = json.loads(ws_msg.get('text'))
    print(f"{msg=}")
    if msg.get('event') == 'ws.onopen':
        return
    _id = msg.get('page_id')
    if not _id:
        return
    _id = int(msg.get('page_id'))
    page = session.query(Page).filter_by(id=_id).first()
    match msg.get('event'):
        case 'remove_page':
            session.delete(page)
        case 'edit_name':
            page.name = msg.get('value')
    session.commit()


@router.websocket("/ws/list_all")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            try:
                ws_msg = await websocket.receive()
                print(f"{ws_msg.get('text')=}")
                event_action(ws_msg)
            except RuntimeError:
                break

            await manager.broadcast(get_pages())
    except WebSocketDisconnect:
        manager.disconnect(websocket)
