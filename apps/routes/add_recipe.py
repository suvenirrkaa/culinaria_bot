from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from apps.database.db import add_recipe
from apps.keyboard.keyb import main_menu_keyboard


class AddRecipeState(StatesGroup):
    title = State()
    description = State()
    category = State()

async def add_recipe_start(message: types.Message):
    await message.answer("Введите название рецепта (или нажмите 'Назад' для отмены):")
    await AddRecipeState.title.set()

async def process_title(message: types.Message, state: FSMContext):
    if message.text.lower() == "назад":
        await state.finish()
        await message.answer("Вы вернулись в главное меню", reply_markup=main_menu_keyboard)
        return
    async with state.proxy() as data:
        data['title'] = message.text
    await message.answer("Введите описание рецепта (или нажмите 'Назад' для отмены):")
    await AddRecipeState.description.set()

async def process_description(message: types.Message, state: FSMContext):
    if message.text.lower() == "назад":
        await state.finish()
        await message.answer("Вы вернулись в главное меню", reply_markup=main_menu_keyboard)
        return
    async with state.proxy() as data:
        data['description'] = message.text
    await message.answer("Введите категорию рецепта (Завтрак, Обед, Ужин, Напитки) (или нажмите 'Назад' для отмены):")
    await AddRecipeState.category.set()

async def process_category(message: types.Message, state: FSMContext):
    if message.text.lower() == "назад":
        await state.finish()
        await message.answer("Вы вернулись в главное меню", reply_markup=main_menu_keyboard)
        return
    async with state.proxy() as data:
        data['category'] = message.text
    await add_recipe(data['title'], data['description'], data['category'])
    await message.answer("Рецепт добавлен!", reply_markup=main_menu_keyboard)
    await state.finish()
