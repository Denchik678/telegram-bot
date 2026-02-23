import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

TOKEN = os.getenv("TOKEN")
ADMIN_ID = 1941085236

bot = Bot(token=TOKEN)
dp = Dispatcher()


class Registration(StatesGroup):
    fullname = State()
    school_class = State()
    nickname = State()
    team = State()
    steam = State()


@dp.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await message.answer("🎮 Реєстрація на шкільний турнір!\n\nВведи своє Прізвище та ім’я:")
    await state.set_state(Registration.fullname)


@dp.message(Registration.fullname)
async def get_fullname(message: Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    await message.answer("🏫 Вкажи свій клас (наприклад 9-А):")
    await state.set_state(Registration.school_class)


@dp.message(Registration.school_class)
async def get_class(message: Message, state: FSMContext):
    await state.update_data(school_class=message.text)
    await message.answer("👤 Введи свій нікнейм у грі:")
    await state.set_state(Registration.nickname)


@dp.message(Registration.nickname)
async def get_nickname(message: Message, state: FSMContext):
    await state.update_data(nickname=message.text)
    await message.answer("👥 Назва команди:")
    await state.set_state(Registration.team)


@dp.message(Registration.team)
async def get_team(message: Message, state: FSMContext):
    await state.update_data(team=message.text)
    await message.answer("🔗 Посилання на Steam:")
    await state.set_state(Registration.steam)


@dp.message(Registration.steam)
async def get_steam(message: Message, state: FSMContext):
    await state.update_data(steam=message.text)
    data = await state.get_data()

    text = (
        f"🎮 НОВА РЕЄСТРАЦІЯ (ШКОЛА)\n\n"
        f"📛 ПІБ: {data['fullname']}\n"
        f"🏫 Клас: {data['school_class']}\n"
        f"👤 Нік: {data['nickname']}\n"
        f"👥 Команда: {data['team']}\n"
        f"🔗 Steam: {data['steam']}\n\n"
        f"📩 Telegram: @{message.from_user.username}"
    )

    await bot.send_message(ADMIN_ID, text)
    await message.answer("✅ Твою заявку прийнято! Чекай інформацію від організатора.")
    await state.clear()


async def main():
    print("Бот запущений...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
