import aiosqlite

DATABASE = 'recipes.db'

async def init_db():
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS recipes (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT NOT NULL,
                            description TEXT NOT NULL,
                            category TEXT NOT NULL)''')
        await db.execute('''CREATE TABLE IF NOT EXISTS favorites (
                            user_id INTEGER NOT NULL,
                            recipe_id INTEGER NOT NULL)''')
        await db.commit()
        await insert_initial_data(db)

async def insert_initial_data(db):
    recipes = [
        # завтрак
        ("Овсяная каша", "Ингредиенты:\nМолоко 250 мл\nОвсяные хлопья 40 г\nСоль и сахар по вкусу\nМасло сливочное по желанию\n\nПриготовление:\n1. Нагреваем в кастрюльке молоко.\n2. Как только молоко закипело, добавляем соль, сахар.\n3. Засыпаем хлопья или цельные зерна крупы.\n4. Далее варим кашу на среднем огне, постоянно помешивая. Время приготовления зависит от выбранного сорта овсянки. Для геркулесовых хлопьев потребуется 10 минут после закипания, для цельных зерен 30 минут.\n5. Когда каша будет готова, добавляем масло, размешиваем и даем постоять еще 5 минут.", "Завтрак"),
        ("Тосты с сыром", "Ингредиенты:\n2 кусочка тостового хлеба\n2 кусочка любимого сыра\n\nПриготовление:\n1. Сыр выкладываем сверху на хлеб\n2. Ставим в духовку на 5-7 минут\nЕсли нет духовки, то на сухую сковороду под крышкой", "Завтрак"),
        ("Омлет", "Ингредиенты:\nКуриные яйца 2 шт\nМолоко 50 мл\nСоль перец по вкусу\nМасло подсолнечное\n\nПриготовление:\n1. Смешать яйца с молоком\n2. Добавить соль и перец\n3. Жарить на сковородке с маслом до готовности", "Завтрак"),

        # обед
        ("Борщ", "Ингредиенты:\nВода - 1,5-2 л.\nСвинина или говядина на кости - 400 г\nКартофель - 4 шт. (средние)\nСвекла - 2 шт. (небольшие)\nМорковь - 1 шт.\nЛук - 3 шт. (средние)\nКапуста белокочанная свежая - 300 г\nТоматная паста - 2 ст. л.\nПодсолнечное масло - 4-5 ст. л.\nСоль, лавровый лист, зелень - по вкусу.\n\nПриготовление:\n1. Варим бульон, в кастрюлю наливаем 1,5-2 литра воды. Добавляем мясо и ставим на средний огонь. Перед закипанием снимаем пену. Как только бульон закипит, накрываем крышкой и варим на медленном огне час-полтора.\n2.Тем временем готовим зажарку. Чистим свеклу, морковь и лук. Свеклу натираем на крупной терке, а морковь - на средней. Лук нарезаем кубиками. На среднем огне в сковороде разогреваем масло, высыпаем туда лук и морковь, жарим 5 минут. Затем добавляем свеклу. Жарим овощи еще 5 минут, добавляем томатную пасту, перемешиваем и жарим все еще 5-7 минут.\n3.А теперь варим сам борщ. Из бульона вынимаем мясо и, пока оно остывает, бросаем в бульон нашинкованную капусту. Через 5-10 минут добавляем нарезанный соломкой картофель. Отделяем мясо от кости и нарезаем кубиками. Возвращаем мясо в борщ, солим его и добавляем зажарку. Перемешиваем борщ, кладем лавровый лист и мелко порубленную зелень, накрываем крышкой и варим все еще 5-7 минут.", "Обед"),
        ("Пельмени", "Ингредиенты:\nПельмени - 400 г\nВода - 2 л\nСоль, перец, лавровый лист - по вкусу\nМасло подсолнечное - 1 ст. ложка\nМасло сливочное - 15 г\n\nПриготовление:\n1. Воду довести до кипения, закинуть пельмени\n2. Добавить специи\n3. После закипания воды с пельменями варить 6-10 минут", "Обед"),
        ("Куриные оладьи", "Ингредиенты:\nФарш куриный (филе куриное) - 600 г\nЯйца куриные - 4-5 шт.\nСыр твердый - 150 г\nСметана - 2-3 ст. ложки\nМука - 2-3 ст. ложки\nЗелень (укроп, петрушка) - 1 пучок\nЛук зеленый - 1 пучок\nСоль - по вкусу\nПерец - по вкусу\nКарри - 0,5 ч. ложки\nРастительное масло - 30 г\n\nПриготовление:\n1.Твердый сыр натереть на крупной терке.\n2. Помыть и нарезать зелень и зеленый лук.\n3. В миску выложить куриный фарш (пропустить через мясорубку куриное филе или купить готовый фарш). Вбить яйца. Посолить, поперчить, добавить зелень, лук, специи, сыр, сметану и муку.\n4. Все хорошо перемешать. Дать постоять 20 минут.\n5. Разогреть сковороду. Налить растительное масло. Столовой ложкой выложить оладьи в горячее масло. Обжарить куриные оладьи с зеленью и сыром до румяной корочки с одной стороны 2-3 минуты на среднем огне.\n6. Затем перевернуть и жарить куриные оладьи до румяности с другой стороны. Так пожарить все оладьи-котлетки.", "Обед"),
        # ужин
        ("Жаркое", "Ингредиенты:\nСвиная корейка без кости - 1 кг\nСало свиное свежее - 50 г\nМасло сливочное - 50 г\nКартофель - 1 кг\nПерец болгарский - 1 шт.\nМорковь - 2 шт.\nЛук репчатый - 2 шт.\nЧеснок - 2 зубчика\nЗелень петрушки свежая - по вкусу\nЗелень петрушки сушёная - по вкусу\nСпеции для мяса - по вкусу\nПерец чёрный горошком - по вкусу\nПерец чёрный молотый - по вкусу\nСоль - по вкусу\n\nПриготовление:\n1. В сотейнике растопить сало, нарезанное мелкими кубиками. Добавить мясо, нарезанное небольшими кусочками. Обжарить до румяной корочки.\n2. Затем добавить морковь, нарезанную кружочками. Обжаривать 5 минут.\n3. Лук, нарезанный полукольцами. Обжаривать 5 минут.\n4. Болгарский перец, нарезанный дольками. Ещё 5 минут\n5. Добавить крупно нарезанный картофель, кусочек сливочного масла, 200 мл воды, специи, сушёную петрушку и соль. Не перемешивать. Накрыть крышкой, убавить огонь и тушить на медленном огне 40 минут.\n6. В конце приготовления добавить нарезанную свежую зелень, измельчённый чеснок. Перемешать и снять с огня.", "Ужин"),
        ("Драники", "Ингредиенты:\nКартошка- 600 г\nЯйца - 1 шт\nЛук репчатый - 1 шт\nПшеничная мука - 1 ст. л.\nСоль - по вкусу\nПерец черный молотый - по вкусу\nРастительное масло - для жарки\nСметана - по вкусу\n\nПриготовление:\n1. Натрем, в первую очередь, на мелкой терке очищенный мытый картофель.\n2. Перекладываем в чашу натертый картофель, и туда же натрем на терке лук.\n3. Картофельную массу необходимо тщательно процедить через сито, хорошо придавливая всю массу. Жидкость выливаем, и перемещаем картофель в чашу.\n4. Добавим в чашу яйцо, муку, все хорошо перемешаем.\n5. Добавим соль и перец по вкусу.\n6. Нам остается только сформировать драники руками и обжарить их на сковороде с подсолнечным маслом. После обжаривания, мы выложим драники на салфетку, чтобы в нее впиталось лишнее масло. Подаем драники со сметаной, или любым другим соусом, на ваш вкус.", "Ужин"),
        ("Легкий салатик", "Ингредиенты:\nЯйца - 2 шт.\nКрабовые палочки - 2 шт.\nПомидор средний - 0,5 шт.\nСыр (нежирный) - небольшой кусочек (около 30 г)\nСметана или майонез (можно кефир) - 1-2 ст. л.\nСпеции - по вкусу\n\nПриготовление:\n1. Яйца сварить вкрутую, порезать кубиками или как вам нравится. Добавить крабовые палочки, помидор, сыр (нежирный), немного зелени, специи по вкусу.\n2. Заправить маложирной сметаной или майонезом (можно даже кефиром обезжиренным), перемешать и... вкусный и сытный ужин готов. Возможны варианты с говядиной или курицей вместо крабовых палочек.", "Ужин"),

        # напитки
        ("Мохито", "Ингредиенты:\nЛайм - 0,5\nСахар - 1 ложка\nСпрайт - 300 мл\nМята - 3 веточки\n\nПриготовление:\n1. Лайм и мяту нарезать и кинуть в чашку\n2. Засыпать туда сахар\n3. Перемять все вместе\n4. Залить спрайтом", "Напитки"),
        ("Ягодный компот", "Ингредиенты:\nКлубника — 100 г\nМалина — 100 г\nКрасная смородина — 100 г\nВода — 3-5 л\nСахар — 50-100 г\n\nПриготовление:\n1. Вымойте ягоды под проточной водой, просушите их. Вскипятите в кастрюле воду. Добавьте сахар. Затем высыпьте ягоды, помешайте. Варите на медленном огне 15-20 минут. Остудите напиток до комнатной температуры. Затем компот перелейте в кувшин и поставьте в холодильник.", "Напитки"),
        ("Лимонад", "Ингредиенты:\nЛимон — 1 шт.\nВода — 2 л\nСахар — 50 г\nМята — по вкусу\n\nПриготовление:\n1. Вымойте лимон, выжмите из него сок. В кувшин налейте воду, можно использовать газированную. Добавьте туда лимонный сок и сахар, размешайте. В готовый напиток можно добавить мяту и лед. По желанию можно сделать лимонад более кислым, добавив в него большее количество цитруса. Следует отметить, что как кислота, так и сахар, содержащиеся в напитке, могут негативно воздействовать на зубную эмаль. Поэтому лимонад нужно пить при помощи трубочки.", "Напитки")
    ]

    for title, description, category in recipes:
        await db.execute('INSERT INTO recipes (title, description, category) VALUES (?, ?, ?)', (title, description, category))
    await db.commit()

async def add_recipe(title, description, category):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute('INSERT INTO recipes (title, description, category) VALUES (?, ?, ?)', (title, description, category))
        await db.commit()

async def get_recipes_by_category(category):
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute('SELECT DISTINCT title FROM recipes WHERE category = ?', (category,)) as cursor:
            recipes = await cursor.fetchall()
            return recipes

async def get_recipe_by_title(title):
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute('SELECT title, description FROM recipes WHERE title = ?', (title,)) as cursor:
            recipe = await cursor.fetchone()
            return recipe

async def add_favorite(user_id, title):
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute('SELECT id FROM recipes WHERE title = ?', (title,)) as cursor:
            recipe_id = await cursor.fetchone()
        if recipe_id:
            await db.execute('INSERT INTO favorites (user_id, recipe_id) VALUES (?, ?)', (user_id, recipe_id[0]))
            await db.commit()

async def remove_favorite(user_id, title):
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute('SELECT id FROM recipes WHERE title = ?', (title,)) as cursor:
            recipe_id = await cursor.fetchone()
        if recipe_id:
            await db.execute('DELETE FROM favorites WHERE user_id = ? AND recipe_id = ?', (user_id, recipe_id[0]))
            await db.commit()

async def get_favorites(user_id):
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute('''
            SELECT recipes.title, recipes.description FROM recipes
            INNER JOIN favorites ON recipes.id = favorites.recipe_id
            WHERE favorites.user_id = ?
        ''', (user_id,)) as cursor:
            favorites = await cursor.fetchall()
            return favorites
async def update_recipe(title, new_title, new_description, new_category):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute('''
            UPDATE recipes
            SET title = ?, description = ?, category = ?
            WHERE title = ?
        ''', (new_title, new_description, new_category, title))
        await db.commit()

async def delete_recipe(title):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute('DELETE FROM recipes WHERE title = ?', (title,))
        await db.commit()
