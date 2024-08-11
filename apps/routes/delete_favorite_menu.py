from aiogram import types
from aiogram.dispatcher import FSMContext

from apps.database.db import remove_favorite

async def delete_favorite_start(call: types.CallbackQuery):
    title = call.data.replace("remove_fav_", "")
    user_id = call.from_user.id
    await remove_favorite(user_id, title)
    await call.message.answer(f"Рецепт '{title}' удален из любимых.", reply_markup=None)
