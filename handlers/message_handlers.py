import asyncio

from handlers.callback import *


@dp.message(Command('start', 'restart'))
async def start(message: Message):
    if db.get_user_id(message.from_user.id) is False:
        await bot.send_message(2051400423,
                               f'🔆 <b>{message.from_user.full_name}</b> впервые запустил бота!')

        db.add_user(message.from_user.id)
        db.add_user_money(message.from_user.id, 10)

    else:
        db.add_user(message.from_user.id)

    db.add_language(message.from_user.id, 'en')
    db.add_user_name(message.from_user.id, message.from_user.full_name)

    await bot.set_my_commands(
        commands=[
            BotCommand(command='restart', description='Restart the bot'),
            BotCommand(command='case', description='Cases'),
            BotCommand(command='inventory', description='Inventory'),
            BotCommand(command='rating', description='Rating'),
            BotCommand(command='language', description='Change language'),
            BotCommand(command='settings', description='Settings'),
        ], scope=BotCommandScopeChat(chat_id=message.from_user.id)
    )

    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🇬🇧 English', callback_data='start_eng_lang'),
                                                    InlineKeyboardButton(text='🇷🇺 Русский',
                                                                         callback_data='start_rus_lang')]])

    await bot.send_message(message.chat.id, '<b>🌎 Choose your language.</b>', reply_markup=markup)
    await message.delete()


@dp.message(Command('language'))
async def language(message: Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🇬🇧 English', callback_data='eng_lang'),
                                                    InlineKeyboardButton(text='🇷🇺 Русский',
                                                                         callback_data='rus_lang')]])

    try:
        await bot.send_message(chat_id=message.from_user.id,
                               text={"en": "🌎 Choose your language",
                                "ru": "🌎 Выберите язык"}[db.get_language(message.from_user.id)],
                               reply_markup=markup)
        await message.delete()

    except KeyError:
        pass


@dp.message(Command('settings'))
async def language(message: Message):
    user_id = message.from_user.id

    asyncio.create_task(settings_menu(user_id, message))


@dp.message(Command('rating'))
async def language(message: Message):
    close_text = {"en": f"🔺 Hide",
                  "ru": f"🔺 Скрыть"}[db.get_language(message.from_user.id)]

    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=close_text, callback_data='keep_show')]])

    try:
        with open('database/user_inventory.json', 'r') as file:
            inventories = json.load(file)
            file.close()

        top_users = {inventory_id: round(sum(skin['skin_cost'] for num, skin in inventories[inventory_id].items()), 2)
                     for inventory_id in inventories.keys()}
        top_users = sorted(top_users.items(), key=lambda item: item[1])[::-1]

    except Exception as e:
        print(e)
        top_users = False

    if top_users is not False:
        top_achieves = {1: '🥇', 2: '🥈', 3: '🥉'}

        top_10_index = [ind for ind, _ in top_users]
        top_10 = [f'{db.get_user_name(inv_id)} — ${inv_cost}' for inv_id, inv_cost in top_users]
        top_10 = '\n'.join(f'{top_achieves.get(num + 1, f" {num + 1}. ")} {user}'
                           for num, user in enumerate(top_10[0:10]))

        user_own_place = str(top_10_index.index(str(message.from_user.id)) + 1)

    else:
        user_own_place = ''
        top_10 = ''

    user_place_text = {'en': f'You are in <b>{user_own_place}{("st" if user_own_place.endswith("1") else "nd" if user_own_place.endswith("2") else "rd" if user_own_place.endswith("3") else "th") if int(user_own_place) not in [11, 12, 13] else "th"}</b> place.',
                       'ru': f'Вы находитесь на <b>{user_own_place}-м</b> месте.'}[
                                   db.get_language(message.from_user.id)]

    try:
        await bot.send_message(chat_id=message.from_user.id,
                               text={"en": f"<b>Top 10 players by inventory price\n\n{top_10}</b>\n\n{user_place_text}",
                                "ru": f"<b>Топ-10 игроков по цене инвентаря\n\n{top_10}</b>\n\n{user_place_text}"}[
                                   db.get_language(message.from_user.id)],
                               reply_markup=markup)
        await message.delete()

    except KeyError:
        pass


@dp.message(F.content_type == ContentType.TEXT)
async def text(message: Message):
    if message.text in ['/case', 'Cases', 'Кейсы']:
        user_id = message.from_user.id
        user_money = db.get_user_money(user_id)

        cases = {'Revolution Case': 2.5, 'Dreams & Nightmares': 2.5, 'Shadow Case': 2.5}

        keyboard_buttons = [[InlineKeyboardButton(
            text=f"{['❌', '✅'][user_money >= cost]}  {case} — ${cost}",
            callback_data=f"case_menu|['{case}', {cost}]")] for case, cost in
            cases.items()]

        markup = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

        try:
            await settings.case_menu[user_id].delete()
            settings.case_menu[user_id] = None
        except:
            pass

        try:
            settings.case_menu[user_id] = await bot.send_photo(chat_id=user_id, photo=FSInputFile('static/image_adds/case_menu.jpg', 'rb'),
                                                               caption={"en": "<b>Cases \n\n"
                                                                              f"Your Balance: ${user_money}</b>",
                                                                        "ru": "<b>Кейсы \n\n"
                                                                              f"Ваш баланс: ${user_money}</b>"}[
                                                                   db.get_language(user_id)],
                                                               reply_markup=markup)
            await message.delete()

        except KeyError:
            pass

    if message.text in ['/inventory', 'Inventory', 'Инвентарь']:
        user_id = message.from_user.id
        asyncio.create_task(show_inventory(user_id, message))
