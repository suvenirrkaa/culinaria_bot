from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def recipe_menu_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text="Добавить в любимые", callback_data="add_to_favorites"))
    keyboard.add(InlineKeyboardButton(text="Удалить рецепт", callback_data="delete_recipe"))
    return keyboard