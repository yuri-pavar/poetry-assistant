import asyncio
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
import requests
import os
from keyboards.kb1 import k_choice_keyboard


router = Router()

MAIN_URL = "http://web:8001/api/"

# class RequestQuote(StatesGroup):
#     query = State()

# @router.message(Command("quote"))
# async def cmd_qa(message: Message, state: FSMContext):
#     await message.answer("✍️ Введите ваш запрос:")
#     await state.set_state(RequestQuote.query)

# @router.message(RequestQuote.query)
# async def handle_query(message: Message, state: FSMContext):
#     await message.answer("⏳ Думаю...")
#     try:
#         response = requests.post(
#             url=MAIN_URL+"quote_async",
#             json={"query": message.text},
#             timeout=60
#         )
#         task_id = response.json().get("task_id")
#         await asyncio.sleep(5)

#         for _ in range(10):
#             res = requests.get(MAIN_URL + f"result/{task_id}")
#             data = res.json()
#             if data.get("status") == "completed":
#                 await message.answer(data["result"]["response"])
#                 break
#             await asyncio.sleep(2)
#         else:
#             await message.answer("⚠️ Не удалось получить результат. Попробуйте позже.")
#     except Exception as e:
#         await message.answer(f"🚫 Ошибка при обращении к сервису: {str(e)}")

#     await state.clear()




class RequestQuote(StatesGroup):
    query = State()
    k = State()


@router.message(Command("quote"))
async def cmd_qa(message: Message, state: FSMContext):
    await message.answer("✍️ Введите ваш запрос:")
    await state.set_state(RequestQuote.query)


@router.message(RequestQuote.query)
async def handle_k(message: Message, state: FSMContext):
    await state.update_data(query=message.text.lower())
    await message.answer("✅ Запрос принят!")
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, выберите количество реферансов:",
        reply_markup=k_choice_keyboard,
    )
    await state.set_state(RequestQuote.k)


@router.message(RequestQuote.k)
async def handle_query(message: Message, state: FSMContext):
    user_data = await state.get_data()
    query = user_data['query']
    k = int(message.text)
    await message.answer("⏳ Думаю...", reply_markup=ReplyKeyboardRemove())
    try:
        response = requests.post(
            url=MAIN_URL+"quote_async",
            json={"query": query, 'k': k},
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
