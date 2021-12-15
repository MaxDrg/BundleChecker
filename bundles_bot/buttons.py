from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class Button:
    def __init__(self):
        # markup button
        button_output = KeyboardButton('Вывести данные')
        button_add = KeyboardButton('Приложения и папки')
        button_update = KeyboardButton('Обновить')
        button_users = KeyboardButton('Пользователи')
        self.markup = ReplyKeyboardMarkup(resize_keyboard=True).row(button_output).row(button_add).row(button_update).row(button_users)

        button_back = KeyboardButton('Вернуться назад')
        self.back = ReplyKeyboardMarkup(resize_keyboard=True).row(button_back)

        delUser = KeyboardButton('Добавить пользователя')
        addUser = KeyboardButton('Удалить пользователя')
        self.user_markup = ReplyKeyboardMarkup(resize_keyboard=True).row(addUser).row(delUser).row(button_back)

        button_create_folder = KeyboardButton('Создать новую папку')
        button_delete_folder = KeyboardButton('Удалить папку')
        self.choose_folder = ReplyKeyboardMarkup(resize_keyboard=True).row(button_create_folder).row(button_delete_folder).row(button_back)
