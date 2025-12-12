import datetime
import psycopg2
import logging
import os, time
from uuid import UUID
from psycopg2.extras import execute_values, RealDictCursor
from typing import Tuple, Any

logger = logging.getLogger(__name__)


class DataConnection:
    def __init__(self):
        self.dbname = os.getenv("DB_NAME", "test")
        self.user = os.getenv("DB_USER", "postgres")
        self.password = os.getenv("DB_PASSWORD", "qwerty")
        self.host = os.getenv("DB_HOST", "localhost")
        self.port = os.getenv("DB_PORT", "5432")
        self.upload_list = []

    def _get_connection(self):
        conn_config = {
            'dbname': self.dbname,
            'user': self.user,
            'password': self.password,
            'host': self.host,
            'port': self.port
        }
        return psycopg2.connect(**conn_config)

    def _execute_query(self, query: str, params: Tuple = None, fetch: bool = False):
        try:
            with self._get_connection() as conn:
                conn.autocommit = True
                with conn.cursor() as cur:
                    cur.execute(query, params)
                    if fetch:
                        return cur.fetchall()
                    return cur
        except psycopg2.Error as e:
            logger.error(f"Ошибка в базе данных: {e}")
            raise

    def get_all_data(self, table: str):
        query = f"""SELECT * FROM {table};"""

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

    def get_data_where(self, table: str, column: str, value: Any, columns='*', operation='='):
        if type(value) is UUID: value = str(value)

        query = f"""SELECT {columns} FROM {table} WHERE {column} {operation} %s;"""

        try:
            with self._get_connection() as conn:
                conn.autocommit = True
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(query, (value,))
                    ans = cur.fetchall()
                    return ans
        except psycopg2.Error as e:
            logger.error(f"Ошибка в получении данных: {e}")
            return []

    def delete_info(self, table: str, column: str, value: Any):
        if type(value) is UUID: value = str(value)
        delete_query = f"DELETE FROM {table} WHERE {column} = %s;"

        try:
            with self._get_connection() as conn:
                conn.autocommit = True
                with conn.cursor() as cur:
                    cur.execute(delete_query, (value,))

        except Exception as e:
            logger.error(f"Ошибка при удалении: {e}")
            raise

    def create_info(self, table: str, values: Tuple, columns: str = ''):
        query = f"INSERT INTO {table} {columns} VALUES %s;"

        try:
            with self._get_connection() as conn:
                conn.autocommit = True
                with conn.cursor() as cur:
                    cur.execute(query, values)
        except Exception as e:
            logger.error(f"Ошибка при загрузке данных: {e}")
            raise


class DataManager(DataConnection):
    def create_database(self):
        """Создание базы данных если не существует"""
        try:
            conn = self._get_connection()
            conn.autocommit = True
            with conn.cursor() as cur:
                cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{self.dbname}'")
                exists = cur.fetchone()
                if not exists:
                    cur.execute(f"CREATE DATABASE {self.dbname}")
                    logger.info(f"База данных {self.dbname} создана")
            conn.close()
        except Exception as e:
            logger.error(f"Ошибка при создании базы данных: {e}")
            raise

    def create_table(self):
        create_query = '''
            CREATE TABLE IF NOT EXISTS documents (
            id_cr VARCHAR(10) PRIMARY KEY NOT NULL UNIQUE,
            title VARCHAR(400) NOT NULL,
            MCB VARCHAR(400),
            age_category VARCHAR(20) NOT NULL,
            developer VARCHAR(1000),
            placement_date DATE,
            data BYTEA NOT NULL,
            creator VARCHAR(50)
            );
            
            CREATE TABLE IF NOT EXISTS accounts (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            login VARCHAR(255) UNIQUE NOT NULL,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            password_hash VARCHAR(255) NOT NULL,
            role VARCHAR(20) NOT NULL CHECK (role IN ('client', 'admin')),
            created_at TIMESTAMP DEFAULT NOW()
        );
        '''

        check_constraint_query = """
            SELECT constraint_name
            FROM information_schema.table_constraints
            WHERE table_name = 'documents'
              AND constraint_name = 'chk_documents_age';
        """

        add_constraint_query = """
            ALTER TABLE documents
            ADD CONSTRAINT chk_documents_age CHECK (
                age_category IN ('Взрослые', 'Дети', 'Взрослые, дети')
            );
            
            ALTER TABLE accounts
            ADD CONSTRAINT chk_accounts_login CHECK ("login" ~* '[a-zA-Z0-9-_]{3,20}');
        """

        self._execute_query(create_query)
        if not self._execute_query(check_constraint_query, fetch=True):
            self._execute_query(add_constraint_query)
        logger.info("Таблица documents, accounts создана/проверена")

    def initialization_db(self):
        """Полная инициализация базы данных"""
        self.create_database()
        self.create_table()

    def add_to_upload_list(self, id_cr, title, MCB="NULL", age_category='Взрослые', developer='NULL',
                           creator="Минздрав", placement_date=datetime.date.today(), data='NULL'):
        self.upload_list.append((id_cr, title, MCB, age_category, developer, placement_date, data, creator))

    def upload_data(self):
        insert_query = """ INSERT INTO documents (id_cr, title, MCB, age_category, developer, placement_date, data, creator)
            VALUES %s"""

        try:
            with self._get_connection() as conn:
                conn.autocommit = True
                with conn.cursor() as cur:
                    execute_values(cur, insert_query, self.upload_list)
            self.upload_list = []
        except Exception as e:
            logger.error(f"Ошибка при загрузке данных: {e}")
            raise

    def delete_data(self, tpl):
        DataManager.delete_info(self, table="documents", column="id_cr", value=tpl)
        # delete_query = "DELETE FROM documents WHERE id_cr IN %s"
        #
        # try:
        #     with self._get_connection() as conn:
        #         conn.autocommit = True
        #         with conn.cursor() as cur:
        #             cur.execute(delete_query, (tpl,))
        #
        # except Exception as e:
        #     logger.error(f"Ошибка при удалении документов: {e}")
        #     raise

    def is_doc_exist(self, doc_id):
        query = """SELECT * FROM documents
        WHERE id_cr = %s;"""

        try:
            with self._get_connection() as conn:
                conn.autocommit = True
                with conn.cursor() as cur:
                    cur.execute(query, (doc_id,))
                    ans = cur.fetchone()
                    return ans
        except Exception as e:
            logger.error(f"Ошибка получения файла: {e}")
            return []

    def get_all_docs(self):
        return DataManager.get_all_data(self, table="documents")
        # query = """SELECT id_cr, title, MCB, age_category, developer, placement_date FROM documents;"""
        #
        # try:
        #     with self._get_connection() as conn:
        #         conn.autocommit = True
        #         with conn.cursor(cursor_factory=RealDictCursor) as cur:
        #             cur.execute(query)
        #             ans = cur.fetchall()
        #             return [dict(row) for row in ans]
        # except Exception as e:
        #     logger.error(f"Ошибка получения всех файлов: {e}")
        #     return []

    def get_docs_paginated(self, page: int = 0, size: int = 10):
        query = """
            SELECT id_cr, title, MCB, age_category, developer, placement_date, creator 
            FROM documents 
            ORDER BY id_cr
            LIMIT %s OFFSET %s;
        """

        try:
            with self._get_connection() as conn:
                conn.autocommit = True
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(query, (size, page * size))
                    ans = cur.fetchall()
                    return [dict(row) for row in ans]
        except Exception as e:
            logger.error(f"Ошибка получения файлов с пагинацией: {e}")
            return []

    def get_my_docs_paginated(self, creator: str, page: int = 0, size: int = 10):
        query = f"""
            SELECT id_cr, title, MCB, age_category, developer, placement_date, creator 
            FROM documents 
            WHERE creator = '{creator}'
            ORDER BY id_cr
            LIMIT %s OFFSET %s;
        """

        try:
            with self._get_connection() as conn:
                conn.autocommit = True
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(query, (size, page * size))
                    ans = cur.fetchall()
                    return [dict(row) for row in ans]
        except Exception as e:
            logger.error(f"Ошибка получения файлов с пагинацией: {e}")
            return []

    def is_client_doc(self, login, doc_id):
        if type(doc_id) is UUID: doc_id = str(doc_id)

        query = f"""SELECT * FROM documents WHERE creator = '{login}' AND id_cr = '{doc_id}';"""

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

    def get_profiles(self, page: int = 0, size: int = 10):
        query = """
            SELECT a.login, a.first_name, a.last_name, a.role, a.created_at,
                COALESCE(
                    (SELECT COUNT(*) 
                     FROM documents d 
                     WHERE d.creator = a.login 
                        OR (a.role = 'admin' AND d.creator = 'Минздрав')
                    ), 0
                ) as documents_count
            FROM accounts a
            ORDER BY a.created_at
            LIMIT %s OFFSET %s;
        """

        try:
            with self._get_connection() as conn:
                conn.autocommit = True
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(query, (size, page * size))
                    ans = cur.fetchall()
                    return [dict(row) for row in ans]
        except Exception as e:
            logger.error(f"Ошибка получения аккаунтов с пагинацией: {e}")
            return []

    def database_exists(self):
        query = "SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s"
        try:
            with self._get_connection() as conn:
                conn.autocommit = True
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(query, (self.dbname,))
                    ans = cur.fetchall() is not None
                    return ans
        except Exception as e:
            logger.error(f"Ошибка получения аккаунтов с пагинацией: {e}")
            return []
