import paramiko
import psycopg2
import urllib
import requests
from config import Config
cfg = Config()

class Database: 
	def __init__(self):
		try:
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(cfg.host, port=cfg.port, username=cfg.username, password=cfg.passw)

			print("A connection to the server has been established")
			self.conn = psycopg2.connect(
  			database = cfg.database,
			user = cfg.user_data,
			password = cfg.password_data,
			host = cfg.host_data,
			port = cfg.port_data
			)
			print ("Database connection established")
		except Exception as err:
			print(str(err))

	async def add_app(self, appBundle: str, status: str, folder_id: int, startTime: str, nextTime: str):
		with self.conn.cursor() as cursor:
			cursor.execute("""INSERT INTO apps_apps (app_name, last_time, status, folder_id, start_time, next_check) VALUES (%s, %s, %s, %s, %s, %s);""", (appBundle, startTime, status, folder_id, startTime, nextTime))
		self.conn.commit()

	async def add_folder(self, folderName: str):
		with self.conn.cursor() as cursor:
			cursor.execute("""INSERT INTO apps_folders (name_folder) VALUES (%s);""", (folderName, ))
		self.conn.commit()

	async def get_folders(self):
		with self.conn.cursor() as cursor:
			cursor.execute("""SELECT name_folder FROM apps_folders;""")
			return cursor.fetchall()

	async def get_folder(self, appName: str):
		with self.conn.cursor() as cursor:
			cursor.execute("""SELECT apps_folders.name_folder FROM apps_folders INNER JOIN apps_apps ON apps_folders.id = apps_apps.folder_id WHERE apps_apps.app_name = %s;""", (str(appName), ))
			return cursor.fetchone()[0]
	
	async def get_foldersId(self, folderName: str):
		with self.conn.cursor() as cursor:
			cursor.execute("""SELECT id FROM apps_folders WHERE name_folder = %s;""", (str(folderName), ))
			return cursor.fetchone()[0]

	async def get_status(self, app_id: str):
		with self.conn.cursor() as cursor:
			cursor.execute("""SELECT status FROM apps_apps WHERE app_name = %s;""", (str(app_id), ))
			return cursor.fetchone()[0]

	async def check_folder(self, folderName: str):
		with self.conn.cursor() as cursor:
			cursor.execute("""SELECT EXISTS(SELECT id FROM apps_folders WHERE name_folder = %s);""", (folderName, ))
			return cursor.fetchone()[0]

	async def getBundles(self):
		with self.conn.cursor() as cursor:
			cursor.execute("""SELECT id, app_name, status, next_check, last_update FROM apps_apps;""")
			return cursor.fetchall()

	async def updateStatus(self, str: str, id: int):
		with self.conn.cursor() as cursor:
			cursor.execute("""UPDATE apps_apps SET status = %s WHERE id = %s;""", (str, id))
		self.conn.commit()

	async def updateTime(self, id: int, nowTime: str, nextTime: str):
		with self.conn.cursor() as cursor:
			cursor.execute("""UPDATE apps_apps SET last_time = %s, next_check = %s WHERE id = %s;""", (nowTime, nextTime, id ))
		self.conn.commit()

	async def updateLastTime(self, id: int, nowTime: str):
		with self.conn.cursor() as cursor:
			cursor.execute("""UPDATE apps_apps SET last_time = %s WHERE id = %s;""", (nowTime, id ))
		self.conn.commit()

	async def delFolder(self, id: int):
		with self.conn.cursor() as cursor:
			cursor.execute("""DELETE FROM apps_apps WHERE folder_id = %s;""", (id, ))
			cursor.execute("""DELETE FROM apps_folders WHERE id = %s;""", (id, ))
		self.conn.commit()

	async def checkCurrentApp(self, name: str):
		with self.conn.cursor() as cursor:
			cursor.execute("""SELECT EXISTS(SELECT id FROM apps_apps WHERE app_name = %s);""", (name, ))
			return cursor.fetchone()[0]

	async def change_folder(self, folder_id, app_name):
		with self.conn.cursor() as cursor:
			cursor.execute("""UPDATE apps_apps SET folder_id = %s WHERE app_name = %s;""", (folder_id, app_name, ))
		self.conn.commit()

	async def change_last_update(self, new_update, app_id):
		with self.conn.cursor() as cursor:
			cursor.execute("""UPDATE apps_apps SET last_update = %s WHERE id = %s;""", (new_update, app_id, ))
		self.conn.commit()

class CRM: 
	def __init__(self):
		try:
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(cfg.host, port=cfg.port, username=cfg.username, password=cfg.passw)
			print("A connection to the server has been established")
			self.conn = psycopg2.connect(
  				database = cfg.crm_database,
				user = cfg.crm_user_data,
				password = cfg.crm_password_data,
				host = cfg.host_data,
				port = cfg.port_data
			)
			print ("Database connection established")
		except Exception as err:
			print(str(err))

	async def get_devs(self):
		with self.conn.cursor() as cursor:
			cursor.execute("""SELECT dev FROM crm_developers;""")
			return cursor.fetchall()

	async def check_folder(self, folder_name: str):
		with self.conn.cursor() as cursor:
			cursor.execute("""SELECT EXISTS(SELECT id FROM crm_folders WHERE folder_name = %s);""", (folder_name, ))
			return cursor.fetchone()[0]

	async def add_app(self, app_id, add_time, folder_name):
		app_name = ''
		last_update = ''
		installs = 0
		status = False
		if not await self.check_folder(folder_name):
			with self.conn.cursor() as cursor:
				cursor.execute("""INSERT INTO crm_folders (folder_name) VALUES (%s);""", (folder_name, ))
			self.conn.commit()
		for dev in await self.get_devs():
			dev = {'dev': dev[0]}
			params = urllib.parse.urlencode(dev, quote_via=urllib.parse.quote)
			headers = {"Authorization": f"Bearer {cfg.app_spy_token}"}
			response = requests.get(cfg.app_spy_url, headers=headers, params=params)
			for data in response.json()['data']:
				if data['id'] == app_id:
					app_name = data['name']
					last_update = data['updated']
					installs = data['installs_exact']
					status = data['available']
		if not last_update:
			with self.conn.cursor() as cursor:
				cursor.execute("""INSERT INTO crm_apps (app_id, add_time, folder_id) VALUES (%s, %s, (SELECT id FROM crm_folders WHERE folder_name = %s));""", (app_id, add_time, folder_name,))
			self.conn.commit()
		else:
			with self.conn.cursor() as cursor:
				cursor.execute("""INSERT INTO crm_apps (app_id, add_time, folder_id, app_name, last_update, installs, status) VALUES (%s, %s, (SELECT id FROM crm_folders WHERE folder_name = %s), %s, %s, %s, %s);""", (app_id, add_time, folder_name, app_name, last_update, installs, status, ))
			self.conn.commit()

	async def change_folder(self, app_id: str ,folder_name: str):
		with self.conn.cursor() as cursor:
			cursor.execute("""UPDATE crm_apps SET folder_id = (SELECT id FROM crm_folders WHERE folder_name = %s) WHERE app_id = %s;""", (folder_name, app_id, ))
		self.conn.commit()