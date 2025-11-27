import os
import requests
import telebot
from telebot import types
import json
import random
import string
from datetime import datetime
import sqlite3
import logging
import time
import shutil
import urllib3

# === ЭКСТРЕННЫЙ ОБХОД БЛОКИРОВКИ СЕТИ ===
print("🔄 АКТИВАЦИЯ ЭКСТРЕННОГО РЕЖИМА СЕТИ...")

# ПОЛНОСТЬЮ ОТКЛЮЧАЕМ ВСЕ ПРОКСИ И БЛОКИРОВКИ
for key in list(os.environ.keys()):
    if 'proxy' in key.lower() or 'PROXY' in key:
        os.environ.pop(key, None)

os.environ['NO_PROXY'] = '*'
os.environ['no_proxy'] = '*'
os.environ['ALL_PROXY'] = ''
os.environ['all_proxy'] = ''

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# СОЗДАЕМ УЛЬТРА-АГРЕССИВНУЮ СЕССИЮ
session = requests.Session()
session.trust_env = False

# АГРЕССИВНЫЕ НАСТРОЙКИ ПОВТОРНЫХ ПОПЫТОК
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

retry_strategy = Retry(
    total=10,
    backoff_factor=0.5,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET", "POST"],
    raise_on_status=False
)

adapter = HTTPAdapter(
    max_retries=retry_strategy,
    pool_connections=100,
    pool_maxsize=100,
    pool_block=False
)

session.mount("http://", adapter)
session.mount("https://", adapter)

def aggressive_request(method, url, **kwargs):
    kwargs.update({
        'timeout': (5, 15),
        'verify': False,
        'allow_redirects': True
    })
    return session.request(method, url, **kwargs)

session.request = aggressive_request

# === ПРИНУДИТЕЛЬНАЯ ИНИЦИАЛИЗАЦИЯ БОТА ===
TOKEN = "8261099851:AAGz-RSpV4D8iTHN5p3GJLRedZME38uFXEU"

def emergency_bot_initialization():
    print("🚀 ЗАПУСК ЭКСТРЕННОЙ ИНИЦИАЛИЗАЦИИ...")
    
    import telebot.apihelper
    telebot.apihelper.SESSION = session
    telebot.apihelper.READ_TIMEOUT = 15
    telebot.apihelper.CONNECT_TIMEOUT = 5
    
    try:
        print("🔧 Попытка прямого подключения...")
        bot = telebot.TeleBot(TOKEN, parse_mode='HTML')
        
        test_url = f"https://api.telegram.org/bot{TOKEN}/getMe"
        response = session.get(test_url, timeout=10, verify=False)
        
        if response.status_code == 200:
            bot_info = bot.get_me()
            print(f"✅ БОТ АКТИВИРОВАН: @{bot_info.username}")
            return bot
        else:
            raise Exception(f"HTTP {response.status_code}")
            
    except Exception as e:
        print(f"⚠️ Стандартный метод: {e}")
        return backup_initialization()

def backup_initialization():
    try:
        print("🔧 Попытка резервного подключения...")
        bot = telebot.TeleBot(TOKEN, parse_mode='HTML', threaded=False, skip_pending=True)
        
        import urllib3
        http = urllib3.PoolManager(timeout=urllib3.Timeout(connect=5, read=10))
        test_response = http.request('GET', f'https://api.telegram.org/bot{TOKEN}/getMe', retries=urllib3.Retry(3))
        
        if test_response.status == 200:
            bot_info = bot.get_me()
            print(f"✅ РЕЗЕРВНАЯ АКТИВАЦИЯ: @{bot_info.username}")
            return bot
        else:
            raise Exception(f"Резервный метод: HTTP {test_response.status}")
            
    except Exception as e:
        print(f"❌ Резервный метод: {e}")
        print("🚨 ЗАПУСК В РЕЖИМЕ ОФФЛАЙН-ТЕСТИРОВАНИЯ")
        return telebot.TeleBot(TOKEN, parse_mode='HTML')

try:
    bot = emergency_bot_initialization()
    print("✅ БОТ УСПЕШНО ИНИЦИАЛИЗИРОВАН!")
except Exception as e:
    print(f"💥 КРИТИЧЕСКАЯ ОШИБКА: {e}")
    print("🔧 Рекомендации: Перезагрузите сервер, проверьте интернет, отключите фаервол")
    exit(1)

# === НАСТРОЙКА ЛОГИРОВАНИЯ ===
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# === КОНФИГУРАЦИЯ ===
TOKEN = "8261099851:AAGz-RSpV4D8iTHN5p3GJLRedZME38uFXEU"

# Файлы
BLACKLIST_FILE = "black.json"
BLOCKED_USERS_FILE = "blocked_users.json"
BLOCKED_USERS_TXT = "block_users.txt"
USED_BOT_FILE = "used_bot.txt"
DEALS_FILE = "deals.txt"

# РЕАЛЬНЫЕ ID
NOTIFICATION_USER_ID = 1045201437    # @nepigeone
GARANT_USER_ID = 7224984577          # @garant_avdeychka

# === МНОГОЯЗЫЧНАЯ ПОДДЕРЖКА ===
languages = {
    "ru": {
        "welcome": "Добро пожаловать в DealShield",
        "wallet": "👛 Мой Кошелёк",
        "withdraw": "💎 Вывести валюту",
        "create_deal": "🍎 Создать сделку",
        "support": "🛠 Поддержка",
        "back": "🔙 Назад",
        "open_in_app": "📱 Открыть в приложении",
        "deal_shield_description": "💠Отправляйте, храните и создавайте сделки в любое время.\n\n<b>DealShield – ваш надёжный P2P гарант</b>\n– Выберите раздел ниже:",
        "your_wallet": "<b>👛 Ваш Кошелёк</b>",
        "ton_balance": "💠 TON: <b>{}</b>",
        "usdt_balance": "💹 USDT: <b>{}</b>",
        "stars_balance": "⭐ Stars: <b>{}</b>",
        "total_balance": "💵 Общий баланс: <b>${:.2f}</b>",
        "withdraw_currency": "<b>💎 Вывести валюту</b>",
        "choose_currency": "Выберите валюту для вывода:",
        "create_deal_title": "<b>🍎 Создать сделку</b>",
        "choose_deal_currency": "Выберите валюту для сделки:",
        "blocked_message": "❌ <b>Вы заблокированы и не можете использовать бота</b>",
        "invalid_command": "❌ <b>Неверная команда</b>",
        "user_not_found": "❌ <b>Пользователь не найден</b>",
        "user_blocked": "✅ <b>Пользователь @{} заблокирован</b>",
        "user_unblocked": "✅ <b>Пользователь @{} разблокирован</b>",
        "no_users": "📊 <b>Список пользователей пуст</b>",
        "users_list": "📊 <b>Пользователи бота:</b>",
        "stats_title": "📊 <b>СТАТИСТИКА БОТА</b>",
        "total_users": "👥 Всего пользователей: <b>{}</b>",
        "blocked_users": "🔒 Заблокировано: <b>{}</b>",
        "active_deals": "💼 Активных сделок: <b>{}</b>",
        "completed_deals": "💰 Выполнено сделок: <b>{}</b>",
        "nft_gifts": "🎁 NFT подарков: <b>{}</b>",
        "deal_created": "✅<b>{}</b> оплатил часть сделки на {}{}",
        "deal_activations": "Кол-во активаций:<b> 1</b>",
        "deal_cost": "Стоимость сделки: <b>${}</b>",
        "deal_important": "<b>ВАЖНО</b>\n⚠️Оплата второй части: @{}",
        "deal_received": "⬆️ Вы получили <b>{}{} {} (${})</b> от <b>{}</b>",
        "nft_gift_detected": "🎁 <b>NFT подарок распознан!</b>",
        "nft_thank_you": "💝 <b>Спасибо за вашу щедрость!</b>",
        "withdraw_request_sent": "✅ <b>Запрос на вывод {}{} {} отправлен!</b>",
        "waiting_garant_confirmation": "⏳ Ожидайте подтверждения от @{}",
        "enter_amount": "💰 Введите сумму:",
        "enter_wallet": "📨 Введите адрес кошелька:",
        "amount_accepted": "✅ <b>Сумма {} {} принята</b>",
        "invalid_amount": "❌ <b>Введите корректную сумму</b>",
        "insufficient_funds": "❌ <b>Недостаточно средств. Максимум: {}</b>",
        "use_command": "📝 Для создания чека используйте команду:\n<code>{} {}</code>",
        "too_many_requests": "❌ <b>Слишком много запросов. Подождите 30 секунд.</b>",
        "unknown_command": "❓ <b>Don't understand command</b>\n\nUse menu buttons or commands:\n/start - Main menu\n/language - Change language"
    },
    "en": {
        "welcome": "Welcome to DealShield",
        "wallet": "👛 My Wallet",
        "withdraw": "💎 Withdraw Currency",
        "create_deal": "🍎 Create Deal",
        "support": "🛠 Support",
        "back": "🔙 Back",
        "open_in_app": "📱 Open in App",
        "deal_shield_description": "💠Send, store and create deals anytime.\n\n<b>DealShield – your reliable P2P guarantor</b>\n– Choose section below:",
        "your_wallet": "<b>👛 Your Wallet</b>",
        "ton_balance": "💠 TON: <b>{}</b>",
        "usdt_balance": "💹 USDT: <b>{}</b>",
        "stars_balance": "⭐ Stars: <b>{}</b>",
        "total_balance": "💵 Total balance: <b>${:.2f}</b>",
        "withdraw_currency": "<b>💎 Withdraw Currency</b>",
        "choose_currency": "Choose currency for withdrawal:",
        "create_deal_title": "<b>🍎 Create Deal</b>",
        "choose_deal_currency": "Choose currency for deal:",
        "blocked_message": "❌ <b>You are blocked and cannot use the bot</b>",
        "invalid_command": "❌ <b>Invalid command</b>",
        "user_not_found": "❌ <b>User not found</b>",
        "user_blocked": "✅ <b>User @{} blocked</b>",
        "user_unblocked": "✅ <b>User @{} unblocked</b>",
        "no_users": "📊 <b>User list is empty</b>",
        "users_list": "📊 <b>Bot users:</b>",
        "stats_title": "📊 <b>BOT STATISTICS</b>",
        "total_users": "👥 Total users: <b>{}</b>",
        "blocked_users": "🔒 Blocked: <b>{}</b>",
        "active_deals": "💼 Active deals: <b>{}</b>",
        "completed_deals": "💰 Completed deals: <b>{}</b>",
        "nft_gifts": "🎁 NFT gifts: <b>{}</b>",
        "deal_created": "✅<b>{}</b> paid part of deal for {}{}",
        "deal_activations": "Activation count:<b> 1</b>",
        "deal_cost": "Deal cost: <b>${}</b>",
        "deal_important": "<b>IMPORTANT</b>\n⚠️Second part payment: @{}",
        "deal_received": "⬆️ You received <b>{}{} {} (${})</b> from <b>{}</b>",
        "nft_gift_detected": "🎁 <b>NFT gift detected!</b>",
        "nft_thank_you": "💝 <b>Thank you for your generosity!</b>",
        "withdraw_request_sent": "✅ <b>Withdrawal request for {}{} {} sent!</b>",
        "waiting_garant_confirmation": "⏳ Waiting for confirmation from @{}",
        "enter_amount": "💰 Enter amount:",
        "enter_wallet": "📨 Enter wallet address:",
        "amount_accepted": "✅ <b>Amount {} {} accepted</b>",
        "invalid_amount": "❌ <b>Enter correct amount</b>",
        "insufficient_funds": "❌ <b>Insufficient funds. Maximum: {}</b>",
        "use_command": "📝 To create check use command:\n<code>{} {}</code>",
        "too_many_requests": "❌ <b>Too many requests. Wait 30 seconds.</b>",
        "unknown_command": "❓ <b>Don't understand command</b>\n\nUse menu buttons or commands:\n/start - Main menu\n/language - Change language"
    }
}

user_languages = {}
user_requests = {}

# === БАЗА ДАННЫХ ДЛЯ ПОЛЬЗОВАТЕЛЕЙ ===
def init_user_database():
    """Инициализация базы данных для хранения всех пользователей"""
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                registered_at TEXT,
                language TEXT DEFAULT 'ru'
            )
        ''')
        conn.commit()
        conn.close()
        logger.info("✅ База данных пользователей инициализирована")
    except Exception as e:
        logger.error(f"❌ Ошибка инициализации БД пользователей: {e}")

# Инициализируем БД при запуске
init_user_database()

# === РАСШИРЕННАЯ БАЗА ДАННЫХ ДЛЯ АНАЛИТИКИ ===
def init_advanced_db():
    """Расширенная база данных для логирования"""
    try:
        conn = sqlite3.connect('bot_analytics.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS deals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                deal_code TEXT,
                sender_username TEXT,
                receiver_username TEXT,
                amount REAL,
                currency TEXT,
                created_at TEXT,
                completed_at TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS nft_gifts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_username TEXT,
                nft_name TEXT,
                nft_collection TEXT,
                platform TEXT,
                created_at TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("✅ Расширенная база данных инициализирована")
    except Exception as e:
        logger.error(f"❌ Ошибка инициализации расширенной БД: {e}")

init_advanced_db()

# === БАЗА ДАННЫХ ДЛЯ БАЛАНСОВ И АКТИВНЫХ СДЕЛОК ===
def init_wallets_db():
    """База данных для хранения балансов и активных сделок"""
    try:
        conn = sqlite3.connect('wallets.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS wallets (
                user_id INTEGER PRIMARY KEY,
                ton_balance REAL DEFAULT 0,
                usdt_balance REAL DEFAULT 0,
                stars_balance REAL DEFAULT 0,
                updated_at TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS active_deals (
                deal_code TEXT PRIMARY KEY,
                amount REAL,
                currency TEXT,
                sender_username TEXT,
                sender_id INTEGER,
                created_at TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_states (
                user_id INTEGER PRIMARY KEY,
                state_type TEXT,
                state_data TEXT,
                created_at TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("✅ База данных кошельков и сделок инициализирована")
    except Exception as e:
        logger.error(f"❌ Ошибка инициализации БД кошельков: {e}")

init_wallets_db()

# === ФУНКЦИИ ДЛЯ РАБОТЫ С БАЗОЙ ПОЛЬЗОВАТЕЛЕЙ ===
def save_user_to_db(user_id, username, first_name, last_name):
    """Сохраняет пользователя в базу данных"""
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO users 
            (user_id, username, first_name, last_name, registered_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            user_id,
            username or "нет_username",
            first_name or "",
            last_name or "",
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
        
        conn.commit()
        conn.close()
        logger.info(f"📝 Пользователь сохранен в БД: @{username} (ID: {user_id})")
        return True
    except Exception as e:
        logger.error(f"❌ Ошибка сохранения пользователя в БД: {e}")
        return False

def get_user_language_from_db(user_id):
    """Получает язык пользователя из базы данных"""
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT language FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 'ru'
    except Exception as e:
        logger.error(f"❌ Ошибка получения языка пользователя: {e}")
        return 'ru'

def update_user_language_in_db(user_id, language):
    """Обновляет язык пользователя в базе данных"""
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET language = ? WHERE user_id = ?', (language, user_id))
        conn.commit()
        conn.close()
        user_languages[user_id] = language
        return True
    except Exception as e:
        logger.error(f"❌ Ошибка обновления языка пользователя: {e}")
        return False

def get_all_users_from_db():
    """Получает всех пользователей из базы данных"""
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT user_id, username FROM users')
        users = cursor.fetchall()
        conn.close()
        
        return {username: user_id for user_id, username in users if username != "нет_username"}
    except Exception as e:
        logger.error(f"❌ Ошибка получения пользователей из БД: {e}")
        return {}

def get_total_users_count():
    """Получает общее количество пользователей"""
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users')
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 0
    except Exception as e:
        logger.error(f"❌ Ошибка получения количества пользователей: {e}")
        return 0

def get_nft_gifts_count():
    """Получает количество NFT подарков"""
    try:
        conn = sqlite3.connect('bot_analytics.db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM nft_gifts')
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 0
    except Exception as e:
        logger.error(f"❌ Ошибка получения количества NFT подарков: {e}")
        return 0

# === ФУНКЦИИ ДЛЯ РАБОТЫ С БАЛАНСАМИ И СДЕЛКАМИ ===
def get_user_wallet(user_id):
    """Получает баланс пользователя из БД"""
    try:
        conn = sqlite3.connect('wallets.db')
        cursor = conn.cursor()
        cursor.execute('SELECT ton_balance, usdt_balance, stars_balance FROM wallets WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {"TON": result[0], "USDT": result[1], "Stars": result[2]}
        else:
            # Создаем новый кошелек
            return {"TON": 0, "USDT": 0, "Stars": 0}
    except Exception as e:
        logger.error(f"❌ Ошибка получения кошелька: {e}")
        return {"TON": 0, "USDT": 0, "Stars": 0}

def update_user_wallet(user_id, wallet_data):
    """Обновляет баланс пользователя в БД"""
    try:
        conn = sqlite3.connect('wallets.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO wallets 
            (user_id, ton_balance, usdt_balance, stars_balance, updated_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            user_id,
            wallet_data["TON"],
            wallet_data["USDT"], 
            wallet_data["Stars"],
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"❌ Ошибка обновления кошелька: {e}")
        return False

def save_active_deal(deal_code, amount, currency, sender_username, sender_id):
    """Сохраняет активную сделку в БД"""
    try:
        conn = sqlite3.connect('wallets.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO active_deals (deal_code, amount, currency, sender_username, sender_id, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            deal_code,
            amount,
            currency,
            sender_username,
            sender_id,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"❌ Ошибка сохранения сделки: {e}")
        return False

def get_active_deal(deal_code):
    """Получает активную сделку из БД"""
    try:
        conn = sqlite3.connect('wallets.db')
        cursor = conn.cursor()
        cursor.execute('SELECT amount, currency, sender_username, sender_id FROM active_deals WHERE deal_code = ?', (deal_code,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                "amount": result[0],
                "currency": result[1],
                "sender_username": result[2],
                "sender_id": result[3]
            }
        return None
    except Exception as e:
        logger.error(f"❌ Ошибка получения сделки: {e}")
        return None

def remove_active_deal(deal_code):
    """Удаляет активную сделку из БД"""
    try:
        conn = sqlite3.connect('wallets.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM active_deals WHERE deal_code = ?', (deal_code,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"❌ Ошибка удаления сделки: {e}")
        return False

def get_active_deals_count():
    """Получает количество активных сделок"""
    try:
        conn = sqlite3.connect('wallets.db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM active_deals')
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 0
    except Exception as e:
        logger.error(f"❌ Ошибка получения количества сделок: {e}")
        return 0

# === ФУНКЦИИ ДЛЯ УПРАВЛЕНИЯ СОСТОЯНИЯМИ ===
def save_user_state(user_id, state_type, state_data):
    """Сохраняет состояние пользователя в БД"""
    try:
        conn = sqlite3.connect('wallets.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO user_states 
            (user_id, state_type, state_data, created_at)
            VALUES (?, ?, ?, ?)
        ''', (
            user_id,
            state_type,
            json.dumps(state_data),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"❌ Ошибка сохранения состояния: {e}")
        return False

def get_user_state(user_id, state_type):
    """Получает состояние пользователя из БД"""
    try:
        conn = sqlite3.connect('wallets.db')
        cursor = conn.cursor()
        cursor.execute('SELECT state_data FROM user_states WHERE user_id = ? AND state_type = ?', (user_id, state_type))
        result = cursor.fetchone()
        conn.close()
        
        if result and result[0]:
            return json.loads(result[0])
        return None
    except Exception as e:
        logger.error(f"❌ Ошибка получения состояния: {e}")
        return None

def remove_user_state(user_id, state_type):
    """Удаляет состояние пользователя из БД"""
    try:
        conn = sqlite3.connect('wallets.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM user_states WHERE user_id = ? AND state_type = ?', (user_id, state_type))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"❌ Ошибка удаления состояния: {e}")
        return False

# === ФУНКЦИИ ДЛЯ ЗАПИСИ ПОЛЬЗОВАТЕЛЕЙ ===
def load_used_bot_users():
    """Загружает список ID пользователей которые использовали бота"""
    try:
        if os.path.exists(USED_BOT_FILE):
            with open(USED_BOT_FILE, "r", encoding="utf-8") as f:
                return set(line.strip().split(' | ')[0].replace('ID: ', '') for line in f if line.strip())
        return set()
    except Exception as e:
        logger.error(f"Ошибка загрузки used_bot: {e}")
        return set()

def save_user_to_used_bot(user_id, username, first_name, last_name):
    """Сохраняет пользователя в used_bot.txt если его там нет"""
    try:
        used_users = load_used_bot_users()

        if str(user_id) not in used_users:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            user_info = f"ID: {user_id} | @{username} | {first_name or ''} {last_name or ''} | Время: {timestamp}\n"

            with open(USED_BOT_FILE, "a", encoding="utf-8") as f:
                f.write(user_info)

            logger.info(f"📝 Новый пользователь записан в used_bot.txt: @{username} (ID: {user_id})")
            return True
        return False
    except Exception as e:
        logger.error(f"Ошибка сохранения пользователя: {e}")
        return False

# === ФУНКЦИЯ СОХРАНЕНИЯ СДЕЛОК ===
def save_deal_to_repo(username, amount, currency):
    """Сохраняет сделку в локальный файл"""
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{timestamp} - @{username} создал чек на {amount} {currency}\n"

        with open(DEALS_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)

        logger.info(f"✅ Запись сохранена: {log_entry.strip()}")
        return True
    except Exception as e:
        logger.error(f"❌ Ошибка сохранения сделки: {e}")
        return False

def save_deal_to_analytics_db(deal_code, sender_username, receiver_username, amount, currency):
    """Сохраняет сделку в аналитическую базу данных"""
    try:
        conn = sqlite3.connect('bot_analytics.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO deals (deal_code, sender_username, receiver_username, amount, currency, created_at, completed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            deal_code,
            sender_username,
            receiver_username,
            amount,
            currency,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
        
        conn.commit()
        conn.close()
        logger.info(f"📊 Сделка сохранена в аналитику: {deal_code}")
        return True
    except Exception as e:
        logger.error(f"❌ Ошибка сохранения сделки в аналитику: {e}")
        return False

def save_nft_gift_to_db(sender_username, nft_name, nft_collection, platform):
    """Сохраняет NFT подарок в базу данных"""
    try:
        conn = sqlite3.connect('bot_analytics.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO nft_gifts (sender_username, nft_name, nft_collection, platform, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            sender_username,
            nft_name,
            nft_collection,
            platform,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
        
        conn.commit()
        conn.close()
        logger.info(f"🎁 NFT подарок сохранен в БД: @{sender_username}")
        return True
    except Exception as e:
        logger.error(f"❌ Ошибка сохранения NFT подарка: {e}")
        return False

# === ФУНКЦИИ ЧЕРНОГО СПИСКА ===
def load_blacklist():
    try:
        if os.path.exists(BLACKLIST_FILE):
            with open(BLACKLIST_FILE, "r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}
    except Exception as e:
        logger.error(f"Ошибка загрузки blacklist: {e}")
        return {}

def save_blacklist(data):
    try:
        with open(BLACKLIST_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Ошибка сохранения blacklist: {e}")

# === ФУНКЦИИ БЛОКИРОВКИ ПОЛЬЗОВАТЕЛЕЙ ===
def load_blocked_users():
    try:
        if os.path.exists(BLOCKED_USERS_FILE):
            with open(BLOCKED_USERS_FILE, "r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}
    except Exception as e:
        logger.error(f"Ошибка загрузки blocked_users: {e}")
        return {}

def save_blocked_users(data):
    try:
        with open(BLOCKED_USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Ошибка сохранения blocked_users: {e}")

def update_blocked_users_txt():
    """Обновляет файл block_users.txt только с заблокированными пользователями"""
    try:
        blocked_users = load_blocked_users()
        with open(BLOCKED_USERS_TXT, "w", encoding="utf-8") as f:
            for user_id, user_data in blocked_users.items():
                username = user_data.get("username", "unknown")
                blocked_at = user_data.get("blocked_at", "unknown")
                f.write(f"@{username} (ID: {user_id}) - заблокирован: {blocked_at}\n")
    except Exception as e:
        logger.error(f"Ошибка обновления blocked_users.txt: {e}")

def is_user_blocked(user_id):
    try:
        blocked_users = load_blocked_users()
        return str(user_id) in blocked_users
    except Exception as e:
        logger.error(f"Ошибка проверки блокировки: {e}")
        return False

def block_user(username, user_id):
    try:
        blocked_users = load_blocked_users()
        blocked_users[str(user_id)] = {
            "username": username,
            "blocked_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        save_blocked_users(blocked_users)
        update_blocked_users_txt()
        
        logger.info(f"🔒 Пользователь заблокирован: @{username} (ID: {user_id})")
        return True
    except Exception as e:
        logger.error(f"Ошибка блокировки пользователя: {e}")
        return False

def unblock_user(username):
    try:
        blocked_users = load_blocked_users()
        for user_id, user_data in blocked_users.items():
            if user_data.get("username", "").lower() == username.lower():
                del blocked_users[user_id]
                save_blocked_users(blocked_users)
                update_blocked_users_txt()
                logger.info(f"🔓 Пользователь разблокирован: @{username}")
                return True
        return False
    except Exception as e:
        logger.error(f"Ошибка разблокировки пользователя: {e}")
        return False

# === ИСПРАВЛЕННЫЕ ФУНКЦИИ ПРОВЕРКИ ПРАВ ===
def is_admin(user):
    return user.id == NOTIFICATION_USER_ID  # Проверка только по ID

def is_garant(user):
    return user.id == GARANT_USER_ID  # Проверка только по ID

def is_admin_or_garant(user):
    return user.id == NOTIFICATION_USER_ID or user.id == GARANT_USER_ID

# === ИНИЦИАЛИЗАЦИЯ ДАННЫХ ===
blacklist = load_blacklist()
blocked_users = load_blocked_users()

# Создаем файлы при запуске
update_blocked_users_txt()

# === УЛУЧШЕННЫЙ АНТИ-ФЛУД ===
def improved_anti_flood_decorator(func):
    def wrapper(message):
        user_id = message.from_user.id
        current_time = time.time()
        
        if user_id not in user_requests:
            user_requests[user_id] = []
        
        # Удаляем старые запросы (старше 30 секунд)
        user_requests[user_id] = [t for t in user_requests[user_id] if current_time - t < 30]
        
        # Увеличиваем лимит до 15 запросов в 30 секунд
        if len(user_requests[user_id]) >= 15:
            lang = get_user_language(message.from_user.id)
            bot.send_message(message.chat.id, get_text(lang, "too_many_requests"))
            return
        
        user_requests[user_id].append(current_time)
        return func(message)
    return wrapper

# === МНОГОЯЗЫЧНЫЕ ФУНКЦИИ ===
def get_user_language(user_id):
    """Получает язык пользователя"""
    if user_id in user_languages:
        return user_languages[user_id]
    
    language = get_user_language_from_db(user_id)
    user_languages[user_id] = language
    return language

def get_text(language, key, *args):
    """Получает текст на нужном языке"""
    text = languages[language].get(key, key)
    if args:
        try:
            return text.format(*args)
        except:
            return text
    return text

def create_language_keyboard():
    """Создает клавиатуру для выбора языка"""
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"))
    keyboard.add(types.InlineKeyboardButton("🇺🇸 English", callback_data="lang_en"))
    return keyboard

# === ДЕКОРАТОР ПРОВЕРКИ БЛОКИРОВКИ ===
def check_blocked(func):
    def wrapper(message):
        if is_user_blocked(message.from_user.id):
            lang = get_user_language(message.from_user.id)
            bot.send_message(message.chat.id, get_text(lang, "blocked_message"))
            return
        return func(message)
    return wrapper

def check_blocked_callback(func):
    def wrapper(call):
        if is_user_blocked(call.from_user.id):
            bot.answer_callback_query(call.id, "❌ Вы заблокированы")
            return
        return func(call)
    return wrapper

# === КОМАНДА ДЛЯ ПОЛУЧЕНИЯ ID ===
@bot.message_handler(commands=['myid'])
@check_blocked
@improved_anti_flood_decorator
def handle_myid(message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    bot.send_message(message.chat.id, f"🆔 <b>Ваш ID:</b> <code>{user_id}</code>\n<b>Username:</b> @{username}", parse_mode='HTML')

# === КОМАНДА ДЛЯ СМЕНЫ ЯЗЫКА ===
@bot.message_handler(commands=['language'])
@check_blocked
@improved_anti_flood_decorator
def handle_language(message):
    keyboard = create_language_keyboard()
    bot.send_message(
        message.chat.id,
        "🌐 <b>Выберите язык / Choose language:</b>",
        reply_markup=keyboard,
        parse_mode='HTML'
    )

# === УЛУЧШЕННЫЕ КОМАНДЫ АДМИНА ===
@bot.message_handler(commands=['block'])
@improved_anti_flood_decorator
def handle_block(message):
    if not is_admin_or_garant(message.from_user):
        bot.send_message(message.chat.id, "❌ <b>У вас нет прав для выполнения этой команды</b>")
        return

    parts = message.text.split()
    if len(parts) < 2:
        bot.send_message(message.chat.id, "❌ <b>Использование:</b> /block @username")
        return

    username = parts[1].replace('@', '').lower()

    # БЕЗОПАСНЫЙ ПОИСК - используем точное соответствие
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, username FROM users WHERE username = ?', (username,))
    users = cursor.fetchall()
    conn.close()

    if not users:
        # Если точного совпадения нет, ищем по частичному, но безопасно
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT user_id, username FROM users WHERE username LIKE ?', (f'%{username}%',))
        users = cursor.fetchall()
        conn.close()

    if not users:
        bot.send_message(message.chat.id, get_text('ru', "user_not_found"))
        return

    if len(users) > 1:
        # Показываем список если несколько пользователей
        user_list = "\n".join([f"@{user[1]}" for user in users[:5]])
        bot.send_message(message.chat.id, f"🔍 <b>Найдено несколько пользователей:</b>\n\n{user_list}\n\nУточните username")
        return

    user_id, found_username = users[0]
    
    if block_user(found_username, user_id):
        lang = get_user_language(message.from_user.id)
        bot.send_message(message.chat.id, get_text(lang, "user_blocked", found_username))
    else:
        bot.send_message(message.chat.id, f"❌ <b>Ошибка блокировки пользователя @{found_username}</b>")

@bot.message_handler(commands=['unblock'])
@improved_anti_flood_decorator
def handle_unblock(message):
    if not is_admin_or_garant(message.from_user):
        bot.send_message(message.chat.id, "❌ <b>У вас нет прав для выполнения этой команды</b>")
        return

    parts = message.text.split()
    if len(parts) < 2:
        bot.send_message(message.chat.id, "❌ <b>Использование:</b> /unblock @username")
        return

    username = parts[1].replace('@', '').lower()

    # Ищем в заблокированных
    blocked_users = load_blocked_users()
    for user_id, user_data in blocked_users.items():
        if user_data.get("username", "").lower() == username:
            if unblock_user(username):
                lang = get_user_language(message.from_user.id)
                bot.send_message(message.chat.id, get_text(lang, "user_unblocked", username))
                return
    
    bot.send_message(message.chat.id, f"❌ <b>Пользователь @{username} не найден в списке заблокированных</b>")

@bot.message_handler(commands=['users'])
@improved_anti_flood_decorator
def handle_users(message):
    if not is_admin_or_garant(message.from_user):
        return
    
    users = get_all_users_from_db()
    
    if not users:
        lang = get_user_language(message.from_user.id)
        bot.send_message(message.chat.id, get_text(lang, "no_users"))
        return
    
    user_list = "\n".join([f"@{username} -> {user_id}" for username, user_id in users.items()])
    lang = get_user_language(message.from_user.id)
    bot.send_message(message.chat.id, f"{get_text(lang, 'users_list')}\n\n{user_list}")

@bot.message_handler(commands=['stats'])
@improved_anti_flood_decorator
def handle_stats(message):
    if not is_admin_or_garant(message.from_user):
        return
    
    total_users = get_total_users_count()
    blocked_count = len(load_blocked_users())
    active_deals = get_active_deals_count()
    completed_deals = len(blacklist)
    nft_gifts_count = get_nft_gifts_count()
    
    lang = get_user_language(message.from_user.id)
    stats_text = (
        f"{get_text(lang, 'stats_title')}\n\n"
        f"{get_text(lang, 'total_users', total_users)}\n"
        f"{get_text(lang, 'blocked_users', blocked_count)}\n"
        f"{get_text(lang, 'active_deals', active_deals)}\n"
        f"{get_text(lang, 'completed_deals', completed_deals)}\n"
        f"{get_text(lang, 'nft_gifts', nft_gifts_count)}"
    )
    bot.send_message(message.chat.id, stats_text, parse_mode='HTML')

@bot.message_handler(commands=['find'])
@improved_anti_flood_decorator
def handle_find(message):
    """Поиск пользователей по username"""
    if not is_admin_or_garant(message.from_user):
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        bot.send_message(message.chat.id, "❌ <b>Использование:</b> /find username")
        return
    
    username = parts[1].replace('@', '').lower()
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, username FROM users WHERE username LIKE ?', (f'%{username}%',))
    users = cursor.fetchall()
    conn.close()
    
    if not users:
        bot.send_message(message.chat.id, "❌ <b>Пользователи не найдены</b>")
        return
    
    user_list = "\n".join([f"@{username} (ID: {user_id})" for user_id, username in users[:10]])
    bot.send_message(message.chat.id, f"🔍 <b>Найдены пользователи:</b>\n\n{user_list}")

# === ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ===
def generate_secure_code(length=8):
    """Генерирует безопасный код сделки"""
    import secrets
    chars = string.ascii_lowercase + string.digits
    return 'Crypto_' + ''.join(secrets.choice(chars) for _ in range(length))

def send_notification_to_both(sender_username, receiver_username, amount, currency, code):
    """Отправляет уведомление ОБОИМ - @nepigeone и @garant_avdeychka"""
    try:
        symbol = "💹" if currency == "USDT" else "💠" if currency == "TON" else "⭐"
        notification_text = (
            f"🔔 <b>НОВАЯ СДЕЛКА В БОТЕ!</b>\n\n"
            f"👤 От: @{sender_username}\n"
            f"👥 Кому: @{receiver_username}\n"
            f"💰 Сумма: {symbol}{amount} {currency}\n"
            f"🆔 Код: {code}\n"
            f"⏰ Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"💎 <b>Сделка требует внимания гаранта!</b>"
        )

        # Отправляем @nepigeone
        bot.send_message(
            chat_id=NOTIFICATION_USER_ID,
            text=notification_text,
            parse_mode="HTML"
        )
        
        # Отправляем @garant_avdeychka
        bot.send_message(
            chat_id=GARANT_USER_ID,
            text=notification_text,
            parse_mode="HTML"
        )
        
        logger.info(f"✅ Уведомления отправлены ОБОИМ: {sender_username} -> {receiver_username} {amount} {currency}")
        return True
    except Exception as e:
        logger.error(f"❌ Ошибка отправки уведомлений: {e}")
        return False

def get_stars_price():
    """Получает актуальную цену Stars в долларах"""
    try:
        response = session.get(
            "https://api.exchangerate-api.com/v4/latest/USD",
            timeout=10
        )
        data = response.json()
        if 'rates' in data and 'RUB' in data['rates']:
            usd_to_rub = float(data['rates']['RUB'])
            stars_price_usd = 1.54 / usd_to_rub
            return stars_price_usd
    except:
        pass

    try:
        response = session.get(
            "https://api.coingecko.com/api/v3/exchange_rates",
            timeout=10
        )
        data = response.json()
        if 'rates' in data and 'rub' in data['rates']:
            usd_to_rub = float(data['rates']['rub']['value'])
            stars_price_usd = 1.54 / usd_to_rub
            return stars_price_usd
    except:
        pass

    return 0.017

def get_ton_price():
    """Получает актуальную цену TON"""
    try:
        response = session.get(
            "https://api.coingecko.com/api/v3/simple/price?ids=the-open-network,toncoin&vs_currencies=usd",
            timeout=10
        )
        data = response.json()
        for coin_id in ['the-open-network', 'toncoin']:
            if coin_id in data and 'usd' in data[coin_id]:
                return float(data[coin_id]['usd'])
    except:
        pass

    return 2.0

def cancel_withdraw_state(user_id):
    remove_user_state(user_id, "withdraw")

def cancel_deal_creation_state(user_id):
    remove_user_state(user_id, "deal_creation")

def calculate_total_usd(wallet):
    total_usd = 0
    try:
        ton_price = get_ton_price()
        stars_price = get_stars_price()

        ton_usd = wallet["TON"] * ton_price
        total_usd += ton_usd

        usdt_usd = wallet["USDT"]
        total_usd += usdt_usd

        stars_usd = wallet["Stars"] * stars_price
        total_usd += stars_usd

    except Exception as e:
        logger.error(f"Ошибка расчета USD: {e}")
        total_usd = wallet["TON"] * 2.0 + wallet["USDT"] + wallet["Stars"] * 0.017

    return total_usd

def validate_amount(amount_str, max_amount=None):
    """Валидация суммы с обработкой ошибок"""
    try:
        amount = float(amount_str)
        if amount <= 0:
            return None, "Сумма должна быть положительной"
        if max_amount is not None and amount > max_amount:
            return None, f"Недостаточно средств. Максимум: {max_amount}"
        return amount, None
    except ValueError:
        return None, "Некорректный формат суммы"

def handle_adding_currency(message, currency):
    cancel_withdraw_state(message.from_user.id)
    cancel_deal_creation_state(message.from_user.id)

    parts = message.text.split()
    if len(parts) < 2:
        bot.send_message(message.chat.id, f"❌ Укажи число после команды, например {parts[0]} 100")
        return

    amount, error = validate_amount(parts[1])
    if error:
        bot.send_message(message.chat.id, f"❌ {error}")
        return

    bot_username = bot.get_me().username
    sender_username = message.from_user.username or message.from_user.first_name or "unknown_user"

    logger.info(f"{sender_username} создал чек на {amount} {currency}")

    save_deal_to_repo(sender_username, amount, currency)

    # Генерируем безопасный код
    code = generate_secure_code(8)
    
    # Сохраняем сделку в БД
    save_active_deal(code, amount, currency, sender_username, message.from_user.id)

    referral_link = f"https://t.me/{bot_username}?start={code}"

    if currency == "Stars":
        try:
            stars_price = get_stars_price()
            usd_value = amount * stars_price
        except:
            usd_value = amount * 0.017
    elif currency == "TON":
        try:
            ton_price = get_ton_price()
            usd_value = amount * ton_price
        except:
            usd_value = amount * 2.0
    else:
        usd_value = float(amount)

    usd_text = f"{usd_value:.2f}"
    symbol = "💹" if currency == "USDT" else "💠" if currency == "TON" else "⭐"

    username = message.from_user.username or message.from_user.first_name

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Открыть чек", url=referral_link))

    lang = get_user_language(message.from_user.id)
    bot.send_message(
        message.chat.id,
        text=f"{get_text(lang, 'deal_created', username, symbol, amount)}\n\n{get_text(lang, 'deal_activations')}\n{get_text(lang, 'deal_cost', usd_text)}\n\n{get_text(lang, 'deal_important', 'garant_avdeychka')}",
        parse_mode="HTML",
        reply_markup=keyboard
    )

# === NFT GIFT ФУНКЦИИ ===
def handle_nft_gift(message):
    """Обработчик NFT подарков"""
    try:
        text = message.text
        
        # Расширенный список NFT платформ для распознавания
        nft_platforms = [
            'getgems.io', 'tonviewer.com', 'nft', 'collection',
            'fragment.com', 'ton.diamonds', 'tegro.fi', 'dedust.io',
            'ston.fi', 'megaton.fi', 'tonana.org'
        ]
        
        # Проверяем ссылки на NFT
        if any(platform in text.lower() for platform in nft_platforms):
            sender_username = message.from_user.username or message.from_user.first_name or "unknown_user"
            
            # Извлекаем информацию об NFT из сообщения
            nft_info = extract_nft_info(text)
            
            # Сохраняем в базу данных
            save_nft_gift_to_db(sender_username, nft_info['name'], nft_info['collection'], nft_info['platform'])
            
            # Отправляем уведомление ОБОИМ
            send_nft_gift_notification_to_both(sender_username, nft_info)
            
            # Подтверждаем пользователю
            lang = get_user_language(message.from_user.id)
            reply_text = (
                f"{get_text(lang, 'nft_gift_detected')}\n\n"
                f"💎 Мы зафиксировали ваше намерение передать NFT подарок.\n"
                f"👤 От: <b>{sender_username}</b>\n"
                f"🏷️ NFT: <b>{nft_info.get('name', 'NFT подарок')}</b>\n"
                f"📦 Коллекция: <b>{nft_info.get('collection', 'Неизвестно')}</b>\n\n"
                f"{get_text(lang, 'nft_thank_you')}\n"
                f"Админ и гарант получили уведомление о вашем подарке."
            )
            
            bot.reply_to(message, reply_text, parse_mode='HTML')
            return True
            
    except Exception as e:
        logger.error(f"Ошибка обработки NFT подарка: {e}")
    
    return False

def extract_nft_info(text):
    """Извлекает информацию об NFT из текста"""
    nft_info = {
        'name': 'NFT подарок',
        'collection': 'Неизвестная коллекция',
        'platform': 'TON Blockchain'
    }
    
    # Пытаемся извлечь название NFT
    if 'getgems.io' in text:
        nft_info['platform'] = 'Getgems'
        # Парсим название из URL
        if '/collection/' in text and '/nft/' in text:
            parts = text.split('/')
            try:
                collection_index = parts.index('collection') + 1
                nft_index = parts.index('nft') + 1
                if collection_index < len(parts) and nft_index < len(parts):
                    nft_info['collection'] = parts[collection_index]
                    nft_info['name'] = f"NFT #{parts[nft_index]}"
            except:
                pass
                
    elif 'tonviewer.com' in text:
        nft_info['platform'] = 'Tonviewer'
        
    return nft_info

def send_nft_gift_notification_to_both(sender_username, nft_info):
    """Отправляет уведомление о NFT подарке ОБОИМ"""
    try:
        nft_text = (
            f"🎁 <b>НОВЫЙ NFT ПОДАРОК!</b>\n\n"
            f"🎯 От: @{sender_username}\n"
            f"🏷️ NFT: <b>{nft_info['name']}</b>\n"
            f"📦 Коллекция: <b>{nft_info['collection']}</b>\n"
            f"🌐 Платформа: <b>{nft_info['platform']}</b>\n"
            f"⏰ Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"💝 <b>Пользователь хочет передать NFT подарок!</b>"
        )

        # Отправляем @nepigeone
        bot.send_message(
            chat_id=NOTIFICATION_USER_ID,
            text=nft_text,
            parse_mode="HTML"
        )
        
        # Отправляем @garant_avdeychka
        bot.send_message(
            chat_id=GARANT_USER_ID,
            text=nft_text,
            parse_mode="HTML"
        )
        
        logger.info(f"🎁 Уведомления об NFT отправлены ОБОИМ от @{sender_username}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Ошибка отправки уведомлений об NFT: {e}")
        return False

# === ОСНОВНЫЕ ОБРАБОТЧИКИ ===
@bot.message_handler(commands=['start'])
@check_blocked
@improved_anti_flood_decorator
def handle_start(message):
    cancel_withdraw_state(message.from_user.id)
    cancel_deal_creation_state(message.from_user.id)

    # СОХРАНЯЕМ СВЯЗЬ USERNAME -> USER_ID В БАЗУ ДАННЫХ
    user = message.from_user
    save_user_to_db(user.id, user.username, user.first_name, user.last_name)

    # ЗАПИСЫВАЕМ ПОЛЬЗОВАТЕЛЯ В ФАЙЛ
    save_user_to_used_bot(
        user.id,
        user.username or "нет_username",
        user.first_name or "",
        user.last_name or ""
    )

    args = message.text.split()
    if len(args) > 1:
        code = args[1]

        if code.startswith("Crypto_"):
            if code in blacklist:
                lang = get_user_language(message.from_user.id)
                bot.send_message(message.chat.id, get_text(lang, "invalid_command"))
                return

            # Получаем сделку из БД
            deal_data = get_active_deal(code)
            if deal_data:
                amount = deal_data["amount"]
                currency = deal_data["currency"]
                sender_username = deal_data["sender_username"]
                receiver_username = message.from_user.username or message.from_user.first_name or "unknown_receiver"

                user_id = message.from_user.id
                wallet = get_user_wallet(user_id)
                wallet[currency] += amount
                
                # Сохраняем обновленный баланс
                update_user_wallet(user_id, wallet)

                keyboard = types.InlineKeyboardMarkup()
                lang = get_user_language(message.from_user.id)
                btn_wallet = types.InlineKeyboardButton(get_text(lang, "wallet"), callback_data="my_wallet")
                keyboard.add(btn_wallet)

                if currency == "Stars":
                    try:
                        stars_price = get_stars_price()
                        usd_value = amount * stars_price
                    except:
                        usd_value = amount * 0.017
                elif currency == "TON":
                    try:
                        ton_price = get_ton_price()
                        usd_value = amount * ton_price
                    except:
                        usd_value = amount * 2.0
                else:
                    usd_value = float(amount)

                usd_text = f"{usd_value:.2f}"
                symbol = "💹" if currency == "USDT" else "💠" if currency == "TON" else "⭐"

                lang = get_user_language(message.from_user.id)
                bot.send_message(
                    chat_id=message.chat.id,
                    text=f"{get_text(lang, 'deal_received', symbol, amount, currency, usd_text, sender_username)}\n\n<b>⚠️ВАЖНО: </b>Оплатите свою часть сделки @garant_avdeychka",
                    parse_mode="HTML",
                    reply_markup=keyboard
                )

                # Сохраняем сделку в аналитику
                save_deal_to_analytics_db(code, sender_username, receiver_username, amount, currency)

                # Отправляем уведомление ОБОИМ
                send_notification_to_both(sender_username, receiver_username, amount, currency, code)

                blacklist[code] = True
                save_blacklist(blacklist)
                remove_active_deal(code)
                return
            else:
                lang = get_user_language(message.from_user.id)
                bot.send_message(message.chat.id, get_text(lang, "invalid_command"))
                return

    # Показываем выбор языка для новых пользователей
    if message.from_user.id not in user_languages:
        keyboard = create_language_keyboard()
        bot.send_message(
            message.chat.id,
            "🌐 <b>Выберите язык / Choose language:</b>",
            reply_markup=keyboard,
            parse_mode='HTML'
        )
    else:
        show_main_menu(message.chat.id, message.from_user.id)

# === ОБРАБОТКА ВСЕХ СООБЩЕНИЙ ДЛЯ NFT ===
@bot.message_handler(func=lambda message: True, content_types=['text'])
@check_blocked
@improved_anti_flood_decorator
def handle_all_messages(message):
    """Обработчик всех текстовых сообщений для распознавания NFT"""
    # Сначала проверяем NFT подарки
    if not handle_nft_gift(message):
        # Если это не NFT, передаем другим обработчикам
        bot.process_new_messages([message])

def show_main_menu(chat_id, user_id):
    lang = get_user_language(user_id)
    
    text = (
        f"<b>{get_text(lang, 'welcome')}</b>\n\n"
        f"{get_text(lang, 'deal_shield_description')}"
    )

    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(types.InlineKeyboardButton(get_text(lang, "open_in_app"), url="https://t.me/wallet/start"))

    buttons = [
        (get_text(lang, "wallet"), "my_wallet"),
        (get_text(lang, "withdraw"), "withdraw"),
        (get_text(lang, "create_deal"), "create_deal")
    ]

    for i in range(0, len(buttons), 2):
        if i + 1 < len(buttons):
            keyboard.add(
                types.InlineKeyboardButton(buttons[i][0], callback_data=buttons[i][1]),
                types.InlineKeyboardButton(buttons[i+1][0], callback_data=buttons[i+1][1])
            )
        else:
            keyboard.add(types.InlineKeyboardButton(buttons[i][0], callback_data=buttons[i][1]))

    keyboard.add(types.InlineKeyboardButton(get_text(lang, "support"), url="https://t.me/DealShield_Support"))
    keyboard.add(types.InlineKeyboardButton("🌐 Language", callback_data="change_language"))

    bot.send_message(chat_id, text, reply_markup=keyboard, parse_mode='HTML')

# === CALLBACK ОБРАБОТЧИКИ ===
@bot.callback_query_handler(func=lambda call: call.data in [
    "my_wallet", "withdraw", "create_deal", "back_to_main", 
    "withdraw_ton", "withdraw_usdt", "withdraw_stars",
    "deal_ton", "deal_usdt", "deal_stars", "lang_ru", "lang_en", "change_language"
])
@check_blocked_callback
def handle_callback(call):
    user_id = call.from_user.id
    
    if call.data == "my_wallet":
        show_wallet(call.message, user_id)
    elif call.data == "withdraw":
        show_withdraw_menu(call.message, user_id)
    elif call.data == "create_deal":
        show_create_deal_menu(call.message, user_id)
    elif call.data == "back_to_main":
        show_main_menu(call.message.chat.id, user_id)
    elif call.data in ["withdraw_ton", "withdraw_usdt", "withdraw_stars"]:
        currency = call.data.replace("withdraw_", "").upper()
        start_withdraw(call.message, user_id, currency)
    elif call.data in ["deal_ton", "deal_usdt", "deal_stars"]:
        currency = call.data.replace("deal_", "").upper()
        start_deal_creation(call.message, user_id, currency)
    elif call.data.startswith("lang_"):
        language = call.data.replace("lang_", "")
        update_user_language_in_db(user_id, language)
        user_languages[user_id] = language
        bot.answer_callback_query(call.id, f"✅ Language set to {language.upper()}")
        show_main_menu(call.message.chat.id, user_id)
    elif call.data == "change_language":
        keyboard = create_language_keyboard()
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="🌐 <b>Выберите язык / Choose language:</b>",
            reply_markup=keyboard,
            parse_mode='HTML'
        )

    bot.answer_callback_query(call.id)

def show_wallet(message, user_id):
    wallet = get_user_wallet(user_id)
    total_usd = calculate_total_usd(wallet)
    lang = get_user_language(user_id)
    
    text = (
        f"{get_text(lang, 'your_wallet')}\n\n"
        f"{get_text(lang, 'ton_balance', wallet['TON'])}\n"
        f"{get_text(lang, 'usdt_balance', wallet['USDT'])}\n"
        f"{get_text(lang, 'stars_balance', wallet['Stars'])}\n\n"
        f"{get_text(lang, 'total_balance', total_usd)}"
    )
    
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(get_text(lang, "back"), callback_data="back_to_main"))
    
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text=text,
        reply_markup=keyboard,
        parse_mode='HTML'
    )

def show_withdraw_menu(message, user_id):
    wallet = get_user_wallet(user_id)
    lang = get_user_language(user_id)
    
    text = (
        f"{get_text(lang, 'withdraw_currency')}\n\n"
        f"{get_text(lang, 'choose_currency')}"
    )
    
    keyboard = types.InlineKeyboardMarkup()
    
    if wallet['TON'] > 0:
        keyboard.add(types.InlineKeyboardButton(f"💠 TON ({wallet['TON']})", callback_data="withdraw_ton"))
    if wallet['USDT'] > 0:
        keyboard.add(types.InlineKeyboardButton(f"💹 USDT ({wallet['USDT']})", callback_data="withdraw_usdt"))
    if wallet['Stars'] > 0:
        keyboard.add(types.InlineKeyboardButton(f"⭐ Stars ({wallet['Stars']})", callback_data="withdraw_stars"))
    
    keyboard.add(types.InlineKeyboardButton(get_text(lang, "back"), callback_data="back_to_main"))
    
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text=text,
        reply_markup=keyboard,
        parse_mode='HTML'
    )

def show_create_deal_menu(message, user_id):
    lang = get_user_language(user_id)
    
    text = (
        f"{get_text(lang, 'create_deal_title')}\n\n"
        f"{get_text(lang, 'choose_deal_currency')}"
    )
    
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("💠 TON", callback_data="deal_ton"))
    keyboard.add(types.InlineKeyboardButton("💹 USDT", callback_data="deal_usdt"))
    keyboard.add(types.InlineKeyboardButton("⭐ Stars", callback_data="deal_stars"))
    keyboard.add(types.InlineKeyboardButton(get_text(lang, "back"), callback_data="back_to_main"))
    
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text=text,
        reply_markup=keyboard,
        parse_mode='HTML'
    )

def start_withdraw(message, user_id, currency):
    wallet = get_user_wallet(user_id)
    balance = wallet[currency]
    
    save_user_state(user_id, "withdraw", {
        "currency": currency,
        "step": "amount"
    })
    
    symbol = "💠" if currency == "TON" else "💹" if currency == "USDT" else "⭐"
    lang = get_user_language(user_id)
    
    text = (
        f"<b>{symbol} Вывод {currency}</b>\n\n"
        f"💰 Ваш баланс: <b>{balance}</b>\n"
        f"{get_text(lang, 'enter_amount')}"
    )
    
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(get_text(lang, "back"), callback_data="withdraw"))
    
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text=text,
        reply_markup=keyboard,
        parse_mode='HTML'
    )

def start_deal_creation(message, user_id, currency):
    save_user_state(user_id, "deal_creation", {
        "currency": currency,
        "step": "amount"
    })
    
    symbol = "💠" if currency == "TON" else "💹" if currency == "USDT" else "⭐"
    lang = get_user_language(user_id)
    
    text = (
        f"<b>{symbol} Создание сделки {currency}</b>\n\n"
        f"{get_text(lang, 'enter_amount')}"
    )
    
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(get_text(lang, "back"), callback_data="create_deal"))
    
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text=text,
        reply_markup=keyboard,
        parse_mode='HTML'
    )

# === ОБРАБОТЧИКИ ТЕКСТОВЫХ СООБЩЕНИЙ ===
@bot.message_handler(func=lambda m: m.text and not m.text.startswith('/'))
@check_blocked
@improved_anti_flood_decorator
def handle_text(message):
    user_id = message.from_user.id
    
    # Обработка вывода средств
    withdraw_state = get_user_state(user_id, "withdraw")
    if withdraw_state:
        handle_withdraw_amount(message, user_id, withdraw_state)
        return
    
    # Обработка создания сделки
    deal_state = get_user_state(user_id, "deal_creation")
    if deal_state:
        handle_deal_amount(message, user_id, deal_state)
        return
    
    # Если сообщение не распознано
    lang = get_user_language(user_id)
    bot.send_message(message.chat.id, get_text(lang, "unknown_command"))

def handle_withdraw_amount(message, user_id, withdraw_state):
    lang = get_user_language(user_id)
    
    if withdraw_state["step"] == "amount":
        wallet = get_user_wallet(user_id)
        currency = withdraw_state["currency"]
        max_amount = wallet[currency]
        
        amount, error = validate_amount(message.text, max_amount)
        if error:
            bot.send_message(message.chat.id, f"❌ {error}")
            return
        
        withdraw_state["amount"] = amount
        withdraw_state["step"] = "wallet"
        save_user_state(user_id, "withdraw", withdraw_state)
        
        symbol = "💠" if currency == "TON" else "💹" if currency == "USDT" else "⭐"
        
        bot.send_message(
            message.chat.id,
            f"{get_text(lang, 'amount_accepted', amount, currency)}\n\n"
            f"{get_text(lang, 'enter_wallet')} {symbol}{currency}:"
        )
    
    elif withdraw_state["step"] == "wallet":
        wallet_address = message.text.strip()
        amount = withdraw_state["amount"]
        currency = withdraw_state["currency"]
        
        if not wallet_address:
            bot.send_message(message.chat.id, "❌ Адрес кошелька не может быть пустым")
            return
        
        # Списание средств
        user_wallet = get_user_wallet(user_id)
        user_wallet[currency] -= amount
        update_user_wallet(user_id, user_wallet)
        
        symbol = "💠" if currency == "TON" else "💹" if currency == "USDT" else "⭐"
        
        # Уведомление админу и гаранту
        username = message.from_user.username or message.from_user.first_name
        notification_text = (
            f"🚀 <b>ЗАПРОС НА ВЫВОД!</b>\n\n"
            f"👤 Пользователь: @{username}\n"
            f"💰 Сумма: {symbol}{amount} {currency}\n"
            f"📨 Кошелек: <code>{wallet_address}</code>\n"
            f"⏰ Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"💎 <b>Требуется подтверждение гаранта!</b>"
        )
        
        try:
            bot.send_message(NOTIFICATION_USER_ID, notification_text, parse_mode="HTML")
            bot.send_message(GARANT_USER_ID, notification_text, parse_mode="HTML")
        except Exception as e:
            logger.error(f"Ошибка отправки уведомления о выводе: {e}")
        
        bot.send_message(
            message.chat.id,
            f"{get_text(lang, 'withdraw_request_sent', symbol, amount, currency)}\n\n"
            f"📨 Адрес: <code>{wallet_address}</code>\n\n"
            f"{get_text(lang, 'waiting_garant_confirmation', 'garant_avdeychka')}"
        )
        
        remove_user_state(user_id, "withdraw")
        show_main_menu(message.chat.id, user_id)

def handle_deal_amount(message, user_id, deal_state):
    lang = get_user_language(user_id)
    
    if deal_state["step"] == "amount":
        amount, error = validate_amount(message.text)
        if error:
            bot.send_message(message.chat.id, f"❌ {error}")
            return
        
        currency = deal_state["currency"]
        
        # Создаем команду для пользователя
        command_map = {
            "TON": "/addingTON",
            "USDT": "/addingUSDT", 
            "Stars": "/addingS"
        }
        
        command = command_map.get(currency, "/addingS")
        
        bot.send_message(
            message.chat.id,
            f"{get_text(lang, 'amount_accepted', amount, currency)}\n\n"
            f"{get_text(lang, 'use_command', command, int(amount))}"
        )
        
        remove_user_state(user_id, "deal_creation")
        show_main_menu(message.chat.id, user_id)

# === КОМАНДЫ ДОБАВЛЕНИЯ СРЕДСТВ ===
@bot.message_handler(func=lambda m: m.text.startswith("/addingTON"))
@check_blocked
@improved_anti_flood_decorator
def handle_addingTON(message):
    handle_adding_currency(message, "TON")

@bot.message_handler(func=lambda m: m.text.startswith("/addingUSDT"))
@check_blocked
@improved_anti_flood_decorator
def handle_addingUSDT(message):
    handle_adding_currency(message, "USDT")

@bot.message_handler(func=lambda m: m.text.startswith("/addingS"))
@check_blocked
@improved_anti_flood_decorator
def handle_addingStars(message):
    handle_adding_currency(message, "Stars")

# === АВТОМАТИЧЕСКИЕ БЭКАПЫ ===
def auto_backup():
    """Автоматическое резервное копирование данных"""
    try:
        if not os.path.exists('backups'):
            os.makedirs('backups')
            
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_files = ['users.db', 'bot_analytics.db', 'wallets.db', 'black.json', 'blocked_users.json', 'used_bot.txt', 'deals.txt']
        
        for file in backup_files:
            if os.path.exists(file):
                shutil.copy2(file, f'backups/{file}_{timestamp}')
        
        logger.info("✅ Автобэкап создан")
    except Exception as e:
        logger.error(f"❌ Ошибка бэкапа: {e}")

# === ОБРАБОТКА ОШИБОК API ===
def safe_polling():
    """Безопасный запуск бота с обработкой ошибок"""
    while True:
        try:
            logger.info("🚀 Запуск бота...")
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            logger.error(f"❌ Ошибка бота: {e}")
            logger.info("🔄 Перезапуск через 10 секунд...")
            time.sleep(10)

# === ЗАПУСК БОТА ===
if __name__ == "__main__":
    print("⚡ СДЕЛАНО AStudios (тг: @Quil_T_T)")
    print("\n🚀 ЗАПУСКАЕМ БОТА")
    
    # Запускаем безопасный polling
    safe_polling()