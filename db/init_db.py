import logging
import os
import sys
import time
from pathlib import Path
from postgres import DataManager

logger = logging.getLogger(__name__)


DOCS_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(DOCS_ROOT, 'docs_processing'))
from upload_files import minzdrav_excel

BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"


if env_path.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except Exception as e:
        print(str(e))


def initialize_database():
    print("Инициализация базы данных...")

    data_manager = DataManager()

    try:
        data_manager.initialization_db()
        print("База данных успешно инициализирована")

        if len(data_manager.get_all_docs()) == 0:
            print("Загрузка начальных данных Минздрава...")
            minzdrav_excel()

    except Exception as e:
        logger.exception("Ошибка при инициализации базы данных: %s", e)
        # Повторная попытка через 5 секунд (не более 3 попыток)
        retry_left = int(os.getenv("INIT_DB_RETRY_COUNT", "3"))
        if retry_left > 1:
            os.environ["INIT_DB_RETRY_COUNT"] = str(retry_left - 1)
            time.sleep(5)
            initialize_database()
        else:
            raise


if __name__ == "__main__":
    initialize_database()
