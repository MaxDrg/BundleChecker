import json

class Folder:
    def __init__(self, file):
        self.file = file

    async def getFolder(self):
        with open(self.file, "r") as json_data:
            return json.load(json_data)

    async def setFolder(self, user_id, folder_name):
        datas = await self.getFolder()
        newData = { str(user_id): str(folder_name) }
        datas.update(newData)
        with open(self.file, "w") as json_data:
            json.dump(datas, json_data, indent=2)

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
        datas = await self.getUsers()
        datas.remove(user_id)
        with open(self.file, "w") as json_data:
            json.dump(datas, json_data, indent=2)