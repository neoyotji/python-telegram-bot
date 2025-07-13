from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Bot ayarları
BOT_TOKEN = "8066865232:AAHhi1udwqK88EjHSPdyXurFF3eURm63n5U"
YONETICI_IDLERI = [1075107046, 1444479231, 1545117757, 990661072, 5424226847]  # Her yöneticinin Telegram ID'si
KANAL_ID = "-2604764592"  # İsteğe bağlı

# /start komutu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hoş geldiniz. Bu alana yazacağınız anılarınız Üstadımız tarafından değerlendirildikten sonra kitap haline getirilecektir.Paylaşımınız için teşekkür ederiz"
    )

# Metin mesajı
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None or update.message.text is None:
        return

    user = update.effective_user
    text = update.message.text
    mesaj = f"Yeni METİN mesajı\n @{user.username or user.full_name} ({user.id})\n İçerik:\n{text}"

    await update.message.reply_text("Mesajınız alındı ve yöneticilere iletildi.")

    for admin_id in YONETICI_IDLERI:
        try:
            await context.bot.send_message(chat_id=admin_id, text=mesaj)
        except Exception as e:
            print(f"HATA (metin): {admin_id} → {e}")

# Fotoğraf mesajı
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None or not update.message.photo:
        return

    user = update.effective_user
    caption = update.message.caption or ""
    file_id = update.message.photo[-1].file_id

    await update.message.reply_text("Fotoğrafınız alındı ve yöneticilere iletildi.")

    for admin_id in YONETICI_IDLERI:
        try:
            await context.bot.send_photo(
                chat_id=admin_id,
                photo=file_id,
                caption=f"Yeni FOTOĞRAF\n @{user.username or user.full_name} ({user.id})\n Açıklama:\n{caption}"
            )
        except Exception as e:
            print(f"HATA (fotoğraf): {admin_id} → {e}")

# PDF / Word gibi belge mesajı
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None or not update.message.document:
        return

    user = update.effective_user
    caption = update.message.caption or ""
    file_id = update.message.document.file_id
    file_name = update.message.document.file_name

    await update.message.reply_text("📎 Belgeniz alındı ve yöneticilere iletildi.")

    for admin_id in YONETICI_IDLERI:
        try:
            await context.bot.send_document(
                chat_id=admin_id,
                document=file_id,
                caption=f"📎 Yeni BELGE\n👤 @{user.username or user.full_name} ({user.id})\n🗂️ Dosya: {file_name}\n✏️ Açıklama:\n{caption}"
            )
        except Exception as e:
            print(f"HATA (belge): {admin_id} → {e}")

# Botu çalıştır
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))  # tüm belgeler için filtre

    print("✅ Bot çalışıyor (metin + fotoğraf + belge destekli)...")
    app.run_polling()
