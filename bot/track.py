import datetime
from time import sleep
import play_scraper
from database import Database
from config import Config
from pytz import timezone
import asyncio

db = Database()
users = Config()

class Track:
    async def tracking():
        for bundle in await db.getBundles():
            nowTime = datetime.datetime.now(timezone('Europe/Kiev')).strftime("%d/%m/%y %H:%M:%S")
            if datetime.datetime.strptime(nowTime, "%d/%m/%y %H:%M:%S") > datetime.datetime.strptime(bundle[3], "%d/%m/%y %H:%M:%S"):
                await db.updateTime(bundle[0], datetime.datetime.now(timezone('Europe/Kiev')).strftime("%d/%m/%y %H:%M:%S"), 
                (datetime.datetime.now(timezone('Europe/Kiev')) + datetime.timedelta(hours=4)).strftime("%d/%m/%y %H:%M:%S"))
                try:
                    update_time = play_scraper.details(bundle[1])['updated']
                    if not update_time == bundle[4]:
                        if not bundle[4] == 'Не существует':
                            for user in await users.addDataUser.getUsers():
                                try:
                                    await users.bot.send_message(user, f"🔄 Приложение {bundle[1]} поменяло дату обновления" +
                                    f" на {update_time}")
                                except:
                                    pass
                        await db.change_last_update(update_time, bundle[0])
                    if bundle[2] == "Не опубликован":
                        for user in await users.addDataUser.getUsers():
                            try:
                                await users.bot.send_message(user, "✅ Обновление статуса приложения!" +
                                "\n\nПриложение {}\n\nиз папки {}\n\nбыло добавлено в Play Market!".format(bundle[1], await db.get_folder(bundle[1])))
                            except:
                                pass
                        await db.updateStatus("Опубликован", bundle[0])
                except Exception as e:
                    print(e)
                    if bundle[2] == "Опубликован":
                        for user in await users.addDataUser.getUsers():
                            try:
                                await users.bot.send_message(user, "❌ Обновление статуса приложения!" +
                                "\n\nПриложение {}\n\nиз папки {}\n\nбыло удалено из Play Market!".format(bundle[1], await db.get_folder(bundle[1])))
                            except:
                                pass
                        await db.updateStatus("Не опубликован", bundle[0])

    async def update():
        for bundle in await db.getBundles():
            await db.updateLastTime(bundle[0], datetime.datetime.now(timezone('Europe/Kiev')).strftime("%d/%m/%y %H:%M:%S"))
            await asyncio.sleep(1)
            try:
                update_time = play_scraper.details(bundle[1])['updated']
                print(update_time)
                if not update_time == bundle[4]:
                    if not bundle[4] == 'Не существует':
                        for user in await users.addDataUser.getUsers():
                            try:
                                await users.bot.send_message(user, f"🔄 Приложение {bundle[1]} поменяло дату обновления" +
                                f" на {update_time}")
                            except:
                                pass
                    await db.change_last_update(update_time, bundle[0])
                if bundle[2] == "Не опубликован":
                    for user in await users.addDataUser.getUsers():
                        try:
                            await users.bot.send_message(user, "✅ Обновление статуса приложения!" +
                                "\n\nПриложение {}\n\nиз папки {}\n\nбыло добавлено в Play Market!".format(bundle[1], await db.get_folder(bundle[1])))
                        except:
                            pass
                    await db.updateStatus("Опубликован", bundle[0])
            except Exception as e:
                print(e)
                if bundle[2] == "Опубликован":
                    for user in await users.addDataUser.getUsers():
                        try:
                            print(bundle[1])
                            await users.bot.send_message(user, "❌ Обновление статуса приложения!" +
                            "\n\nПриложение {}\n\nиз папки {}\n\nбыло удалено из Play Market!".format(bundle[1], await db.get_folder(bundle[1])))
                        except:
                            pass
                    await db.updateStatus("Не опубликован", bundle[0])
        


    async def trackNow(newBundle):
        try:
            play_scraper.details(newBundle)['updated']
            return "Опубликован"
        except:
            return "Не опубликован"