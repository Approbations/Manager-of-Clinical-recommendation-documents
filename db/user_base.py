import psycopg2
import logging
from typing import Tuple, Any
from uuid import UUID
import hashlib
from psycopg2.extras import RealDictCursor
from db.postgres import DataConnection

logger = logging.getLogger(__name__)


class UserConnection(DataConnection):
    def registry(self, login, password, role: str = "client"):
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

    def authenticate(self, login, password):
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

    def change_profile(self, first_name, last_name, login):
        query = f"""UPDATE accounts SET first_name = '{first_name}', last_name = '{last_name}' 
                WHERE login = '{login}';"""

        try:
            with self._get_connection() as conn:
                conn.autocommit = True
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    cur.execute(query)
                    return "ok"
        except Exception as e:
            logger.error(f"Ошибка при обновлении данных: {e}")

    def get_user_profile(self, login):
        query = f"""SELECT a.login, a.first_name, a.last_name, a.role, a.created_at,
                    COALESCE(
                        (SELECT COUNT(*) 
                         FROM documents d 
                         WHERE d.creator = a.login 
                            OR (a.role = 'admin' AND d.creator = 'Минздрав')
                        ), 0
                    ) as documents_count
                FROM accounts a
                WHERE a.login = '{login}';"""

        try:
            with self._get_connection() as conn:
                conn.autocommit = True
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(query)
                    ans = cur.fetchall()
                    return ans
        except psycopg2.Error as e:
            logger.error(f"Ошибка в получении данных: {e}")
            return []
