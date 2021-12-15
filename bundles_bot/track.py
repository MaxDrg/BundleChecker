import datetime
from google_play_scraper import app
from database import Database
from config import Config
from pytz import timezone

db = Database()
users = Config()

class Track:
    async def tracking():
        for bundle in await db.getBundles():
            if datetime.datetime.now(timezone('Europe/Kiev')) > datetime.datetime.strptime(bundle[3], "%d/%m/%y %H:%M:%S"):
                await db.updateTime(bundle[0], datetime.datetime.now(timezone('Europe/Kiev')).strftime("%d/%m/%y %H:%M:%S"), 
                (datetime.datetime.now(timezone('Europe/Kiev')) + datetime.timedelta(hours=4)).strftime("%d/%m/%y %H:%M:%S"))
                try:
                    result  =  app ( 
                        bundle[1], 
                        lang = 'ru' ,  # по умолчанию 'en' 
                        country = 'ru'  # по умолчанию 'us' 
                    )
                    if bundle[2] == "Не опубликован":
                        for user in await users.addDataUser.getUsers():
                            try:
                                await users.bot.send_message(user, "Обновление статуса приложения!" +
                                "\n\nПриложение {} было добавлено в Play Market!".format(bundle[1]))
                            except:
                                pass
                        await db.updateStatus("Опубликован", bundle[0])
                except:
                    if bundle[2] == "Опубликован":
                        for user in await users.addDataUser.getUsers():
                            try:
                                await users.bot.send_message(user, "Обновление статуса приложения!" +
                                "\n\nПриложение {} было удалено из Play Market!".format(bundle[1]))
                            except:
                                pass
                        await db.updateStatus("Не опубликован", bundle[0])

    async def update():
        for bundle in await db.getBundles():
            await db.updateLastTime(bundle[0], datetime.datetime.now(timezone('Europe/Kiev')).strftime("%d/%m/%y %H:%M:%S"))
            try:
                result  =  app ( 
                    bundle[1], 
                    lang = 'ru' ,  # по умолчанию 'en' 
                    country = 'ru'  # по умолчанию 'us' 
                )
                if bundle[2] == "Не опубликован":
                    for user in await users.addDataUser.getUsers():
                        try:
                            await users.bot.send_message(user, "Обновление статуса приложения!" +
                            "\n\nПриложение {} было добавлено в Play Market!".format(bundle[1]))
                        except:
                            pass
                    await db.updateStatus("Опубликован", bundle[0])
            except:
                if bundle[2] == "Опубликован":
                    for user in await users.addDataUser.getUsers():
                        try:
                            await users.bot.send_message(user, "Обновление статуса приложения!" +
                            "\n\nПриложение {} было удалено из Play Market!".format(bundle[1]))
                        except:
                            pass
                    await db.updateStatus("Не опубликован", bundle[0])

    async def trackNow(newBundle):
        try:
            result = app(
                newBundle, 
                lang = 'ru' ,  # по умолчанию 'en' 
                country = 'ru'  # по умолчанию 'us' 
            )
            return "Опубликован"
        except:
            return "Не опубликован"