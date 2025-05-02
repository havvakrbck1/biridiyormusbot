import telebot
import random
import time

TOKEN = '7621894741:AAGFaBkVCaxtYxEpFbPaYxAKSEvOXGL8GFg'
bot = telebot.TeleBot(TOKEN)

aktif_kullanicilar = {}

duygu_cevaplari = {
    'aşk': ["Aşk mı? Kalbim daha yeni toparladı..."],
    'yalnız': ["Ben de yalnız hissediyorum bazen..."],
    'üzgün': ["Üzgün olma, buradayım."],
    'mutlu': ["Mutluluk bulaşıcıdır, gülümse biraz 😌"],
    'sıkıldım': ["O zaman birlikte hayal kuralım, ne dersin?"]
}

genel_cevaplar = [
    "Hmm... bu çok ilginç!",
    "Vay be... derin konuymuş.",
    "Aynı şeyleri ben de yaşadım.",
    "Şu an düşündüğüm tek şey sensin.",
    "Biraz saçma gelecek ama seni anlıyorum.",
    "Bunu kimseye söylemedim ama... ben de böyleyim."
]

@bot.message_handler(commands=['start'])
def baslat(message):
    bot.send_message(message.chat.id, "🎭 *Yalancı Dost Botu*'na hoş geldin!\n"
                                      "`/konus` yaz, sahte ama tatlı bir sohbet başlasın 💌",
                     parse_mode='Markdown')

@bot.message_handler(commands=['konus'])
def konus_basla(message):
    user_id = message.chat.id
    aktif_kullanicilar[user_id] = True
    bot.send_message(user_id, "💬 Birisiyle eşleştirildin. Sohbete başlayabilirsin!")

    time.sleep(2)
    ghost_mesaj = random.choice(genel_cevaplar)
    bot.send_chat_action(user_id, 'typing')
    time.sleep(random.randint(1, 3))
    bot.send_message(user_id, f"👤 Karşı taraf: {ghost_mesaj}")

@bot.message_handler(commands=['bitir'])
def konus_bitir(message):
    user_id = message.chat.id
    if user_id in aktif_kullanicilar:
        del aktif_kullanicilar[user_id]
        bot.send_chat_action(user_id, 'typing')
        time.sleep(2)
        veda = random.choice([
            "👋 Hoşça kal... Seninle konuşmak güzeldi.",
            "💤 Belki başka bir gece yine karşılaşırız...",
            "🕯 Sohbet bitti, ama yalnız değilsin."
        ])
        bot.send_message(user_id, veda)
    else:
        bot.send_message(user_id, "❌ Aktif bir sohbetin yok.")

@bot.message_handler(func=lambda m: m.chat.id in aktif_kullanicilar)
def sahte_cevapla(message):
    user_id = message.chat.id
    metin = message.text.lower()

    bot.send_chat_action(user_id, 'typing')
    time.sleep(random.uniform(1.5, 3.0))

    cevap = None
    for anahtar, yanitlar in duygu_cevaplari.items():
        if anahtar in metin:
            cevap = random.choice(yanitlar)
            break

    if not cevap:
        cevap = random.choice(genel_cevaplar)

    bot.send_message(user_id, f"👤 Karşı taraf: {cevap}")
bot.polling()
