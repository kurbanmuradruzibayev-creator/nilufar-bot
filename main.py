from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Savollar va javoblar (A1 dan C2 gacha)
questions = [
    ("What is the capital of England? \n(a) London \n(b) Paris \n(c) Rome", "a"),      # A1
    ("Choose the correct sentence: \n(a) He go to school. \n(b) He goes to school. \n(c) He going to school.", "b"),  # A2
    ("Complete the sentence: I have been living here ____ 2010. \n(a) since \n(b) for \n(c) at", "a"),  # B1
    ("What is the synonym of 'complicated'? \n(a) simple \n(b) complex \n(c) easy", "b"),  # B2
    ("Identify the passive voice sentence: \n(a) She writes a letter. \n(b) A letter is written by her. \n(c) She wrote a letter.", "b"),  # C1
    ("Choose the correct subjunctive mood sentence: \n(a) If I was you, I would go. \n(b) If I were you, I would go. \n(c) If I am you, I would go.", "b"),  # C2
]

level_names = ["A1", "A2", "B1", "B2", "C1", "C2"]

# Foydalanuvchilar holatini saqlaymiz: user_id -> {'score': int, 'current': int}
user_scores = {}

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Salom! Ingliz tilidagi darajangizni baholash uchun test. \n"
        "6 ta savolga javob bering.\n"
        "Boshlash uchun /test ni bosing."
    )

def test(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_scores[user_id] = {'score': 0, 'current': 0}
    update.message.reply_text("Test boshlandi! Birinchi savol:")
    ask_question(update, context, user_id)

def ask_question(update: Update, context: CallbackContext, user_id):
    current = user_scores[user_id]['current']
    if current < len(questions):
        update.message.reply_text(questions[current][0])
    else:
        score = user_scores[user_id]['score']
        if score > 0:
            level = level_names[score - 1]
        else:
            level = "No level"
        update.message.reply_text(f"✅ Test yakunlandi!\nSizning darajangiz: {level} ({score} ta to'g'ri javob)")
        user_scores.pop(user_id)

def handle_answer(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in user_scores:
        update.message.reply_text("❗ Test boshlash uchun /test buyrug'ini yozing.")
        return

    current = user_scores[user_id]['current']
    if current >= len(questions):
        update.message.reply_text("ℹ️ Test allaqachon tugadi. /test ni qayta yozing.")
        return

    user_answer = update.message.text.lower().strip()
    correct_answer = questions[current][1]

    if user_answer == correct_answer:
        user_scores[user_id]['score'] += 1
        update.message.reply_text("✅ To'g'ri!")
    else:
        update.message.reply_text(f"❌ Noto'g'ri! To'g'ri javob: {correct_answer}")

    user_scores[user_id]['current'] += 1
    ask_question(update, context, user_id)

def main():
    TOKEN = "SIZNING_BOT_TOKENINGIZNI_BU_YERGA_QO'YING"  # 👉 bu yerga BotFather dan olingan tokenni yozing
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("test", test))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_answer))

    print("🤖 Bot ishga tushdi...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":   # ❌ sizda `if name == "main":` edi
    main()
