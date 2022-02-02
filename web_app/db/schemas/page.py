from typing import Optional

from pydantic import BaseModel


class AddPageSchema(BaseModel):
    url: str
    element: Optional[str]
    block: Optional[str]
