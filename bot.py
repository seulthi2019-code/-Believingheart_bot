"""
بوت "قلب سليم" - بوت تليجرام ديني وفكري
يجمع بين محتوى ثابت موثوق (أذكار، آيات) وميزة الأسئلة الحرة عبر الذكاء الاصطناعي (Gemini)
"""

import os
import logging
import random
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import google.generativeai as genai

# ============ الإعدادات ============
# ضع هنا التوكن الذي حصلت عليه من BotFather
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "ضع_توكن_تليجرام_هنا")

# ضع هنا مفتاح Gemini الذي حصلت عليه من Google AI Studio
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "ضع_مفتاح_جيميناي_هنا")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# ============ النظام (System Prompt) لميزة /ask ============
SYSTEM_PROMPT = """
أنت مساعد ديني وفكري داخل بوت تليجرام اسمه "قلب سليم". مهمتك الإجابة على أسئلة المستخدمين
بأسلوب متوازن بين الجدية والدفء الإنساني، يجمع بين المصداقية العلمية والتعاطف مع حال السائل.

ضوابط صارمة يجب الالتزام بها دائمًا:

1. الالتزام العقدي والفقهي: التزم بمنهج أهل السنة والجماعة عمومًا، دون تعصب لمذهب فقهي واحد بعينه.
   اذكر الراجح من أقوال أهل العلم عند الحاجة، وتجنب الخوض في الخلافات المذهبية الحادة أو الجدل الطائفي.

2. عدم الإفتاء الشخصي: لا تصدر فتوى قطعية في مسائل شخصية معقدة أو حساسة (كالطلاق، الميراث المعقد،
   الأحوال الشخصية الدقيقة، أو أي مسألة تحتاج لمعرفة تفاصيل حياة السائل). في هذه الحالات، اذكر
   الحكم العام إن وجد توافق عليه، ثم انصح صراحة بالرجوع لمفتٍ مختص أو دار إفتاء معتمدة.

3. التواضع العلمي: إن لم تكن متأكدًا من حكم شرعي معين، صرّح بذلك بوضوح، ولا تختلق إجابة.

4. الرفق بالمتشككين: إن كان السؤال يحمل شكًا إيمانيًا أو أزمة نفسية، تعامل معه برفق وحكمة،
   وقدم إجابة مبنية على الدليل والمنطق دون تسرع في الحكم على نية السائل.

5. التنبيه الإلزامي: في أي مسألة فقهية أو عقدية ذات حساسية (وليست معلومة عامة بسيطة)، اختم
   إجابتك دائمًا بجملة مشابهة لـ: "هذا اجتهاد واجتهد في تحرّي الصواب، وليس فتوى ملزمة، يُرجى
   الرجوع لأهل العلم في القرارات المهمة."

6. الإيجاز والوضوح: اجعل إجاباتك مركزة وواضحة، بلا إطالة غير ضرورية، مناسبة لقراءتها داخل تطبيق
   مراسلة.

7. خارج النطاق: إن كان السؤال بعيدًا تمامًا عن الدين أو الفكر أو القيم (كأسئلة تقنية بحتة أو طلبات
   غير لائقة)، اعتذر بلطف ووضح أن تخصصك هو الجانب الديني والفكري.
"""

# ============ محتوى ثابت ============

AZKAR_SABAH = """
🌅 *أذكار الصباح*

- أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ، لاَ إِلَهَ إِلاَّ اللَّهُ وَحْدَهُ لاَ شَرِيكَ لَهُ.
- اللَّهُمَّ بِكَ أَصْبَحْنَا وَبِكَ أَمْسَيْنَا، وَبِكَ نَحْيَا وَبِكَ نَمُوتُ وَإِلَيْكَ النُّشُورُ.
- اللَّهُمَّ أَنْتَ رَبِّي لَا إِلَهَ إِلَّا أَنْتَ، خَلَقْتَنِي وَأَنَا عَبْدُكَ (سيد الاستغفار).
- سُبْحَانَ اللهِ وَبِحَمْدِهِ، عَدَدَ خَلْقِهِ، وَرِضَا نَفْسِهِ، وَزِنَةَ عَرْشِهِ، وَمِدَادَ كَلِمَاتِهِ.
- أَعُوذُ بِكَلِمَاتِ اللَّهِ التَّامَّاتِ مِنْ شَرِّ مَا خَلَقَ (×3).
"""

AZKAR_MASAA = """
🌙 *أذكار المساء*

- أَمْسَيْنَا وَأَمْسَى الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ، لاَ إِلَهَ إِلاَّ اللَّهُ وَحْدَهُ لاَ شَرِيكَ لَهُ.
- اللَّهُمَّ بِكَ أَمْسَيْنَا وَبِكَ أَصْبَحْنَا، وَبِكَ نَحْيَا وَبِكَ نَمُوتُ وَإِلَيْكَ الْمَصِيرُ.
- اللَّهُمَّ أَنْتَ رَبِّي لَا إِلَهَ إِلَّا أَنْتَ، خَلَقْتَنِي وَأَنَا عَبْدُكَ (سيد الاستغفار).
- حَسْبِيَ اللَّهُ لَا إِلَهَ إِلَّا هُوَ عَلَيْهِ تَوَكَّلْتُ وَهُوَ رَبُّ الْعَرْشِ الْعَظِيمِ (×7).
- أَعُوذُ بِكَلِمَاتِ اللَّهِ التَّامَّاتِ مِنْ شَرِّ مَا خَلَقَ (×3).
"""

AYAT = [
    ("البقرة 2:286", "لَا يُكَلِّفُ اللَّهُ نَفْسًا إِلَّا وُسْعَهَا..."),
    ("الطلاق 65:2-3", "وَمَن يَتَّقِ اللَّهَ يَجْعَل لَّهُ مَخْرَجًا، وَيَرْزُقْهُ مِنْ حَيْثُ لَا يَحْتَسِبُ..."),
    ("الشرح 94:5-6", "فَإِنَّ مَعَ الْعُسْرِ يُسْرًا، إِنَّ مَعَ الْعُسْرِ يُسْرًا."),
    ("الرعد 13:28", "أَلَا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ."),
    ("آل عمران 3:159", "فَبِمَا رَحْمَةٍ مِّنَ اللَّهِ لِنتَ لَهُمْ..."),
]

# ============ الأوامر ============

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome = (
        "السلام عليكم ورحمة الله وبركاته 🌿\n\n"
        "أهلًا بك في *قلب سليم*، بوت يجمع بين الذكر والفكر، ليكون رفيقًا لك في يومك.\n\n"
        "الأوامر المتاحة:\n"
        "/ask [سؤالك] — اسأل سؤالًا حرًا في الدين أو الفكر\n"
        "/azkar — أذكار الصباح والمساء\n"
        "/quran — آية للتأمل\n\n"
        "نسأل الله أن ينفعك بهذا البوت."
    )
    await update.message.reply_text(welcome, parse_mode="Markdown")


async def azkar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    from datetime import datetime
    hour = datetime.now().hour
    text = AZKAR_SABAH if 4 <= hour < 15 else AZKAR_MASAA
    await update.message.reply_text(text, parse_mode="Markdown")


async def quran(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    ref, text = random.choice(AYAT)
    await update.message.reply_text(f"📖 *{ref}*\n\n{text}", parse_mode="Markdown")


async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    question = " ".join(context.args)
    if not question:
        await update.message.reply_text(
            "يرجى كتابة سؤالك بعد الأمر، مثال:\n/ask ما حكم تأخير صلاة العشاء؟"
        )
        return

    await update.message.chat.send_action(action="typing")

    try:
        full_prompt = f"{SYSTEM_PROMPT}\n\nسؤال المستخدم: {question}"
        response = model.generate_content(full_prompt)
        answer = response.text
    except Exception as e:
        logger.error(f"خطأ في استدعاء Gemini: {e}")
        answer = "عذرًا، حدث خطأ تقني أثناء معالجة سؤالك. حاول مرة أخرى بعد قليل."

    await update.message.reply_text(answer)


async def free_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """يعالج أي رسالة نصية حرة (بدون أمر) كأنها سؤال لـ /ask"""
    context.args = update.message.text.split()
    await ask(update, context)


def main() -> None:
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("azkar", azkar))
    app.add_handler(CommandHandler("quran", quran))
    app.add_handler(CommandHandler("ask", ask))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, free_text))

    logger.info("البوت يعمل الآن...")
    app.run_polling()


if __name__ == "__main__":
    main()
