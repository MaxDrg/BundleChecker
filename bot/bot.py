import asyncio
import logging
import aioschedule
import datetime
from config import Config
from database import Database, CRM
from buttons import Button
from track import Track
from states import States
from aiogram import executor, types
from config import Config
from url import Web
from pytz import timezone
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Configure logging
logging.basicConfig(level=logging.INFO)
cfg = Config()
btn = Button()
db = Database()
crm = CRM()

# first
@cfg.dp.message_handler(commands="start")
async def Start(message: types.Message):
    if await checkUser(message.from_user.id):
        await cfg.bot.send_message(message.from_user.id, "Привет {}!\nЭтот бот".format(message.from_user.first_name) +
        " создан для отслеживания работы приложений в Google Play Market", reply_markup=btn.markup)
    else:
        await cfg.bot.send_message(message.from_user.id, "Привет {}!\nК сожалению,".format(message.from_user.first_name) +
        " этот бот для вас недоступен, обратитесь к администратору :(")

@cfg.dp.message_handler(lambda message: message.text == 'Приложения и папки') 
async def folders_apps(message: types.Message):
    if await checkUser(message.from_user.id):
        await cfg.bot.send_message(message.from_user.id, "Введите номер папки для нового приложения или создайте новую" + 
        "\n\nСписок папок:{}".format(await printList()), 
        reply_markup=btn.choose_folder)
        await States.setFolder.set()
    else:
        await cfg.bot.send_message(message.from_user.id, "К сожалению,".format(message.from_user.first_name) +
        " этот бот для вас недоступен, обратитесь к администратору :(")

@cfg.dp.message_handler(lambda message: message.text == 'Обновить') 
async def update(message: types.Message):
    if await checkUser(message.from_user.id):
        await Track.update()
        await cfg.bot.send_message(message.from_user.id, "Статусы приложений обновлены!")
    else:
        await cfg.bot.send_message(message.from_user.id, "К сожалению,".format(message.from_user.first_name) +
        " этот бот для вас недоступен, обратитесь к администратору :(")

@cfg.dp.message_handler(lambda message: message.text == 'Вывести данные') 
async def print(message: types.Message):
    if await checkUser(message.from_user.id):
        await cfg.bot.send_message(message.from_user.id, "Введите номер папки данные которой хотите вывести" + 
        "\n\nСписок папок:{}".format(await printList()), 
        reply_markup=btn.back)
        await States.setOpenFolder.set()
    else:
        await cfg.bot.send_message(message.from_user.id, "К сожалению,".format(message.from_user.first_name) +
        " этот бот для вас недоступен, обратитесь к администратору :(")

@cfg.dp.message_handler(lambda message: message.text == 'Пользователи') 
async def users(message: types.Message):
    if await checkUser(message.from_user.id):
        await cfg.bot.send_message(message.from_user.id, "Выберите операцию над пользователями:", reply_markup=btn.user_markup)
        await States.users.set()
    else:
        await cfg.bot.send_message(message.from_user.id, "К сожалению,".format(message.from_user.first_name) +
        " этот бот для вас недоступен, обратитесь к администратору :(")

# second

@cfg.dp.message_handler(state=States.setFolder) 
async def setFolder(message: types.Message, state: FSMContext):
    if await checkUser(message.from_user.id):
        if message.text == "Создать новую папку":
            await cfg.bot.send_message(message.from_user.id, "Введите название новой папки:", 
            reply_markup=btn.back)
            await States.addFolder.set()
        elif message.text == "Удалить папку":
            await cfg.bot.send_message(message.from_user.id, "Введите номер папки, которую хотите удалить" + 
            f"\n\nСписок папок: {await printList()}\n\nВнимание, при удалении папки, удаляется всё её содержимое!", 
            reply_markup=btn.back)
            await States.delFolder.set()
        elif message.text == "Вернуться назад":
            await cfg.bot.send_message(message.from_user.id, "Вы в главном меню", 
            reply_markup=btn.markup)
            await state.finish()
        elif message.text.isdigit() and int(message.text) > 0:
            folderList = await db.get_folders()
            if int(message.text) <= len(folderList):
                await cfg.addDataFolder.setFolder(message.from_user.id, folderList[int(message.text) - 1][0])
                await cfg.bot.send_message(message.from_user.id, "Введите бандл нового приложения или список бандлов:\n\n( разделите через абзац ! )", reply_markup=btn.back)
                await States.addApp.set()
            else:
                await cfg.bot.send_message(message.from_user.id, "Указанная папка не найдена!")
        else:
            await cfg.bot.send_message(message.from_user.id, "Данные введены некорректно!")
    else:
        await cfg.bot.send_message(message.from_user.id, "К сожалению,".format(message.from_user.first_name) +
        " этот бот для вас недоступен, обратитесь к администратору :(")

@cfg.dp.message_handler(state=States.setOpenFolder) 
async def setOpenFolder(message: types.Message, state: FSMContext):
    if await checkUser(message.from_user.id):
        if message.text == "Вернуться назад":
            await cfg.bot.send_message(message.from_user.id, "Вы в главном меню", 
            reply_markup=btn.markup)
            await state.finish()
        elif message.text.isdigit() and int(message.text) > 0:
            folderList = await db.get_folders()
            if int(message.text) <= len(folderList):
                web = Web(folderList[int(message.text) - 1][0])
                link = InlineKeyboardMarkup().add(InlineKeyboardButton('Перейти', url=web.url))
                await cfg.bot.send_message(message.from_user.id, "Вы в главном меню", 
                reply_markup=btn.markup)
                await state.finish()
                await cfg.bot.send_message(message.from_user.id, f"Ссылка на данные таблицы {folderList[int(message.text) - 1][0]}:", reply_markup=link)
            else:
                await cfg.bot.send_message(message.from_user.id, "Указанная папка не найдена!")
        else:
            await cfg.bot.send_message(message.from_user.id, "Данные введены некорректно!")
    else:
        await cfg.bot.send_message(message.from_user.id, "К сожалению,".format(message.from_user.first_name) +
        " этот бот для вас недоступен, обратитесь к администратору :(")

@cfg.dp.message_handler(state=States.users) 
async def set_users(message: types.Message, state: FSMContext):
    if await checkUser(message.from_user.id):
        if message.text == "Вернуться назад":
            await cfg.bot.send_message(message.from_user.id, "Вы в главном меню", 
            reply_markup=btn.markup)
            await state.finish()
        if message.text == "Добавить пользователя":
            await cfg.bot.send_message(message.from_user.id, "Введите id нового пользователя:", reply_markup=btn.back)
            await States.addUser.set()
        elif message.text == "Удалить пользователя":
            await cfg.bot.send_message(message.from_user.id, f"Укажите номер ID пользователя, которого хотите удалить\n\nСписок пользователей:{await printUsers()}", reply_markup=btn.back)
            await States.delUser.set()
    else:
        await cfg.bot.send_message(message.from_user.id, "К сожалению,".format(message.from_user.first_name) +
        " этот бот для вас недоступен, обратитесь к администратору :(")

# third

@cfg.dp.message_handler(state=States.addFolder)
async def add_folder(message: types.Message):
    if await checkUser(message.from_user.id):
        if message.text == "Вернуться назад":
            await cfg.bot.send_message(message.from_user.id, "Введите номер папки для нового приложения или создайте новую" + 
            "\n\nСписок папок:{}".format(await printList()), 
            reply_markup=btn.choose_folder)
            await States.setFolder.set()
        else:
            if await db.check_folder(message.text):
                await cfg.bot.send_message(message.from_user.id, "Папка с таким названием уже существует!")
                return
            await db.add_folder(message.text)
            await cfg.bot.send_message(message.from_user.id, "Папка успешно создана")
            await cfg.bot.send_message(message.from_user.id, "Введите номер папки для нового приложения или создайте новую" + 
            "\n\nСписок папок:{}".format(await printList()), 
            reply_markup=btn.choose_folder)
            await States.setFolder.set()
    else:
        await cfg.bot.send_message(message.from_user.id, "К сожалению,".format(message.from_user.first_name) +
        " этот бот для вас недоступен, обратитесь к администратору :(")

@cfg.dp.message_handler(state=States.delFolder) 
async def delFolder(message: types.Message, state: FSMContext):
    if await checkUser(message.from_user.id):
        if message.text == "Вернуться назад":
            await cfg.bot.send_message(message.from_user.id, "Введите номер папки для нового приложения или создайте новую" + 
            "\n\nСписок папок:{}".format(await printList()), 
            reply_markup=btn.choose_folder)
            await States.setFolder.set()
        elif message.text.isdigit() and int(message.text) > 0:
            folderList = await db.get_folders()
            if int(message.text) <= len(folderList):
                await db.delFolder(await db.get_foldersId(folderList[int(message.text) - 1][0]))
                await cfg.bot.send_message(message.from_user.id, "Папка успешно удалена!")
                await crm.del_folder(folderList[int(message.text) - 1][0])
                await cfg.bot.send_message(message.from_user.id, "Введите номер папки для нового приложения или создайте новую" + 
                "\n\nСписок папок:{}".format(await printList()), 
                reply_markup=btn.choose_folder)
                await States.setFolder.set()
            else:
                await cfg.bot.send_message(message.from_user.id, "Указанная папка не найдена!")
        else:
            await cfg.bot.send_message(message.from_user.id, "Данные введены некорректно!")
    else:
        await cfg.bot.send_message(message.from_user.id, "К сожалению,".format(message.from_user.first_name) +
        " этот бот для вас недоступен, обратитесь к администратору :(")


@cfg.dp.message_handler(state=States.addApp)
async def add_app(message: types.Message):
    if await checkUser(message.from_user.id):
        if message.text == "Вернуться назад":
            await cfg.bot.send_message(message.from_user.id, "Введите номер папки для нового приложения или создайте новую" + 
            "\n\nСписок папок:{}".format(await printList()), 
            reply_markup=btn.choose_folder)
            await States.setFolder.set()
            return
        old_apps = []
        new_bundles = message.text.split('\n')
        folders = await cfg.addDataFolder.getFolder()
        for new_bundle in new_bundles:
            if await db.checkCurrentApp(new_bundle):
                old_apps.append(new_bundle)
                await cfg.bot.send_message(message.from_user.id, f'Приложение {new_bundle} уже существует в папке {await db.get_folder(new_bundle)} со статусом "{await db.get_status(new_bundle)}"')
            else:
                name = new_bundle
                status = await Track.trackNow(name)
                await db.add_app(
                    appBundle=name,
                    status=status,
                    folder_id=await db.get_foldersId(folders.get(str(message.from_user.id))),
                    startTime=datetime.datetime.now(timezone('Europe/Kiev')).strftime("%d/%m/%y %H:%M:%S"),
                    nextTime=(datetime.datetime.now(timezone('Europe/Kiev')) + datetime.timedelta(hours=4)).strftime("%d/%m/%y %H:%M:%S")
                )
                await crm.add_app(name, datetime.datetime.now(timezone('Europe/Kiev')), folders.get(str(message.from_user.id)))
                await cfg.bot.send_message(message.from_user.id, "Бандл '{}'\nуспешно добавлен в папку {}\n\nСтатус приложения: {}".format(name, folders.get(str(message.from_user.id)), status))
        if old_apps:
            app_list = ''
            await cfg.addDataApps.add_app(message.from_user.id, 
                folders.get(str(message.from_user.id)),
                old_apps)
            for old_app in old_apps:
                app_list += old_app + "\n"
            await cfg.bot.send_message(message.from_user.id, f"Приложения\n\n{app_list}\nуже существуют в других папках." +
            "\n\nXотите перенести их в текущую папку?", 
            reply_markup=btn.change_folder )
            await States.changeFolder.set()
        else:
            await cfg.bot.send_message(message.from_user.id, "Введите номер папки для нового приложения или создайте новую" + 
            "\n\nСписок папок:{}".format(await printList()), 
            reply_markup=btn.choose_folder)
            await States.setFolder.set()
    else:
        await cfg.bot.send_message(message.from_user.id, "К сожалению,".format(message.from_user.first_name) +
        " этот бот для вас недоступен, обратитесь к администратору :(")

@cfg.dp.message_handler(state=States.addUser) 
async def add_user(message: types.Message):
    if await checkUser(message.from_user.id):
        if message.text == "Вернуться назад":
            await cfg.bot.send_message(message.from_user.id, "Выберите операцию над пользователями:", reply_markup=btn.user_markup)
            await States.users.set()
        else:
            await cfg.addDataUser.addUser(message.text)
            await cfg.bot.send_message(message.from_user.id, "Пользователь успешно добавлен !")
            await cfg.bot.send_message(message.from_user.id, "Выберите операцию над пользователями:", reply_markup=btn.user_markup)
            await States.users.set()
    else:
        await cfg.bot.send_message(message.from_user.id, "К сожалению,".format(message.from_user.first_name) +
        " этот бот для вас недоступен, обратитесь к администратору :(")
    
@cfg.dp.message_handler(state=States.changeFolder) 
async def change_folder(message: types.Message):
    if await checkUser(message.from_user.id):
        if message.text == 'Да':
            response = await cfg.addDataApps.change_apps(message.from_user.id)
            folder = await db.get_foldersId(response['folder'])
            app_list = ''
            for app in response['apps']:
                await db.change_folder(folder, app)
                await crm.change_folder(app, response['folder'])
                app_list += app + "\n"
            await cfg.bot.send_message(message.from_user.id, f"Приложения\n\n{app_list}\n" +
                f"были добавлены в папку {response['folder']}")
        await cfg.bot.send_message(message.from_user.id, "Введите номер папки для нового приложения или создайте новую" + 
            "\n\nСписок папок:{}".format(await printList()), 
            reply_markup=btn.choose_folder)
        await States.setFolder.set()
    else:
        await cfg.bot.send_message(message.from_user.id, "К сожалению,".format(message.from_user.first_name) +
        " этот бот для вас недоступен, обратитесь к администратору :(")

@cfg.dp.message_handler(state=States.delUser) 
async def del_user(message: types.Message):
    if await checkUser(message.from_user.id):
        if message.text == "Вернуться назад":
            await cfg.bot.send_message(message.from_user.id, "Выберите операцию над пользователями:", reply_markup=btn.user_markup)
            await States.users.set()
        elif message.text.isdigit() and int(message.text) > 0:
            UsersList = await cfg.addDataUser.getUsers()
            if int(message.text) <= len(UsersList):
                await cfg.addDataUser.delUser(UsersList[int(message.text) - 1])
                await cfg.bot.send_message(message.from_user.id, "ID пользователя успешно удалён !")
                await cfg.bot.send_message(message.from_user.id, "Выберите операцию над пользователями:", reply_markup=btn.user_markup)
                await States.users.set()
            else:
                await cfg.bot.send_message(message.from_user.id, "Указанный id пользователя не найдена!")
        else:
            await cfg.bot.send_message(message.from_user.id, "Данные введены некорректно!")
    else:
        await cfg.bot.send_message(message.from_user.id, "К сожалению,".format(message.from_user.first_name) +
        " этот бот для вас недоступен, обратитесь к администратору :(")

async def printList():
    folders = ""
    index = 0
    for folder in await db.get_folders():
        index += 1
        folder = "\n{}. ".format(index) + folder[0]
        folders += folder
    if folders == "":
        folders = " cписок пуст\n\nДля добавления создайте папку!"
    return folders

async def printUsers():
    users = ""
    index = 0
    for user in await cfg.addDataUser.getUsers():
        index += 1
        user = "\n{}. ".format(index) + user
        users += user
    if users == "":
        users = " cписок пользователей пуст!"
    return users

async def checkUser(user_id):
    for user in await cfg.addDataUser.getUsers():
        if str(user) == str(user_id):
            return True
    return False

async def scheduler_users():
    aioschedule.every(3).seconds.do(Track.tracking)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

# Run function with await
async def on_startup(_):
    asyncio.create_task(scheduler_users())

if __name__ == "__main__":
    executor.start_polling(cfg.dp, skip_updates=True, on_startup=on_startup)