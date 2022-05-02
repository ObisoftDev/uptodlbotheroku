from telegram import ChatAction,InlineQueryResultArticle,InlineQueryResultPhoto, ParseMode, InputTextMessageContent, Update,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext,MessageHandler,Filters,CallbackQueryHandler
from telegram.utils.helpers import escape_markdown
from uuid import uuid4
import uptod
import os


CACHE = {}


def inlinequery(update: Update, context: CallbackContext) -> None:
    global CACHE
    #if not update.inline_query.from_user.username in ADMIN_USERS:return

    try:
        if CACHE[update.inline_query.from_user.username]:pass
    except:
        CACHE[update.inline_query.from_user.username] = 'windows'

    try:
        query = update.inline_query.query

        if query == "":pass
        else:
            results = []
            try:

                tag = CACHE[update.inline_query.from_user.username]
                list = uptod.search(query,tag)

                for item in list:
                    results.append(InlineQueryResultArticle(
                        id=str(uuid4()),
                        title=item['name'],
                        thumb_url=item['img'],
                        description = '#'+tag,
                        input_message_content=InputTextMessageContent('#uptodlview '+item['name'],parse_mode=ParseMode.HTML)
                    ))
            except Exception as ex:
                results.append(InlineQueryResultArticle(
                        id=str(uuid4()),
                        title= '❌' + query + ' no se encontro nada' + '❌',
                        input_message_content=InputTextMessageContent('#uptodlerror',parse_mode=ParseMode.HTML)
                    ))
            update.inline_query.answer(results,cache_time=0)
    except Exception as ex:
        print(str(ex))


def sendHtml(update,html,markups=None):
    return update.message.reply_text(html, parse_mode=ParseMode.HTML,reply_markup=markups)

def editHtml(message,html,markups=None):
    return message.edit_text(html, parse_mode=ParseMode.HTML,reply_markup=markups)

def process_msg(update,context):
    #if not update.message.chat.username in ADMIN_USERS:sendHtml(update,'El Bot esta en Mantenimiento...')

    try:

        msg = update.message.text

        update.message.chat.send_action(action=ChatAction.UPLOAD_DOCUMENT)

        try:
            if CACHE[update.message.chat.username]:pass
        except:
            CACHE[update.message.chat.username] = 'windows'


        if '/start' in msg:
            reply = '<a href="https://www.uptodown.com">~<b>Bienvenidos a UptoDL</b>~</a>\n'
            reply += '<b>Actualizaciones:</b>\n'
            reply += '<b>1-Buscador En Linea @uptodl</b>\n'
            reply += '<b>2-Extractor De Informacion</b>\n'
            reply += '<b>3-/uptodlwin - Modo Apps Windows</b>\n'
            reply += '<b>4-/uptodland - Modo Apps Android</b>\n'
            sendHtml(update,reply)

        if '/uptodlwin' in msg or '/uptodlwin@uptodlbot' in msg or '/win@uptodlbot' in msg:
            CACHE[update.message.chat.username] = 'windows'
            sendHtml(update,'<b>'+update.message.chat.username+' : #windows</b>')

        if '/uptodland' in msg or '/uptodland@uptodlbot' in msg or '/and@uptodlbot' in msg:
            CACHE[update.message.chat.username] = 'android'
            sendHtml(update,'<b>'+update.message.chat.username+' : #android</b>')

        if '#uptodlview' in msg:
            tag = CACHE[update.message.chat.username]
            name = str(msg).replace('#uptodlview ','')
            search = uptod.search(name,tag)
            pcp  = ''
            for p in search:
                if p['name']==name:
                    pcp = p
                    break
            if pcp!='':
                buttons = []
                info = uptod.getInfo(pcp)
                buttons.append([InlineKeyboardButton(text=info['name'],url=info['url'])])
                reply = '<a href="'+pcp['img']+'">'+pcp['name']+'</a>\n'
                reply+= '<b>'+info['text']+'</b>\n\n'
                reply+= '<b>@uptodlbot</b>\n\n'
                reply+= '<b>Para descargar el archivo copiar el enlace del boton abajo en el siguiente bot @UploadsRobot</b>\n\n'
                try:
                    sendHtml(update,reply,InlineKeyboardMarkup(buttons))
                except:
                    reply+= '<a href="'+info['url']+'">🎗️Enlace Aqui🎗️</a>'
                    sendHtml(update,reply)

    except Exception as ex:
        print(str(ex))

    pass


def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def main() -> None:
    try:
        updater = Updater('BOT TOKEN')

        dispatcher = updater.dispatcher

        dispatcher.add_handler(MessageHandler(Filters.text,process_msg))
        dispatcher.add_handler(InlineQueryHandler(inlinequery,pass_update_queue=True))

        updater.start_polling()
        updater.idle()
    except Exception as ex:
        print(str(ex))
        main()


if __name__ == '__main__':
    main()
