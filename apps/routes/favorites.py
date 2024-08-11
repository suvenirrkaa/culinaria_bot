from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from apps.database.db import add_favorite, get_recipe_by_title

class AddFavoriteState(StatesGroup):
    title = State()

async def add_favorite_start(message: types.Message):
    await message.answer("Отправьте название рецепта для добавления в любимые:")
    await AddFavoriteState.title.set()

async def process_favorite_title(message: types.Message, state: FSMContext):
    title = message.text
    recipe = await get_recipe_by_title(title)
    if recipe:
        await add_favorite(message.from_user.id, title)
        await message.answer("Рецепт добавлен в любимые!")
    else:
        await message.answer("Рецепт с таким названием не найден!")
    await state.finish()
