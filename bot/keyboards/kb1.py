from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_menu_buttons = ["/help", "/cancel", "/askme", "/quote", "/generate"]
k_choice_buttons = [str(i+1) for i in range(5)]


main_menu_keyboard = ReplyKeyboardMarkup(
    # keyboard=[[KeyboardButton(text=b)] for b in main_menu_buttons],
    keyboard=[[KeyboardButton(text=b) for b in k_choice_buttons]],
    resize_keyboard=True
)

k_choice_keyboard = ReplyKeyboardMarkup(
    # keyboard=[[KeyboardButton(text=b)] for b in k_choice_buttons],
    keyboard=[[KeyboardButton(text=b) for b in k_choice_buttons]],
    resize_keyboard=True
)