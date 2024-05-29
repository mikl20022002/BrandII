import os
import json
import telebot
from telebot.types import InputMediaPhoto, InputMediaVideo


def create_dirs():
    tg_path = ['accounts', 'tg']
    vk_path = ['accounts', 'vk']
    buffer_path = ['accounts', 'buffer']
    unify_profiles_path = ['accounts', 'profiles']

    tg_path = os.path.join(*tg_path)
    vk_path = os.path.join(*vk_path)
    buffer_path = os.path.join(*buffer_path)
    unify_profiles_path = os.path.join(*unify_profiles_path)

    os.makedirs(tg_path, exist_ok=True)
    os.makedirs(vk_path, exist_ok=True)
    os.makedirs(buffer_path, exist_ok=True)
    os.makedirs(unify_profiles_path, exist_ok=True)

    return tg_path, vk_path, buffer_path, unify_profiles_path


def create_media_group(media_list):
    media_group = []
    for media in media_list:
        media_type = list(media.keys())[0]
        file_id = media[media_type]
        if media_type == 'photo':
            media_group.append(InputMediaPhoto(media=file_id))
        elif media_type == 'video':
            media_group.append(InputMediaVideo(media=file_id))
    return media_group

# region tg json
def tg_json_add_media(user_id, channel, media_type, media_id):
    '''

    :param username: юзернейм пользователя
    :param channel: подключенный канал пользователя
    :param file_type: приемлeмые типы: Photo, Video
    :param file_address: адресс файла на серверах телеграмм. Получается через message
    :return:
    '''

    json_path = os.path.join(TG_BASE_PATH, str(user_id))
    with open(json_path, "r") as file:
        data = json.load(file)

    new_file = {
        media_type: media_id
    }
    data[channel]["media"].append(new_file)

    with open(json_path, "w") as file:
        json.dump(data, file, indent=4)


def tg_json_add_video_note(user_id, channel, video_note_id):
    json_path = os.path.join(TG_BASE_PATH, str(user_id))
    with open(json_path, "r") as file:
        data = json.load(file)

    new_file = {
        'video_note': video_note_id
    }
    data[channel]["video_note"].append(new_file)

    with open(json_path, "w") as file:
        json.dump(data, file, indent=4)

def tg_json_get_media(user_id, channel_id):
    json_path = os.path.join(TG_BASE_PATH, str(user_id))
    with open(json_path, "r") as file:
        data = json.load(file)

    media = data[channel_id]['media']
    return media

def tg_json_add_text(user_id, channel, text):
    json_path = os.path.join(TG_BASE_PATH, str(user_id))
    with open(json_path, "r") as file:
        data = json.load(file)

    data[channel]['text'] = text

    with open(json_path, "w") as file:
        json.dump(data, file, indent=4)

def tg_json_get_text(user_id, channel):
    json_path = os.path.join(TG_BASE_PATH, str(user_id))
    with open(json_path, "r") as file:
        data = json.load(file)

    text = data[channel]['text']

    return text

def tg_json_get_video_note(user_id, channel):
    json_path = os.path.join(TG_BASE_PATH, str(user_id))
    with open(json_path, "r") as file:
        data = json.load(file)

    video_note = data[channel]['video_note']

    return video_note

def tg_json_delete_media(user_id, channel):
    json_path = os.path.join(TG_BASE_PATH, str(user_id))
    with open(json_path, "r") as file:
        data = json.load(file)

    data[channel]["media"] = []

    with open(json_path, "w") as file:
        json.dump(data, file, indent=4)


def tg_json_delete_text(user_id, channel):
    json_path = os.path.join(TG_BASE_PATH, str(user_id))
    with open(json_path, "r") as file:
        data = json.load(file)

    data[channel]["text"] = None

    with open(json_path, "w") as file:
        json.dump(data, file, indent=4)

def tg_json_delete_video_note(user_id, channel):
    json_path = os.path.join(TG_BASE_PATH, str(user_id))
    with open(json_path, "r") as file:
        data = json.load(file)

    data[channel]["video_note"] = []

    with open(json_path, "w") as file:
        json.dump(data, file, indent=4)


def tg_json_add_channel(user_id, channel):
    json_path = os.path.join(TG_BASE_PATH, str(user_id))
    with open(json_path, "r") as file:
        data = json.load(file)

    data[channel] = {'text': None, 'media': [], 'video_note': []}

    with open(json_path, "w") as file:
        json.dump(data, file, indent=4)


def create_tg_json(user_id):
    tg_user_path = os.path.join(TG_BASE_PATH, str(user_id))
    with open(tg_user_path, 'w') as file:
        data = {}
        json.dump(data, file, indent=4)
# endregion


#region buffer
def create_buffer(user_id):
    buffer_path = os.path.join(BUFFER_BASE_PATH, str(user_id))
    with open(buffer_path, 'w') as file:
        data = {'text': None,
                'media':[],
                'specials':[]}
        json.dump(data, file, indent=4)

def update_buffer_text(user_id, text):
    buffer_path = os.path.join(BUFFER_BASE_PATH, str(user_id))
    with open(buffer_path, 'r') as file:
        data = json.load(file)

    data['text'] = text

    with open(buffer_path, 'w') as file:
        json.dump(data, file, indent=4)

def get_buffer_text(user_id):
    buffer_path = os.path.join(BUFFER_BASE_PATH, str(user_id))
    with open(buffer_path, 'r') as file:
        data = json.load(file)

    text = data['text']
    return text

def update_buffer_media(user_id, media_type, media_id):
    buffer_path = os.path.join(BUFFER_BASE_PATH, str(user_id))
    with open(buffer_path, 'r') as file:
        data = json.load(file)

    data['media'].append({media_type:media_id})

    with open(buffer_path, 'w') as file:
        json.dump(data, file, indent=4)

def update_buffer_specials(user_id, special_type, special_id):
    buffer_path = os.path.join(BUFFER_BASE_PATH, str(user_id))
    with open(buffer_path, 'r') as file:
        data = json.load(file)

    data['specials'].append({special_type:special_id})

    with open(buffer_path, 'w') as file:
        json.dump(data, file, indent=4)

def update_buffer_video_note(user_id, video_id):
    update_buffer_specials(user_id, 'video_note', video_id)


def update_buffer_story(user_id, video_id):
    update_buffer_specials(user_id, 'story', video_id)


def clear_buffer(user_id):
    buffer_path = os.path.join(BUFFER_BASE_PATH, str(user_id))
    with open(buffer_path, 'r') as file:
        data = json.load(file)

    data['media'] = []
    data['specials'] = []
    data['text'] = None

    with open(buffer_path, 'w') as file:
        json.dump(data, file, indent=4)

def get_buffer_media(user_id):
    buffer_path = os.path.join(BUFFER_BASE_PATH, str(user_id))
    with open(buffer_path, 'r') as file:
        data = json.load(file)

    media = data['media']
    return media

def get_buffer_special(user_id):
    buffer_path = os.path.join(BUFFER_BASE_PATH, str(user_id))
    with open(buffer_path, 'r') as file:
        data = json.load(file)

    media = data['specials']
    return media

# endregion


# region unify profiles
def create_profile_json(user_id):
    prof_path = os.path.join(PROFILES_BASE_PATH, str(user_id))
    with open(prof_path, 'w') as file:
        data = {'unify':'not',
                'name':None,
                'sex':None,
                'age':None,
                'profession':None,
                'hobbies':None,
                'hashtags':None,
                'content': None,
                'emoji':None}
        json.dump(data, file, indent=4)

def update_profile(user_id, type, text):
    prof_path = os.path.join(PROFILES_BASE_PATH, str(user_id))
    with open(prof_path, 'r') as file:
        data = json.load(file)

    data[type] = text

    with open(prof_path, 'w') as file:
        json.dump(data, file, indent=4)

def get_profile_atr(user_id, type):
    prof_path = os.path.join(PROFILES_BASE_PATH, str(user_id))
    with open(prof_path, 'r') as file:
        data = json.load(file)

    info = data[type]
    return info

def need_unify(user_id):
    unify = get_profile_atr(user_id, 'unify')
    if unify == 'ok':
        return True
    else:
        return False
#endregion


TG_BASE_PATH, VK_BASE_PATH, BUFFER_BASE_PATH, PROFILES_BASE_PATH = create_dirs()