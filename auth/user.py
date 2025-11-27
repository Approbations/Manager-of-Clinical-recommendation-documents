from fastapi import APIRouter, HTTPException
from services.user_service import UserService

router = APIRouter()


@router.post("/registry")
async def register_user(login: str, password: str, role: str = "client"):
    try:
        new_user = UserService.registry(login, password, role)
        return {"message": "Пользователь успешно зарегистрирован", "user": new_user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login_user(login: str, password: str):
    try:
        token_data = UserService.login(login, password)
        return token_data
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

'''CREATE TABLE IF NOT EXISTS accounts (
	id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	login VARCHAR(255) UNIQUE NOT NULL,
	password_hash VARCHAR(255) NOT NULL,
	role VARCHAR(20) NOT NULL CHECK (role IN ('client', 'admin')),
	created_at TIMESTAMP DEFAULT NOW()
);

ALTER TABLE documents
ADD COLUMN creator VARCHAR(50);

UPDATE documents
SET creator = 'Минздрав';'''
