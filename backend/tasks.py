from celery import Celery
from celery.utils.log import get_task_logger
import os
from datetime import datetime
import subprocess

celery = Celery("tasks")
celery.config_from_object("celeryconfig")

logger = get_task_logger(__name__)

@celery.task
def scrapping_task():
    logger.info("Scrapping task executed")

@celery.task
def dump_task():
    DB_USER = 'postgres'
    DB_PASS = '12345'
    DB_NAME = 'postgres'
    dir_to_store = os.path.dirname(os.path.abspath(__file__))
    dumps_folder = os.path.join(dir_to_store, "dumps")
    os.makedirs(dumps_folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    dumps_file = os.path.join(dumps_folder, f"dumps_{timestamp}.sql")
    dumps_command = [
        "pg_dump",
        f"--username={DB_USER}",
        f"--password={DB_PASS}",
        f"--dbname={DB_NAME}",
        f"--file={dumps_file}",
    ]
    try:
        subprocess.run(dumps_command, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(e)
        
    logger.info("PostgreSQL Backup created")