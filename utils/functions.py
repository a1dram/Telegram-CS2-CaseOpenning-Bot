from config import *

async_lock = asyncio.Lock()

async def settings_menu(user_id, message, edit_cap=False):
    sort_type = db.get_inventory_sort(user_id)
    quick_sell = db.get_quick_sell(user_id)

    if edit_cap is False:
        try:
            await settings.user_settings[user_id].delete()
            settings.user_settings[user_id] = None

        except:
            pass

    text_sort_type = {'cost': {'ru': 'По цене', 'en': 'By price'},
                      'date': {'ru': 'По новизне', 'en': 'By novelty'},
                      'rare': {'ru': 'По редкости', 'en': 'By rare'},
                      'float': {'ru': 'По флоату', 'en': 'By float'}}[sort_type][db.get_language(user_id)]

    text_quick_sell = [{'en': 'Disabled', 'ru': 'Отключена'}, {'en': 'Enabled', 'ru': 'Включена'}][eval(quick_sell)][
        db.get_language(user_id)]

    inventory_text = {'ru': 'Сортировка инвентаря', 'en': 'Inventory sorting'}[
        db.get_language(user_id)]

    sale_text = {'ru': 'Быстрая продажа', 'en': 'Quick sale'}[db.get_language(user_id)]

    close_button = {"en": f"🔺 Hide",
                    "ru": f"🔺 Скрыть"}[db.get_language(user_id)]

    markup = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=inventory_text, callback_data='inventory_sort')],
                         [InlineKeyboardButton(text=sale_text,
                                               callback_data='quick_sale')],
                         [InlineKeyboardButton(text=close_button, callback_data='keep_show')]])

    if edit_cap is False:
        try:
            settings.user_settings[user_id] = await bot.send_photo(
                chat_id=user_id,
                photo=FSInputFile('static/image_adds/settings_logo.jpg', 'rb'),
                caption={"en": "<b>⚙️ Settings</b>\n\n"
                               f"Inventory sorting: <b>{text_sort_type}</b>\n"
                               f"Quick sale: <b>{text_quick_sell}</b>",
                         "ru": "<b>⚙️ Настройки</b>\n\n"
                               f"Сортировка инвентаря: <b>{text_sort_type}</b>\n"
                               f"Быстрая продажа: <b>{text_quick_sell}</b>"}[
                    db.get_language(user_id)],
                reply_markup=markup, protect_content=True)
            await message.delete()

        except KeyError:
            pass
    else:
        await bot.edit_message_caption(chat_id=user_id, message_id=message.message_id,
                                       caption={"en": "<b>⚙️ Settings</b>\n\n"
                                                      f"Inventory sorting: <b>{text_sort_type}</b>\n"
                                                      f"Quick sale: <b>{text_quick_sell}</b>",
                                                "ru": "<b>⚙️ Настройки</b>\n\n"
                                                      f"Сортировка инвентаря: <b>{text_sort_type}</b>\n"
                                                      f"Быстрая продажа: <b>{text_quick_sell}</b>"}[
                                           db.get_language(user_id)],
                                       reply_markup=markup)


async def quick_sale_menu(user_id, message):
    quick_sale_type = eval(db.get_quick_sell(user_id))

    text_quick_sell = \
        [{'en': 'Disabled', 'ru': 'Отключена'}, {'en': 'Enabled', 'ru': 'Включена'}][quick_sale_type][
            db.get_language(user_id)]

    sale_text = [{'ru': 'Включить', 'en': 'Turn on'},
                 {'ru': 'Выключить', 'en': 'Turn off'}][quick_sale_type][
        db.get_language(user_id)]

    close_button = {"en": f"🔺 Hide",
                    "ru": f"🔺 Скрыть"}[db.get_language(user_id)]

    back_button = {"en": f"← Back",
                   "ru": f"← Назад"}[db.get_language(user_id)]

    markup = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=sale_text, callback_data='quick_sale_on')],
                         [InlineKeyboardButton(text=back_button,
                                               callback_data='settings_back'),
                          InlineKeyboardButton(text=close_button, callback_data='keep_show')]])

    await bot.edit_message_caption(chat_id=user_id, message_id=message.message_id,
                                   caption={"en": "<b>⚡️ Quick Sale\n\n"
                                                  f"This function removes the confirmation "
                                                  f"of the sale of the item.</b>\n\n"
                                                  f"Status: <b>{text_quick_sell}</b>",
                                            "ru": "<b>⚡️ Быстрая продажа\n\n"
                                                  f"Эта функция убирает подтверждение "
                                                  f"продажи предмета.</b>\n\n"
                                                  f"Статус: <b>{text_quick_sell}</b>"}[
                                       db.get_language(user_id)],
                                   reply_markup=markup)


async def inventory_sort_menu(user_id, message):
    sort_type = db.get_inventory_sort(user_id)

    new_sort_type = {'cost': {'ru': 'По цене', 'en': 'By price'},
                     'date': {'ru': 'По новизне', 'en': 'By novelty'},
                     'rare': {'ru': 'По редкости', 'en': 'By rare'},
                     'float': {'ru': 'По флоату', 'en': 'By float'}}

    text_sort_type = new_sort_type[sort_type][db.get_language(user_id)]

    all_types = [new_sort_type['rare'], new_sort_type['cost'], new_sort_type['date'], new_sort_type['float']]

    close_button = {"en": f"🔺 Hide",
                    "ru": f"🔺 Скрыть"}[db.get_language(user_id)]

    back_button = {"en": f"← Back",
                   "ru": f"← Назад"}[db.get_language(user_id)]

    markup = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=s_type[db.get_language(user_id)],
                                               callback_data='sorting_' + s_type['en'].lower().replace(' ', '_')) for
                          s_type in all_types if s_type[db.get_language(user_id)] != text_sort_type],
                         [InlineKeyboardButton(text=back_button,
                                               callback_data='settings_back'),
                          InlineKeyboardButton(text=close_button, callback_data='keep_show')]])

    await bot.edit_message_caption(chat_id=user_id, message_id=message.message_id,
                                   caption={"en": "<b>👝 Inventory Sorting\n\n"
                                                  f"This function sorts your inventory.</b>\n\n"
                                                  f"Sorting status: <b>{text_sort_type}</b>\n\n"
                                                  f"<b>Sorting options ↓</b>",
                                            "ru": "<b>👝 Сортировка инвентаря\n\n"
                                                  f"Эта функция сортирует ваш инвентарь.</b>\n\n"
                                                  f"Статус: <b>{text_sort_type}</b>\n\n"
                                                  f"<b>Варианты сортировки ↓</b>"}[
                                       db.get_language(user_id)],
                                    reply_markup=markup)


async def show_inventory(user_id, message, message_cap=False, page_count=0):
    len_user_skins = db.get_user_items(user_id)

    if len_user_skins < 0:
        db.add_user_items(user_id, 0)
        len_user_skins = 0

    skins_on_page = 6
    page_number = page_count // skins_on_page + 1 if page_count != 0 else 1
    page_c2 = len_user_skins / skins_on_page

    if len_user_skins <= 0:
        all_pages = 1
    else:
        all_pages = int(page_c2) if page_c2.is_integer() else int(page_c2) + 1

    try:
        with open('database/user_inventory.json', 'r') as file:
            inventories = json.load(file)
            file.close()

        user_inventory = inventories[str(user_id)]
        len_user_skins = len(user_inventory)
        user_skins_cost = round(sum(skin['skin_cost'] for num, skin in user_inventory.items()), 2)

    except:
        user_inventory = {}
        # len_user_skins = 0
        user_skins_cost = 0

    sort_type = db.get_inventory_sort(user_id)

    if sort_type == 'rare':
        user_inventory = sorted(user_inventory.items(), key=lambda item: item[0])
        user_inventory = {key: value for key, value in user_inventory[0 + page_count:skins_on_page + page_count]}

    elif sort_type == 'cost':
        user_inventory = sorted(user_inventory.items(), key=lambda item: float(item[1]['skin_cost']))[::-1]
        user_inventory = {key: value for key, value in user_inventory[0 + page_count:skins_on_page + page_count]}

    elif sort_type == 'date':
        user_inventory = sorted(user_inventory.items(), key=lambda item: int(item[0][1:]))[::-1]
        user_inventory = {key: value for key, value in user_inventory[0 + page_count:skins_on_page + page_count]}

    elif sort_type == 'float':
        user_inventory = sorted(user_inventory.items(), key=lambda item: float(item[1]['skin_float']))
        user_inventory = {key: value for key, value in user_inventory[0 + page_count:skins_on_page + page_count]}

    # markup = InlineKeyboardMarkup(row_width=2)
    markup_list = []

    if len_user_skins > 0:
        for num, skin in user_inventory.items():
            rare_pattern = skin['rare_pattern']
            rare_pattern_logo = f"💎, " if rare_pattern else ''

            markup_list.append([
                InlineKeyboardButton(text=f"{skin['skin_name']} ({rare_pattern_logo}{skin['skin_exterior']}, ${skin['skin_cost']})", 
                                     callback_data=f"show_skin|{num}")
                                     ])

        if len_user_skins > skins_on_page:
            if len_user_skins - page_count > skins_on_page:
                if page_count >= skins_on_page:
                    markup_list.append(
                        [
                        InlineKeyboardButton(text='<<<', callback_data=f'back_page_inv|{page_count - skins_on_page}'),
                        InlineKeyboardButton(text='>>>', callback_data=f'next_page_inv|{page_count + skins_on_page}')
                        ])
                else:
                    markup_list.append(
                        [InlineKeyboardButton(text='>>>', callback_data=f'next_page_inv|{page_count + skins_on_page}')]
                        )
            else:
                markup_list.append(
                    [InlineKeyboardButton(text='<<<', callback_data=f'back_page_inv|{page_count - skins_on_page}')]
                    )

    close_button = {"en": f"🔺 Hide",
                    "ru": f"🔺 Скрыть"}[db.get_language(user_id)]

    markup_list.append([InlineKeyboardButton(text=close_button, callback_data='keep_show')])
    markup = InlineKeyboardMarkup(inline_keyboard=markup_list)

    user_items_limit = db.get_inventory_capacity(user_id)

    if message_cap is False:
        try:
            await settings.inventory_history[user_id].delete()
            settings.inventory_history[user_id] = None
        except:
            pass

        try:
            text_sort_type = {'cost': {'ru': 'По цене', 'en': 'By price'},
                              'date': {'ru': 'По новизне', 'en': 'By novelty'},
                              'rare': {'ru': 'По редкости', 'en': 'By rare'},
                              'float': {'ru': 'По флоату', 'en': 'By float'}}[sort_type][
                db.get_language(message.from_user.id)]

            settings.inventory_history[user_id] = await bot.send_photo(
                chat_id=user_id, photo=FSInputFile('static/image_adds/inventory.jpg', 'rb'),
                caption={"en": "<b>🗄 Inventory</b> \n\n"
                               f"Inventory cost: <b>${user_skins_cost}</b>\n"
                               f"Total items: <b>{len_user_skins}/{user_items_limit}</b>\n\n"
                               f"Sorting: <b>{text_sort_type}</b>\n"
                               f"Page: <b>{page_number}/{all_pages}</b>",

                         "ru": "<b>🗄 Инвентарь</b> \n\n"
                               f"Стоимость инвентаря: <b>${user_skins_cost}</b>\n"
                               f"Всего предметов: <b>{len_user_skins}/{user_items_limit}</b>\n\n"
                               f"Сортировка: <b>{text_sort_type}</b>\n"
                               f"Страница: <b>{page_number}/{all_pages}</b>"}[
                    db.get_language(user_id)],
                reply_markup=markup)

            await message.delete()

        except KeyError:
            pass

    else:
        try:
            text_sort_type = {'cost': {'ru': 'По цене', 'en': 'By price'},
                              'date': {'ru': 'По новизне', 'en': 'By novelty'},
                              'rare': {'ru': 'По редкости', 'en': 'By rare'},
                              'float': {'ru': 'По флоату', 'en': 'By float'}}[sort_type][
                db.get_language(user_id)]

            await bot.edit_message_caption(
                chat_id=user_id, message_id=message.message_id,
                caption={"en": "<b>🗄 Inventory</b> \n\n"
                               f"Inventory cost: <b>${user_skins_cost}</b>\n"
                               f"Total items: <b>{len_user_skins}/{user_items_limit}</b>\n\n"
                               f"Sorting: <b>{text_sort_type}</b>\n"
                               f"Page: <b>{page_number}/{all_pages}</b>",

                         "ru": "<b>🗄 Инвентарь</b> \n\n"
                               f"Стоимость инвентаря: <b>${user_skins_cost}</b>\n"
                               f"Всего предметов: <b>{len_user_skins}/{user_items_limit}</b>\n\n"
                               f"Сортировка: <b>{text_sort_type}</b>\n"
                               f"Страница: <b>{page_number}/{all_pages}</b>"}[
                    db.get_language(user_id)],
                reply_markup=markup)

        except:
            pass


async def sell_item(user_id, call, show=False):
    async with async_lock:
        sell_number = call.data[call.data.find('|') + 1:]
    
        try:
            with open('database/user_inventory.json', 'r') as file:
                inventories = json.load(file)
                file.close()

            user_inventory = inventories[str(user_id)]
            new_user_inventory = user_inventory

            skin_cost = user_inventory[sell_number]['skin_cost']
            skin_name = user_inventory[sell_number]['skin_name']

            db.add_user_money(call.message.chat.id, float(skin_cost))

            del new_user_inventory[sell_number]
            inventories[str(user_id)] = {**new_user_inventory, **user_inventory}

            with open('database/user_inventory.json', 'w') as file:
                json.dump(inventories, file)
                file.close()

            sold_talk = {"en": f'You sold {skin_name} for ${skin_cost}',
                         "ru": f'Вы продали {skin_name} за ${skin_cost}'}[
                db.get_language(call.message.chat.id)]

            await bot.answer_callback_query(callback_query_id=call.id, text=sold_talk, cache_time=10)

            try:
                await bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
            except:
                pass

            len_user_inventory = db.get_user_items(user_id)

            # if user_id in settings.inventory_history.keys() and show is True:
            try:
                if settings.inventory_history[user_id] is not None:
                    asyncio.create_task(show_inventory(user_id, settings.inventory_history[user_id], True))

            except KeyError:
                pass

            db.add_user_items(user_id, len_user_inventory - 1)

        except KeyError:
            no_skin = {"en": 'This skin is no longer in your inventory.',
                       "ru": 'Этого скина больше нет в вашем инвентаре.'}[
                db.get_language(call.message.chat.id)]

            await bot.answer_callback_query(callback_query_id=call.id, text=no_skin, cache_time=10, show_alert=True)
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
