import asyncio
import random
import os
from playwright.async_api import async_playwright
from pyfiglet import Figlet
import subprocess

def print_logo():
    f = Figlet(font='block', width=100)
    logo_text = "WЫWaring"
    footer_text = "by soar812"

    print("\n" + "="*60)
    rendered_logo = f.renderText(logo_text)
    print(rendered_logo, end='')  # ← убираем лишний \n от print
    # Центрируем footer по ширине терминала или по максимальной строке логотипа
    max_line_width = max(len(line) for line in rendered_logo.splitlines())
    padding = " " * ((max_line_width - len(footer_text)) // 2)
    print(padding + footer_text)
    print("="*60 + "\n")
    
def random_picture():
        pic1 = "./photo.jpg"
        pic2 = "./photo_2025-10-07_16-41-56.jpg"
        pic3 = "./photo_2025-10-07_16-42-09.jpg"
        pic4 = "./photo_2025-10-07_16-42-13.jpg"
        pic5 = "./photo_2025-10-07_16-42-15.jpg"
        rand_int = random.randint(0,4)
        if rand_int == 0:
            return pic1
        elif rand_int == 1:
            return pic2
        elif rand_int == 2:
            return pic3
        elif rand_int == 3:
            return pic4
        elif rand_int == 4:
            return pic5
        
# === Настройки ===
print("введите сначала имя первого контаката и нажмите Enter после этого \nвведите имя второго контакта без ошибок соблюдая регистрт и опять нажмиите Enter\nесли хотите использовать дефолтный профиль (Филип,Алмаз) то просто напиши 1")
CONTACT_1_NAME = str(input())
if CONTACT_1_NAME != '1':
    print("имя контакта 1 записано успешно")
elif CONTACT_1_NAME == '1':
    CONTACT_1_NAME = "Алмаз"
print("Введи имя 2")
CONTACT_2_NAME = str(input())
if CONTACT_2_NAME != '1':
    print("имя контакта 2 записано успешно")
elif CONTACT_2_NAME == '1': 
    CONTACT_2_NAME = "Филип"

print("Хочешь ли ты редактировать фразы которыми будут общаться боты? ")
redact = str(input())
if redact == 'да' or '+' or "yes":
    file_path = "./phrases.txt"
    subprocess.run(["notepad", file_path])
elif redact == 'нет' or 'я гей' or 'окак':
    print("ОКАК")
def howlong():
    print("Сколько минут будет идти диалог? ")
    how_long = int(input(""))
    return how_long
SESSION_DIR_1 = "./whatsapp_session_1"
SESSION_DIR_2 = "./whatsapp_session_2"

# Укажи путь к фото (должен существовать!)
PHOTO_PATH = "./photo.jpg"  # ← замени на свой файл, например: "cat.png"
VIDEO_PATH = "./video.mp4"
# Смысловые фразы для генерации

with open('phrases.txt', 'r', encoding='utf-8') as f:
    PHRASES = [line.strip() for line in f if line.strip()]




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
        await page.set_input_files("input[type='file']", random_picture())
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
    end_time = asyncio.get_event_loop().time() +  howlong() * 60  # 30 минут
    message_count = 0

    while asyncio.get_event_loop().time() < end_time:
        # Аккаунт 1 пишет
        msg1 = random.choice(PHRASES)
        await send_message(page1, CONTACT_1_NAME, msg1, "Аккаунт 1")
        message_count += 1

        # Каждое 4-е сообщение — отправляем фото
        if message_count % 3 == 0 and os.path.exists(PHOTO_PATH):
            await asyncio.sleep(2)
            await send_photo(page1, CONTACT_1_NAME, PHOTO_PATH, "Аккаунт 1")

        await asyncio.sleep(random.uniform(8, 15))

        # Аккаунт 2 пишет
        msg2 = random.choice(PHRASES)
        await send_message(page2, CONTACT_2_NAME, msg2, "Аккаунт 2")
        message_count += 1

        # Каждое 6-е сообщение — фото от второго аккаунта (можно настроить)
        if message_count % 4 == 0 and os.path.exists(PHOTO_PATH):
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
    