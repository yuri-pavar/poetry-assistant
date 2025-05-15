import asyncio
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
import requests
import os


router = Router()

MAIN_URL = "http://web:8001/api/"

class RequestPoem(StatesGroup):
    query = State()

@router.message(Command("generate"))
async def cmd_qa(message: Message, state: FSMContext):
    await message.answer("✍️ Введите ваш запрос:")
    await state.set_state(RequestPoem.query)

@router.message(RequestPoem.query)
async def handle_query(message: Message, state: FSMContext):
    await message.answer("⏳ Думаю...")
    try:
        response = requests.post(
            url=MAIN_URL+"poem_async",
            json={"query": message.text},
            timeout=60
        )
        task_id = response.json().get("task_id")
        await asyncio.sleep(5)

        for _ in range(10):
            res = requests.get(MAIN_URL + f"result/{task_id}")
            data = res.json()
            if data.get("status") == "completed":
                await message.answer(data["result"]["response"])
                break
            await asyncio.sleep(2)
        else:
            await message.answer("⚠️ Не удалось получить результат. Попробуйте позже.")
    except Exception as e:
        await message.answer(f"🚫 Ошибка при обращении к сервису: {str(e)}")

    await state.clear()
