from telebot import types, TeleBot
from messages import *
from database import *
from lm_connection import *
import re
from backend import *


# region мудрости написания ботов

# Если bot.register_next_step_handler() не стоит последней строкой в функции, вызвать return что бы дальнейший код не выполнялся.


# endregion

bot_token = '5851142761:AAGuCbwSsDkWmbX77-ZQ91hKwv15QiD-RJ0'
bot = TeleBot(bot_token)

bot_commands = [
    telebot.types.BotCommand('start', 'старт')  # Создаём кнопку "Меню"
]

bot.set_my_commands(bot_commands)

# region sending text\files to user
def text_to_user(chat_id: int, text: str, reply_markup=None) -> None:
    bot.send_message(chat_id, text, reply_markup=reply_markup, parse_mode=None)


def photo_to_user(chat_id: int, path: str) -> None:
    with open(path, "rb") as photo:
        bot.send_photo(chat_id, photo)


def file_to_user(chat_id: int, path: str) -> None:
    with open(path, "rb") as file:
        bot.send_photo(chat_id, file)


def text_to_channel(channel_id, text):
    text = text.replace('*', '')
    text = text.replace('#', '')

    bot.send_message(chat_id=channel_id, text=text, parse_mode='html')


def media_to_channel(channel_id, media):
    bot.send_media_group(channel_id, media)

# endregion

# region tg registration

def connect_tg_channel(message):
    '''
    Подключает тг канал пользователя к боту если выполнены все условия.

    :param message: message.text должен содержать ссылку на подключаемый канал юзера.
    :return: None
    '''

    if func_check(message):
        return

    channel_link = message.text

    # Проверяем, является ли ссылка корректной ссылкой на канал Telegram
    if re.match(r'https?://t\.me/', channel_link):
        channel_id = '@' + channel_link.split("/")[-1]

    else:
        text_to_user(message.chat.id, GET_TG_CHANNEL_ID_DENY)
        bot.register_next_step_handler(message, connect_tg_channel)
        return

    #Проверяем права бота в чате, если админ то норм
    if channel_id is not None and check_tg_channel_admin_rules(channel_id):

        #проверяем был ли подключен канал ранее
        if channel_id in get_tg_channel_list(message.chat.id):
            text_to_user(message.chat.id, TG_CHANNEL_DUPLICATE_CONNECT_DENY)
        else:
            set_tg_channel_list(channel_id, message.chat.id)
            tg_json_add_channel(message.chat.id, channel_id)
            # query = 'UPDATE users_accounts SET tg_account = ? WHERE user_id = ?'
            # c.execute(query, (channel_id, message.chat.id))
            # conn.commit()

            text_to_user(message.chat.id, TG_CHANNEL_CONNECT_OK)
            my_tg_accounts(message)

    else:
        text_to_user(message.chat.id, TG_CHANNEL_CONNECT_DENY)
        bot.register_next_step_handler(message, connect_tg_channel)
        return


def check_tg_channel_admin_rules(channel_id):
    '''
    Проверяет наличие у бота прав админа в канале.

    :param channel_id: id канала, полученный через def get_tg_id
    :return:
    '''
    bot_info = bot.get_me()
    bot_member_status = bot.get_chat_member(chat_id=channel_id, user_id=bot_info.id).status

    if bot_member_status in ['administrator', 'creator']:
        return True
    else:
        return False

def look_tg_channel(message):
    if is_tg_connected(message):
        tg_channels_lst = get_tg_channel_list(message.chat.id)
        tg_channels_str = '\n'.join(tg_channels_lst)
        text_to_user(message.chat.id, LOOK_TG_CHANNEL_OK + tg_channels_str)

    else:
        text_to_user(message.chat.id, LOOK_TG_CHANNEL_DENY)

# endregion

# region useful func
def create_multikeyboard(button_list:list[dict]):
    '''
    Создает объект клавиатуры с требуемым количеством, названиями,
    callback-ами кнопок.

    :param button_list: список словарей формата:
    [
       {'text':'текст кнопки1', 'callback':'текст callback кнопки 1'},
       {'text':'текст кнопки2', 'callback':'текст callback кнопки 2'}
    ]

    :return: InLineKeyboardMarkup, передается в text_to_user
     что бы добавить кнопки в сообщении
    '''
    keyboard = types.InlineKeyboardMarkup()

    for button_data in button_list:
        text = button_data.get('text')
        callback_data = button_data.get('callback')

        button = types.InlineKeyboardButton(text, callback_data=callback_data)
        keyboard.add(button)

    return keyboard

def func_check(message):
    if message.text == None:
        return False

    if message.text.startswith('/'):
        message_handler(message)
        return True

    else:
        return False

# endregion

# region registration of new user

def start(message):
    '''
    Отправляет юзеру сообщение с приветсвием.
    Проверяет есть ли он в базе:
        Нет - заносит
        Есть - не меняет базу, перенаправляет на основной функционал, пропуская регистрацию

    :param message: передается автоматически
    :return: None
    '''

    user_not_registered = True if get_user_row(message.chat.id, 'tech_info') is None else False

    if user_not_registered:
        user = message.from_user
        data = (user.id,
                user.username,
                user.first_name,
                user.last_name,
                user.language_code)

        text_to_user(message.chat.id, START_MESSAGE)

        insert_account_info(data)

        create_tg_json(message.chat.id)
        create_buffer(message.chat.id)
        update_editing_status(message.chat.id, 0)

    user_tech_info = get_user_row(message.chat.id, 'tech_info')

    if user_tech_info[2] == 0:
        registration_name(message)
    else:
        main_menu(message)



def registration_name(message):
    text_to_user(message.chat.id, REGISTRATION_NAME_MESSAGE)
    bot.register_next_step_handler(message, registration_finished)
#на данный момент перенаправление сразу на registration_finished

def name_check(message):
    if func_check(message):
        return

    name_pattern = r'^[а-яёА-ЯЁa-zA-Z]+(\s[а-яёА-ЯЁa-zA-Z]+){2,}$'
    name = message.text
    if re.match(name_pattern, name):
        registration_email(message)
    else:
        text_to_user(message.chat.id, NAME_DENY)
        bot.register_next_step_handler(message, name_check)


def registration_email(message):
    if func_check(message):
        return

    text_to_user(message.chat.id, REGISTRATION_EMAIL_MASSAGE)

    #заносим фамилию в базу
    query = 'UPDATE users_info SET user_fio = ? WHERE user_id = ?'
    c.execute(query, (message.text, message.chat.id))
    conn.commit()

    bot.register_next_step_handler(message, email_check)


def email_check(message):
    if func_check(message):
        return

    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    user_email = message.text
    if re.match(email_pattern, user_email):

        #заносим емайл в базу
        query = 'UPDATE users_info SET user_email = ? WHERE user_id = ?'
        c.execute(query, (message.text, message.chat.id))
        conn.commit()

        registration_finished(message)
    else:
        text_to_user(message.chat.id, EMAIL_DENY)
        bot.register_next_step_handler(message, email_check)


def registration_finished(message):
    text_to_user(message.chat.id, REGISTRATION_FINISH_MESSAGE)

    #отмечаем прохождение регистрации в базе
    query = 'UPDATE tech_info SET registration_finished = ? WHERE user_id = ?'
    c.execute(query, (1, message.chat.id))
    conn.commit()

    service_presentation(message)
# endregion

# region main menu

def service_presentation(message):
    text_to_user(message.chat.id, SERVICE_PRESENTATION_MESSAGE)
    with open(r'brendII_video.mp4', 'rb') as file:
        #делаем кнопку
        markup = types.InlineKeyboardMarkup(row_width=1)
        b1 = types.InlineKeyboardButton("Ознакомился", callback_data='got_acquainted')
        markup.add(b1)
        #посылаем ознакомительноые видео вместе с кнопкой
        bot.send_video(message.chat.id, video=file, reply_markup=markup)


def main_menu(message):

    markup = types.InlineKeyboardMarkup(row_width=1)
    b1 = types.InlineKeyboardButton("Мои аккаунты", callback_data='my_accounts')
    b2 = types.InlineKeyboardButton("Создать пост", callback_data='create_post_main_menu')
    b3 = types.InlineKeyboardButton("Создать сторис", callback_data='create_story_main_menu')

    # b4 = types.InlineKeyboardButton("Подготовить записи", callback_data='prepare_post')
    b5 = types.InlineKeyboardButton('Разослать записи', callback_data='sending_posts_check')
    markup.add(b1, b2, b3, b5)

    text_to_user(message.chat.id, MAIN_MENU_MESSAGE, reply_markup=markup)

def all_prepare_post(message):
    tg_prepare_post(message)
    #(на будущее) подготовка для вк и инсты должна начинатся отсюда


# region set post text
def create_post_main_menu(message):

    markup = types.InlineKeyboardMarkup(row_width=1)
    b1 = types.InlineKeyboardButton("Задать текст", callback_data='set_post_text')
    b2 = types.InlineKeyboardButton("Задать медиа", callback_data='set_post_photo_video')
    back_b = types.InlineKeyboardButton("◀ Назад", callback_data='back_to_main_menu')
    markup.add(b1, b2, back_b)

    text_to_user(message.chat.id, CREATE_POST_MAIN_MENU, reply_markup=markup)

def set_post_text(message):
    update_editing_status(message.chat.id, 0)

    markup = types.InlineKeyboardMarkup(row_width=1)
    b1 = types.InlineKeyboardButton("Добавить свой текст", callback_data='add_user_post_text_step1')
    b2 = types.InlineKeyboardButton("Сгенерировать текст", callback_data='generate_post_text_step1')
    back_b = types.InlineKeyboardButton("◀ Назад", callback_data='create_post_main_menu')
    markup.add(b1, b2, back_b)

    text_to_user(message.chat.id, GENERATE_POST_MESSAGE, reply_markup=markup)

def add_user_post_text_step1(message):
    update_editing_status(message.chat.id, 1)

    markup = types.InlineKeyboardMarkup(row_width=1)
    back_b = types.InlineKeyboardButton("◀ Назад", callback_data='back_to_create_post')
    markup.add(back_b)

    text_to_user(message.chat.id, ADD_USER_POST_TEXT, reply_markup=markup)
    bot.register_next_step_handler(message, add_user_post_text_step2)

def add_user_post_text_step2(message):
    if func_check(message):
        return

    if is_editing_allowed(message.chat.id):
        update_buffer_text(message.chat.id, message.text)
        update_editing_status(message.chat.id, 0)
        main_menu(message)

def generate_post_text_step1(message):
    update_editing_status(message.chat.id, 1)

    markup = types.InlineKeyboardMarkup(row_width=1)
    back_b = types.InlineKeyboardButton("◀ Назад", callback_data='back_to_create_post')
    markup.add(back_b)

    text_to_user(message.chat.id, GENERATE_POST_TEXT, reply_markup=markup)
    bot.register_next_step_handler(message, generate_post_text_step2)

def generate_post_text_step2(message):
    if func_check(message):
        return

    if is_editing_allowed(message.chat.id):
        text_to_user(message.chat.id, POST_GENERATING_WAIT)

        print('Editing allowed: ', is_editing_allowed(message.chat.id))
        gen_text = ask_gpt(WRITE_A_BLOG_SYS_PROMPT + message.text)

        text_to_user(message.chat.id, gen_text)

        update_buffer_text(message.chat.id, gen_text)
        update_editing_status(message.chat.id, 0)

        text_to_user(message.chat.id, BUFFER_TEXT_WAS_UPDATED)
        main_menu(message)
# endregion


#region set post media
def set_post_media(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    b1 = types.InlineKeyboardButton("Добавить фото", callback_data='add_post_photo')
    b2 = types.InlineKeyboardButton("Добавить видео", callback_data='add_post_video')
    back_b =  types.InlineKeyboardButton("◀ Назад", callback_data='back_from_set_media')
    markup.add(b1, b2, back_b)

    text_to_user(message.chat.id, SET_POST_MEDIA, reply_markup=markup)

def add_post_photo_step1(message):
    text_to_user(message.chat.id, ADD_POST_PHOTO)
    bot.register_next_step_handler(message, add_post_photo_step2)


def add_post_photo_step2(message):
    file_id = message.photo[-1].file_id
    update_buffer_media(message.chat.id, 'photo', file_id)
    text_to_user(message.chat.id, PHOTO_ADDED)
    set_post_media(message)

def add_post_video_step1(message):
    text_to_user(message.chat.id, ADD_POST_VIDEO)
    bot.register_next_step_handler(message, add_post_video_step2)


def add_post_video_step2(message):
    file_id = message.video.file_id
    update_buffer_media(message.chat.id, 'video', file_id)
    text_to_user(message.chat.id, VIDEO_ADDED)
    set_post_media(message)

#endregion


#region create story
def create_story_main_menu_step1(message):
    text_to_user(message.chat.id, CREATE_STORY_MAIN_MENU)
    bot.register_next_step_handler(message, create_story_main_menu_step2)

def create_story_main_menu_step2(message):
    if func_check(message):
        return

    if message.content_type == 'video_note':
        print(message)
        file_id = message.video_note.file_id
        update_buffer_video_note(message.chat.id, file_id)
        main_menu(message)

#endregion


#region tg prepare

def tg_prepare_post(message) -> None:
    """
    Запускает цикл подготовки постов для всех подключенных каналов пользователя.

    :param message:
    :return:
    """
    user_id = message.chat.id
    tg_channels = get_tg_channel_list(user_id)

    text_to_user(message.chat.id, TG_PREPARE_POST)

    for i, channel_id in enumerate(tg_channels):
        tg_prepare_channel(channel_id, user_id, i)

    # text_to_user(message.chat.id, TG_PREPARE_POST_FINISH)
    # send_out_posts(message)
    clear_buffer(user_id)
    return

def tg_prepare_channel(channel_id, user_id, prompt_num) -> None:
    """
    Берет основной текст из буфера, переписывает его под отдельный канал новыми словами
    и сохраняет его в json файл этого канала.
    (Текст для поста будет взят оттуда при постинге в каналы)

    :param channel_id: идентификатор канала
    :param user_id: идентификатор пользователя
    :param prompt_num: номер используемого промпта для редактирования текста
    (необходимо для большего различия между постами)
    """

    #подготовка текста
    text = get_buffer_text(user_id)
    raw_media = get_buffer_media(user_id)
    raw_special = get_buffer_special(user_id)

    if text is not None:
        #(устарело) обрабатывает весь текст за раз
        # modified_text = ask_gpt(CHANGE_TEXT_SYS_PROMPT_1[prompt_num] + text + CHANGE_TEXT_SYS_PROMPT_2)
        # tg_json_add_text(user_id, channel_id, modified_text)

        #(эксперементальное) дробит текст на параграфы и переписывает каждый параграф отдельно затем объединяет.
        text = change_text(text, prompt_num)
        tg_json_add_text(user_id, channel_id, text)

    #Подготовка медиа. Пока все просто добавляется к файлам.
    #(на будущее) можно будет выполнять разные доп подготовки в зависимости от типа файла

    if raw_media is not None:
        for media in raw_media:
            media_type = list(media.keys())[0]
            if media_type == 'photo':
                tg_json_add_media(user_id, channel_id, media_type, media[media_type])

            elif media_type == 'video':
                tg_json_add_media(user_id, channel_id, media_type, media[media_type])

    if raw_special is not None:
        for special in raw_special:
            special_type = list(special.keys())[0]
            if special_type == 'video_note':
                tg_json_add_video_note(user_id, channel_id, special[special_type])

def change_text(text, prompt_num):
    old_parag = text_to_paragraphs(text)
    new_parag = []

    for parag in old_parag:
        modified_parag = ask_gpt(CHANGE_TEXT_SYS_PROMPT_1[prompt_num] + parag + CHANGE_TEXT_SYS_PROMPT_2)
        new_parag.append(modified_parag)

    text = '\n\n'.join(new_parag)
    text = ask_gpt(CHANGE_TEXT_SYS_PROMPT_3[prompt_num] + text)

    # проверка целесообразности первого абзаца
    paragraphs = text_to_paragraphs(text)
    print('paragraphs: ', paragraphs)
    print('дробим на слова: ', paragraphs[0].strip().split())
    first_parag_len = len(paragraphs[0].strip().split())
    if first_parag_len <= 10:
        print('______deliting first parag______')
        paragraphs = paragraphs[1:]
    text = '\n\n'.join(paragraphs)

    return text

def text_to_paragraphs(text:str) -> list:
    parag = text.split('\n')
    parag = [p for p in parag if p.strip()]
    return parag

def is_content_exists(user_id):
    text = get_buffer_text(user_id)
    raw_media = get_buffer_media(user_id)
    raw_special = get_buffer_special(user_id)
    if text is None and len(raw_media) == 0 and len(raw_special) == 0:
        return False
    return True
#endregion


# region send out posts
def sending_posts_check(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    b1 = types.InlineKeyboardButton('Разослать', callback_data='sending_posts')
    markup.add(b1)

    text_to_user(message.chat.id, SENDING_POSTS_CHECK, reply_markup=markup)


def send_out_posts(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    b1 = types.InlineKeyboardButton('Разослать', callback_data='sending_posts')
    markup.add(b1)

    text_to_user(message.chat.id, SEND_OUT_POSTS, reply_markup=markup)

def sending_posts(message):
    if is_content_exists(message.chat.id):
        tg_prepare_post(message)
    else:
        text_to_user(message.chat.id, NO_CONTENT_FOR_POST)
        return main_menu(message)

    user_id = message.chat.id
    tg_channels = get_tg_channel_list(user_id)

    for channel_id in tg_channels:
        print('sending posts to: ', channel_id)
        #посылаем текст
        text = tg_json_get_text(user_id, channel_id)
        if text is not None:
            text_to_channel(channel_id, text)

        #посылаем файлы
        raw_media = tg_json_get_media(user_id, channel_id)
        if len(raw_media) != 0:
            media_files = create_media_group(raw_media)
            media_to_channel(channel_id, media_files)

        raw_video_note = tg_json_get_video_note(user_id, channel_id)
        if len(raw_video_note) != 0:
            for vn in raw_video_note:
                #TODO: разобраться как добавить видео
                bot.send_video_note(channel_id, vn['video_note'])


        #чистим json тг канала
        tg_json_delete_media(user_id, channel_id)
        tg_json_delete_text(user_id, channel_id)
        tg_json_delete_video_note(user_id, channel_id)

    text_to_user(message.chat.id, POST_WAS_SENT)
    main_menu(message)
# endregion


# region accounts info
def my_accounts(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    b1 = types.InlineKeyboardButton("Телеграмм", callback_data='my_tg_accounts')
    b2 = types.InlineKeyboardButton("Вконтакте", callback_data='my_vk_accounts')
    b3 = types.InlineKeyboardButton("Инстаграмм", callback_data='my_inst_accounts')
    back_b = types.InlineKeyboardButton("◀ Назад", callback_data='back_to_main_menu')
    markup.add(b1, b2, b3, back_b)

    text_to_user(message.chat.id, MY_ACCOUNTS_MESSAGE, reply_markup=markup)

def my_tg_accounts(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    b1 = types.InlineKeyboardButton("Подключить аккаунт", callback_data='connect_tg_channel')
    b2 = types.InlineKeyboardButton("Посмотреть аккаунты", callback_data='look_tg_channel')
    back_b = types.InlineKeyboardButton("◀ Назад", callback_data='back_to_my_accounts')
    markup.add(b1, b2, back_b)

    text_to_user(message.chat.id, MY_TG_ACCOUNTS_MESSAGE, reply_markup=markup)

def my_vk_accounts(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    b1 = types.InlineKeyboardButton("Подключить аккаунт", callback_data='connect_vk_channel')
    b2 = types.InlineKeyboardButton("Посмотреть аккаунты", callback_data='look_vk_channel')
    back_b = types.InlineKeyboardButton("◀ Назад", callback_data='back_to_my_accounts')
    markup.add(b1, b2, back_b)

    text_to_user(message.chat.id, MY_TG_ACCOUNTS_MESSAGE, reply_markup=markup)

def my_inst_accounts(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    b1 = types.InlineKeyboardButton("Подключить аккаунт", callback_data='connect_inst_channel')
    b2 = types.InlineKeyboardButton("Посмотреть аккаунты", callback_data='look_inst_channel')
    back_b = types.InlineKeyboardButton("◀ Назад", callback_data='back_to_my_accounts')
    markup.add(b1, b2, back_b)

    text_to_user(message.chat.id, MY_TG_ACCOUNTS_MESSAGE, reply_markup=markup)
# endregion

# endregion


# region posts processing
def is_tg_connected(message):
    tg_accounts = get_tg_channel_list(message.chat.id)

    if len(tg_accounts) == 0:
        return False
    else:
        return True

#endregion


# region message handlers
@bot.message_handler(content_types=['text'])
def message_handler(message):
    if message.text.startswith('/'):

        command = message.text

        if command == '/start':
            start(message)

        elif command == '/menu':
            user_registered = False if get_user_row(message.chat.id, 'tech_info') is None else True

            if user_registered:
                user_tech_info = get_user_row(message.chat.id, 'tech_info')
                if user_tech_info[2] == 1:
                    main_menu(message)
                else:
                    text_to_user(message.chat.id, MENU_COMMAND_DENY)
            else:
                text_to_user(message.chat.id, MENU_COMMAND_DENY)

        elif command == '/tg_connect':
            text_to_user(message.chat.id, TG_CONNECT_STEP1)
            bot.register_next_step_handler(message, connect_tg_channel)

# endregion


# region callback handlers
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    bot.answer_callback_query(call.id)

    if call.data == 'my_accounts':
        my_accounts(call.message)

    elif call.data == 'set_post_text':
        set_post_text(call.message)

    elif call.data == 'my_tg_accounts':
        my_tg_accounts(call.message)

    elif call.data == 'connect_tg_channel':
        text_to_user(call.message.chat.id, TG_CONNECT_FROM_MAIN_MENU)
        bot.register_next_step_handler(call.message, connect_tg_channel)

    elif call.data == 'look_tg_channel':
        look_tg_channel(call.message)

    elif call.data == 'back_to_main_menu':
        main_menu(call.message)

    elif call.data == 'back_to_create_post_main_menu':
        create_post_main_menu(call.message)

    elif call.data == 'back_to_my_accounts':
        my_accounts(call.message)

    elif call.data == 'add_user_post_text_step1':
        add_user_post_text_step1(call.message)

    elif call.data == 'generate_post_text_step1':
        generate_post_text_step1(call.message)

    elif call.data == 'back_to_create_post':
        set_post_text(call.message)

    elif call.data == 'set_post_photo_video':
        set_post_media(call.message)

    elif call.data == 'prepare_post':
        all_prepare_post(call.message)

    elif call.data == 'sending_posts':
        sending_posts(call.message)

    elif call.data == 'add_post_photo':
        add_post_photo_step1(call.message)

    elif call.data == 'add_post_video':
        add_post_video_step1(call.message)

    elif call.data == 'back_from_set_media':
        main_menu(call.message)

    elif call.data == 'sending_posts_check':
        sending_posts_check(call.message)

    elif call.data == 'got_acquainted':
        main_menu(call.message)

    elif call.data == 'my_vk_accounts':
        my_vk_accounts(call.message)

    elif call.data == 'my_inst_accounts':
        my_inst_accounts(call.message)

    elif call.data == 'create_post_main_menu':
        create_post_main_menu(call.message)

    elif call.data == 'create_story_main_menu':
        create_story_main_menu_step1(call.message)
# endregion

bot.infinity_polling()
