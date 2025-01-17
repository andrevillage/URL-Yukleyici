import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from pyrogram import Client, types
from database.database import db
from plugins.yt_dlp_button import yt_dlp_call_back
from plugins.dl_button import ddl_call_back
from translation import Translation
from pyrogram import Client, filters
from plugins.settings.settings import Settings


@Client.on_callback_query()
async def button(bot, update):
    user_id = update.from_user.id
    if update.data == "home":
        await update.answer()
        await update.message.edit_text(
            text=Translation.START_TEXT.format(update.from_user.mention),
            reply_markup=Translation.START_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "help":
        await update.answer()
        await update.message.edit_text(
            text=Translation.HELP_TEXT,
            reply_markup=Translation.HELP_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "Settings":
        await update.answer()
        await Settings(update.message)
    elif update.data == "showThumbnail":
        thumbnail = await db.get_thumbnail(user_id)
        if not thumbnail:
            await update.answer("Herhangi bir thumbnail ayarlamadınız!", show_alert=True)
        else:
            await update.answer()
            await bot.send_photo(update.message.chat.id, thumbnail, "Ayarlı Thumbnail",
                               reply_markup=types.InlineKeyboardMarkup([[
                                   types.InlineKeyboardButton("Sil",
                                                              callback_data="deleteThumbnail")
                               ]]))
    elif update.data == "deleteThumbnail":
        await db.set_thumbnail(user_id, None)
        await update.answer("Başarıyla silindi.", show_alert=True)
        await update.message.delete(True)
    elif update.data == "setThumbnail":
        await update.answer(Translation.THUMBNAIL_TEXT, show_alert=True)
    elif update.data == "triggerGenSS":
        await update.answer()
        generate_ss = await db.get_generate_ss(user_id)
        if generate_ss:
            await db.set_generate_ss(user_id, False)
        else:
            await db.set_generate_ss(user_id, True)
        await Settings(update.message)
    elif update.data == "triggerGenSample":
        await update.answer()
        generate_sample_video = await db.get_generate_sample_video(user_id)
        if generate_sample_video:
            await db.set_generate_sample_video(user_id, False)
        else:
            await db.set_generate_sample_video(user_id, True)
        await Settings(update.message)
    elif update.data == "setCaption":
        await update.answer()
        caption = await db.get_caption(user_id)
        if caption:
            await db.set_caption(user_id, False)
        else:
            await db.set_caption(user_id, True)
        await Settings(update.message)
    elif update.data == "aria2":
        await update.answer()
        aria2 = await db.get_aria2(user_id)
        if aria2:
            await db.set_aria2(user_id, False)
        else:
            await db.set_aria2(user_id, True)
        await Settings(update.message)
    elif update.data == "triggerUploadMode":
        await update.answer()
        upload_as_doc = await db.get_upload_as_doc(user_id)
        if upload_as_doc:
            await db.set_upload_as_doc(user_id, False)
        else:
            await db.set_upload_as_doc(user_id, True)
        await Settings(update.message)
    elif update.data == "notifon":
        notif = await db.get_notif(user_id)
        if notif:
            await update.answer("Bot bildirimleri kapatıldı.")
            await db.set_notif(user_id, False)
        else:
            await update.answer("Bot bildirimleri etkinleştirildi.")
            await db.set_notif(user_id, True)
        await Settings(update.message)
    elif "close" in update.data:
        await update.message.delete(True)
    elif "|" in update.data:
        await yt_dlp_call_back(bot, update)
    elif "=" in update.data:
        await ddl_call_back(bot, update)
    else:
        await update.message.delete()
