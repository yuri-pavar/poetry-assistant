import asyncio
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.enums import ParseMode
import requests
import os
from .utils import prepare_for_html


router = Router()

MAIN_URL = "http://web:8001/api/"

class RequestQA(StatesGroup):
    query = State()

@router.message(Command("askme"))
async def cmd_qa(message: Message, state: FSMContext):
    await message.answer("✍️ Введите ваш запрос:")
    await state.set_state(RequestQA.query)

@router.message(RequestQA.query)
async def handle_query(message: Message, state: FSMContext):
    await message.answer("⏳ Думаю...")
    try:
        response = requests.post(
            url=MAIN_URL+"generate_async",
            json={"query": message.text},
            timeout=60
        )
        task_id = response.json().get("task_id")
        await asyncio.sleep(5)

        for _ in range(10):
            res = requests.get(MAIN_URL + f"result/{task_id}")
            data = res.json()
            if data.get("status") == "completed":
                txt_response = prepare_for_html(data["result"]["response"])
                # await message.answer(data["result"]["response"], parse_mode=ParseMode.MARKDOWN_V2)
                await message.answer(txt_response, parse_mode=ParseMode.HTML)
                break
            await asyncio.sleep(2)
        else:
            await message.answer("⚠️ Не удалось получить результат. Попробуйте позже.")
    except Exception as e:
        await message.answer(f"🚫 Ошибка при обращении к сервису: {str(e)}")

    await state.clear()
