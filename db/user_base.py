import psycopg2
import logging
from typing import Tuple, Any
from uuid import UUID
import hashlib
from psycopg2.extras import RealDictCursor
from db.postgres import DataConnection

logger = logging.getLogger(__name__)


class UserConnection(DataConnection):
    def registry(self, login: str, password: str, role: str = "client"):
        pass_hash = hashlib.sha256(password.encode()).hexdigest()
        query = """
            INSERT INTO accounts (login, password_hash, role)
            VALUES (%s, %s, %s)
            RETURNING id, login, role;
        """
        try:
            with self._get_connection() as conn:
                conn.autocommit = True
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(query, (login, pass_hash, role))
                    user = cur.fetchone()
                    return user
        except Exception as e:
            logger.error(f"Ошибка при регистрации: {e}")
            raise

    def authenticate(self, login: str, password: str):
        pass_hash = hashlib.sha256(password.encode()).hexdigest()
        query = """
            SELECT id, login, role FROM accounts
            WHERE login = %s AND password_hash = %s;
        """
        try:
            with self._get_connection() as conn:
                conn.autocommit = True
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(query, (login, pass_hash))
                    user = cur.fetchone()
                    return user
        except Exception as e:
            logger.error(f"Ошибка при аутентификации: {e}")
            raise
