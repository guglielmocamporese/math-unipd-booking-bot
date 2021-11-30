from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import telegram
import subprocess

def run_bash_cmd(cmd):
    """
    Run a bash command from python.
    """
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode('utf8'), error

def _act(update, context, bash_file):
    """
    Wrapper to book, check, remove functions.
    """
    args = ' ' + ' '.join(context.args)
    args = args.replace(' —', ' --')
    if ('user' not in args) and ('pwd' not in args):
        context.bot.send_message(update.message.chat_id, 'You must provide the math "user" and "pwd".', parse_mode=telegram.ParseMode.HTML)
    else:
        out, err = run_bash_cmd(bash_file + args)
        context.bot.send_message(update.message.chat_id, out, parse_mode=telegram.ParseMode.HTML)

def book(update, context): _act(update, context, 'bash scripts/book.sh')
def check(update, context): _act(update, context, 'bash scripts/check.sh')
def remove(update, context): _act(update, context, 'bash scripts/remove.sh')

def start(update, context):
    """
    Start function for the bot.
    """
    chat_id = update.message.chat_id
    first_name = update.message.chat.first_name
    example_str = ('/book --user math_user --pwd math_pass --this_week'
        '\n/check --user math_user --pwd math_pass --next_month'
        '\n/remove --user math_user --pwd math_pass --tomorrow')
    url = 'https://github.com/guglielmocamporese/math-unipd-booking'
    start_str = f'Welcome {first_name}, these are some examples for using this BOT.\n\n' + example_str + f'\n\nMore information at {url}'
    context.bot.send_message(chat_id, start_str, parse_mode=telegram.ParseMode.MARKDOWN)
    

if __name__ == '__main__':
    print('Running bot...')
    BOT_TOKEN = '2113822109:AAE_z5WPZjX9jRi-v6ehFj2jDstW3weAW-A'
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('book', book))
    dispatcher.add_handler(CommandHandler('check', check))
    dispatcher.add_handler(CommandHandler('remove', remove))
    updater.start_polling()
    updater.idle()
