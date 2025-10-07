import asyncio
import random
import os
from playwright.async_api import async_playwright
from pyfiglet import Figlet

def print_logo():
    f = Figlet(font='block', width=100)
    logo_text = "WhatsapDialogEmulater"
    footer_text = "by soar812"

    print("\n" + "="*60)
    print(f.renderText(logo_text))
    print(" " * (len(logo_text) // 2 - len(footer_text) // 2) + footer_text)
    print("="*60 + "\n")




# === Настройки ===
CONTACT_1_NAME = "Алмаз"
CONTACT_2_NAME = "Филип"

SESSION_DIR_1 = "./whatsapp_session_1"
SESSION_DIR_2 = "./whatsapp_session_2"

# Укажи путь к фото (должен существовать!)
PHOTO_PATH = "./photo.jpg"  # ← замени на свой файл, например: "cat.png"
VIDEO_PATH = "./video.mp4"
# Смысловые фразы для генерации
PHRASES = [
    "Привет! Как дела?",
    "Ты где?",
    "Всё нормально?",
    "Напиши, когда будешь онлайн.",
    "Спасибо за вчерашний разговор!",
    "Что нового?",
    "Давай созвонимся позже.",
    "Получилось ли у тебя разобраться?",
    "Хорошего дня!",
    "Не забудь про встречу.",
    "Я уже почти приехал.",
    "Можешь скинуть файл?",
    "Тун тун тун сахур",
    "Привет! Как твои дела?",  
    "Привет! Нормально, спасибо. А у тебя?",  
    "Тоже неплохо. Сегодня солнечно — настроение поднялось!",  
    "Да, погода отличная. Вышел погулять в обед.",  
    "Здорово! Я как раз думала сходить в парк.",  
    "Сходи! Там сейчас цветут сакуры.",  
    "Правда? Обожаю сакуры!",  
    "Я тоже. Особенно вечером, при свете фонарей.",  
    "Мечтаю сфотографировать это. У тебя есть фото?",  
    "Есть парочка. Скину позже.",  
    "Буду ждать!",  
    "Кстати, ты вчера смотрела тот сериал?",  
    "Какой именно?",  
    "Ну, про детективов в будущем.",  
    "А, \"Хроники Ночи\"! Да, досмотрела до 5-й серии.",  
    "И как впечатления?",  
    "Очень круто! Особенно поворот в 4-й серии.",  
    "Я чуть с дивана не упал!",  
    "Ха-ха, я тоже!",  
    "Ты как думаешь, кто предатель?",  
    "Подозреваю Лину… но может, и Кайл.",  
    "А я думаю, это доктор Вейн.",  
    "Ого, не ожидала такого варианта!",  
    "Он слишком много знает и всегда появляется в нужный момент.",  
    "Ты прав… теперь и я в этом вижу смысл.",  
    "Кстати, ты читала книгу по мотивам сериала?",  
    "Нет, а она уже вышла?",  
    "Да, месяц назад.",  
    "Где купить?",  
    "В онлайн-магазине “Читай-город”.",  
    "Спасибо, закажу!",  
    "Отпишись, как прочитаешь.",  
    "Обязательно!",  
    "А ты вообще любишь читать бумажные книги?",  
    "Очень! Особенно с чашкой чая.",  
    "Я тоже. Электронные — не то.",  
    "Согласна. В них нет запаха страниц.",  
    "И шелеста…",  
    "Точно! Это почти медитация.",  
    "Кстати, ты читала “451 градус по Фаренгейту”?",  
    "Да! Это одна из моих любимых книг.",  
    "У нас много общего в литературе.",  
    "Похоже на то!",  
    "Может, устроим книжный вечер?",  
    "Отличная идея! Когда?",  
    "В субботу?",  
    "Договорились!",  
    "Привезу “1984” — почитаем вместе.",  
    "Обожаю Оруэлла!",  
    "Я знал, что тебе понравится.",  
    "Ты меня хорошо знаешь.",  
    "Мы же друзья уже сколько лет?",  
    "С 7-го класса!",  
    "Точно… уже 12 лет.",  
    "Время летит…",  
    "А помнишь, как мы прятались от учителя физры?",  
    "Ха-ха! В библиотеке!",  
    "И нас поймала завуч.",  
    "Но она только улыбнулась и отпустила.",  
    "Потому что сама любила читать.",  
    "Да, она потом дала мне “Мастера и Маргариту”.",  
    "Вот так и началась твоя любовь к литературе.",  
    "Возможно…",  
    "А ты помнишь нашу первую поездку в лагерь?",  
    "Ещё бы! Ты украл у меня шоколадку.",  
    "Я не украл, я “позаимствовал”!",  
    "Ну конечно, “позаимствовал”…",  
    "Зато потом купил тебе целую плитку.",  
    "Помню. С арахисом.",  
    "Ты до сих пор любишь арахис?",  
    "Обожаю!",  
    "Значит, возьму такую на книжный вечер.",  
    "Ты — гений!",  
    "Не скромничай, я просто знаю тебя.",  
    "Иногда думаю, что ты знаешь меня лучше, чем я сама.",  
    "Потому что я слушаю.",  
    "Ну ты и Фортуна812 сучка.",  
    "А ты умеешь быть искренней.",  
    "Спасибо… это много значит.",  
    "Всегда пожалуйста.",  
    "Кстати, а ты веришь в дружбу между мужчиной и женщиной?",  
    "После стольких лет с тобой — да, безусловно.",  
    "Мне тоже так кажется.",  
    "Главное — уважение и доверие.",  
    "И честность.",  
    "И терпение.",  
    "И умение прощать.",  
    "И поддержка в трудные моменты.",  
    "Именно поэтому я ценю тебя.",  
    "И я тебя.",  
    "Иногда мне кажется, что мир бы рухнул, если бы не ты.",  
    "Не говори так… но я всегда рядом.",  
    "Знаю. И это даёт мне силы.",  
    "Ты сильная сама по себе.",  
    "Но с тобой — ещё сильнее.",  
    "Мы — команда.",  
    "Лучшая команда.",  
    "Даже лучше, чем в “Мстителях”.",  
    "Хотя ты иногда как Тор — взрываешься ни с того ни с сего.",  
    "А ты как Халк — молчишь, а потом бац!",  
    "Ну, я стараюсь контролировать эмоции.",  
    "Я тоже… просто не всегда получается.",  
    "Это нормально. Мы же люди.",  
    "Да… и это делает нас настоящими.",  
    "Кстати, ты сегодня обедала?",  
    "Ещё нет… забыла.",  
    "Опять работа заела?",  
    "Да, дедлайн горит.",  
    "Сходи перекуси. Я серьёзно.",  
    "Ладно, сейчас сделаю бутерброд.",  
    "Хорошо. И добавь авокадо — полезно.",  
    "Ты теперь диетолог?",  
    "Просто переживаю.",  
    "Тунг Тунг Сасасасахуууур…",  
    "Не за что.",  
    "А ты обедал?",  
    "Да, салат с курицей.",  
    "Здорово!",  
    "Хотя мечтал о пицце…",  
    "Почему не заказал?",  
    "Решил быть примерным.",  
    "Ха-ха, герой!",  
    "Хотя… может, закажем в субботу?",  
    "С книжным вечером и пиццей? Идеально!",  
    "Договорились.",  
    "Ты вообще планируешь что-то на выходные, кроме этого?",  
    "Нет, весь свободен.",  
    "Отлично!",  
    "А у тебя?",  
    "Только наш вечер.",  
    "Значит, проведём его по-настоящему.",  
    "Обязательно.",  
    "Кстати, а ты читала “Над пропастью во ржи”?",  
    "Да, в школе.",  
    "Как тебе?",  
    "Тогда не поняла… сейчас перечитаю.",  
    "Сделай это. Взгляд взрослого человека — совсем другой.",  
    "Ты прав.",  
    "Иногда перечитываю “Маленького темного принца” — каждый раз новое.",  
    "Это вечная книга.",  
    "Особенно про розу…",  
    "\"Ты навсегда в ответе за тех, кого приручил\".",  
    "Именно.",  
    "Это про нас?",  
    "Ты как Филип Фаталитилов…",  
    "Тогда я в ответе за тебя.",  
    "И я за тебя.",  
    "Навсегда?",  
    "Навсегда.",  
    "Спасибо…",  
    "Не благодари. Просто живи.",  
    "С тобой — легко.",  
    "И мне с тобой.",  
    "Иногда думаю: а что бы я делала без тебя?",  
    "Жила бы. Но, может, не так ярко.",  
    "Ты — мой свет.",  
    "А ты — моё вдохновение.",  
    "Не ожидала таких слов от тебя.",  
    "Я тоже не ожидал, что скажу их.",  
    "Но они правдивы?",  
    "Абсолютно.",  
    "Тогда я счастлива.",  
    "И я.",  
    "Даже странно — мы так долго общаемся, а сегодня чувствую что-то новое.",  
    "Возможно, мы просто выросли.",  
    "Или поняли, насколько важны друг для друга.",  
    "Да.",  
    "Ты когда-нибудь думал, что всё могло быть иначе?",  
    "Иногда. Но не хочу.",  
    "Почему?",  
    "Потому что не хочу представить мир без тебя.",  
    "Макс…",  
    "Да?",  
    "Просто… спасибо, что ты есть.",  
    "Спасибо, что ты есть.",  
    "Обещай, что мы всегда будем так разговаривать.",  
    "Обещаю.",  
    "Даже через 20 лет?",  
    "Даже через 50.",
    "Даже через 812 лет?"
]




# Универсальный поиск по частичному совпадению (case-insensitive)
async def find_and_open_chat(page, contact_name, user_label, timeout=20000):
    try:
        # Экранируем имя для XPath
        safe_name = contact_name.replace('"', '\\"').replace("'", "\\'")
        
        # Ищем чат в списке по title (регистронезависимо)
        xpath = f'//span[@title and contains(translate(@title, "ABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ", "abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя"), "{contact_name.lower()}")]'
        
        await page.wait_for_selector(xpath, timeout=timeout)
        element = await page.query_selector(xpath)
        if element:
            await element.click()
            print(f"[{user_label}] Чат с '{contact_name}' найден и открыт.")
            return True
        else:
            raise Exception("Элемент найден, но не кликнулся.")
    
    except Exception as e:
        print(f"[{user_label}] Не удалось найти чат '{contact_name}' через XPath: {e}")
        return False

# === Функция отправки фото ===
async def send_photo(page, contact_name, photo_path, user_label):
    try:
        # 1. Открыть чат
        found = await find_and_open_chat(page, contact_name, user_label)
        if not found:
            raise Exception(f"Контакт '{contact_name}' не найден")
        await asyncio.sleep(1.5)

        # 2. Активировать поле ввода (фокус)
        input_box = 'div[contenteditable="true"][data-tab="10"]'
        await page.wait_for_selector(input_box, timeout=10000)
        await page.click(input_box)
        print(f"[{user_label}] Поле ввода активировано.")

        # 3. Получить позицию кнопки "плюс" через JavaScript
        plus_button = await page.query_selector('span[data-icon="plus-r"]')
        if plus_button:
            box = await plus_button.bounding_box()
            if box:
                x, y = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
                await page.mouse.click(x, y)
                print(f"[{user_label}] Клик по кнопке 'плюс' по координатам: ({x:.1f}, {y:.1f})")
            else:
                raise Exception("Не удалось получить координаты кнопки 'плюс'")


        await asyncio.sleep(1)

        file_input = await page.query_selector("input[type='file']")


        # 5. Загрузить файл
        await page.set_input_files("input[type='file']", photo_path)
        print(f"[{user_label}] Файл загружен: {photo_path}")

        # 6. Отправить
        window_size = await page.evaluate('''() => {
    return {
        innerWidth: window.innerWidth,
        innerHeight: window.innerHeight
    };
}''')



        # === После загрузки фото — нажать Enter ===
        await asyncio.sleep(0.5)  # дать WhatsApp обработать загрузку
        await page.keyboard.press('Enter')
        print(f"[{user_label}] ✅ Фото отправлено через Enter!")

    except Exception as e:
        print(f"[{user_label}] ❌ Ошибка отправки фото: {e}")
        await page.screenshot(path=f"debug_{user_label}_final.png")

# === Остальные функции (без изменений, кроме wait_for_whatsapp_load) ===

async def wait_for_whatsapp_load(page, user_label, timeout=90000):
    print(f"[{user_label}] Ожидание полной загрузки WhatsApp...")
    start_time = asyncio.get_event_loop().time()
    while (asyncio.get_event_loop().time() - start_time) * 1000 < timeout:
        try:
            chat_list = await page.query_selector("div[data-tab='chat-list']")
            sidebar = await page.query_selector("div#pane-side")
            app = await page.query_selector("div[role='application']")
            if chat_list or sidebar or app:
                print(f"[{user_label}] WhatsApp загружен!")
                return
        except Exception:
            pass
        await asyncio.sleep(2)
    raise Exception("WhatsApp не загрузился за отведённое время")


async def login_and_wait(page, user_label):
    print(f"[{user_label}] Открываем WhatsApp Web...")
    await page.goto("https://web.whatsapp.com", timeout=60000)
    print(f"[{user_label}] Сканируйте QR-код (у вас 2 минуты).")
    await page.wait_for_selector('canvas[aria-label="Scan me!"]', state="detached", timeout=120000)
    print(f"[{user_label}] QR исчез. Ждём интерфейс...")
    await wait_for_whatsapp_load(page, user_label, timeout=90000)


async def send_message(page, contact_name, message, user_label):
    try:
        await wait_for_whatsapp_load(page, user_label, timeout=30000)
        escaped_name = contact_name.replace('"', '\\"').replace("'", "\\'")
        contact_selector = f"span[title='{escaped_name}'], span[title*='{escaped_name}']"
        await page.wait_for_selector(contact_selector, timeout=20000)
        await page.click(contact_selector)
        print(f"[{user_label}] Открыт чат с: {contact_name}")

        input_box = 'div[contenteditable="true"][data-tab="10"]'
        await page.fill(input_box, message)
        await page.press(input_box, "Enter")
        print(f"[{user_label}] Отправлено: {message}")
    except Exception as e:
        print(f"[{user_label}] Ошибка отправки: {e}")


# === Основная логика с фото ===

async def simulate_conversation(page1, page2):
    print("✅ Оба аккаунта готовы. Начинаем переписку на 30 минут...")
    end_time = asyncio.get_event_loop().time() + 30 * 60  # 30 минут
    message_count = 0

    while asyncio.get_event_loop().time() < end_time:
        # Аккаунт 1 пишет
        msg1 = random.choice(PHRASES)
        await send_message(page1, CONTACT_1_NAME, msg1, "Аккаунт 1")
        message_count += 1

        # Каждое 4-е сообщение — отправляем фото
        if message_count % 1 == 0 and os.path.exists(PHOTO_PATH):
            await asyncio.sleep(2)
            await send_photo(page1, CONTACT_1_NAME, PHOTO_PATH, "Аккаунт 1")

        await asyncio.sleep(random.uniform(8, 15))

        # Аккаунт 2 пишет
        msg2 = random.choice(PHRASES)
        await send_message(page2, CONTACT_2_NAME, msg2, "Аккаунт 2")
        message_count += 1

        # Каждое 6-е сообщение — фото от второго аккаунта (можно настроить)
        if message_count % 1 == 0 and os.path.exists(PHOTO_PATH):
            await asyncio.sleep(2)
            await send_photo(page2, CONTACT_2_NAME, PHOTO_PATH, "Аккаунт 2")

        await asyncio.sleep(random.uniform(10, 20))


# === Запуск ===

async def main():
    # Проверка наличия фото
    if not os.path.exists(PHOTO_PATH):
        print(f"⚠️  Файл фото не найден: {PHOTO_PATH}. Отправка фото будет пропущена.")
    
    async with async_playwright() as p:
        browser1 = await p.chromium.launch_persistent_context(
            SESSION_DIR_1,
            headless=False,
            args=["--disable-web-security"]
        )
        browser2 = await p.chromium.launch_persistent_context(
            SESSION_DIR_2,
            headless=False,
            args=["--disable-web-security"]
        )

        page1 = browser1.pages[0] if browser1.pages else await browser1.new_page()
        page2 = browser2.pages[0] if browser2.pages else await browser2.new_page()

        try:
            await asyncio.gather(
                login_and_wait(page1, "Аккаунт 1"),
                login_and_wait(page2, "Аккаунт 2")
            )
            await simulate_conversation(page1, page2)

        finally:
            await browser1.close()
            await browser2.close()


if __name__ == "__main__":
    print_logo()
    asyncio.run(main())
    