from typing import Dict, Any

from fastapi import APIRouter
from werkzeug.security import generate_password_hash

from db.models import User
from db.schemas import UserRegistrationSchema
from db.session import SessionLocal

session = SessionLocal()
router = APIRouter()


@router.post('/user_registration')
def user_registration(request: UserRegistrationSchema) -> Dict[str, Any]:
    user = session.query(User).filter_by(email=request.email).first()
    if user:
        return {'msg': 'User with this email already exists.'}
    user = User()
    user.email = request.email
    user.password = generate_password_hash(request.password, method='sha256')
    session.add(user)
    session.commit()
    return {'msg': 'User created.'}
