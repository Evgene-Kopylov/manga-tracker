import json
import os
from typing import List, MutableMapping, Any

from dotenv import load_dotenv, find_dotenv
from fastapi import APIRouter, Request
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from db.models import Page
from db.session import SessionLocal
from routers.page_utils import get_name, get_pages
from routers.tests.rmq_pablish import Publisher

session = SessionLocal()
router = APIRouter()

load_dotenv(find_dotenv())
url = os.environ.get('AMQP_URL', "amqp://guest:guest@localhost:5672/")
rmq_config = {
    'url': url,
    'exchange': 'manga_tracker'
}
publisher = Publisher(rmq_config)

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
async def list_all(request: Request):
    return templates.TemplateResponse(
        "list_all.html", {"request": request})


def event_action(ws_msg: MutableMapping[str, Any]) -> None:
    """

    @param ws_msg: websocket msg
    """
    if not ws_msg.get('text'):
        return
    msg = json.loads(ws_msg.get('text'))
    if msg.get('event') == 'ws.onopen':
        return
    _id = msg.get('page_id')
    if not _id:
        return
    print(f"{msg=}")
    _id = int(msg.get('page_id'))
    page = session.query(Page).filter_by(id=_id).first()
    if msg.get('event') == 'remove_page':
        session.delete(page)
    elif msg.get('event') == 'edit_name':
        page.name = msg.get('value')
    else:
        return
    session.commit()


@router.websocket("/ws/list_all")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            try:
                ws_msg = await websocket.receive()
                event_action(ws_msg)
            except RuntimeError:
                break

            await manager.broadcast(get_pages())
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@router.get('/add_page')
def add_page(url: str, element: str, block: str
             ) -> RedirectResponse:
    page = session.query(Page).filter_by(
        url=url
    ).first()
    if not page:
        page = Page()
        page.url = url
        page.element = element
        page.block = block
        page.name = get_name(url)
        session.add(page)
        page.pending = True
        session.commit()
        publisher.publish('new_page', str(page.id))
    else:
        print('page duplicate')

    return RedirectResponse(
        url='/' + f"?new_id={page.id}"
    )
