from telegram.ext import BaseHandler, CommandHandler
from app.handlers.commands import start, help, add_note, del_note

HANDLERS: tuple[BaseHandler] = (CommandHandler("start", start),
                                CommandHandler("help", help),
                                CommandHandler("add_note", add_note),
                                CommandHandler("del_note", del_note),
                                )


