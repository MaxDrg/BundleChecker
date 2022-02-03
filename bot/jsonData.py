import json

class Folder:
    def __init__(self, file):
        self.file = file

    async def getFolder(self):
        with open(self.file, "r") as json_data:
            return json.load(json_data)

    async def setFolder(self, user_id, folder_name):
        data = await self.getFolder()
        newData = { str(user_id): str(folder_name) }
        data.update(newData)
        with open(self.file, "w") as json_data:
            json.dump(data, json_data, indent=2)

class Users:
    def __init__(self, file):
        self.file = file

    async def getUsers(self):
        with open(self.file, "r") as json_data:
            return json.load(json_data)

    async def addUser(self, user_id):
        datas = await self.getUsers()
        datas.append(user_id)
        with open(self.file, "w") as json_data:
            json.dump(datas, json_data, indent=2)

    async def delUser(self, user_id):
        data = await self.getUsers()
        data.remove(user_id)
        with open(self.file, "w") as json_data:
            json.dump(data, json_data, indent=2)

class Apps:
    def __init__(self, file):
        self.file = file

    async def change_apps(self, user_id):
        with open(self.file, "r") as json_data:
            return json.load(json_data)[str(user_id)]

    async def get_apps(self):
        with open(self.file, "r") as json_data:
            return json.load(json_data)

    async def add_app(self, user_id, folder, apps):
        data = await self.get_apps()
        newData = { str(user_id): {
            "folder": folder,
            "apps": apps } 
        }
        data.update(newData)
        with open(self.file, "w") as json_data:
            json.dump(data, json_data, indent=2)