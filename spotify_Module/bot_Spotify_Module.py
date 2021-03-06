"""
Ребята не стоит вскрывать этот код. 
Вы молодые, шутливые, вам все легко. Это не то. Это не Stuxnet и даже не шпионские программы ЦРУ. Сюда лучше не лезть. 
Серьезно, любой из вас будет жалеть. 
Лучше закройте код и забудьте что там писалось. 
Я вполне понимаю что данным сообщением вызову дополнительный интерес, но хочу сразу предостеречь пытливых - стоп. Остальные просто не найдут.
"""

import time

from spotify_Module import localization
from spotify_Module import bot_Sender

from spotify_Module import bot_SuperShuffle
from spotify_Module import bot_LibraryTops
from spotify_Module import bot_MusicQuiz
from spotify_Module import bot_Player_Control
from spotify_Module import bot_BlockedTracks
from spotify_Module import bot_LibraryStatistics
from spotify_Module import bot_LibraryHelper

from spotify_Module.spotify_Logger import logger
from libraries import spotify_Oauth
from libraries import database_Manager as db_Manager

bot_Version = 0.5

language_Vocabluary = localization.load_Vocabluary()



def to_Main_Menu(user_ID):
    """
    Return user to main menu
    """
    logger.info(f"Sending Main Menu Keyboard For User {user_ID}")
    db_Manager.write_User_Position(user_ID, "main_Menu")
    user_Language = db_Manager.get_User_Language(user_ID)
    bot_Sender.controls_Main_Menu(user_ID, language_Name=user_Language)



def process_User_Language(language_Code):
    if language_Code == "ru" or language_Code == "uk" or language_Code == "be": #Russian, Ukrainian, Belarusian
        user_Language = "RUS"
    else:
        user_Language = "ENG"
    
    return user_Language



def logout_Command(message):
    """
    Exit command processing

    Removing a user from all tables in the database
    """
    user_ID = message.from_user.id
    if db_Manager.check_Bot_Reg(user_ID):
        logger.info(f"Preparing Logout For User {user_ID}")
        user_Unique_ID = db_Manager.get_User_UniqueID(user_ID)
        user_Language = db_Manager.get_User_Language(user_ID)
        
        db_Manager.delete_User(user_Unique_ID, "bot_Users")
        db_Manager.delete_User(user_Unique_ID, "spotify_Users")
        db_Manager.delete_User(user_Unique_ID, "users_TopTracks")
        db_Manager.delete_User(user_Unique_ID, "users_TopArtists")

        logger.info(f"Logout Successful For User {user_ID}")
        bot_Sender.user_Leaving(message.from_user.id, language_Name=user_Language)



def language_Command(message):
    """
    Language change command processing
    """
    user_ID = message.from_user.id
    if db_Manager.check_Spotify_Login(user_ID):
        logger.info(f"Sending Language Selector Keyboard For User {user_ID}")
        user_ID = message.from_user.id
        bot_Sender.language_Selector(user_ID, db_Manager.get_User_Language(user_ID))
        db_Manager.write_User_Position(user_ID, "language_Select")



def menu_Command(message):
    """
    Menu command processing

    If the user is logged in, return him to the main menu
    """
    user_ID = message.from_user.id

    if db_Manager.check_Spotify_Login(user_ID):
        to_Main_Menu(user_ID)



def contacts_Command(message):
    """
    Contact command processing

    Send developer contacts to user
    """
    user_ID = message.from_user.id

    logger.info(f"Sending Contacts For User {user_ID}")
    user_Language = db_Manager.get_User_Language(user_ID)
    bot_Sender.send_Developer_Contacts(user_ID, language_Name=user_Language)



logger.info("Spotify Module Ready")



def chat_Messages_Handler(message):
    user_ID = message.from_user.id
    logger.info(f"New Message: {message.text} From: {user_ID}")

    if not db_Manager.check_Bot_Reg(user_ID): #If the person is not in the database, then we add him Telegram to the database
        generated_Unique_ID = db_Manager.generate_Unique_ID()
        user_LanguageCode = message.from_user.language_code

        user_FirstName = message.from_user.first_name
        user_UserName = message.from_user.username
        user_LastName = message.from_user.last_name

        reg_Timestamp = int(time.time())

        logger.info(f"User {user_ID} ({user_FirstName}, {user_LastName}, {user_UserName}) Not In Reg Table. Registration...")
        db_Manager.register_User(user_ID, generated_Unique_ID, process_User_Language(user_LanguageCode), bot_Version, reg_Timestamp)



    #Optimization for DB
    user_Position_Cache = db_Manager.get_User_Position(user_ID) #Write the user position to the variable
    user_Language = db_Manager.get_User_Language(user_ID) #Write the user language to the variable



    if not db_Manager.check_Spotify_Login(user_ID): #If the user is not yet logged into Spotify, we suggest logging in
        logger.info(f"User {user_ID} Not In Spotify Table. Sending Offer For Login")
        user_Unique_ID = db_Manager.get_User_UniqueID(user_ID)
        spotify_Auth_Link = spotify_Oauth.generate_Auth_Link(user_Unique_ID)
        bot_Sender.spotify_Login_Offer(user_ID, spotify_Auth_Link, language_Name=user_Language)



    if db_Manager.check_Spotify_Login(user_ID):
        logger.info(f"User {user_ID} Have Spotify Login")


        #Checking for in_Work position
        if user_Position_Cache == "work_In_Progress":
            bot_Sender.denied_Work_Reason(user_ID, language_Name=user_Language)


        #Language change menu
        if user_Position_Cache == "language_Select":
            if message.text == language_Vocabluary[user_Language]["keyboard_Buttons"]["language"]["ENG"]:
                db_Manager.write_User_Language(user_ID, "ENG")
                bot_Sender.language_Changed(user_ID, "ENG")
                to_Main_Menu(user_ID)

            elif message.text == language_Vocabluary[user_Language]["keyboard_Buttons"]["language"]["RUS"]:
                db_Manager.write_User_Language(user_ID, "RUS")
                bot_Sender.language_Changed(user_ID, "RUS")
                to_Main_Menu(user_ID)
            
            else:
                bot_Sender.astray_Notification(user_ID, db_Manager.get_User_Language(user_ID))


        if db_Manager.get_User_BotVersion(user_ID) < bot_Version: #If the user's keyboard version is old, then move to the main menu
            to_Main_Menu(user_ID)
            bot_Sender.jarvis_Updated(user_ID, language_Name=user_Language, jarvis_Version=bot_Version)
            db_Manager.write_User_BotVersion(user_ID, bot_Version)


        #MAIN MENU


        if user_Position_Cache == "main_Menu":
            if message.text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["inline_Help"]: #Inline Help
                logger.info(f"Sending Inline Help for user {user_ID}")
                bot_Sender.inline_Mode_Help(user_ID, language_Name=user_Language)

            elif message.text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["super_Shuffle"]: #Super-Shuffle
                logger.info(f"User {user_ID} Entered To Super Shuffle")
                db_Manager.write_User_Position(user_ID, "user_SuperShuffle")
                bot_Sender.superShuffle_Description(user_ID, language_Name=user_Language)
                bot_Sender.shuffle_Tracks_Count(user_ID, language_Name=user_Language)
                logger.info(f"Sending Super Shuffle Selector For User {user_ID}")

            elif message.text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["your_Tops"]: #Your Tops
                logger.info(f"User {user_ID} Entered To Your Tops")
                db_Manager.write_User_Position(user_ID, "user_YourTops")
                bot_Sender.yourTops_Description(user_ID, language_Name=user_Language)
                bot_Sender.tops_Type_Select(user_ID, language_Name=user_Language)
                logger.info(f"Sending Your Tops Selector For User {user_ID}")
            
            elif message.text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["musicQuiz"]: #Music Quiz
                logger.info(f"User {user_ID} Entered To Music Quiz")
                db_Manager.write_User_Position(user_ID, "user_MusicQuiz_Type")
                bot_Sender.musicQuiz_Rules(user_ID, language_Name=user_Language)
                bot_Sender.musicQuiz_Type_Select(user_ID, language_Name=user_Language)
                logger.info(f"Sending Music Quiz Type Selector For User {user_ID}")

            elif message.text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["blocked_Tracks"]: #Blocked Tracks
                logger.info(f"User {user_ID} Entered To Blocked Tracks")
                db_Manager.write_User_Position(user_ID, "user_BlockedTracks")
                bot_Sender.blocked_Tracks_Description(user_ID, language_Name=user_Language)
                bot_BlockedTracks.send_BlockedTracks(user_ID, language_Name=user_Language)
            
            elif message.text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["library_Statistics"]: #Library Statistics
                logger.info(f"User {user_ID} Entered To Library Statistics")
                db_Manager.write_User_Position(user_ID, "user_LibraryStatistics_Type")
                bot_Sender.library_Statistics_Description(user_ID, language_Name=user_Language)
                bot_Sender.library_Statistics_Type(user_ID, language_Name=user_Language)
                logger.info(f"Sending Statistics Type Selector For User {user_ID}")

            elif message.text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["library_Helper"]: #Library Helper
                logger.info(f"User {user_ID} Entered To Library Helper")
                db_Manager.write_User_Position(user_ID, "user_LibraryHelper_Menu")
                bot_Sender.send_LibraryHelper_Menu(user_ID, language_Name=user_Language)
                logger.info(f"Sending Library Helper Selector For User {user_ID}")

            else:
                if message.content_type == "photo": #СПАСИБО КИРЮШЕ ЗА ПАСХАЛКУ
                    bot_Sender.send_Easter_Egg(user_ID, language_Vocabluary[user_Language]["chat_Messages"]["easter_Eggs"]["britt_Robertson"])
                
                else:
                    message_Text = message.text.lower()
                
                    if message_Text == "42":
                        bot_Sender.send_Easter_Egg(user_ID, language_Vocabluary[user_Language]["chat_Messages"]["easter_Eggs"]["42"])
                        bot_Player_Control.start_Playback("track", "7qXddTDsEuxInJ8jzX1D9a", user_ID=user_ID, user_Language=user_Language)

                    elif message_Text == "tears in rain":
                        bot_Sender.send_Easter_Egg(user_ID, language_Vocabluary[user_Language]["chat_Messages"]["easter_Eggs"]["blade_Runner"])
                        bot_Player_Control.start_Playback("track", "2LxEIWrZkzfc55c3rk05DH", user_ID=user_ID, user_Language=user_Language)

                    elif message_Text == "grogu":
                        bot_Player_Control.start_Playback("track", "0PqdMQecGbrFd2c35l4ROS", user_ID=user_ID, user_Language=user_Language)

                    elif message_Text == "the oa":
                        bot_Player_Control.start_Playback("track", "0wokCRaKD0zPNhMRXAgVsr", user_ID=user_ID, user_Language=user_Language)                                        

                    else:
                        bot_Sender.astray_Notification(user_ID, language_Name=user_Language)


        #SUPER-SHUFFLE


        if user_Position_Cache == "user_SuperShuffle":
            bot_SuperShuffle.process_SuperShuffle_Message(user_ID, message_Text=message.text, user_Language=user_Language)


        #YOUR TOPS

        if user_Position_Cache == "user_YourTops":
            bot_LibraryTops.process_Type_Selector_Message(user_ID, message_Text=message.text, user_Language=user_Language)

        if user_Position_Cache == "user_TopTracks_Time":
            bot_LibraryTops.process_TopSongs_Time_Selector_Message(user_ID, message_Text=message.text, user_Language=user_Language)

        if user_Position_Cache == "user_TopArtists_Time":
            bot_LibraryTops.process_TopArtists_Time_Selector_Message(user_ID, message_Text=message.text, user_Language=user_Language)


        #MUSIC QUIZ


        if user_Position_Cache == "user_MusicQuiz_Type":
            bot_MusicQuiz.process_Type_Selector_Message(user_ID, message_Text=message.text, user_Language=user_Language)

        if user_Position_Cache == "user_MusicQuiz_Time":
            bot_MusicQuiz.process_Time_Selector_Message(user_ID, message_Text=message.text, user_Language=user_Language)
        
        if user_Position_Cache == "user_MusicQuiz_inGame":
            bot_MusicQuiz.process_InGame_Message(user_ID, message_Text=message.text, user_Language=user_Language)


        #LIBRARY STATISTICS


        if user_Position_Cache == "user_LibraryStatistics_Type":
            bot_LibraryStatistics.process_Type_Selector_Message(user_ID, message_Text=message.text, user_Language=user_Language)


        #LIBRARY HELPER


        if user_Position_Cache == "user_LibraryHelper_Menu":
            bot_LibraryHelper.process_Type_Selector_Message(user_ID, message_Text=message.text, user_Language=user_Language)
        
        if user_Position_Cache == "user_PlaylistDuplicates_SelectPlaylist":
            bot_LibraryHelper.analyze_Playlist(user_ID, user_Language=user_Language, playlist_Name=message.text)
        
        if user_Position_Cache == "user_PlaylistDuplicates_MakeChoice":
            bot_LibraryHelper.process_Removing_Choice(user_ID, user_Language=user_Language, message_Text=message.text, tracks_Section="playlist")

        if user_Position_Cache == "user_LikedSongsDuplicates_MakeChoice":
            bot_LibraryHelper.process_Removing_Choice(user_ID, user_Language=user_Language, message_Text=message.text, tracks_Section="likedSongs")
