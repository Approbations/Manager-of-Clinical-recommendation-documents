from db.user_base import UserConnection
from fastapi import HTTPException
import datetime
import jwt

user_base = UserConnection()
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class UserService:
    @staticmethod
    def registry(login: str, password: str, role: str = "client"):
        user = user_base.registry(login, password, role)
        if not user:
            raise HTTPException(status_code=400, detail="Не удалось зарегестрировать пользователя")
        return user

    @staticmethod
    def login(login: str, password: str):
        user = user_base.authenticate(login, password)
        if not user:
            raise HTTPException(status_code=401, detail="Неверный логин или пароль")

        access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {
            "sub": str(user["id"]),
            "login": user["login"],
            "role": user["role"],
            "exp": datetime.datetime.utcnow() + access_token_expires
        }
        access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token": access_token, "token_type": "bearer", "user": user}
