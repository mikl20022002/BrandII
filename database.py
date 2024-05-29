import sqlite3
import datetime
import json
#____________BASE CREATION____________
database_name = 'project_citadel.db'
conn = sqlite3.connect(database_name, check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users_info
                (
                  id INTEGER PRIMARY KEY,
                  registr_date TEXT,
                  registr_time TEXT,
                  user_id INTEGER,
                  user_username TEXT,
                  user_first_name TEXT,
                  user_last_name TEXT,
                  user_lang_code TEXT,
                  user_fio TEXT,
                  user_email TEXT
                )''')
conn.commit()


c.execute('''CREATE TABLE IF NOT EXISTS users_accounts
                (
                  id INTEGER PRIMARY KEY,
                  user_id INTEGER, 
                  tg_accounts TEXT,
                  vk_accounts TEXT
                )''')
conn.commit()

#TODO: text и фото теперь в json, убрать отсюда
c.execute('''CREATE TABLE IF NOT EXISTS tech_info
                (
                 id INTEGER PRIMARY KEY,
                 user_id INTEGER, 
                 registration_finished INTEGER,
                 editing_allowed INTEGER
                )''')
conn.commit()

#____________AUTOMATION FUNC____________
def insert_account_info(data: tuple):
    """
    Вызывается при контакте бота с новым пользователем,
    заполняя в базу информацию об аккаунте.

    :param data: (id пользователя,
                  имя аккаунта,
                  имя пользователя,
                  фамилия пользователя,
                  языковой код пользователя)
    :return: None
    """
    date = datetime.date.today().strftime('%Y-%m-%d')
    time = datetime.datetime.now().strftime('%H:%M:%S')

    c.execute(f'''INSERT INTO users_info (
                    registr_date,
                    registr_time, 
                    user_id, 
                    user_username, 
                    user_first_name, 
                    user_last_name,
                    user_lang_code
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)''', (date, time, *data))

    c.execute(f''' INSERT INTO users_accounts (user_id) VALUES (?)''', (data[0],))

    c.execute(f''' INSERT INTO tech_info (user_id, registration_finished) VALUES (?, ?)''', (data[0], 0))
    conn.commit()

def update_lm_answer(user_id, answer):
    query = 'UPDATE tech_info SET post_text = ? WHERE user_id = ?'
    c.execute(query, (answer, user_id))
    conn.commit()

def get_user_row(user_id: int, table_name):
    """
    Возвращает строку соответствующую конкретному пользователю из определенной таблицы.
    Может использоватся для проверки наличия пользователя в базе.

    :param user_id: id пользователя
    :return:
    """
    c.execute(f"SELECT * FROM {table_name} WHERE user_id = ?", (user_id,))
    return c.fetchone()

def set_tg_channel_list(string_var, row_num):

    # Получаем ячейку из таблицы
    c.execute("SELECT tg_accounts FROM users_accounts WHERE user_id=?", (row_num,))
    cell = c.fetchone()[0]

    if cell is None or cell == "":
        # Если ячейка пуста, заносим список с одним элементом
        cell = [string_var]
    else:
        # Если ячейка не пуста, добавляем элемент в конец списка
        cell = json.loads(cell)
        cell.append(string_var)

    # Записываем список обратно в ячейку
    c.execute("UPDATE users_accounts SET tg_accounts=? WHERE user_id=?", (json.dumps(cell), row_num))
    conn.commit()

def get_tg_channel_list(user_id):

    # Получаем ячейку из таблицы
    c.execute("SELECT tg_accounts FROM users_accounts WHERE user_id=?", (user_id,))
    cell = c.fetchone()[0]

    if cell is None or cell == "":
        # Если ячейка пуста, возвращаем пустой список
        return []
    else:
        # Если ячейка не пуста, возвращаем список
        return json.loads(cell)

def update_editing_status(user_id, new_status):
    c.execute('UPDATE tech_info SET editing_allowed=? WHERE user_id=?', (new_status, user_id))
    conn.commit()

def is_editing_allowed(user_id):
    res = c.execute('SELECT editing_allowed FROM tech_info WHERE user_id=?', (user_id,)).fetchone()
    if res[0] == 1:
        return True
    else:
        return False

print('users_info:', c.execute('SELECT * FROM users_info').fetchall())
print('users_accounts:', c.execute('SELECT * FROM users_accounts').fetchall())
# print('tech_info:', c.execute('SELECT * FROM tech_info').fetchall()


