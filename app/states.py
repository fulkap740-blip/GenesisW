from aiogram.fsm.state import StatesGroup, State


class RequestForm(StatesGroup):
    video = State()
    proof = State()
    views = State()
