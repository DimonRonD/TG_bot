from telegram import Update, BotCommand
from telegram.ext import ContextTypes, CallbackContext
import psycopg2


HOST = '127.0.0.1'
DATABASE = 'TGbotDB'
USER = 'tgbotty'
PASSWORD = 'yttobgt'
BOT_TOKEN = '8329047740:AAEINfj4EFBzLmlJC4cH5DaJDAZwAcdQbiA'


commands = [
    BotCommand("start", "Начать работу бота"),
    BotCommand("help", "Дополнительная информация по по командам"),
    BotCommand("add_note", "Создать заметку"),
    BotCommand("del_note", "Удалить заметку"),
]


def echo(update: Update, context: CallbackContext) -> None:
    """Эхо-бот: отвечает тем же, что и получил."""
    user_text = update.message.text
    update.message.reply_text(f'Вы сказали: {user_text}')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user = update.effective_user
    username = user.username
    message_text = update.message.text
    await context.bot.set_my_commands(commands)
    if update.effective_chat:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Добро пожаловать, {user_id}, {username}!\n Ваш текст: {message_text}",
        )

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="""
            Это проект-питомец Дмитрия Петлина
            Для начала работы введите команду /start
            Для добавления заметки введите команду /add_note
            """
        )

async def add_note(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    user = update.effective_user
    username = user.username
    user_text = update.message.text.replace('/add_note', '').strip()
    conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
    try:
        cursor = conn.cursor()
    except psycopg2.OperationalError:
        print(psycopg2.OperationalError)

    cursor.execute(f'insert into notes (uid, uname, date_note, note) values ({user_id}, \'{username}\', CURRENT_DATE, \'{user_text}\');')
    conn.commit()
    cursor.execute(f'SELECT * FROM notes WHERE uid={user_id};', (1,))

    # Fetch all results
    rows = cursor.fetchall()
    all_notes_str = ''
    for row in sorted(rows):
        all_notes_str += str(row[0]) + '\t' + str(row[3]) + '\t' + str(row[4]) + '\n'

    if update.effective_chat:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Добро пожаловать, {user_id}, {username}!\nВсе заметки:\n {all_notes_str}",
        )

    cursor.close()
    conn.close()


async def del_note(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    user = update.effective_user
    username = user.username
    user_text = update.message.text.replace('/del_note', '').strip()
    conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
    try:
        cursor = conn.cursor()
    except psycopg2.OperationalError:
        print(psycopg2.OperationalError)
    cursor.execute(f'SELECT * FROM notes WHERE uid={user_id} and id={user_text};', (1,))

    rows = cursor.fetchall()
    result = ''
    if rows:
        result += f"Зашли в DELETE\n"
        cursor.execute(f'DELETE FROM notes WHERE uid={user_id} and id={user_text};')
        conn.commit()
        result += (f'Заметка: {str(rows)} удалена')
    else:
        result += (f'Сочетание {user_text} и {user_id} для пользователя {username} не найдено')
    cursor.close()
    conn.close()

    all_notes_str = list_notes(user_id)
    for row in sorted(rows):
        all_notes_str += str(row[0]) + '\t' + str(row[3]) + '\t' + str(row[4]) + '\n'
    if update.effective_chat:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=result + '\nВсе заметки:\n' + all_notes_str
        )


def list_notes(user_id):
    conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
    try:
        cursor = conn.cursor()
    except psycopg2.OperationalError:
        print(psycopg2.OperationalError)

    cursor.execute(f'SELECT * FROM notes WHERE uid={user_id};', (1,))

    # Fetch all results
    rows = cursor.fetchall()
    all_notes_str = ''
    for row in sorted(rows):
        all_notes_str += str(row[0]) + '\t' + str(row[3]) + '\t' + str(row[4]) + '\n'

    cursor.close()
    conn.close()

    return all_notes_str