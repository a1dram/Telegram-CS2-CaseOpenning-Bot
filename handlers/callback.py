import asyncio

from utils.functions import *


@dp.callback_query(lambda call: True)
async def callback(call):
    if call.message:
        if 'eng_lang' in call.data:
            if 'start' not in call.data:
                await bot.answer_callback_query(callback_query_id=call.id,
                                                text='💠 Bot translated into English.',
                                                cache_time=10)

                await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

            await bot.set_my_commands(
                commands=[
                    BotCommand(command='restart', description='Restart the bot'),
                    BotCommand(command='case', description='Cases'),
                    BotCommand(command='inventory', description='Inventory'),
                    BotCommand(command='rating', description='Rating'),
                    BotCommand(command='language', description='Change language'),
                    BotCommand(command='settings', description='Settings'),
                ], scope=BotCommandScopeChat(chat_id=call.message.chat.id)
            )
            db.add_language(call.message.chat.id, 'en')

        if 'rus_lang' in call.data:
            if 'start' not in call.data:
                await bot.answer_callback_query(call.id,
                                                text='💠 Бот переведён на русский язык.',
                                                cache_time=10)

                await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

            await bot.set_my_commands(
                commands=[
                    BotCommand(command='restart', description='Перезапустить бота'),
                    BotCommand(command='case', description='Кейсы'),
                    BotCommand(command='inventory', description='Инвентарь'),
                    BotCommand(command='rating', description='Рейтинг'),
                    BotCommand(command='language', description='Изменить язык'),
                    BotCommand(command='settings', description='Настройки'),
                ], scope=BotCommandScopeChat(chat_id=call.message.chat.id)
            )
            db.add_language(call.message.chat.id, 'ru')

        if 'start' in call.data:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

            case_button = {"en": f"Cases",
                           "ru": f"Кейсы"}[db.get_language(call.message.chat.id)]

            inventory_button = {"en": f"Inventory",
                                "ru": f"Инвентарь"}[db.get_language(call.message.chat.id)]

            markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=case_button), KeyboardButton(text=inventory_button)]],
                                         resize_keyboard=True)

            start_message = {"en": f"<b>Greetings! I am C2CaseBot.</b>\n\n",
                             "ru": f"<b>Приветcтвую! Я - C2CaseBot.</b>\n\n"}[db.get_language(call.message.chat.id)]

            await bot.send_message(chat_id=call.message.chat.id, text=start_message, reply_markup=markup)

        if 'case_menu' in call.data:
            async with async_lock:
                user_id = call.message.chat.id

                len_user_inventory = db.get_user_items(user_id)
                user_items_limit = db.get_inventory_capacity(user_id)

                if len_user_inventory < 0:
                    db.add_user_items(user_id, 0)
                    len_user_inventory = 0

                if len_user_inventory < user_items_limit:

                    case_data = call.data
                    case_info = eval(case_data[case_data.find('['):])
                    case_name = case_info[0].split()[0]
                    case_cost = case_info[1]

                    user_money = db.get_user_money(user_id)

                    if user_money >= case_cost:
                        user_language = db.get_language(user_id)
                        new_user_money = user_money - case_cost

                        try:
                            try:
                                await settings.inventory_history[user_id].delete()
                                settings.inventory_history[user_id] = None
                            except:
                                pass

                            video_f = FSInputFile(path=f"static/CaseBase/{case_name}/animation.mp4", filename="animation.mp4")

                            video = await bot.send_video(chat_id=user_id, video=video_f)

                            try:
                                await bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
                            except:
                                pass

                            for file in os.listdir():
                                if file in ['output.jpg', 'new_img.jpg']:
                                    os.remove(file)

                            user_name = call.message.chat.username

                            if user_name is None:
                                user_name = call.message.chat.first_name

                            skin_info = download_skin_photo(user_name, case_name)

                            skin_file = skin_info['skin_file']
                            skin_cost = skin_info['skin_cost']
                            skin_name = skin_info['full_skin_name']
                            skin_float = skin_info['skin_float']
                            skin_date = skin_info['skin_date']
                            rare_pattern = skin_info['rare_pattern']

                            if 0 < skin_float < 0.07:
                                skin_ex = 'FN'
                            elif 0.07 < skin_float < 0.15:
                                skin_ex = 'MW'
                            elif 0.15 < skin_float < 0.38:
                                skin_ex = 'FT'
                            elif 0.38 < skin_float < 0.45:
                                skin_ex = 'WW'
                            elif 0.45 < skin_float < 1:
                                skin_ex = 'BS'
                            else:
                                skin_ex = 'Vanilla'

                            skin_type = {'🟦': 'e',
                                         '🟪': 'd',
                                         '🎆': 'c',
                                         '🟥': 'b',
                                         '🟨': 'a'}[skin_name[0]]

                            try:
                                with open('database/user_inventory.json', 'r') as file:
                                    inventories = json.load(file)
                                    file.close()

                                user_inventory = inventories[str(user_id)]

                                skin_number = skin_type + str(max([int(num[1:]) for num in user_inventory.keys()]) + 1)

                                updating_inventory = {skin_number: {'skin_name': skin_name,
                                                                    'skin_cost': skin_cost,
                                                                    'skin_float': skin_float,
                                                                    'skin_date': skin_date,
                                                                    'skin_exterior': skin_ex,
                                                                    'case': case_name,
                                                                    'rare_pattern': rare_pattern}}

                                new_user_inventory = {**updating_inventory, **user_inventory}
                                inventories[str(user_id)] = new_user_inventory

                                with open('database/user_inventory.json', 'w') as file:
                                    json.dump(inventories, file)
                                    file.close()

                                len_user_inventory = len(new_user_inventory)
                                if len_user_inventory == 0:
                                    len_user_inventory = 1

                            except Exception as e:
                                print('cs2_callback.py:', e)
                                try:
                                    with open('database/user_inventory.json', 'r') as file:
                                        inventories = json.load(file)
                                        file.close()
                                except Exception:
                                    inventories = ''

                                skin_number = f"{skin_type}1"

                                if inventories:
                                    inventories[str(user_id)] = {skin_number: {'skin_name': skin_name,
                                                                               'skin_cost': skin_cost,
                                                                               'skin_float': skin_float,
                                                                               'skin_date': skin_date,
                                                                               'skin_exterior': skin_ex,
                                                                               'case': case_name,
                                                                               'rare_pattern': rare_pattern
                                                                               }}
                                else:
                                    inventories = {user_id: {skin_number: {'skin_name': skin_name,
                                                                           'skin_cost': skin_cost,
                                                                           'skin_float': skin_float,
                                                                           'skin_date': skin_date,
                                                                           'skin_exterior': skin_ex,
                                                                           'case': case_name,
                                                                           'rare_pattern': rare_pattern}}}

                                with open('database/user_inventory.json', 'w') as file:
                                    json.dump(inventories, file)
                                    file.close()

                                len_user_inventory = 1

                            sell_button = {"en": f"Sell (${skin_cost})",
                                           "ru": f"Продать (${skin_cost})"}[user_language]

                            keep_button = {"en": f"Keep",
                                           "ru": f"Оставить"}[user_language]

                            skin_markup = InlineKeyboardMarkup(
                                inline_keyboard=[
                                    [InlineKeyboardButton(text=sell_button,
                                                          callback_data=f'sure_sell|{skin_number}'),
                                     InlineKeyboardButton(text=keep_button, callback_data='keep')]])

                            await video.delete()
                            skin_awaited = await bot.send_photo(chat_id=user_id, photo=FSInputFile(skin_file, 'rb'),
                                                                reply_markup=skin_markup)

                            if user_id in settings.skin_history.keys():
                                user_skin_history = settings.skin_history[user_id]
                                user_skin_history.append(skin_awaited)
                                settings.skin_history[user_id] = user_skin_history
                            else:
                                settings.skin_history[user_id] = [skin_awaited]

                            db.add_user_items(user_id, len_user_inventory)

                            try:
                                os.remove(skin_file)
                            except FileNotFoundError:
                                pass

                        except:
                            print('case_menu Error:', e)
                            new_user_money = user_money
                            await bot.send_message(chat_id=user_id, text=f'🛑 Произошла ошибка, средства возвращены')
                            await bot.send_message(chat_id=2051400423, text=f'case_menu Error from {user_id}')

                        db.add_user_money(user_id, new_user_money - user_money)

                else:
                    full_text = {"en": 'Your inventory is full.\n\nFree up space by selling any item.',
                                 "ru": 'Ваш инвентарь полон.\n\nОсвободите место, продав любой предмет.'}[
                        db.get_language(call.message.chat.id)]

                    await bot.answer_callback_query(callback_query_id=call.id, text=full_text, cache_time=10, show_alert=True)

        if call.data.startswith('sure_sell'):
            user_id = call.message.chat.id

            try:
                quick_sale = eval(db.get_quick_sell(user_id))

                if 'show' not in call.data:
                    add_show = ''
                    show = False
                else:
                    add_show = '_show'
                    show = True

                if quick_sale:
                    asyncio.create_task(sell_item(user_id, call, show))

                else:
                    sell_data = call.data
                    skin_number = sell_data[sell_data.find('|') + 1:]

                    with open('database/user_inventory.json', 'r') as file:
                        inventories = json.load(file)
                        file.close()

                    user_inventory = inventories[str(call.message.chat.id)]
                    skin_info = user_inventory[skin_number]

                    skin_cost = skin_info['skin_cost']
                    # skin_name = skin_info['skin_name']

                    sure_sell = {"en": ['Yes', 'No'],
                                 "ru": ['Да', 'Нет']}[
                        db.get_language(user_id)]

                    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=sure, callback_data=(
                        f'sell|{skin_number}' if sure in ['Yes', 'Да'] else
                        f'not_sell{add_show}|{skin_number}')) for sure in sure_sell]])

                    sell_question = {'en': f'<b>Are you sure you want to sell this skin for ${skin_cost}?</b>',
                                     'ru': f'<b>Вы уверены, что хотите продать этот скин за ${skin_cost}?</b>'}[
                        db.get_language(user_id)]

                    await bot.edit_message_caption(chat_id=user_id, message_id=call.message.message_id,
                                                   reply_markup=markup, caption=sell_question)

            except:
                no_skin = {"en": 'This skin is no longer in your inventory.',
                           "ru": 'Этого скина больше нет в вашем инвентаре.'}[
                    db.get_language(user_id)]

                await bot.answer_callback_query(call.id, no_skin, cache_time=10, show_alert=True)
                await bot.delete_message(chat_id=user_id, message_id=call.message.message_id)

            # asyncio.create_task(sure_sell())

        if call.data.startswith('sell'):
            async with async_lock:
                user_id = call.message.chat.id
                asyncio.create_task(sell_item(user_id, call))

        if call.data.startswith('not_sell'):
            sell_data = call.data

            skin_number = sell_data[sell_data.find('|') + 1:]

            with open('database/user_inventory.json', 'r') as file:
                inventories = json.load(file)
                file.close()

            user_inventory = inventories[str(call.message.chat.id)]
            skin_info = user_inventory[skin_number]

            skin_cost = skin_info['skin_cost']
            # skin_name = skin_info['skin_name']

            sell_button = {"en": f"Sell (${skin_cost})",
                           "ru": f"Продать (${skin_cost})"}[db.get_language(call.message.chat.id)]

            if 'show' in call.data:
                keep_button = {"en": f"🔺 Hide",
                               "ru": f"🔺 Скрыть"}[db.get_language(call.message.chat.id)]

                keyboard = [
                    [InlineKeyboardButton(text=sell_button,
                                          callback_data=f'sure_sell_show|{skin_number}')],
                    [InlineKeyboardButton(text=keep_button, callback_data='keep_show')]]

            else:
                keep_button = {"en": f"Keep",
                               "ru": f"Оставить"}[db.get_language(call.message.chat.id)]

                keyboard = [
                    [InlineKeyboardButton(text=sell_button,
                                          callback_data=f'sure_sell|{skin_number}'),
                     InlineKeyboardButton(text=keep_button, callback_data='keep')]]

            skin_markup = InlineKeyboardMarkup(
                inline_keyboard=keyboard)

            await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                           reply_markup=skin_markup)

        if 'show_skin' in call.data:
            async with async_lock:
                user_id = call.message.chat.id
                show_data = call.data

                skin_number = show_data[show_data.find('|') + 1:]

                try:
                    try:
                        if user_id in settings.skin_history.keys():
                            user_skin_history = settings.skin_history[user_id]
                            for skin in user_skin_history:
                                await bot.delete_message(chat_id=call.message.chat.id,
                                                         message_id=skin.message_id)

                        settings.skin_history[user_id] = []
                    except:
                        pass

                    with open('database/user_inventory.json', 'r') as file:
                        inventories = json.load(file)
                        file.close()

                    user_inventory = inventories[str(user_id)]
                    skin_info = user_inventory[skin_number]

                    skin_cost = skin_info['skin_cost']
                    skin_name = skin_info['skin_name']
                    skin_float = skin_info['skin_float']
                    skin_date = skin_info['skin_date']
                    skin_case = skin_info['case']
                    rare_pattern = skin_info['rare_pattern']

                    skin_file = load_skin_photo(skin_name, skin_float, skin_cost, skin_date, skin_case, rare_pattern)

                    sell_button = {"en": f"Sell (${skin_cost})",
                                   "ru": f"Продать (${skin_cost})"}[db.get_language(user_id)]

                    keep_button = {"en": f"🔺 Hide",
                                   "ru": f"🔺 Скрыть"}[db.get_language(user_id)]

                    skin_markup = InlineKeyboardMarkup(
                        inline_keyboard=[
                            [InlineKeyboardButton(text=sell_button,
                                                  callback_data=f'sure_sell_show|{skin_number}')],
                            [InlineKeyboardButton(text=keep_button, callback_data='keep_show')]])

                    settings.inventory_skin_history[user_id] = await bot.send_photo(chat_id=user_id,
                                                                                    photo=FSInputFile(skin_file, 'rb'),
                                                                                    reply_markup=skin_markup)

                    try:
                        os.remove(skin_file)
                    except FileNotFoundError:
                        pass

                except KeyError:
                    no_skin = {"en": 'This skin is no longer in your inventory.',
                               "ru": 'Этого скина больше нет в вашем инвентаре.'}[
                        db.get_language(call.message.chat.id)]

                    await bot.answer_callback_query(callback_query_id=call.id, text=no_skin, cache_time=10, show_alert=True)
                    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

            # asyncio.create_task(show_skin())

        if 'keep' in call.data:
            if 'show' not in call.data:
                keep_text = {"en": 'The skin remained in the inventory.',
                             "ru": 'Скин остался в инвентаре.'}[
                    db.get_language(call.message.chat.id)]

                await bot.answer_callback_query(callback_query_id=call.id, text=keep_text, cache_time=10)
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

        if call.data == 'quick_sale':
            user_id = call.message.chat.id
            asyncio.create_task(quick_sale_menu(user_id, call.message))

        if call.data == 'quick_sale_on':
            user_id = call.message.chat.id
            db.add_quick_sell(user_id, ['True', 'False'][eval(db.get_quick_sell(user_id))])
            asyncio.create_task(quick_sale_menu(user_id, call.message))

        if call.data == 'inventory_sort':
            user_id = call.message.chat.id
            asyncio.create_task(inventory_sort_menu(user_id, call.message))

        if 'sorting' in call.data:
            user_id = call.message.chat.id
            sort = call.data[call.data.find('by_') + 3:]
            sort = {'price': 'cost',
                    'novelty': 'date',
                    'rare': 'rare',
                    'float': 'float'}[sort]

            db.add_inventory_sort(user_id, sort)
            asyncio.create_task(inventory_sort_menu(user_id, call.message))

        if call.data == 'settings_back':
            user_id = call.message.chat.id
            asyncio.create_task(settings_menu(user_id, call.message, True))

        if 'page_inv' in call.data:
            user_id = call.message.chat.id
            message = call.message

            page_count = int(call.data[call.data.find('|') + 1:])
            asyncio.create_task(show_inventory(user_id, message, True, page_count))
