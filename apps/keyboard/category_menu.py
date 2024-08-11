from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def category_menu_keyboard(recipes):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for recipe in recipes:
        keyboard.add(InlineKeyboardButton(text=recipe[0], callback_data=f"recipe_{recipe[0]}"))
    return keyboard
