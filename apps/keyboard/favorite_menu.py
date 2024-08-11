from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def favorite_menu_keyboard(favorites):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for title, _ in favorites:
        keyboard.add(InlineKeyboardButton(text=title, callback_data=f"fav_recipe_{title}"))
    return keyboard

def favorite_recipe_keyboard(title):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text="Удалить из любимых", callback_data=f"remove_fav_{title}"))
    return keyboard
