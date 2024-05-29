#обычные сообщения
START_MESSAGE = '(Текст приветствия. Упоминание дальнейшей регистрации.)'
REGISTRATION_NAME_MESSAGE = 'Привет, как тебя зовут?'
REGISTRATION_EMAIL_MASSAGE = 'Введите вашу почту'
REGISTRATION_FINISH_MESSAGE = 'Спасибо, регистрация окончена'
SERVICE_PRESENTATION_MESSAGE = '(Текст для ознакомления с сервисом.)'
MAIN_MENU_MESSAGE = 'Вы находитесь в главном меню. (кнопки с функционалом)'
TG_ACCOUNT_NOT_CONNECTED = 'Вы не привязали ни одного канала теллеграмм.\n Для привязки напишите "/tg_connect"'
GENERATION_WAITING_MESSAGE = 'Обрабатываем ваш запрос. Время ожидания может составить до двух минут.'
PROCESS_GENERATED_POST_QUE = 'Вы хотите отредактировать данный текст или запостить без изменений?'
GENERATE_POST_MESSAGE = 'Какой тип текста создать?'
MY_ACCOUNTS_MESSAGE = 'Посмотреть аккаунты:'
MY_TG_ACCOUNTS_MESSAGE = 'Выберите действие'
TG_CONNECT_FROM_MAIN_MENU = 'Отправьте ссылку на канал'
ADD_USER_POST_TEXT = 'Пришлите текст поста'
GENERATE_POST_TEXT = 'На какую тему сгенерировать пост?'
BUFFER_TEXT_WAS_UPDATED = 'Базовый текст поста был обновлен'
TG_PREPARE_POST = 'Идет подготовка постов для каналов, пожалуйста подождите'
TG_PREPARE_POST_FINISH = 'Подготовка завершена, вы можете разослать посты сейчас или сделать это позднее'
SEND_OUT_POSTS = 'Разослать посты?'
POST_GENERATING_WAIT = 'Текст генерируется, пожалуйста подождите.'
SET_POST_PHOTO_VIDEO = 'Пришлите фото/видео одним сообщением так, как вы хотите видеть их в каналах.'
SET_POST_MEDIA = 'Выберите тип'
ADD_POST_PHOTO = 'Пришлите фото'
ADD_POST_VIDEO = 'Пришлите видео'
PHOTO_ADDED = 'Фото добавлено'
VIDEO_ADDED = 'Видео добавлено'
SENDING_POSTS_CHECK = 'Подтвердите рассылку'
NO_CONTENT_FOR_POST = 'Вы не добавили наполнения поста'
POST_WAS_SENT = 'Посты разосланы.'
CREATE_POST_MAIN_MENU = 'Выберите опцию'
CREATE_STORY_MAIN_MENU = 'Пришлите видео для сторис (кружка)'

#сообщения подтверждения
TG_CHANNEL_CONNECT_OK = 'Канал успешно подключен'
TG_POST_SENT_OK = 'Сообщение успешно отправлено в канал'
LOOK_TG_CHANNEL_OK = 'Список подключенных каналов: \n'


#сообщения ведущие по пути
TG_CONNECT_STEP1 = '''Что бы наш бот мог взаимодейстовать с вашим каналом, добавьте его в администраторы. (инструкция)\nПосле добавления пришлите ссылку на ваш канал.'''
TG_CONNECT_STEP2 = 'Пришлите ссылку на канал, в котором вы назначили бота администратором (инструкция)'
TG_POST_STEP1 = 'Пришлите сообщение которое хотите отправить'
WRITE_A_BLOG_STEP1 = 'На какую тему подготовить текст?'
GIVE_IDEAS_STEP1 = 'На какую тему вам нужны идеи?'
CREATE_A_PLAN_STEP1 = 'На какую тему подготовить план?'
TAKE_EDITED_POST_STEP1 = 'Скопируйте и отредактируйте текст по вашему желанию, после чего отправьте нам.'

#сообщения отклонения
NAME_DENY = 'Похоже ваше ФИО указано некорректно или содержит специальные символы. Введите еще раз.'
TG_CHANNEL_CONNECT_DENY = 'Похоже вы забыли добавить нашего бота в администраторы.\n Добавьте бота в администраторы и пришлите ссылку еще раз.'
GET_TG_CHANNEL_ID_DENY = 'Похоже вы отправили неисправную ссылку. Проверьте правильность выбранной ссылки и отправьте ее еще раз.'
EMAIL_DENY = 'Проверьте написание почты, похоже она введена неверно'
MESSAGE_HANDLER_DENY = 'Такой команды не существует'
MENU_COMMAND_DENY = 'Вы не имеете доступа к функционалу так как не прошли регистрацию'
TG_POST_SENT_DENY = 'Кажется возникли проблемы с доставкой вашего сообщения. Попробуйте позднее.'
LOOK_TG_CHANNEL_DENY = 'Вы не подключили ни одного канала'
TG_CHANNEL_DUPLICATE_CONNECT_DENY = 'Этот канал уже был подключен ранее'

#промпты
WRITE_A_BLOG_SYS_PROMPT = '''Напиши пост на данную далее тему размером до 200 слов. 
                             Пост не должен состоять только из пунктов, он также должен содержать непрерывные абзацы.
                             Не используй курсив или жирный шрифт.
                             Не используй выделение глав решетками #.
                             Нельзя писать подобные высказывания: "Надеюсь это вам поможет, буду рад ответить на вопросы".
                             Тема: '''

GIVE_IDEAS_SYS_PROMPT = '''Придумай около 7 идей на данную тему.
                           Не используй курсив или жирный шрифт.
                           Не используй выделение глав решетками #.
                           Нельзя писать подобные высказывания: "Надеюсь это вам поможет, буду рад ответить на вопросы".
                           Тема: '''

CREATE_A_PLAN_SYS_PROMPT = '''Подготовь четкий, структурированный план на данную далее тему.
                              Не используй курсив или жирный шрифт.
                              Не используй выделение глав решетками #.
                              Нельзя писать подобные высказывания: "Надеюсь это вам поможет, буду рад ответить на вопросы".
                              Тема: '''


CHANGE_TEXT_SYS_PROMPT_1 = ["Rewrite this text in different words. It should look very different but convey the same message: ",
                          "Change the wording of this text while keeping the main idea: ",
                          "Present this text using different words, but without changing its meaning: ",
                          "Paraphrase this text so that it looks unique but conveys the same idea: "]

CHANGE_TEXT_SYS_PROMPT_2 = "\nYou're not allowed to write that the text has been edited."

CHANGE_TEXT_SYS_PROMPT_3 = 'Take out all the phrases that says that text was edited. But do not touch main corpus of text that comes after this phrases. Text: '