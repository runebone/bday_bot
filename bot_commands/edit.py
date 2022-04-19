from bot_commands.common import *

def process_edit_step(message, bot, db):
    try:
        pass

    except Exception as e:
        bot.send_message(message.chat.id, \
                FailText.UncaughtError.format(str(e)))

        tb = sys.exc_info()[2]
        raise e.with_traceback(tb)
