from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu_keyboard.add(KeyboardButton("Завтрак"))
main_menu_keyboard.add(KeyboardButton("Обед"))
main_menu_keyboard.add(KeyboardButton("Ужин"))
main_menu_keyboard.add(KeyboardButton("Напитки"))
main_menu_keyboard.add(KeyboardButton("Добавить свой рецепт"))
main_menu_keyboard.add(KeyboardButton("Редактировать рецепт"))
main_menu_keyboard.add(KeyboardButton("Удалить рецепт"))
main_menu_keyboard.add(KeyboardButton("Добавить любимый рецепт"))
main_menu_keyboard.add(KeyboardButton("Любимые рецепты"))
main_menu_keyboard.add(KeyboardButton("Назад"))

