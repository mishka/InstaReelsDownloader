import re
from datetime import datetime

from ReelsAPI import Insta

from telegram import ParseMode
from telegram.ext import Updater, MessageHandler, CommandHandler


Pattern = r'((?:https?:\/\/)?(?:www\.)?instagram\.com\/(?:p|reel)\/([^/?#&]+))\/'
Gram = Insta()


def log(text):
    print(f"| {datetime.now().strftime('%H:%M:%S')} | {text}")


def start(update, context):
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Hi, send an instagram url that contains a video to use this bot.'
    )


def processor(update, context):
    text = update.message.text    
    chat_id = update.message.chat_id
    name = update.message.chat.first_name
    username = update.message.chat.username
    message_id = update.message.message_id
        
    if not text:
        log(f"@{username} | {name} | {chat_id}\nRequest doesn't contain text, skipping...")
        return

    log(f'Request: {username} | {name} | {text}')

    result = re.search(Pattern, text)

    if not result:
        context.bot.send_message(
            chat_id = chat_id,
            reply_to_message_id = message_id,
            text = "_I'm sorry, I couldn't find an instagram url in your message._",
            parse_mode = ParseMode.MARKDOWN
        )
        return
    
    try:
        video = Gram.VideoURL(result.group(0))
    except:
        context.bot.send_message(
            chat_id = chat_id,
            reply_to_message_id = message_id,
            text = "_I'm sorry, something went wrong while trying to find the video._",
            parse_mode = ParseMode.MARKDOWN
        )
        return

    if video is not None:
        try:
            context.bot.send_video(
                chat_id = chat_id,
                video = video,
                reply_to_message_id = message_id,
                supports_streaming = True
            )
        except:
            context.bot.send_message(
                chat_id = chat_id,
                reply_to_message_id = message_id,
                text = f"I'm sorry, telegram is being a lil meanie and not accepting the video.\n\nHere's the URL instead;\n\n{video}"
            )
    else:
        context.bot.send_message(
            chat_id = chat_id,
            reply_to_message_id = message_id,
            text = "_I'm sorry, something went wrong while trying to find the video._",
            parse_mode = ParseMode.MARKDOWN
        )

def main():
    updater = Updater(
        token = '',
        use_context = True,
        request_kwargs = {'read_timeout': 1000, 'connect_timeout': 1000}
    )

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(None, processor))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    log('ONLINE')
    main()