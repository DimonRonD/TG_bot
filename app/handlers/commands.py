from telegram import Update
from telegram.ext import ContextTypes
import psycopg2
from colorama import Fore, Back, Style

HOST = '127.0.0.1'
DATABASE = 'TGbotDB'
USER = 'tgbotty'
PASSWORD = 'yttobgt'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user = update.effective_user
    username = user.username
    if update.effective_chat:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Добро пожаловать, {user_id}, {username}!",
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

async def add_note(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user = update.effective_user
    username = user.username
    conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
    try:
        cursor = conn.cursor()
    except psycopg2.OperationalError:
        print(psycopg2.OperationalError)

    cursor.execute(f'insert into notes (uid, uname, date_note, note) values ({user_id}, \'{username}\', CURRENT_DATE, \'my very long text\');')
    conn.commit()
    cursor.execute('SELECT * FROM notes;', (1,))

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