import telebot
import time
import json
from datetime import datetime
from spotify_Module import localization

with open("bot_Keys.json") as bot_Keys_File:
    bot_Keys = json.load(bot_Keys_File)

spotify_Bot = telebot.TeleBot(bot_Keys["telegram"]["telegram_Key"])

language_Vocabluary = localization.load_Vocabluary()



def controls_Main_Menu(chat_id, language_Name):
    """
    Клавиатура основного меню
    """
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
    keyboard.row(language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["inline_Help"])
    keyboard.row(language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["your_Tops"], language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["super_Shuffle"])
    keyboard.row(language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["musicQuiz"], language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["library_Statistics"])
    keyboard.row(language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["blocked_Tracks"], language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["library_Helper"])
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["notifications"]["choose_Category"], reply_markup=keyboard)



def spotify_Login_Offer(chat_id, spotify_Auth_Link, language_Name):
    """
    Просьба о входе в аккаунт Spotify
    """
    login_Keyboard = telebot.types.InlineKeyboardMarkup()
    login_Button = telebot.types.InlineKeyboardButton(text=language_Vocabluary[language_Name]["keyboard_Buttons"]["inline_Buttons"]["authorize_Spotify"], url=spotify_Auth_Link)
    login_Keyboard.add(login_Button)
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["authorization"]["spotify_Login_Offer"], parse_mode="Markdown", reply_markup=login_Keyboard)



def language_Selector(chat_id, language_Name):
    """
    Клавиатура выбора языка
    """
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.row(language_Vocabluary[language_Name]["keyboard_Buttons"]["language"]["ENG"])
    keyboard.row(language_Vocabluary[language_Name]["keyboard_Buttons"]["language"]["RUS"])

    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["authorization"]["choose_Language"], parse_mode="Markdown", reply_markup=keyboard)



def language_Changed(chat_id, language_Name):
    """
    Язык сменен успешно
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["notifications"]["language_Changed"], parse_mode="Markdown")



def user_Leaving(chat_id, language_Name):
    """
    Уведомление пользователю об успешном выходе из бота
    """
    #Первое сообщение с кнопкой /start
    start_Keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    start_Keyboard.row("/start")
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["authorization"]["user_Leaving"], parse_mode="Markdown", reply_markup=start_Keyboard)

    #Второе сообщение с кнопкой отключения бота
    keyboard = telebot.types.InlineKeyboardMarkup()
    disable_Button = telebot.types.InlineKeyboardButton(text=language_Vocabluary[language_Name]["keyboard_Buttons"]["inline_Buttons"]["disable_Jarvis"], url="https://www.spotify.com/account/apps/")
    keyboard.add(disable_Button)
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["authorization"]["disable_Bot"], parse_mode="Markdown", reply_markup=keyboard)



def auth_Complete(chat_id, user_Nickname, language_Name):
    """
    Успешная авторизация
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["authorization"]["auth_Complete"].format(user_Nickname=user_Nickname), parse_mode="Markdown")



def send_Developer_Contacts(chat_id, language_Name):
    """
    Отправить контакты разработчика
    """
    links_Keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
    discord_Button = telebot.types.InlineKeyboardButton(text="Discord", url="https://discord.gg/Z4A4qdw")
    vk_Button = telebot.types.InlineKeyboardButton(text="VK", url="https://vk.com/koteyk0o")
    links_Keyboard.add(discord_Button, vk_Button)
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["authorization"]["developer_Contacts"], parse_mode="Markdown", reply_markup=links_Keyboard)    



def superShuffle_Description(chat_id, language_Name):
    """
    Описание функции супер-шаффл
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["superShuffle"]["superShuffle_Description"], parse_mode="Markdown")



def yourTops_Description(chat_id, language_Name):
    """
    Описание функции ваши-топы
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["yourTops"]["yourTops_Description"], parse_mode="Markdown")



def send_MusicQuiz_Round(chat_id, musicQuiz_Round_Data, language_Name):
    """
    Отправить пользователю музыкальную викторину
    """
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1)
    keyboard.row(musicQuiz_Round_Data["keyboard"][0])
    keyboard.row(musicQuiz_Round_Data["keyboard"][1])
    keyboard.row(musicQuiz_Round_Data["keyboard"][2])
    keyboard.row(musicQuiz_Round_Data["keyboard"][3])

    musicQuiz_Round = musicQuiz_Round_Data["current_Round"] + 1
    audio_Title = f"Round #{musicQuiz_Round}"
    audio_File = musicQuiz_Round_Data["audio_File"]

    spotify_Bot.send_audio(chat_id, audio=audio_File, title=audio_Title, caption=language_Vocabluary[language_Name]["chat_Messages"]["musicQuiz"]["musicQuiz_Question"], reply_markup=keyboard)



def musicQuiz_Rules(chat_id, language_Name):
    """
    Отправить пользователю правила игры в музыкальную викторину
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["musicQuiz"]["musicQuiz_Rules"], parse_mode="Markdown")



def shuffle_Tracks_Count(chat_id, language_Name):
    """
    Вопрос пользователю о количестве треков для супер-шаффла
    """
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    keyboard.row(language_Vocabluary[language_Name]["keyboard_Buttons"]["offset_Size"]["100_Songs"], language_Vocabluary[language_Name]["keyboard_Buttons"]["offset_Size"]["200_Songs"], language_Vocabluary[language_Name]["keyboard_Buttons"]["offset_Size"]["all_Offset"])
    keyboard.row(language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["back_To_Menu"])
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["superShuffle"]["tracks_Count_Question"], reply_markup=keyboard)



def tops_Type_Select(chat_id, language_Name):
    """
    Вопрос пользователю о типе топа
    """
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    keyboard.row(language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["songs"], language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["artists"])
    keyboard.row(language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["back_To_Menu"])
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["yourTops"]["select_Top_Type"], reply_markup=keyboard)



def tops_Time_Period(chat_id, language_Name):
    """
    Вопрос пользователю о периоде выборки для топа
    """
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    keyboard.row(language_Vocabluary[language_Name]["keyboard_Buttons"]["time_Buttons"]["4_Weeks"], language_Vocabluary[language_Name]["keyboard_Buttons"]["time_Buttons"]["6_Months"], language_Vocabluary[language_Name]["keyboard_Buttons"]["time_Buttons"]["all_Time"])
    keyboard.row(language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["back_To_Menu"])
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["yourTops"]["select_Top_Time"], reply_markup=keyboard)



def musicQuiz_Type_Select(chat_id, language_Name):
    """
    Вопрос пользователю о выборке для викторины
    """
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.row(language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["liked_Songs"], language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["top_Songs"])
    keyboard.row(language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["back_To_Menu"])
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["musicQuiz"]["quiz_Section"], reply_markup=keyboard)



def top_Database_Error(chat_id, language_Name):
    """
    Ошибка базы данных топов
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["yourTops"]["database_Error"], parse_mode="Markdown")



def astray_Notification(chat_id, language_Name):
    """
    Сообщить пользователю о возможности вызова клавиатуры
    """ 
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["notifications"]["astray_Notification"], parse_mode="Markdown")



def send_Easter_Egg(chat_id, message):
    """
    Пасхалки!
    """
    spotify_Bot.send_message(chat_id, message, parse_mode="Markdown")



def insufficient_Data_For_Top(chat_id, language_Name):
    """
    Не хватает песен для составления топа
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["yourTops"]["insufficient_Data_For_Top"], parse_mode="Markdown")



def no_ActiveDevices(chat_id, language_Name):
    """
    Нет активных устройств для начала воспроизведения
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["errors"]["start_Playing_NoDevice"], parse_mode="Markdown")



def premium_Required(chat_id, language_Name):
    """
    Для начала воспроизведения требуется премиум-подписка
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["errors"]["start_Playing_PremiumRequired"], parse_mode="Markdown")



def playback_Error(chat_id, language_Name):
    """
    Невозможно начать воспроизведение
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["errors"]["start_Playing_RequestError"], parse_mode="Markdown")



def playback_Started(chat_id, language_Name):
    """
    Воспроизведение началось
    """
    playback_Text = language_Vocabluary[language_Name]["chat_Messages"]["notifications"]["playback_Started"]
    spotify_Bot.send_message(chat_id, playback_Text, parse_mode="Markdown")



def song_Added_To_Queue(chat_id, language_Name):
    """
    Песня была добавлена в список воспроизведения
    """
    playback_Text = language_Vocabluary[language_Name]["chat_Messages"]["notifications"]["added_To_Queue"]
    spotify_Bot.send_message(chat_id, playback_Text, parse_mode="Markdown")



def musicQuiz_Preparing(chat_id, language_Name):
    """
    Игровая сессия подготавливается
    """
    markup = telebot.types.ReplyKeyboardRemove(selective=False)
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["musicQuiz"]["musicQuiz_Preparing"], reply_markup=markup, parse_mode="Markdown")



def musicQuiz_Incorrect_Answer(chat_id, musicQuiz_Round_Stats, language_Name):
    """
    Неправильный ответ викторины
    """
    right_Answer = musicQuiz_Round_Stats["round_Answer"]
    took_Time_Answer = int(time.time()) - musicQuiz_Round_Stats["round_Prepared_Timestamp"]
    message_Text = language_Vocabluary[language_Name]["chat_Messages"]["musicQuiz"]["musicQuiz_Incorrect_Answer"].format(right_Answer=right_Answer, took_Time_Answer=took_Time_Answer)

    markup = telebot.types.ReplyKeyboardRemove(selective=False)
    spotify_Bot.send_message(chat_id, message_Text, reply_markup=markup, parse_mode="HTML")



def musicQuiz_Correct_Answer(chat_id, musicQuiz_Round_Stats, language_Name):
    """
    Правильный ответ викторины
    """
    right_Answer = musicQuiz_Round_Stats["round_Answer"]
    took_Time_Answer = int(time.time()) - musicQuiz_Round_Stats["round_Prepared_Timestamp"]
    message_Text = language_Vocabluary[language_Name]["chat_Messages"]["musicQuiz"]["musicQuiz_Correct_Answer"].format(right_Answer=right_Answer, took_Time_Answer=took_Time_Answer)

    markup = telebot.types.ReplyKeyboardRemove(selective=False)
    spotify_Bot.send_message(chat_id, message_Text, reply_markup=markup, parse_mode="HTML")



def musicQuiz_Answer_Timeout(chat_id, musicQuiz_Round_Stats, language_Name):
    """
    Закончилось время на ответ викторины
    """
    right_Answer = musicQuiz_Round_Stats["round_Answer"]
    took_Time_Answer = int(time.time()) - musicQuiz_Round_Stats["round_Prepared_Timestamp"]
    message_Text = language_Vocabluary[language_Name]["chat_Messages"]["musicQuiz"]["musicQuiz_Answer_Timeout"].format(right_Answer=right_Answer, took_Time_Answer=took_Time_Answer)

    markup = telebot.types.ReplyKeyboardRemove(selective=False)
    spotify_Bot.send_message(chat_id, message_Text, reply_markup=markup, parse_mode="HTML")



def musicQuiz_End(chat_id, musicQuiz_Statistic, language_Name):
    """
    Конец музыкальной викторины
    """
    markup = telebot.types.ReplyKeyboardRemove(selective=False)

    total_Rounds = musicQuiz_Statistic["total_Rounds"]
    correct_Answers = musicQuiz_Statistic["correct_Answers"]
    message_Text = language_Vocabluary[language_Name]["chat_Messages"]["musicQuiz"]["musicQuiz_End"].format(total_Rounds=total_Rounds, correct_Answers=correct_Answers)
    spotify_Bot.send_message(chat_id, message_Text, reply_markup=markup, parse_mode="Markdown")



def musicQuiz_Error_NoTracks(chat_id, language_Name):
    """
    Ошибка MusicQuiz - не хватило треков для начала игры
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["musicQuiz"]["musicQuiz_Error_NoSongs"], parse_mode="Markdown")



def musicQuiz_Error_RoundProcess(chat_id, language_Name):
    """
    Ошибка MusicQuiz - возникла ошибка при обработке раунда
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["musicQuiz"]["musicQuiz_Error_RoundProcess"], parse_mode="Markdown")



def not_Enough_Songs(chat_id, language_Name, songs_Count=None):
    """
    Недостаточно песен
    """
    if songs_Count:
        message_Text = language_Vocabluary[language_Name]["chat_Messages"]["errors"]["not_Enough_Minimum_Songs"].format(songs_Count=songs_Count)
    else:
        message_Text = language_Vocabluary[language_Name]["chat_Messages"]["errors"]["not_Enough_Songs"]

    spotify_Bot.send_message(chat_id, message_Text, parse_mode="Markdown")



def blocked_Tracks_Description(chat_id, language_Name):
    """
    Описание раздела Заблокированные песни
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["blocked_Tracks"]["description"], parse_mode="Markdown")



def downloading_Information(chat_id, language_Name, hide_Keyboard=True):
    """
    Выполняется загрузка информации
    """
    if hide_Keyboard:
        markup = telebot.types.ReplyKeyboardRemove(selective=False)
        spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["notifications"]["downloading_Information"], reply_markup=markup, parse_mode="Markdown")

    else:
        spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["notifications"]["downloading_Information"], parse_mode="Markdown")



def cannot_Authorize(chat_id, language_Name):
    """
    Ошибка авторизации пользователя
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["errors"]["cannot_Authorize"], parse_mode="Markdown")



def servers_Link_Error(chat_id, language_Name):
    """
    Ошибка связи с серверами Спотифая
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["errors"]["servers_Link_Error"], parse_mode="Markdown")



def unknown_Error(chat_id, language_Name):
    """
    Неизвестная ошибка
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["errors"]["unknown_Error"], parse_mode="Markdown")



def denied_Work_Reason(chat_id, language_Name):
    """
    Пока выполняется работа, вы не можете использовать эту функцию
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["errors"]["denied_Work_Reason"], parse_mode="Markdown")



def playlist_Preparing(chat_id, language_Name, hide_Keyboard=True):
    """
    Плейлист готовится
    """
    if hide_Keyboard:
        markup = telebot.types.ReplyKeyboardRemove(selective=False)
        spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["notifications"]["playlist_Preparing"], reply_markup=markup, parse_mode="Markdown")

    else:
        spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["notifications"]["playlist_Preparing"], parse_mode="Markdown")



def jarvis_Updated(chat_id, language_Name, jarvis_Version):
    """
    Джарвис был обновлен
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["notifications"]["jarvis_Updated"].format(jarvis_Version=jarvis_Version), parse_mode="Markdown")



def inline_Mode_Help(chat_id, language_Name):
    """
    Помощь по Inline режиму
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["messages"]["inline_Help"], parse_mode="Markdown")



def library_Statistics_Description(chat_id, language_Name):
    """
    Описание раздела статистика библиотеки
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["library_Statistics"]["description"], parse_mode="Markdown")



def library_Statistics_Type(chat_id, language_Name):
    """
    Вопрос пользователю о типе статистики
    """
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.row(language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["by_Decades"], language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["by_Artists"], language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["by_Genres"])
    keyboard.row(language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["back_To_Menu"])
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["library_Statistics"]["statistic_Section"], reply_markup=keyboard)



def playlist_Ready(chat_id, playlist_Data, language_Name):
    """
    Плейлист готов
    """
    keyboard = telebot.types.InlineKeyboardMarkup()

    playlist_ID = playlist_Data["playlist_ID"] #Шифровка callback даты для последующего парсинга (ограничение в 64 байта)
    play_On_Spotify = telebot.types.InlineKeyboardButton(text=language_Vocabluary[language_Name]["keyboard_Buttons"]["inline_Buttons"]["play_On_Spotify"], callback_data=f"player#play#playlist#{playlist_ID}")
    open_On_Spotify = telebot.types.InlineKeyboardButton(text=language_Vocabluary[language_Name]["keyboard_Buttons"]["inline_Buttons"]["open_On_Spotify"], url=playlist_Data["external_URL"])
    keyboard.add(play_On_Spotify)
    keyboard.add(open_On_Spotify)

    ready_Data = {}
    ready_Data["name"] = language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["name"] + playlist_Data["name"] + "\n"
    ready_Data["description"] = language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["description"] + playlist_Data["description"] + "\n"
    ready_Data["total_Tracks"] = language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["total_Tracks"] + str(playlist_Data["total_Tracks"]) + "\n"
    ready_Data["playlist_Summary"] = ready_Data["name"] + ready_Data["description"] + ready_Data["total_Tracks"]

    ready_Text = language_Vocabluary[language_Name]["chat_Messages"]["notifications"]["playlist_Ready"] + "\n\n" + ready_Data["playlist_Summary"]

    spotify_Bot.send_photo(chat_id, playlist_Data["playlist_Cover"], caption=ready_Text, reply_markup=keyboard, parse_mode="HTML")



def artists_Top(chat_id, top_Data, language_Name, message_ID=None):
    """
    Вывод топа исполнителей пользователя
    """
    keyboard = telebot.types.InlineKeyboardMarkup()

    time_Range = top_Data["time_Range"]

    previous_Page = top_Data["current_Page"] - 1 #Индекс предыдущей страницы
    previous_Page_Button = telebot.types.InlineKeyboardButton(text=language_Vocabluary[language_Name]["keyboard_Buttons"]["inline_Buttons"]["previous_Page"], callback_data=f"interface#topArtists#page#{time_Range}#{previous_Page}")

    next_Page = top_Data["current_Page"] + 1 #Индекс следующей страницы
    next_Page_Button = telebot.types.InlineKeyboardButton(text=language_Vocabluary[language_Name]["keyboard_Buttons"]["inline_Buttons"]["next_Page"], callback_data=f"interface#topArtists#page#{time_Range}#{next_Page}")

    if not top_Data["current_Page"] <= 1 and not top_Data["current_Page"] >= top_Data["max_Pages"]: #Херня для создания красивой клавиатуры
        keyboard.add(previous_Page_Button, next_Page_Button)
    elif not top_Data["current_Page"] <= 1:
        keyboard.add(previous_Page_Button)
    elif not top_Data["current_Page"] >= top_Data["max_Pages"]:
        keyboard.add(next_Page_Button)

    time_Range = language_Vocabluary[language_Name]["chat_Messages"]["yourTops"][time_Range]
    last_Update = datetime.utcfromtimestamp(int(top_Data["last_Update"])).strftime("%m-%d-%Y %H:%M")

    chat_Top_Data = {}
    chat_Top_Data["top_Summary"] = language_Vocabluary[language_Name]["chat_Messages"]["yourTops"]["top_Artists_Header"].format(time_Range=time_Range, previous_Page=top_Data["current_Page"], next_Page=top_Data["max_Pages"]) + "\n\n"

    chat_Top_Data["top_Summary"] += language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["last_Update"] + last_Update + "\n\n"

    for top_Item in top_Data["items"]:
        prefix = top_Data["items"][top_Item]["prefix"]
        artist = top_Data["items"][top_Item]["artist"]
        followers = top_Data["items"][top_Item]["followers"]
        chat_Top_Data[top_Item] = f"<b>{top_Item + 1}.</b> {artist} - {followers} Followers <b>{prefix}</b>\n\n"
        chat_Top_Data["top_Summary"] += chat_Top_Data[top_Item]

    if message_ID: #Если предоставлен ID сообщения, то редактируем сообщение, если нет, отправляем новое
        spotify_Bot.edit_message_text(chat_Top_Data["top_Summary"], chat_id=chat_id, message_id=message_ID, reply_markup=keyboard, parse_mode="HTML")
    else:
        spotify_Bot.send_message(chat_id, chat_Top_Data["top_Summary"], reply_markup=keyboard, parse_mode="HTML")



def blocked_Tracks(chat_id, blocked_Data, language_Name):
    """
    Вывод заблокированных песен
    """
    message = {}
    message["header"] = language_Vocabluary[language_Name]["chat_Messages"]["blocked_Tracks"]["message_Header"]
    message["country"] = language_Vocabluary[language_Name]["chat_Messages"]["blocked_Tracks"]["your_Account_Country"].format(user_Country=blocked_Data["user_Country"])
    message["blocked_Tracks"] = language_Vocabluary[language_Name]["chat_Messages"]["blocked_Tracks"]["blocked_Songs_Number"].format(blocked_Number=blocked_Data["blocked_Count"], total_Number=blocked_Data["tracks_Count"])
    message["summary"] = message["header"] + "\n\n" + message["country"] + "\n\n" + message["blocked_Tracks"] + "\n\n"

    for blocked_Item in range(len(blocked_Data["tracks"])):
        artist = blocked_Data["tracks"][blocked_Item]["artist"]
        name = blocked_Data["tracks"][blocked_Item]["name"]
        summary = f"<b>{blocked_Item + 1}.</b> {artist} - {name}\n\n"
        message["summary"] += summary
    
    spotify_Bot.send_message(chat_id, message["summary"], parse_mode="HTML")



def decades_Statistic(chat_id, statistic_Data, language_Name):
    """
    Вывод статистики по декадам
    """
    message = {}
    message["header"] = language_Vocabluary[language_Name]["chat_Messages"]["library_Statistics"]["decades_Statistic_Header"]
    message["total_Songs"] = language_Vocabluary[language_Name]["chat_Messages"]["library_Statistics"]["total_Tracks"].format(total_Songs=statistic_Data["total_Tracks"])
    message["summary"] = message["header"] + "\n\n" + message["total_Songs"] + "\n\n"
    
    for decade in range(len(statistic_Data["statistic_Data"])):
        decade_Item = language_Vocabluary[language_Name]["chat_Messages"]["library_Statistics"]["decade_Statistic"].format(decade=statistic_Data["statistic_Data"][decade]["decade"], songs_Count=statistic_Data["statistic_Data"][decade]["tracks_In_Decade"], percent_Of_Total=statistic_Data["statistic_Data"][decade]["percent_Of_Total"])
        message["summary"] += decade_Item + "\n\n"

    spotify_Bot.send_message(chat_id, message["summary"], parse_mode="HTML")



def artists_Statistic(chat_id, statistic_Data, language_Name):
    """
    Вывод статистики по исполнителям
    """
    message = {}
    message["header"] = language_Vocabluary[language_Name]["chat_Messages"]["library_Statistics"]["artists_Statistic_Header"]
    message["total_Songs"] = language_Vocabluary[language_Name]["chat_Messages"]["library_Statistics"]["total_Tracks"].format(total_Songs=statistic_Data["total_Tracks"])
    message["summary"] = message["header"] + "\n\n" + message["total_Songs"] + "\n\n"
    
    for artist in range(len(statistic_Data["statistic_Data"])):
        artist_Item = language_Vocabluary[language_Name]["chat_Messages"]["library_Statistics"]["artist_Statistic"].format(artist=statistic_Data["statistic_Data"][artist]["artist"], songs_Count=statistic_Data["statistic_Data"][artist]["artist_Tracks"], percent_Of_Total=statistic_Data["statistic_Data"][artist]["percent_Of_Total"])
        message["summary"] += artist_Item + "\n\n"

    spotify_Bot.send_message(chat_id, message["summary"], parse_mode="HTML")



def genres_Statistic(chat_id, statistic_Data, language_Name):
    """
    Вывод статистики по жанрам
    """
    message = {}
    message["header"] = language_Vocabluary[language_Name]["chat_Messages"]["library_Statistics"]["genres_Statistic_Header"]
    message["summary"] = message["header"] + "\n\n"
    
    for genre in range(len(statistic_Data)):
        genre_Item = f"<b>{genre + 1}.</b> {statistic_Data[genre]}"
        message["summary"] += genre_Item + "\n\n"

    spotify_Bot.send_message(chat_id, message["summary"], parse_mode="HTML")



def duplicates_Found(chat_id, duplicates_Data, language_Name):
    #keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    #keyboard.row(language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["delete"], language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["leave_As_Is"])

    message = {}
    message["header"] = language_Vocabluary[language_Name]["chat_Messages"]["library_Helper"]["duplicates_Remover"]["list_Description"]
    message["summary"] = message["header"] + "\n\n"
    for duplicate in range(len(duplicates_Data["tracks"])):
        duplicate_Item = language_Vocabluary[language_Name]["chat_Messages"]["library_Helper"]["duplicates_Remover"]["duplicates_Message"].format(song_Artists=duplicates_Data["tracks"][duplicate]["artists"], song_Name=duplicates_Data["tracks"][duplicate]["name"], duplicates_Amount=duplicates_Data["tracks"][duplicate]["duplicate_Count"])
        message["summary"] += duplicate_Item + "\n\n"
    
    spotify_Bot.send_message(chat_id, message["summary"], parse_mode="HTML")



def send_LibraryHelper_Menu(chat_id, language_Name):
    """
    Отправить меню помощника библиотеки
    """
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    keyboard.row(language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["library_Duplicates"])
    keyboard.row(language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["playlist_Duplicates"])

    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["notifications"]["choose_Category"], reply_markup=keyboard)



def send_Playlist_Selector(chat_id, playlists_Names, language_Name):
    """
    Отправить пользователю клавиатуру с плейлистами
    """
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    keyboard.row(playlists_Names[0]["playlist_Name"])
    keyboard.row(playlists_Names[1]["playlist_Name"])
    keyboard.row(playlists_Names[2]["playlist_Name"])
    keyboard.row(playlists_Names[3]["playlist_Name"])

    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["library_Helper"]["duplicates_Remover"]["playlist_Selector"], reply_markup=keyboard, parse_mode="Markdown")



def duplicates_Remover_Description(chat_id, section_Name, language_Name):
    """
    Описание функции удаления дубликатов из плейлистов

    section_Name - playlist ИЛИ liked_Songs
    """
    if section_Name == "playlist":
        message = language_Vocabluary[language_Name]["chat_Messages"]["library_Helper"]["duplicates_Remover"]["description_Playlists"]
    elif section_Name == "liked_Songs":
        message = language_Vocabluary[language_Name]["chat_Messages"]["library_Helper"]["duplicates_Remover"]["description_Library"]

    spotify_Bot.send_message(chat_id, message, parse_mode="Markdown")



def no_Playlists(chat_id, language_Name):
    """
    Нет доступных плейлистов
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["errors"]["no_Playlists"], parse_mode="Markdown")



def playlist_NotFound(chat_id, language_Name):
    """
    Плейлист не найден
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["errors"]["playlist_NotFound"], parse_mode="Markdown")



def duplicates_Not_Found(chat_id, language_Name):
    """
    Дубликаты не найдены
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["library_Helper"]["duplicates_Remover"]["duplicates_Not_Found"], parse_mode="Markdown")



def removing_Success(chat_id, language_Name):
    """
    Удаление успешно
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["library_Helper"]["duplicates_Remover"]["removing_Success"], parse_mode="Markdown")



def removing_Failure(chat_id, language_Name):
    """
    Удаление произошло с ошибками
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["library_Helper"]["duplicates_Remover"]["removing_Failure"], parse_mode="Markdown")



def removing_In_Progress(chat_id, language_Name):
    """
    Удаление в процессе
    """
    markup = telebot.types.ReplyKeyboardRemove(selective=False)
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["library_Helper"]["duplicates_Remover"]["removing_In_Progress"], reply_markup=markup, parse_mode="Markdown")



def tracks_Top(chat_id, top_Data, language_Name, message_ID=None):
    """
    Вывод топа песен пользователя
    """
    keyboard = telebot.types.InlineKeyboardMarkup()

    time_Range = top_Data["time_Range"]

    previous_Page = top_Data["current_Page"] - 1 #Индекс предыдущей страницы
    previous_Page_Button = telebot.types.InlineKeyboardButton(text=language_Vocabluary[language_Name]["keyboard_Buttons"]["inline_Buttons"]["previous_Page"], callback_data=f"interface#topTracks#page#{time_Range}#{previous_Page}")

    next_Page = top_Data["current_Page"] + 1 #Индекс следующей страницы
    next_Page_Button = telebot.types.InlineKeyboardButton(text=language_Vocabluary[language_Name]["keyboard_Buttons"]["inline_Buttons"]["next_Page"], callback_data=f"interface#topTracks#page#{time_Range}#{next_Page}")

    create_Playlist_Button = telebot.types.InlineKeyboardButton(text=language_Vocabluary[language_Name]["keyboard_Buttons"]["inline_Buttons"]["create_Playlist"], callback_data=f"interface#topTracks#createPlaylist#{time_Range}")

    keyboard.add(create_Playlist_Button) #Кнопка создания плейлиста

    if not top_Data["current_Page"] <= 1 and not top_Data["current_Page"] >= top_Data["max_Pages"]: #Херня для создания красивой клавиатуры
        keyboard.add(previous_Page_Button, next_Page_Button)
    elif not top_Data["current_Page"] <= 1:
        keyboard.add(previous_Page_Button)
    elif not top_Data["current_Page"] >= top_Data["max_Pages"]:
        keyboard.add(next_Page_Button)

    time_Range = language_Vocabluary[language_Name]["chat_Messages"]["yourTops"][time_Range]
    last_Update = datetime.utcfromtimestamp(int(top_Data["last_Update"])).strftime("%m-%d-%Y %H:%M")

    chat_Top_Data = {}
    chat_Top_Data["top_Summary"] = language_Vocabluary[language_Name]["chat_Messages"]["yourTops"]["top_Songs_Header"].format(time_Range=time_Range, previous_Page=top_Data["current_Page"], next_Page=top_Data["max_Pages"]) + "\n\n"

    chat_Top_Data["top_Summary"] += language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["last_Update"] + last_Update + "\n\n"

    for top_Item in top_Data["items"]: #Подготавливаем список песен
        prefix = top_Data["items"][top_Item]["prefix"]
        artists = top_Data["items"][top_Item]["artists"]
        name = top_Data["items"][top_Item]["name"]
        chat_Top_Data[top_Item] = f"<b>{top_Item + 1}.</b> {artists} - {name} <b>{prefix}</b>\n\n"
        chat_Top_Data["top_Summary"] += chat_Top_Data[top_Item]

    if message_ID: #Если предоставлен ID сообщения, то редактируем сообщение, если нет, отправляем новое
        spotify_Bot.edit_message_text(chat_Top_Data["top_Summary"], chat_id=chat_id, message_id=message_ID, reply_markup=keyboard, parse_mode="HTML")
    else:
        spotify_Bot.send_message(chat_id, chat_Top_Data["top_Summary"], reply_markup=keyboard, parse_mode="HTML")
