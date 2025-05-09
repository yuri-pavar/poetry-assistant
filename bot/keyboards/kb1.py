from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_menu_buttons = ["/help", "/cancel", "/qa"]

main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=b)] for b in main_menu_buttons],
    resize_keyboard=True
)