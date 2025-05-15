import asyncio
from handlers import qa, quote, poem
from keyboards.kb1 import main_menu_keyboard

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.strategy import FSMStrategy
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, BotCommand, ReplyKeyboardRemove
import os


BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage(), fsm_strategy=FSMStrategy.CHAT)
dp.include_router(qa.router)
dp.include_router(quote.router)
dp.include_router(poem.router)

@dp.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="👋 Привет! Я бот, который поможет тебе с русской поэзией.\n"
             "Можешь задать любой вопрос о поэзии, проанализировать стих или сочинить новый!",
        # reply_markup=main_menu_keyboard,
        reply_markup=ReplyKeyboardRemove()
    )

@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "📌 Возможности бота:\n"
        "/askme — задать вопрос о поэзии\n"
        "/quote — найти строки из произведений по запросу\n"
        "/generate — сгенерировать стихотворение на заданную тему в стиле автора\n"
        "/cancel — отменить ввод\n"
        "/help — справка"
    )

@dp.message(Command(commands=["cancel"]))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("⛔️ Ввод отменён. Начнём сначала?", reply_markup=main_menu_keyboard)

async def set_main_menu(bot: Bot):
    commands = [
        BotCommand(command="/help", description="Справка по работе бота"),
        BotCommand(command="/cancel", description="Отменить ввод"),
        BotCommand(command="/askme", description="Задать вопрос о поэзии"),
        BotCommand(command="/quote", description="Получить строки из произведений"),
        BotCommand(command="/generate", description="Генерация стихотворения")
    ]
    await bot.set_my_commands(commands)

async def main():
    dp.startup.register(set_main_menu)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
