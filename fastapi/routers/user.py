from typing import Dict, Any, Optional

from fastapi import APIRouter, Header, Request
from werkzeug.security import generate_password_hash

from db.models import User
from db.schemas import UserRegistrationSchema
from db.session import SessionLocal

session = SessionLocal()
router = APIRouter()


@router.post('/user_registration')
def user_registration(request: Request, u: UserRegistrationSchema) -> Dict[str, Any]:
    user = session.query(User).filter_by(email=u.email).first()
    if user:
        return {'msg': 'User with this email already exists.'}
    user = User()
    user.email = u.email
    user.password = generate_password_hash(u.password, method='sha256')
    session.add(user)
    session.commit()
    my_header = request.headers.get('api-key')
    return {
        'msg': 'User created.',
        'api-key': my_header
    }


@router.get('/user')
def user_info():
    return

