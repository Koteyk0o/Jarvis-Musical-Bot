import time
import random
import urllib
from spotify_Module import localization
from spotify_Module import bot_Sender
from libraries import database_Manager as db_Manager
from spotify_Module import spotify_Exceptions
from spotify_Module.spotify_Logger import logger
from spotify_Module import spotify_Service



musicQuiz_User_Songs = {}
musicQuiz_User_Stats = {}



language_Vocabluary = localization.load_Vocabluary()



def to_Main_Menu(user_ID):
    """
    Return user to main menu
    """
    logger.info(f"Sending Main Menu Keyboard For User {user_ID}")
    db_Manager.write_User_Position(user_ID, "main_Menu")
    user_Language = db_Manager.get_User_Language(user_ID)
    bot_Sender.controls_Main_Menu(user_ID, language_Name=user_Language)



def process_Type_Selector_Message(user_ID, message_Text, user_Language):
    if message_Text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["liked_Songs"]:
        db_Manager.write_User_Position(user_ID, "work_In_Progress")
        bot_Sender.musicQuiz_Preparing(user_ID, language_Name=user_Language)
        create_MusicQuiz_Liked_Songs(user_ID, language_Name=user_Language)

    elif message_Text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["top_Songs"]:
        db_Manager.write_User_Position(user_ID, "user_MusicQuiz_Time")
        bot_Sender.tops_Time_Period(user_ID, language_Name=user_Language)

    elif message_Text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["back_To_Menu"]:
        to_Main_Menu(user_ID)

    else:
        bot_Sender.astray_Notification(user_ID, language_Name=user_Language)



def process_Time_Selector_Message(user_ID, message_Text, user_Language):
    if message_Text == language_Vocabluary[user_Language]["keyboard_Buttons"]["time_Buttons"]["4_Weeks"]:
        db_Manager.write_User_Position(user_ID, "work_In_Progress")
        bot_Sender.musicQuiz_Preparing(user_ID, language_Name=user_Language)
        create_MusicQuiz_Top_Tracks(user_ID, language_Name=user_Language, time_Range="short_term")

    elif message_Text == language_Vocabluary[user_Language]["keyboard_Buttons"]["time_Buttons"]["6_Months"]:
        db_Manager.write_User_Position(user_ID, "work_In_Progress")
        bot_Sender.musicQuiz_Preparing(user_ID, language_Name=user_Language)
        create_MusicQuiz_Top_Tracks(user_ID, language_Name=user_Language, time_Range="medium_term")

    elif message_Text == language_Vocabluary[user_Language]["keyboard_Buttons"]["time_Buttons"]["all_Time"]:
        db_Manager.write_User_Position(user_ID, "work_In_Progress")
        bot_Sender.musicQuiz_Preparing(user_ID, language_Name=user_Language)
        create_MusicQuiz_Top_Tracks(user_ID, language_Name=user_Language, time_Range="long_term")

    else:
        bot_Sender.astray_Notification(user_ID, language_Name=user_Language)    



def process_InGame_Message(user_ID, message_Text, user_Language):
    try:
        if message_Text == musicQuiz_User_Stats[user_ID]["round_Answer"]: #If user message = correct answer
            if (int(time.time()) - musicQuiz_User_Stats[user_ID]["round_Prepared_Timestamp"]) <= 10: #If no more than 10 seconds have passed since the creation of the round
                bot_Sender.musicQuiz_Correct_Answer(user_ID, musicQuiz_User_Stats[user_ID], language_Name=user_Language) #Count the answer
                musicQuiz_User_Stats[user_ID]["correct_Answers"] += 1
            else:
                bot_Sender.musicQuiz_Answer_Timeout(user_ID, musicQuiz_User_Stats[user_ID], language_Name=user_Language) #Otherwise, defeat

        else:
            bot_Sender.musicQuiz_Incorrect_Answer(user_ID, musicQuiz_User_Stats[user_ID], language_Name=user_Language) #Defeat if the answer is wrong



        musicQuiz_User_Stats[user_ID]["game_Round"] += 1



        if musicQuiz_User_Stats[user_ID]["game_Round"] < musicQuiz_User_Stats[user_ID]["total_Rounds"]: #While round < number of rounds, send rounds, otherwise send the end of the quiz and return to the main menu
            process_MusicQuiz_Round(user_ID, language_Name=user_Language, game_Round=musicQuiz_User_Stats[user_ID]["game_Round"])
        else:
            bot_Sender.musicQuiz_End(user_ID, musicQuiz_User_Stats[user_ID], language_Name=user_Language)
            to_Main_Menu(user_ID)

    except Exception as error:
        logger.error(f"MUSIC QUIZ ERROR WHEN PREPARING ROUND FOR USER {user_ID} ERROR: {error}")
        bot_Sender.musicQuiz_Error_RoundProcess(user_ID, language_Name=user_Language)
        to_Main_Menu(user_ID)    



def process_MusicQuiz_Round(user_ID, language_Name, game_Round):
    """
    Prepare dataset for the music quiz round

    user_ID - Telegram user ID

    game_Round - The round number of the music quiz
    """
    try:
        musicQuiz_Keyboard_Items = []
        musicQuiz_Keyboard_Items.append(musicQuiz_User_Songs[user_ID]["right_Answers"][game_Round])

        list_Size = len(musicQuiz_User_Songs[user_ID]["other_Answers"]) - 1

        key_Indexes = [] #Generation of 3 random numbers to add WRONG answers to the keyboard
        while len(key_Indexes) < 3:
            index = random.randint(10, list_Size)
            if index not in key_Indexes:
                key_Indexes.append(index)

        for index in range(3): #Adding 3 random answers to the keyboard
            answer_Item = key_Indexes[index]
            musicQuiz_Keyboard_Items.append(musicQuiz_User_Songs[user_ID]["other_Answers"][answer_Item])

        random.shuffle(musicQuiz_Keyboard_Items) #Shuffle keyboard

        audio_File = urllib.request.urlopen(musicQuiz_User_Songs[user_ID]["right_Answers"][game_Round]["audio_URL"]).read()

        musicQuiz_Round_Data = {
            "current_Round":game_Round,
            "audio_File":audio_File,
        }

        keyboard_Keys = []
        for key in range(4): #Translating keyboard data into human form
            keyboard_Keys.append(musicQuiz_Keyboard_Items[key]["artists"] + " - " + musicQuiz_Keyboard_Items[key]["name"])

        musicQuiz_Round_Data["keyboard"] = keyboard_Keys
        musicQuiz_User_Stats[user_ID].update({
            "game_Round":game_Round,
            "round_Prepared_Timestamp":int(time.time()),
            "round_Answer":musicQuiz_User_Songs[user_ID]["right_Answers"][game_Round]["artists"] + " - " + musicQuiz_User_Songs[user_ID]["right_Answers"][game_Round]["name"],
        })
        
    except:
        logger.error(f"ERROR OCCURED WHEN PROCESSING MUSIC QUIZ FOR USER {user_ID}")
        bot_Sender.musicQuiz_Error_RoundProcess(user_ID, language_Name=language_Name)
        to_Main_Menu(user_ID)

    else:
        bot_Sender.send_MusicQuiz_Round(user_ID, musicQuiz_Round_Data, language_Name=language_Name)



def create_MusicQuiz_Top_Tracks(user_ID, language_Name, time_Range):
    """
    Prepare a selection of top tracks for a music quiz

    user_ID - Telegram user ID

    time_Range - Time range to sample (short_term, medium_term, long_term)
    """
    try:
        musicQuiz_Data = spotify_Service.create_MusicQuiz_Top_Tracks(db_Manager.get_User_UniqueID(user_ID), time_Range)
        logger.info(f"Creating Top Tracks Music Quiz For User {user_ID}")

    except spotify_Exceptions.no_Tops_Data:
        bot_Sender.not_Enough_Songs(user_ID, language_Name=language_Name, songs_Count=50)
        to_Main_Menu(user_ID)

    except spotify_Exceptions.http_Error:
        bot_Sender.cannot_Authorize(user_ID, language_Name=language_Name)
        logger.error(f"HTTP ERROR OCCURED WHEN PREPARING TOP TRACKS MUSIC QUIZ FOR USER {user_ID}")
        to_Main_Menu(user_ID)

    except spotify_Exceptions.http_Connection_Error:
        bot_Sender.servers_Link_Error(user_ID, language_Name=language_Name)
        logger.error(f"CONNECTION ERROR OCCURED WHEN PREPARING TOP TRACKS MUSIC QUIZ FOR USER {user_ID}")
        to_Main_Menu(user_ID)

    except spotify_Exceptions.musicQuiz_Error_NoTracks:
        bot_Sender.musicQuiz_Error_NoTracks(user_ID, language_Name=language_Name)
        logger.error(f"MUSIC QUIZ ERROR WHEN PREPARING GAME FOR USER {user_ID}")
        to_Main_Menu(user_ID)

    except:
        bot_Sender.unknown_Error(user_ID, language_Name=language_Name)
        logger.error(f"UNKNOWN ERROR OCCURED WHEN PREPARING TOP TRACKS MUSIC QUIZ FOR USER {user_ID}")
        to_Main_Menu(user_ID)

    else:
        if not db_Manager.get_User_Position(user_ID) == "main_Menu":
            musicQuiz_User_Songs[user_ID] = musicQuiz_Data
            musicQuiz_User_Stats[user_ID] = {
                "game_Round":0,
                "round_Prepared_Timestamp":0,
                "round_Answer":"",
                "correct_Answers":0,
                "total_Rounds":10,
            }
            db_Manager.write_User_Position(user_ID, "user_MusicQuiz_inGame")
            process_MusicQuiz_Round(user_ID, language_Name=language_Name, game_Round=0)
        
        else:
            logger.error(f"MUSIC QUIZ PREPARED FOR USER {user_ID}, BUT THE USER LEFT THE GAME")



def create_MusicQuiz_Liked_Songs(user_ID, language_Name):
    """
    Prepare a selection of Liked Songs for a music quiz

    user_ID - Telegram user ID
    """
    try:
        user_Unique_ID = db_Manager.get_User_UniqueID(user_ID)
        spotify_Service.check_User_Liked_Songs(user_Unique_ID, 50)
        musicQuiz_Data = spotify_Service.create_MusicQuiz_Liked_Songs(user_Unique_ID)
        logger.info(f"Creating Liked Songs Music Quiz For User {user_ID}")

    except spotify_Exceptions.no_Tracks:
        bot_Sender.not_Enough_Songs(user_ID, language_Name=language_Name, songs_Count=50)
        to_Main_Menu(user_ID)

    except spotify_Exceptions.http_Error:
        bot_Sender.cannot_Authorize(user_ID, language_Name=language_Name)
        logger.error(f"HTTP ERROR OCCURED WHEN PREPARING LIKED SONGS MUSIC QUIZ FOR USER {user_ID}")
        to_Main_Menu(user_ID)

    except spotify_Exceptions.http_Connection_Error:
        bot_Sender.servers_Link_Error(user_ID, language_Name=language_Name)
        logger.error(f"CONNECTION ERROR OCCURED WHEN PREPARING LIKED SONGS MUSIC QUIZ FOR USER {user_ID}")
        to_Main_Menu(user_ID)

    except spotify_Exceptions.musicQuiz_Error_NoTracks:
        bot_Sender.musicQuiz_Error_NoTracks(user_ID, language_Name=language_Name)
        logger.error(f"MUSIC QUIZ ERROR WHEN PREPARING GAME FOR USER {user_ID}")
        to_Main_Menu(user_ID)

    except:
        bot_Sender.unknown_Error(user_ID, language_Name=language_Name)
        logger.error(f"UNKNOWN ERROR OCCURED WHEN PREPARING LIKED SONGS MUSIC QUIZ FOR USER {user_ID}")
        to_Main_Menu(user_ID)

    else:
        if not db_Manager.get_User_Position(user_ID) == "main_Menu":
            musicQuiz_User_Songs[user_ID] = musicQuiz_Data
            musicQuiz_User_Stats[user_ID] = {
                "game_Round":0,
                "round_Prepared_Timestamp":0,
                "round_Answer":"",
                "correct_Answers":0,
                "total_Rounds":10,
            }
            db_Manager.write_User_Position(user_ID, "user_MusicQuiz_inGame")
            process_MusicQuiz_Round(user_ID, language_Name=language_Name, game_Round=0)
        
        else:
            logger.error(f"MUSIC QUIZ PREPARED FOR USER {user_ID}, BUT THE USER LEFT THE GAME")