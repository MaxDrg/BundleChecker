from aiogram.dispatcher.filters import state

class States(state.StatesGroup):
    setFolder = state.State()
    addFolder = state.State()
    delFolder = state.State()
    addApp = state.State()
    setOpenFolder = state.State()

    menu = state.State()

    users = state.State()
    addUser = state.State()
    delUser = state.State()