from pydantic import BaseModel


class UserRegistrationSchema(BaseModel):
    email: str
    password: str
