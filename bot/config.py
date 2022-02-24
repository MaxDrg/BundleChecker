from aiogram import Bot, Dispatcher
from jsonData import Folder, Users, Apps
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os

class Config:
    def __init__(self):
        self.bot = Bot(token=os.environ.get('TELEGRAM_TOKEN'))
        self.dp = Dispatcher(self.bot, storage=MemoryStorage())

        self.addDataFolder = Folder(file=os.environ.get('DATA_FOLDERS'))
        self.addDataUser = Users(file=os.environ.get('DATA_USERS'))
        self.addDataApps = Apps(file=os.environ.get('DATA_APPS'))

        self.host = os.environ.get('HOST')
        self.port = os.environ.get('PORT')
        self.username = os.environ.get('USER')
        self.passw = os.environ.get('PASS')

        self.database = os.environ.get('DATABASE')
        self.user_data = os.environ.get('DATA_USER')
        self.password_data = os.environ.get('DATA_PASS')
        self.host_data = os.environ.get('HOST')
        self.port_data = os.environ.get('DATA_PORT')

        self.crm_database = os.environ.get('CRM_DATABASE')
        self.crm_user_data = os.environ.get('CRM_DATA_USER')
        self.crm_password_data = os.environ.get('CRM_DATA_PASS')

        self.app_spy_token = os.environ.get('APPSTORESPY_TOKEN')
        self.app_spy_url = os.environ.get('APPSTORESPY_URL')

        self.url = os.environ.get('URL')