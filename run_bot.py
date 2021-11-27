from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import requests
import subprocess

def run_bash_cmd(cmd):
    """
    Run a bash command from python.
    """
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode('utf8'), error

def _act(update, context, bash_file):
    args = ' ' + ' '.join(context.args)
    args = args.replace(' —', ' --')
    if ('user' not in args) and ('pwd' not in args):
        context.bot.send_message(update.message.chat_id, 'You must provide the math "user" and "pwd".')
    else:
        out, err = run_bash_cmd(bash_file + args)
        context.bot.send_message(update.message.chat_id, out)

def book(update, context):
    _act(update, context, './scripts/book')

def check(update, context):
    _act(update, context, './scripts/check')

def remove(update, context):
    _act(update, context, './scripts/remove')

def start(update, context):
    chat_id = update.message.chat_id
    first_name = update.message.chat.first_name
    context.bot.send_message(chat_id, f'Welcome {first_name}')

def main():
    BOT_TOKEN = '2113822109:AAE_z5WPZjX9jRi-v6ehFj2jDstW3weAW-A'
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('book', book))
    dispatcher.add_handler(CommandHandler('check', check))
    dispatcher.add_handler(CommandHandler('remove', remove))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
