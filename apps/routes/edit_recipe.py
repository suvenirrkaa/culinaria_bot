from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from apps.database.db import update_recipe, delete_recipe

class EditRecipeState(StatesGroup):
    title = State()
    new_title = State()
    new_description = State()
    new_category = State()

async def start_edit_recipe(message: types.Message):
    await message.answer("Введите название рецепта, который хотите отредактировать:")
    await EditRecipeState.title.set()

async def process_title_edit(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text
    await message.answer("Введите новое название рецепта (или оставьте как есть):")
    await EditRecipeState.new_title.set()

async def process_new_title(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['new_title'] = message.text
    await message.answer("Введите новое описание рецепта (или оставьте как есть):")
    await EditRecipeState.new_description.set()

async def process_new_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['new_description'] = message.text
    await message.answer("Введите новую категорию рецепта (Завтрак, Обед, Ужин, Напитки) (или оставьте как есть):")
    await EditRecipeState.new_category.set()

async def finish_edit_recipe(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await update_recipe(data['title'], data['new_title'], data['new_description'], data['new_category'])
    await message.answer(f"Рецепт '{data['new_title']}' обновлен!")
    await state.finish()

async def delete_recipe_start(message: types.Message):
    await message.answer("Введите название рецепта, который хотите удалить:")
    await EditRecipeState.title.set()

async def process_delete_recipe(message: types.Message, state: FSMContext):
    title = message.text
    await delete_recipe(title)
    await message.answer(f"Рецепт '{title}' удален!")
    await state.finish()
