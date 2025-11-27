from fastapi import APIRouter, HTTPException, Body
from services.user_service import UserService

router = APIRouter()


@router.post("/registry")
async def register_user(login=Body(), password=Body(), role: str = "client"):
    try:
        new_user = UserService.registry(login, password, role)
        return {"message": "Пользователь успешно зарегистрирован", "user": new_user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login_user(login=Body(), password=Body()):
    try:
        token_data = UserService.login(login, password)
        return token_data
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
