from aiogram import types
from aiogram import types
from apps.database.db import get_recipes_by_category
from apps.keyboard.category_menu import category_menu_keyboard

async def show_recipes_by_category(message: types.Message):
    category = message.text
    recipes = await get_recipes_by_category(category)
    if recipes:
        await message.answer(f"Выберите рецепт из категории '{category}':", reply_markup=category_menu_keyboard(recipes))
    else:
        await message.answer(f"Рецепты для категории '{category}' отсутствуют")
