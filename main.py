import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
import os
import asyncio

from apps.database.db import init_db, get_recipe_by_title, get_recipes_by_category, get_favorites, add_favorite
from apps.keyboard.keyb import main_menu_keyboard
from apps.keyboard.category_menu import category_menu_keyboard
from apps.keyboard.favorite_menu import favorite_menu_keyboard, favorite_recipe_keyboard
from apps.routes.add_recipe import AddRecipeState, add_recipe_start, process_title, process_description, process_category
from apps.routes.show_recipe import show_recipes_by_category
from apps.routes.favorites import AddFavoriteState, add_favorite_start, process_favorite_title
from apps.routes.delete_favorite_menu import delete_favorite_start
from apps.routes.edit_recipe import EditRecipeState, start_edit_recipe, process_title_edit, process_new_title, process_new_description, finish_edit_recipe, delete_recipe_start, process_delete_recipe

 
load_dotenv()

API_TOKEN = os.getenv('BOT_TOKEN')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Добро пожаловать в кулинарный бот от Марии! Выберите действие:", reply_markup=main_menu_keyboard)

@dp.message_handler(Text(equals=["Завтрак", "Обед", "Ужин", "Напитки"]))
async def show_recipes_by_category_handler(message: types.Message):
    category = message.text
    logging.info(f"Категория: {category}")
    await show_recipes_by_category(message)

@dp.callback_query_handler(lambda call: call.data.startswith("recipe_"))
async def show_recipe_by_title_handler(call: types.CallbackQuery):
    title = call.data.replace("recipe_", "")
    logging.info(f"Выбран рецепт: {title}")
    recipe = await get_recipe_by_title(title)
    if recipe:
        await call.message.answer(f"{recipe[0]}\n\n{recipe[1]}", reply_markup=main_menu_keyboard)
    else:
        await call.message.answer(f"Рецепт '{title}' не найден", reply_markup=main_menu_keyboard)

@dp.message_handler(Text(equals="Добавить свой рецепт"), state='*')
async def add_recipe_start_handler(message: types.Message):
    await add_recipe_start(message)

@dp.message_handler(state=AddRecipeState.title)
async def process_title_handler(message: types.Message, state: FSMContext):
    await process_title(message, state)

@dp.message_handler(state=AddRecipeState.description)
async def process_description_handler(message: types.Message, state: FSMContext):
    await process_description(message, state)

@dp.message_handler(state=AddRecipeState.category)
async def process_category_handler(message: types.Message, state: FSMContext):
    await process_category(message, state)

@dp.message_handler(Text(equals="Любимые рецепты"))
async def show_favorite_recipes(message: types.Message):
    user_id = message.from_user.id
    favorites = await get_favorites(user_id)
    if favorites:
        await message.answer("Ваши любимые рецепты:", reply_markup=favorite_menu_keyboard(favorites))
    else:
        await message.answer("У вас нет любимых рецептов")

@dp.callback_query_handler(lambda call: call.data.startswith("fav_recipe_"))
async def show_favorite_recipe(call: types.CallbackQuery):
    title = call.data.replace("fav_recipe_", "")
    recipe = await get_recipe_by_title(title)
    if recipe:
        await call.message.answer(f"{recipe[0]}\n\n{recipe[1]}", reply_markup=favorite_recipe_keyboard(title))
    else:
        await call.message.answer(f"Рецепт '{title}' не найден")

@dp.callback_query_handler(lambda call: call.data.startswith("remove_fav_"))
async def remove_favorite_recipe(call: types.CallbackQuery):
    await delete_favorite_start(call)

@dp.message_handler(Text(equals="Добавить любимый рецепт"), state='*')
async def add_favorite_start_handler(message: types.Message):
    await add_favorite_start(message)

@dp.message_handler(state=AddFavoriteState.title)
async def process_favorite_title_handler(message: types.Message, state: FSMContext):
    await process_favorite_title(message, state)

@dp.message_handler(Text(equals="Назад"))
async def go_back_handler(message: types.Message):
    await message.answer("Вы вернулись в главное меню", reply_markup=main_menu_keyboard)


@dp.message_handler(Text(equals="Редактировать рецепт"))
async def edit_recipe_start_handler(message: types.Message):
    await start_edit_recipe(message)

@dp.message_handler(state=EditRecipeState.title)
async def process_title_edit_handler(message: types.Message, state: FSMContext):
    await process_title_edit(message, state)

@dp.message_handler(state=EditRecipeState.new_title)
async def process_new_title_handler(message: types.Message, state: FSMContext):
    await process_new_title(message, state)

@dp.message_handler(state=EditRecipeState.new_description)
async def process_new_description_handler(message: types.Message, state: FSMContext):
    await process_new_description(message, state)

@dp.message_handler(state=EditRecipeState.new_category)
async def finish_edit_recipe_handler(message: types.Message, state: FSMContext):
    await finish_edit_recipe(message, state)


@dp.message_handler(Text(equals="Удалить рецепт"))
async def delete_recipe_start_handler(message: types.Message):
    await delete_recipe_start(message)

@dp.message_handler(state=EditRecipeState.title)
async def process_delete_recipe_handler(message: types.Message, state: FSMContext):
    await process_delete_recipe(message, state)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())
    executor.start_polling(dp, loop=loop, skip_updates=True)
