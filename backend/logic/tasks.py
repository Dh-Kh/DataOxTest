from celery import shared_task
from celery.utils.log import get_task_logger
import os
from datetime import datetime
from .selenium_task import constructor, add_to_database

logger = get_task_logger(__name__)

@shared_task
def scrapping_task():
    logger.info("Task started")
    constructor()
    logger.info("First step completed")
    add_to_database()
    logger.info("Scrapping task executed")

@shared_task
def dump_task():
    DB_HOST = 'pgdb'
    DB_USER = 'postgres'
    DB_NAME = 'postgres'
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    BACKUP_FOLDER = os.path.join(SCRIPT_DIR, 'dumps')  
    TIMESTAMP = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    BACKUP_FILE = DB_NAME + '_' + TIMESTAMP + '.sql'
    os.makedirs(BACKUP_FOLDER, exist_ok=True)
    BACKUP_CMD = "pg_dump -h {0} -U {1} -d {2} > {3}".format(DB_HOST, DB_USER, DB_NAME, os.path.join(BACKUP_FOLDER, BACKUP_FILE))
    os.system(BACKUP_CMD)

