# -*- coding: utf-8 -*-
import os
import re
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, InputMediaVideo
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CallbackQueryHandler, filters
from openai import OpenAI

# Load config
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

CHANNEL_BETRADER = -1002468278246
CHANNEL_BETRADER_UZ = -1002468278246
CHANNEL_FIRDAVS = -1002383272008

client = OpenAI(api_key=OPENAI_API_KEY)

# --- KALIT SO'ZLAR ---
trading_keywords_uz = [
    "aksiyalar", "fond bozori", "sarmoya", "foyda", "zarar", "risk", "kapital", "savdo",
    "pozitsiya", "savdo hajmi", "tahlil", "grafik", "narx", "tushish", "ko‘tarilish", "bozor",
    "dividend", "broker", "savdolar", "buyurtma", "portfel", "moliyaviy erkinlik", "psixologiya",
    "order", "margin", "qimmatli qog‘oz", "platforma", "indikator", "trend", "volatillik",
    "soxta signallar", "treyd", "scalping", "swing", "day trading", "long", "short", "buy", "sell", "balans",
    "S&P 500", "NASDAQ", "Dow Jones", "indeks", "ETF", "IPO", "diversifikatsiya",
    "blue chip", "kapitalizatsiya", "moliyaviy hisobot", "qimmatli qog‘ozlar bozori", 
    "likvidlik", "insayder", "volyum", "risk menejment", "algoritmik savdo", "fundamental tahlil", 
    "texnik tahlil", "daromadlilik", "EPS", "P/E", "dividend rentabelligi"
]

trading_keywords_ru = [
    "трейдинг", "акции", "фондовый рынок", "инвестор", "инвестиции", "прибыль", "убыток", "риск",
    "капитал", "позиция", "объем", "анализ", "график", "цена", "рост", "падение", "рынок", "дивиденды",
    "брокер", "торговля", "психология", "портфель", "заказ", "доходность", "сделка", "лосс", "плечо",
    "баланс", "ликвидность", "сигналы", "платформа", "индикатор", "тренд", "волатильность", "лонг",
    "шорт", "бай", "селл", "уровень", "стратегия", "S&P 500", "NASDAQ", "Dow Jones", "индекс", "ETF", "IPO", "диверсификация",
    "blue chip", "капитализация", "финансовая отчетность", "фондовый рынок", 
    "ликвидность", "инсайдер", "объем", "управление рисками", "алгоритмическая торговля", 
    "фундаментальный анализ", "технический анализ", "доходность", "EPS", "P/E", "дивидендная доходность"
]

smm_keywords_uz = [
    "kontent", "vizual", "sarlavha", "post", "storilar", "story", "qamrov", "reaksiya",
    "komment", "like", "followers", "videokontent", "reels", "ijtimoiy tarmoqlar", "target",
    "reklama", "sotuv", "trafik", "qiziqish", "tahlil", "struktura", "brend", "obuna", "ko‘rinish",
    "reach", "engagement", "konversiya", "aksiya", "tayming", "hook", "feedback", "auditoriya",
    "nisbat", "tasdiq", "mavzu", "so‘rovnoma", "avtomatizatsiya", "yashirin savdo", "progrev", "savdo varonkasi"
]

smm_keywords_ru = [
    "контент", "визуал", "заголовок", "пост", "сторис", "видео", "охват", "реакция", "комментарий",
    "лайк", "подписчики", "reels", "социальные сети", "таргет", "реклама", "продажи", "трафик",
    "интерес", "анализ", "структура", "бренд", "оформление", "обложка", "вовлеченность", "конверсия",
    "акция", "тайминг", "хук", "отзывы", "аудитория", "показатели", "визитка", "опрос", "автоматизация",
    "прогрев", "воронка продаж", "виральность", "актуальность", "интерактив", "стратегия"
]

# Xabarlarni tillarga ko'ra sozlash
MESSAGES = {
    "uz": {
        "no_text": "❌ Bu xabarda matn yo‘q.",
        "choose_channel": "Qaysi kanal uchun post tayyorlaymiz?",
        "choose_language": "Endi tilni tanlang:",
        "processing": "✅ Tanlangan til: {lang}\n\n⏳ Matn qayta yozilmoqda...",
        "posted": "✅ Post kanalga joylandi!",
        "post_error": "❌ Postni kanalga joylashda xatolik: {error}",
        "gpt_error": "❌ GPT xatosi: {error}",
        "too_long_error": "⚠️ Matn juda uzun, qisqartirib qayta yozilmoqda...",
        "betrader_button": "📈 BeTrader uchun",
        "betrader_uz_button": "📈 @Betrader_uz",
        "firdavs_button": "📊 FirdavsUrinov uchun",
        "uz_button": "🇺🇿 O'zbek tili",
        "ru_button": "🇷🇺 Русский язык",
        "confirm_button": "✅ Kanalga joylash",
        "rewrite_button": "🔄 Qayta yozish",
        "shorten_button": "✂️ Qisqaroq yozish"
    },
    "ru": {
        "no_text": "❌ В этом сообщении нет текста.",
        "choose_channel": "Для какого канала готовим пост?",
        "choose_language": "Теперь выберите язык:",
        "processing": "✅ Выбранный язык: {lang}\n\n⏳ Текст переписывается...",
        "posted": "✅ Пост размещен в канале!",
        "post_error": "❌ Ошибка при размещении поста в канал: {error}",
        "gpt_error": "❌ Ошибка GPT: {error}",
        "too_long_error": "⚠️ Текст слишкzом длинный, переписывается короче...",
        "betrader_button": "📈 Для BeTrader",
        "betrader_uz_button": "📈 @Betrader_uz",
        "firdavs_button": "📊 Для FirdavsUrinov",
        "uz_button": "🇺🇿 Узбекский язык",
        "ru_button": "🇷🇺 Русский язык",
        "confirm_button": "✅ Разместить в канал",
        "rewrite_button": "🔄 Переписать",
        "shorten_button": "✂️ Сократить"
    }
}

# HTML teglarini tekshirish va tuzatish funksiyasi
def fix_html_tags(text):
    open_b_count = text.count("<b>")
    close_b_count = text.count("</b>")
    open_i_count = text.count("<i>")
    close_i_count = text.count("</i>")

    if open_b_count > close_b_count:
        text += "</b>" * (open_b_count - close_b_count)
    elif close_b_count > open_b_count:
        text = text.replace("</b>", "", close_b_count - open_b_count)

    if open_i_count > close_i_count:
        text += "</i>" * (open_i_count - close_i_count)
    elif close_i_count > open_i_count:
        text = text.replace("</i>", "", close_i_count - open_i_count)

    return text

# Matnni qisqartirish (teglarni buzmaslik uchun)
def truncate_text(text, limit=1000):
    if len(text) <= limit:
        return text

    truncated = text[:limit]
    open_b_count = truncated.count("<b>") - truncated.count("</b>")
    open_i_count = truncated.count("<i>") - truncated.count("</i>")

    if open_b_count > 0:
        truncated += "</b>" * open_b_count
    if open_i_count > 0:
        truncated += "</i>" * open_i_count

    if not truncated.endswith("..."):
        truncated += "..."

    return truncated

# Telegram qo‘llab-quvvatlamaydigan HTML teglarni olib tashlash yoki almashtirish
def clean_unsupported_html(text):
    # <h1>, <h2>, <h3> kabi sarlavha teglarni <b> ga almashtirish
    text = re.sub(r"<h[1-6]>", "<b>", text)
    text = re.sub(r"</h[1-6]>", "</b>", text)

    # <p> teglarini oddiy qatorlar bilan almashtirish (bo‘sh qator qo‘shish)
    text = re.sub(r"<p>", "", text)
    text = re.sub(r"</p>", "\n\n", text)

    # <ul> va <li> teglarini oddiy ro‘yxat sifatida ko‘rsatish
    text = re.sub(r"<ul>", "", text)
    text = re.sub(r"</ul>", "", text)
    text = re.sub(r"<li>", "• ", text)
    text = re.sub(r"</li>", "\n", text)

    # Boshqa qo‘llab-quvvatlanmaydigan teglarni olib tashlash
    text = re.sub(r"<[^>]+>", "", text, flags=re.MULTILINE)

    # Ortiqcha bo‘sh qatorlarni tozalash
    text = re.sub(r"\n\n+", "\n\n", text)
    return text.strip()

# Matndan keraksiz gaplarni, linklarni va reklama iboralarini olib tashlash
def clean_post(text):
    text = re.sub(r"Forwarded from.*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"@[A-Za-z0-9_]+", "", text)
    text = re.sub(r"https?://t\.me/\S+", "", text)
    text = re.sub(r"подписывайтесь.*$", "", text, flags=re.MULTILINE | re.IGNORECASE)
    text = re.sub(r"подписаться.*$", "", text, flags=re.MULTILINE | re.IGNORECASE)
    text = re.sub(r"присоединяйтесь.*$", "", text, flags=re.MULTILINE | re.IGNORECASE)
    text = re.sub(r"подпишитесь\s*на\s*.*?\s*для\s*получения\s*дополнительной\s*информации\.?\s*$", "", text, flags=re.MULTILINE | re.IGNORECASE)
    text = re.sub(r"\bFTT\b", "", text, flags=re.IGNORECASE)
    text = re.sub(r"Хотите узнать больше?.*", "", text)
    text = re.sub(r"Подпишись на обновления.*", "", text)
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"(bit\.ly|linktr\.ee|taplink|exode|tgstation)\S*", "", text)
    text = re.sub(r"Hook:.*?\n", "", text, flags=re.MULTILINE | re.IGNORECASE)
    text = re.sub(r"Pravilno oformlenyye punkty, kotoryye doslovno povtoryayutsya i\.\.\..*", "", text, flags=re.MULTILINE | re.IGNORECASE)

    # Matnni jumlalarga bo'lish va har 2-3 jumlada bo'sh qator qo'shish
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    formatted_text = ""
    for i, sentence in enumerate(sentences):
        formatted_text += sentence.strip()
        if i < len(sentences) - 1:
            formatted_text += " "
            if (i + 1) % 3 == 0:
                formatted_text += "\n\n"

    formatted_text = re.sub(r"\n\n+", "\n\n", formatted_text)
    seen = set()
    result = []
    for line in formatted_text.split("\n"):
        if line.strip() and line not in seen:
            result.append(line)
            seen.add(line)
    return "\n".join(result).strip()

# Kiruvchi matnni gaplarga ajratish
def split_sentences(text):
    sentences = re.split(r'\.\s*', text.strip())
    return [s.strip() for s in sentences if s.strip()]

# Matnni faqat bitta hook bilan qayta yozish
def create_hook(text):
    lines = text.split("\n")
    if lines:
        hook = lines[0].strip()
        remaining_text = "\n".join(lines[1:]).strip()
        remaining_text = remaining_text.replace(hook, "", 1).strip()
        return hook, remaining_text
    return text, ""

# Prompt yaratish funksiyasi
def create_prompt(original_text, target, lang, shorten=False):
    formatted_text = "\n".join(split_sentences(original_text))
    # Tilni aniq ko‘rsatish va sifatli qayta yozish uchun qo‘shimcha ko‘rsatma
    lang_instruction = (
        "Javobni faqat o‘zbek tilida yoz, boshqa tillardan foydalanma. Agar kiruvchi matn boshqa tilda bo‘lsa, uni o‘zbek tiliga tarjima qil va qayta yoz. "
        "Matnni tabiiy, o‘qilishi oson va professional SMM postiga mos qilib qayta yoz. So‘zlarni mexanik tarzda tarjima qilishdan saqlan, o‘zbek tilida tabiiy va ravon bo‘lishiga e’tibor ber."
    ) if lang == "uz" else (
        "Ответ должен быть только на русском языке, не используй другие языки. Если исходный текст на другом языке, переведи его на русский и перепиши. "
        "Перепиши текст естественно, чтобы он читался легко и выглядел профессионально для SMM-поста."
    )

    if lang == "ru":
        if target in ["betrader", "betrader_uz"]:
            if shorten:
                return f"""
                Ты — профессиональный трейдер фондового рынка США, финансовый аналитик и креативный копирайтер со стажем. Проверь текст на орфографические, грамматические и стилистические ошибки и исправь их. Если в исходном тексте есть цитаты, обязательно используй их.

                Перепиши этот пост на русском языке, сделав его на 30-50% короче, но сохранив основной смысл:
                ---
                {formatted_text}
                ---
                {lang_instruction}
                Сделай его ярким, аналитичным, понятным. Начни с хука (выдели его жирным шрифтом с помощью ** и закрой **). Используй курсив (_ и закрой _) для акцента на ключевых идеях. Важные цифры или факты (например, проценты) выделяй жирным шрифтом (** и закрой **). Раздели текст на логические абзацы: после каждых 2-3 предложений добавляй пустую строку, чтобы текст выглядел структурированно и легко читался. Убери лишние ссылки, советы и упоминания других тг каналов. Удали фразы вроде "Подпишитесь на ... для получения дополнительной информации". Закончи призывом к действию, который должен быть в отдельном абзаце. Не используй HTML-теги, используй только Markdown-форматирование (** для жирного, _ для курсива).
                """
            return f"""
            Ты — профессиональный трейдер фондового рынка США, финансовый аналитик и креативный копирайтер со стажем. Проверь текст на орфографические, грамматические и стилистические ошибки и исправь их. Если в исходном тексте есть цитаты, обязательно используй их.

            Перепиши этот пост на русском языке:
            ---
            {formatted_text}
            ---
            {lang_instruction}
            Сделай его ярким, аналитичным, понятным, но не слишком длинным. Начни с хука (выдели его жирным шрифтом с помощью ** и закрой **). Используй курсив (_ и закрой _) для акцента на ключевых идеях. Важные цифры или факты (например, проценты) выделяй жирным шрифтом (** и закрой **). Раздели текст на логические абзацы: после каждых 2-3 предложений добавляй пустую строку, чтобы текст выглядел структурированно и легко читался. Убери лишние ссылки, советы и упоминания других тг каналов. Удали фразы вроде "Подпишитесь на ... для получения дополнительной информации". Закончи призывом к действию, который должен быть в отдельном абзаце. Не используй HTML-теги, используй только Markdown-форматирование (** для жирного, _ для курсива).
            """
        elif target == "firdavs":
            if shorten:
                return f"""
                Ты — профессиональный SMM менеджер и креативный копирайтер. Проверь текст на орфографические, грамматические и стилистические ошибки и исправь их. Если в исходном тексте есть цитаты, обязательно используй их.

                Перепиши этот пост на русском языке, сделав его на 30-50% короче, но сохранив основной смысл:
                ---
                {formatted_text}
                ---
                {lang_instruction}
                Сделай его ярким, аналитичным, понятным. Начни с хука (выдели его жирным шрифтом с помощью ** и закрой **). Используй курсив (_ и закрой _) для акцента на ключевых идеях. Важные цифры или факты (например, проценты) выделяй жирным шрифтом (** и закрой **). Раздели текст на логические абзацы: после каждых 2-3 предложений добавляй пустую строку, чтобы текст выглядел структурированно и легко читался. Убери лишние ссылки, советы и упоминания других тг каналов. Удали фразы вроде "Подпишитесь на ... для получения дополнительной информации". Закончи призывом к действию, который должен быть в отдельном абзаце. Не используй HTML-теги, используй только Markdown-форматирование (** для жирного, _ для курсива).
                """
            return f"""
            Ты — профессиональный SMM менеджер и креативный копирайтер. Проверь текст на орфографические, грамматические и стилистические ошибки и исправь их. Если в исходном тексте есть цитаты, обязательно используй их.

            Перепиши этот пост на русском языке:
            ---
            {formatted_text}
            ---
            {lang_instruction}
            Сделай его ярким, аналитичным, понятным, но не слишком длинным. Начни с хука (выдели его жирным шрифтом с помощью ** и закрой **). Используй курсив (_ и закрой _) для акцента на ключевых идеях. Важные цифры или факты (например, проценты) выделяй жирным шрифтом (** и закрой **). Раздели текст на логические абзацы: после каждых 2-3 предложений добавляй пустую строку, чтобы текст выглядел структурированно и легко читался. Убери лишние ссылки, советы и упоминания других тг каналов. Удали фразы вроде "Подпишитесь на ... для получения дополнительной информации". Закончи призывом к действию, который должен быть в отдельном абзаце. Не используй HTML-теги, используй только Markdown-форматирование (** для жирного, _ для курсива).
            """
    else:  # uz
        if target in ["betrader", "betrader_uz"]:
            if shorten:
                return f"""
                Sen — professional treyder, fond bozori bo‘yicha analitik va kreativ kopiraytersan. Matnni imlo, grammatika va stilistik xatolar uchun tekshir va tuzat. Agar matn ichida iqtiboslar bo‘lsa, ularni albatta ishlat.

                Quyidagi postni o‘zbek tilida 30-50% qisqartirib, lekin asosiy mazmunini saqlab qayta yoz:
                ---
                {formatted_text}
                ---
                {lang_instruction}
                Matnni SMM postiga mos qilib, qiziqarli va o‘qilishi oson qil. Hook bilan boshla (uni ** bilan qalin shrift bilan yoz va ** bilan yop). Asosiy fikrlarni ta’kidlash uchun kursiv (_ bilan boshla va _ bilan yop) ishlat. Muhim raqamlar yoki faktlarni (masalan, foizlarni) qalin shrift bilan (** bilan boshla va ** bilan yop) ajratib ko‘rsat. Matnni mantiqiy abzatslarga bo‘l: har 2-3 jumlada bo‘sh qator qoldirib, matn tuzilgan va o‘qish uchun qulay ko‘rinsin. Ortiqcha linklar, maslahatlar va boshqa tg kanallar haqidagi ma’lumotlarni olib tashla. "Obuna bo‘ling ... qo‘shimcha ma’lumot olish uchun" kabi iboralarni olib tashla. Oxirida CTA qo‘sh, u alohida abzatsda bo‘lsin. HTML teglarni ishlatma, faqat Markdown formatidan foydalan (** qalin shrift uchun, _ kursiv uchun).
                """
            return f"""
            Sen — professional treyder, fond bozori bo‘yicha analitik va kreativ kopiraytersan. Matnni imlo, grammatika va stilistik xatolar uchun tekshir va tuzat. Agar matn ichida iqtiboslar bo‘lsa, ularni albatta ishlat.

            Quyidagi postni o‘zbek tilida qayta yoz:
            ---
            {formatted_text}
            ---
            {lang_instruction}
            Matnni SMM postiga mos qilib, qiziqarli va o‘qilishi oson qil. Hook bilan boshla (uni ** bilan qalin shrift bilan yoz va ** bilan yop). Asosiy fikrlarni ta’kidlash uchun kursiv (_ bilan boshla va _ bilan yop) ishlat. Muhim raqamlar yoki faktlarni (masalan, foizlarni) qalin shrift bilan (** bilan boshla va ** bilan yop) ajratib ko‘rsat. Matnni mantiqiy abzatslarga bo‘l: har 2-3 jumlada bo‘sh qator qoldirib, matn tuzilgan va o‘qish uchun qulay ko‘rinsin. Matnni juda uzun qilma. Ortiqcha linklar, maslahatlar va boshqa tg kanallar haqidagi ma’lumotlarni olib tashla. "Obuna bo‘ling ... qo‘shimcha ma’lumot olish uchun" kabi iboralarni olib tashla. Oxirida CTA qo‘sh, u alohida abzatsda bo‘lsin. HTML teglarni ishlatma, faqat Markdown formatidan foydalan (** qalin shrift uchun, _ kursiv uchun).
            """
        elif target == "firdavs":
            if shorten:
                return f"""
                Sen — professional SMM menejersan va kreativ kopiraytersan. Matnni imlo, grammatika va stilistik xatolar uchun tekshir va tuzat. Agar matn ichida iqtiboslar bo‘lsa, ularni albatta ishlat.

                Quyidagi postni o‘zbek tilida 30-50% qisqartirib, lekin asosiy mazmunini saqlab qayta yoz:
                ---
                {formatted_text}
                ---
                {lang_instruction}
                Matnni SMM postiga mos qilib, qiziqarli va o‘qilishi oson qil. Hook bilan boshla (uni ** bilan qalin shrift bilan yoz va ** bilan yop). Asosiy fikrlarni ta’kidlash uchun kursiv (_ bilan boshla va _ bilan yop) ishlat. Muhim raqamlar yoki faktlarni (masalan, foizlarni) qalin shrift bilan (** bilan boshla va ** bilan yop) ajratib ko‘rsat. Matnni mantiqiy abzatslarga bo‘l: har 2-3 jumlada bo‘sh qator qoldirib, matn tuzilgan va o‘qish uchun qulay ko‘rinsin. Ortiqcha linklar, maslahatlar va boshqa tg kanallar haqidagi ma’lumotlarni olib tashla. "Obuna bo‘ling ... qo‘shimcha ma’lumot olish uchun" kabi iboralarni olib tashla. Oxirida CTA qo‘sh, u alohida abzatsda bo‘lsin. HTML teglarni ishlatma, faqat Markdown formatidan foydalan (** qalin shrift uchun, _ kursiv uchun).
                """
            return f"""
            Sen — professional SMM menejersan va kreativ kopiraytersan. Matnni imlo, grammatika va stilistik xatolar uchun tekshir va tuzat. Agar matn ichida iqtiboslar bo‘lsa, ularni albatta ishlat.

            Quyidagi postni o‘zbek tilida qayta yoz:
            ---
            {formatted_text}
            ---
            {lang_instruction}
            Matnni SMM postiga mos qilib, qiziqarli va o‘qilishi oson qil. Hook bilan boshla (uni ** bilan qalin shrift bilan yoz va ** bilan yop). Asosiy fikrlarni ta’kidlash uchun kursiv (_ bilan boshla va _ bilan yop) ishlat. Muhim raqamlar yoki faktlarni (masalan, foizlarni) qalin shrift bilan (** bilan boshla va ** bilan yop) ajratib ko‘rsat. Matnni mantiqiy abzatslarga bo‘l: har 2-3 jumlada bo‘sh qator qoldirib, matn tuzilgan va o‘qish uchun qulay ko‘rinsin. Matnni juda uzun qilma. Ortiqcha linklar, maslahatlar va boshqa tg kanallar haqidagi ma’lumotlarni olib tashla. "Obuna bo‘ling ... qo‘shimcha ma’lumot olish uchun" kabi iboralarni olib tashla. Oxirida CTA qo‘sh, u alohida abzatsda bo‘lsin. HTML teglarni ishlatma, faqat Markdown formatidan foydalan (** qalin shrift uchun, _ kursiv uchun).
            """

    # Spoiler uchun || markasi ishlatiladi
    text = text.replace("||", "")  # ||spoiler||'larni tekshirib o'zgartirish
    
    return text.strip()
        
async def handle_all_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg.text and not msg.caption and not msg.media_group_id:
        lang = context.user_data.get("lang", "uz")
        await msg.reply_text(MESSAGES[lang]["no_text"])
        return

    # Media groupni aniqlash
    media_group_id = msg.media_group_id
    if media_group_id:
        # Agar media group mavjud bo'lsa, bularni to'plam sifatida saqlaymiz
        if "media_group" not in context.user_data:
            context.user_data["media_group"] = []
        context.user_data["media_group"].append({
            "photo": msg.photo[-1].file_id if msg.photo else None,
            "video": msg.video.file_id if msg.video else None,
            "caption": msg.caption
        })

        # Agar bu media groupdagi birinchi xabar bo'lsa, kanalni tanlashni so'raymiz
        if len(context.user_data["media_group"]) == 1:
            lang = context.user_data.get("lang", "uz")
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton(MESSAGES[lang]["betrader_uz_button"], callback_data="target_betrader_uz")],
                [InlineKeyboardButton(MESSAGES[lang]["firdavs_button"], callback_data="target_firdavs")]
            ])
            await msg.reply_text(MESSAGES[lang]["choose_channel"], reply_markup=keyboard)

        context.user_data["original_text"] = msg.caption or context.user_data.get("original_text", "")
        return
    else:
        # Agar bu oddiy rasm yoki video bo'lsa, uni saqlaymiz
        context.user_data["media_group"] = None
        context.user_data["photo"] = msg.photo[-1].file_id if msg.photo else None
        context.user_data["video"] = msg.video.file_id if msg.video else None

    lang = context.user_data.get("lang", "uz")
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(MESSAGES[lang]["betrader_uz_button"], callback_data="target_betrader_uz")],
        [InlineKeyboardButton(MESSAGES[lang]["firdavs_button"], callback_data="target_firdavs")]
    ])

    await msg.reply_text(MESSAGES[lang]["choose_channel"], reply_markup=keyboard)
    context.user_data["original_text"] = msg.text or msg.caption or ""

# Postni tasdiqlash yoki yuborish
async def handle_confirm_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    target = context.user_data.get("target")
    lang = context.user_data.get("lang", "uz")
    media_group = context.user_data.get("media_group")
    photo = context.user_data.get("photo")
    video = context.user_data.get("video")
    final_text = context.user_data.get("final_text")

    if target == "betrader":
        channel_id = CHANNEL_BETRADER
    elif target == "betrader_uz":
        channel_id = CHANNEL_BETRADER_UZ
    else:
        channel_id = CHANNEL_FIRDAVS

    try:
        if media_group:
            media = []
            for item in media_group:
                if item["photo"]:
                    media.append(InputMediaPhoto(media=item["photo"], caption=final_text if not media else "", parse_mode="HTML"))
                elif item["video"]:
                    media.append(InputMediaVideo(media=item["video"], caption=final_text if not media else "", parse_mode="HTML"))
            await context.bot.send_media_group(chat_id=channel_id, media=media)
        elif photo:
            await context.bot.send_photo(chat_id=channel_id, photo=photo, caption=final_text, parse_mode="HTML")
        elif video:
            await context.bot.send_video(chat_id=channel_id, video=video, caption=final_text, parse_mode="HTML")
        else:
            await context.bot.send_message(chat_id=channel_id, text=final_text, parse_mode="HTML")

        await query.message.reply_text(MESSAGES[lang]["posted"])
    except Exception as e:
        await query.message.reply_text(MESSAGES[lang]["post_error"].format(error=e))

async def handle_target_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    target = query.data.replace("target_", "")
    context.user_data["target"] = target

    lang = context.user_data.get("lang", "uz")
    print(f"handle_target_choice: lang={lang}")
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(MESSAGES[lang]["uz_button"], callback_data="lang_uz")],
        [InlineKeyboardButton(MESSAGES[lang]["ru_button"], callback_data="lang_ru")]
    ])
    await query.message.reply_text(MESSAGES[lang]["choose_language"], reply_markup=keyboard)

async def handle_language_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.replace("lang_", "")
    context.user_data["lang"] = lang
    print(f"handle_language_choice: lang={lang}")
    await process_text(update, context)

# -*- coding: utf-8 -*-
import os
import re
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, InputMediaVideo
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CallbackQueryHandler, filters
from openai import OpenAI

# Load config
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

CHANNEL_BETRADER = -1002431616018
CHANNEL_BETRADER_UZ = -1002468278246
CHANNEL_FIRDAVS = -1002383272008

client = OpenAI(api_key=OPENAI_API_KEY)

# Xabarlarni tillarga ko'ra sozlash
MESSAGES = {
    "uz": {
        "no_text": "❌ Bu xabarda matn yo‘q.",
        "choose_channel": "Qaysi kanal uchun post tayyorlaymiz?",
        "choose_language": "Endi tilni tanlang:",
        "processing": "✅ Tanlangan til: {lang}\n\n⏳ Matn qayta yozilmoqda...",
        "posted": "✅ Post kanalga joylandi!",
        "post_error": "❌ Postni kanalga joylashda xatolik: {error}",
        "gpt_error": "❌ GPT xatosi: {error}",
        "too_long_error": "⚠️ Matn juda uzun, qisqartirib qayta yozilmoqda...",
        "betrader_button": "📈 BeTrader uchun",
        "betrader_uz_button": "📈 @Betrader_uz",
        "firdavs_button": "📊 FirdavsUrinov uchun",
        "uz_button": "🇺🇿 O'zbek tili",
        "ru_button": "🇷🇺 Русский язык",
        "confirm_button": "✅ Kanalga joylash",
        "rewrite_button": "🔄 Qayta yozish",
        "shorten_button": "✂️ Qisqaroq yozish"
    },
    "ru": {
        "no_text": "❌ В этом сообщении нет текста.",
        "choose_channel": "Для какого канала готовим пост?",
        "choose_language": "Теперь выберите язык:",
        "processing": "✅ Выбранный язык: {lang}\n\n⏳ Текст переписывается...",
        "posted": "✅ Пост размещен в канале!",
        "post_error": "❌ Ошибка при размещении поста в канал: {error}",
        "gpt_error": "❌ Ошибка GPT: {error}",
        "too_long_error": "⚠️ Текст слишкzом длинный, переписывается короче...",
        "betrader_button": "📈 Для BeTrader",
        "betrader_uz_button": "📈 @Betrader_uz",
        "firdavs_button": "📊 Для FirdavsUrinov",
        "uz_button": "🇺🇿 Узбекский язык",
        "ru_button": "🇷🇺 Русский язык",
        "confirm_button": "✅ Разместить в канал",
        "rewrite_button": "🔄 Переписать",
        "shorten_button": "✂️ Сократить"
    }
}

# Matndan keraksiz gaplarni, linklarni va reklama iboralarini olib tashlash
def clean_post(text):
    text = re.sub(r"Forwarded from.*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"@[A-Za-z0-9_]+", "", text)
    text = re.sub(r"https?://t\.me/\S+", "", text)
    text = re.sub(r"подписывайтесь.*$", "", text, flags=re.MULTILINE | re.IGNORECASE)
    text = re.sub(r"подписаться.*$", "", text, flags=re.MULTILINE | re.IGNORECASE)
    text = re.sub(r"присоединяйтесь.*$", "", text, flags=re.MULTILINE | re.IGNORECASE)
    text = re.sub(r"подпишитесь\s*на\s*.*?\s*для\s*получения\s*дополнительной\s*информации\.?\s*$", "", text, flags=re.MULTILINE | re.IGNORECASE)
    text = re.sub(r"\bFTT\b", "", text, flags=re.IGNORECASE)
    text = re.sub(r"Хотите узнать больше?.*", "", text)
    text = re.sub(r"Подпишись на обновления.*", "", text)
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"(bit\.ly|linktr\.ee|taplink|exode|tgstation)\S*", "", text)
    text = re.sub(r"Hook:.*?\n", "", text, flags=re.MULTILINE | re.IGNORECASE)
    text = re.sub(r"Pravilno oformlenyye punkty, kotoryye doslovno povtoryayutsya i\.\.\..*", "", text, flags=re.MULTILINE | re.IGNORECASE)

    # Matnni jumlalarga bo'lish va har 2-3 jumlada bo'sh qator qo'shish
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    formatted_text = ""
    for i, sentence in enumerate(sentences):
        formatted_text += sentence.strip()
        if i < len(sentences) - 1:
            formatted_text += " "
            if (i + 1) % 3 == 0:
                formatted_text += "\n\n"

    formatted_text = re.sub(r"\n\n+", "\n\n", formatted_text)
    seen = set()
    result = []
    for line in formatted_text.split("\n"):
        if line.strip() and line not in seen:
            result.append(line)
            seen.add(line)
    return "\n".join(result).strip()

# Matnni faqat bitta hook bilan qayta yozish
def create_hook(text):
    lines = text.split("\n")
    if lines:
        hook = lines[0].strip()
        remaining_text = "\n".join(lines[1:]).strip()
        remaining_text = remaining_text.replace(hook, "", 1).strip()
        return hook, remaining_text
    return text, ""

# Matnni Markdown V1 formatida tozalash
def clean_markdown(text):
    text = text.replace("**", "")  # qalin shriftlar alohida qo‘shilyapti
    # * * va _ _ ikkalasini ham italik sifatida aniqlash
    text = re.sub(r"\*(.*?)\*|_(.*?)_", r"<i>\1\2</i>", text)  # italikni HTMLga o‘zgartirish
    text = text.replace("`", "``")
    text = text.replace("||", "")
    return text.strip()

# --- YORDAMCHI FUNKSIYALAR ---
def get_keywords(lang, target):
    if lang == "uz":
        return trading_keywords_uz if target in ["betrader", "betrader_uz"] else smm_keywords_uz
    else:
        return trading_keywords_ru if target in ["betrader", "betrader_uz"] else smm_keywords_ru

def emphasize_keywords(text, keywords):
    for kw in sorted(keywords, key=lambda k: -len(k)):
        pattern = re.compile(rf'(?<!<b>)\b({re.escape(kw)})\b(?!</b>)', re.IGNORECASE)
        text = pattern.sub(r'<b>\1</b>', text)
    return text

def add_line_breaks_every_2_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    new_text = ""
    for i, s in enumerate(sentences):
        new_text += s.strip() + " "
        if (i + 1) % 2 == 0:
            new_text += "\n\n"
    return new_text.strip()

def format_hook(text):
    lines = text.strip().split("\n")
    if lines:
        hook = lines[0].strip()
        body = "\n".join(lines[1:]).strip()
        return f"<b>{hook}</b>\n\n{body}"
    return text

# --- ASOSIY QAYTA ISHLASH FUNKSIYASI (GPT javobi ustida ishlatiladi) ---
def full_formatting_pipeline(gpt_text, lang, target):
    keywords = get_keywords(lang, target)
    text = gpt_text.strip()
    text = emphasize_keywords(text, keywords)
    text = add_line_breaks_every_2_sentences(text)
    text = format_hook(text)
    return text.strip()

# Kiruvchi matnni qayta ishlash
async def process_text(update: Update, context: ContextTypes.DEFAULT_TYPE, shorten=False):
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get("lang", "uz")
    print(f"process_text: lang={lang}")
    original_text = context.user_data.get("original_text")
    target = context.user_data.get("target")
    media_group = context.user_data.get("media_group")
    photo = context.user_data.get("photo")
    video = context.user_data.get("video")

    await query.message.reply_text(MESSAGES[lang]["processing"].format(lang=lang.upper()))

    try:
        prompt = create_prompt(original_text, target, lang, shorten=shorten)
        print(f"Prompt: {prompt}")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        new_text = response.choices[0].message.content.strip()
        print(f"GPT response: {new_text}")

        if new_text.strip() == original_text.strip():
            raise Exception("GPT matnni qayta yozmadi, iltimos qayta urinib ko‘ring.")

        # Matnni tozalash
        # To‘liq formatlash pipeline
        clean_text = full_formatting_pipeline(new_text, lang, target)

        # Birinchi qatorni aniqlash va Markdown formatida qalin qilish
        lines = clean_text.split("\n")
        if lines:
            first_line = lines[0].strip()
            remaining_lines = "\n".join(lines[1:]).strip() if len(lines) > 1 else ""
            clean_text = f"**{first_line}**\n\n{remaining_lines}"

        # Markdown uchun matnni tozalash
        clean_text = clean_markdown(clean_text)

        # Matnni qisqartirish
        clean_text = truncate_text(clean_text, limit=1000)

        # Final post uchun tahrirlar (Markdown formatida link qo'shish)
        if target == "betrader":
            clean_text += '\n\n<a href="https://t.me/betrader_uz">Be Trader – Команда профессиональных трейдеров</a>'
        elif target == "betrader_uz":
            clean_text += '\n\n<a href="https://t.me/Betrader_uz">Betrader_uz – Команда профессиональных трейдеров</a>'
        else:
            clean_text += '\n\n<a href="https://t.me/firdavsurinov">SMM: Firdavs Urinov</a>'

        print(f"Final text before sending to Telegram: {clean_text}")

        context.user_data["final_text"] = clean_text

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(MESSAGES[lang]["confirm_button"], callback_data="confirm_post")],
            [InlineKeyboardButton(MESSAGES[lang]["rewrite_button"], callback_data="rewrite_post"),
             InlineKeyboardButton(MESSAGES[lang]["shorten_button"], callback_data="shorten_post")]
        ])

        if media_group:
            media = []
            for item in media_group:
                if item["photo"]:
                    media.append(InputMediaPhoto(media=item["photo"], caption=clean_text if not media else "", parse_mode="HTML"))
                elif item["video"]:
                    media.append(InputMediaVideo(media=item["video"], caption=clean_text if not media else "", parse_mode="HTML"))
            await query.message.reply_media_group(media=media)
            await query.message.reply_text("Postni tasdiqlang:" if lang == "uz" else "Подтвердите пост:", reply_markup=keyboard)
        elif photo:
            await query.message.reply_photo(photo=photo, caption=clean_text, parse_mode="HTML", reply_markup=keyboard)
        elif video:
            await query.message.reply_video(video=video, caption=clean_text, parse_mode="HTML", reply_markup=keyboard)
        else:
            await query.message.reply_text(clean_text, parse_mode="HTML", reply_markup=keyboard)

    except Exception as e:
        if "Message caption is too long" in str(e):
            await query.message.reply_text(MESSAGES[lang]["too_long_error"])
            context.user_data["shorten"] = True
            await process_text(update, context, shorten=True)
        else:
            await query.message.reply_text(MESSAGES[lang]["gpt_error"].format(error=e))

async def handle_rewrite_or_shorten(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    action = query.data
    shorten = action == "shorten_post"
    await process_text(update, context, shorten=shorten)

    try:
        if media_group:
            media = []
            for item in media_group:
                if item["photo"]:
                    media.append(InputMediaPhoto(media=item["photo"], caption=final_text if not media else "", parse_mode="HTML"))
                elif item["video"]:
                    media.append(InputMediaVideo(media=item["video"], caption=final_text if not media else "", parse_mode="HTML"))
            await context.bot.send_media_group(chat_id=channel_id, media=media)
        elif photo:
            await context.bot.send_photo(chat_id=channel_id, photo=photo, caption=final_text, parse_mode="HTML")
        elif video:
            await context.bot.send_video(chat_id=channel_id, video=video, caption=final_text, parse_mode="HTML")
        else:
            await context.bot.send_message(chat_id=channel_id, text=final_text, parse_mode="HTML")

        await query.message.reply_text(MESSAGES[lang]["posted"])
    except Exception as e:
        await query.message.reply_text(MESSAGES[lang]["post_error"].format(error=e))

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT | filters.CAPTION | filters.PHOTO | filters.VIDEO, handle_all_messages))
    app.add_handler(CallbackQueryHandler(handle_target_choice, pattern="^target_"))
    app.add_handler(CallbackQueryHandler(handle_language_choice, pattern="^lang_"))
    app.add_handler(CallbackQueryHandler(handle_rewrite_or_shorten, pattern="^(rewrite_post|shorten_post)$"))
    app.add_handler(CallbackQueryHandler(handle_confirm_post, pattern="^confirm_post$"))
    print("Bot ishga tushdi...")
    app.run_polling()