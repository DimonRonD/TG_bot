from telegram.ext import BaseHandler, CommandHandler
from app.handlers.commands import start, pet

HANDLERS: tuple[BaseHandler] = (CommandHandler("start", start), CommandHandler("pet", pet),)
