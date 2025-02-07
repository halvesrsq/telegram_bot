import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters, CallbackQueryHandler  # CallbackQueryHandler'ı ekledik

# Kripto cüzdan adresi
wallet_address = "TLRDMn63VXP74rPrcxbi9caB2twf243tjv"  # Buraya cüzdan adresini yaz

# BlockCypher API endpoint
url = f"https://api.blockcypher.com/v1/btc/main/addrs/{wallet_address}/full"

# Ödeme kontrol fonksiyonu
def check_payment():
    response = requests.get(url)
    data = response.json()
    
    # Yanıtı yazdıralım, böylece veriyi kontrol edebiliriz
    print(data)
    
    # Eğer 'final_balance' varsa, kontrol yapalım
    if 'final_balance' in data:
        if data['final_balance'] > 0:
            return True
        else:
            return False
    else:
        print("final_balance anahtarı bulunamadı.")
        return False

# /start komutunu işleme fonksiyonu
async def start(update: Update, context: CallbackContext) -> None:
    # Inline butonlar
    keyboard = [
        [InlineKeyboardButton("Ödeme Yapıldı", callback_data='payment_done')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Ödeme adresi ve talimatları içeren mesaj
    message = (
        "Ödeme Adresiniz: `USDT-TRC20: TLRDMn63VXP74rPrcxbi9caB2twf243tjv`\n\n"
        "Lütfen bu adresi kullanarak ödeme yapın. "
        "Ödeme yaptıktan sonra aşağıdaki butona tıklayarak işleminizi tamamlayabilirsiniz."
    )
    
    await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')

# Kullanıcı mesajını işleme fonksiyonu
async def handle_message(update: Update, context: CallbackContext) -> None:
    # Ödeme kontrolünü başlatıyoruz
    await update.message.reply_text("Ödemeniz kontrol ediliyor...")
    
    if check_payment():
        await update.message.reply_text("Ödemeniz alınmıştır. Teşekkür ederiz!")
    else:
        await update.message.reply_text("Ödemeniz henüz alınmadı. Lütfen tekrar deneyin.")

# Callback veri işleme
async def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    # Ödeme butonuna tıklanma durumu
    if query.data == 'payment_done':
        if check_payment():
            await query.edit_message_text("Ödemeniz alınmıştır. Teşekkür ederiz!")
        else:
            await query.edit_message_text("Ödemeniz henüz alınmadı. Lütfen tekrar deneyin.")

def main():
    # Botunuzu başlatın
    application = Application.builder().token("7599540562:AAFnqlkeDGmAyyIJBtLXt8qS7GQypeumKKI").build()  # Buraya BotFather'dan aldığın API token'ını yaz

    # Komutları ekleyin
    application.add_handler(CommandHandler("start", start))
    
    # Kullanıcı mesajlarını dinleyin
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Callback veri işleme
    application.add_handler(CallbackQueryHandler(button_callback))  # Burada CallbackQueryHandler ekliyoruz

    # Botu başlat
    application.run_polling()

if __name__ == '__main__':
    main()
