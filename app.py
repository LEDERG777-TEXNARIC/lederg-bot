#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import telebot
from telebot import types
import requests
import json
import time
import os
import threading
import random
import socket
import datetime
import re
import sys
import signal
from urllib.parse import parse_qs, unquote
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

# Отключение системного спама ошибок сети в консоли (таймауты/обрывы не будут мозолить глаза)
telebot.logger.setLevel(logging.CRITICAL)

# ==================== ГЛОБАЛЬНЫЕ НАСТРОЙКИ СИСТЕМЫ ====================
TOKEN = "8939573062:AAHknUKGdCbDAuFeff_778rEuFru4n6iXbU"
bot = telebot.TeleBot(TOKEN)

# Директории и файлы баз данных
USERS_DIR = "Accounts"
SETTINGS_FILE = "user_settings.json"
CACHE_FILE = "proxy_cache.json"
REPORTS_FILE = "reports_db.json"
ADMIN_CFG = "admin_config.json"

# Оперативная память системы
SHORT_LINKS_CACHE = {}  
USER_STATE = {} 

print(f"[{time.strftime('%H:%M:%S')}] 🧬 Система LEDERG MTPROTO PROXY запущена и готова к работе.")

# === МАСШТАБНАЯ БАЗА ИСТОЧНИКОВ MTPROTO (ДЛЯ ПОЛЬЗОВАТЕЛЕЙ) ===
PROXY_SOURCES = [
    "https://raw.githubusercontent.com/Argh94/Proxy-List/main/mtproto.txt",
    "https://raw.githubusercontent.com/SoliSpirit/mtproto/master/all_proxies.txt",
    "https://raw.githubusercontent.com/Grim1313/mtproto-for-telegram/master/all_proxies.txt",
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/tg/mtproto.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/mtproto.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/mtproto.txt",
    "https://raw.githubusercontent.com/prxchk/proxy-list/main/mtproto.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub6_MTProto.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies.txt",
    "https://raw.githubusercontent.com/BioniC356/telegram-proxy-parser/master/proxies/mtproto.txt",
    "https://raw.githubusercontent.com/a2o/sneaky-proxies/main/mtproto.txt",
    "https://raw.githubusercontent.com/mahdibland/Telegram-Proxies/master/mtproto.txt",
    "https://raw.githubusercontent.com/peckpeck/MTProxy/master/mtproto.txt",
    "https://raw.githubusercontent.com/Leon1o1/Telegram-Proxies/master/mtproto.txt",
    "https://raw.githubusercontent.com/yoohoomail1392/vless/main/tg",
    "https://raw.githubusercontent.com/shaghayeghhjh/Telegram_Proxy/main/telegram_proxy.txt",
    "https://raw.githubusercontent.com/L4Zzy1/telegram-proxies/master/mtproto.txt",
    "https://raw.githubusercontent.com/sasan386/telegram/main/mtproto",
    "https://raw.githubusercontent.com/Shuntiseks/Telegram-Proxy-MTPROTO/main/proxies.txt",
    "https://raw.githubusercontent.com/MTProToTg1/Mtproto1/main/Mtproto.txt",
    "https://raw.githubusercontent.com/NvidiaTg2002/Free_mtproto/main/Telegram_proxies",
    "https://raw.githubusercontent.com/ALIILAPRO/MTPROTO_Telegram_Proxies/main/TelegramProxy.txt",
    "https://raw.githubusercontent.com/soroushmirzaei/telegram-proxies-collector/main/proxies",
    "https://raw.githubusercontent.com/amooSponge/MTProxyList/master/proxy.txt",
    "https://raw.githubusercontent.com/KryptonXX/mtproxy_list/main/proxies",
    "https://raw.githubusercontent.com/v11002345/proxylist/master/mtp_proxy",
    "https://raw.githubusercontent.com/amirhesamsz/Tg_Mtproxy/main/mtproto.txt",
    "https://raw.githubusercontent.com/hmnp42/MTProxy/master/All-Proxies.txt",
    "https://raw.githubusercontent.com/mizai99/Tg_Mtproto/main/Mtproto.txt",
    "https://raw.githubusercontent.com/tash0306/MTProxyList/master/proxy.txt",
    "https://raw.githubusercontent.com/MehradAshoori/MehradProxy/master/List",
    "https://raw.githubusercontent.com/MrAliXm/Mtproto/main/proxies.txt",
    "https://raw.githubusercontent.com/FarzadShariati/Tg_Mtproto/main/Mtproto.txt",
    "https://raw.githubusercontent.com/BeniPari/BeniPari/main/mttp",
    "https://raw.githubusercontent.com/AmirevVn/MTProto-Proxy-list/main/Proxylist.txt",
    "https://raw.githubusercontent.com/vitoo930930/proxyp-poroxp-vless-trojan-vmess/main/Mtproxy/mtproto.txt",
    "https://raw.githubusercontent.com/Shantyyv/Proxy/main/M_PROXY",
    "https://raw.githubusercontent.com/shaghayegh20001000/Shaghi_Proxy/main/proxy.txt",
    "https://raw.githubusercontent.com/V2rayConfigsByAmin/Mtproto/main/proxies.txt",
    "https://raw.githubusercontent.com/Rooney1341/MTProxy/main/mtproto.txt",
    "https://raw.githubusercontent.com/sajjadb2c/MyProxies/main/Proxys_All.txt",
    "https://raw.githubusercontent.com/P40331000/Mtp/main/List.txt",
    "https://raw.githubusercontent.com/Ahmetya2123/A/main/all_proxies.txt",
    "https://raw.githubusercontent.com/ImanMontajabi/Telegram-Proxy/master/mtproto.txt",
    "https://raw.githubusercontent.com/yemount/mtproto/master/all_proxies.txt",
    "https://raw.githubusercontent.com/Azi1z/Proxy-List/main/mtproto.txt",
    "https://raw.githubusercontent.com/xHosse/TG-Proxies/master/mtprox",
    "https://raw.githubusercontent.com/TelegramProxy/TelegramProxy/main/mtproto.txt",
    "https://raw.githubusercontent.com/Hassan0n2002/TMT_P/main/P-T",
    "https://raw.githubusercontent.com/devho3ein/tg-proxy/refs/heads/main/proxys/All_Proxys.txt",
    "https://raw.githubusercontent.com/ALIILAPRO/MTProtoProxy/main/mtproto.txt",
    "https://raw.githubusercontent.com/Firmfox/Proxify/main/telegram_proxies/mtproto.txt",
    "https://raw.githubusercontent.com/MustafaBaqer/VestraNet-Nodes/main/protocols/mtproto.txt",
    "https://raw.githubusercontent.com/telemt/telemt/main/proxies.txt",
    "https://raw.githubusercontent.com/iwh3n/tg-proxy/main/proxys/All_Proxys.txt"
]

# ==================== БЕЗОПАСНОЕ ЗАВЕРШЕНИЕ РАБОТЫ (CTRL + C) ====================
def graceful_exit(signum, frame):
    print(f"\n[{time.strftime('%H:%M:%S')}] 🛑 Получен сигнал завершения. Очистка ресурсов и безопасное отключение...")
    sys.exit(0)

signal.signal(signal.SIGINT, graceful_exit)
signal.signal(signal.SIGTERM, graceful_exit)

# ==================== МЕНЕДЖМЕНТ БАЗ ДАННЫХ И ПАМЯТИ ====================
def load_json(filepath=SETTINGS_FILE):
    """Загружает данные из JSON файла с защитой от ошибок"""
    try: 
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as file:
                return json.load(file)
    except: pass
    return {}

def save_json(filepath, data):
    """Безопасно сохраняет данные в JSON формат"""
    try: 
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except: pass

def get_admins():
    """Возвращает список ID администраторов проекта"""
    data = load_json(ADMIN_CFG)
    admins = data.get("owners", [])
    return admins if isinstance(admins, list) else []

def add_admin(chat_id):
    """Добавляет пользователя в список администраторов"""
    data = load_json(ADMIN_CFG)
    admins = data.get("owners", [])
    if chat_id not in admins:
        admins.append(chat_id)
        data["owners"] = admins
        save_json(ADMIN_CFG, data)
        return True
    return False

def remove_admin(chat_id):
    """Удаляет пользователя из списка администраторов"""
    data = load_json(ADMIN_CFG)
    admins = data.get("owners", [])
    if chat_id in admins:
        admins.remove(chat_id)
        data["owners"] = admins
        save_json(ADMIN_CFG, data)
        return True
    return False

def get_user_setting(user_id, key, default=None):
    """Чтение персональной настройки пользователя"""
    return load_json().get(str(user_id), {}).get(key, default)

def update_user_setting(user_id, key, value, is_list_append=False):
    """Обновление персональной настройки пользователя"""
    db = load_json()
    uid = str(user_id)
    if uid not in db: db[uid] = {}
    if is_list_append:
        current_list = db[uid].get(key, [])
        if value not in current_list: current_list.append(value)
        db[uid][key] = current_list
    else: 
        db[uid][key] = value
    save_json(SETTINGS_FILE, db)

def escape_html(text):
    """Фильтр для предотвращения ошибок Markdown/HTML разметки Telegram"""
    if not text: return ""
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def hash_url(url):
    """Хэширует длинные ссылки для безопасной передачи в кнопках Telegram (лимит 64 байта)"""
    global SHORT_LINKS_CACHE
    if len(SHORT_LINKS_CACHE) > 3000: SHORT_LINKS_CACHE.clear()
    url_hash = f"{abs(hash(url)):x}"[:12]
    SHORT_LINKS_CACHE[url_hash] = url
    return url_hash

def retrieve_url(url_hash):
    """Восстанавливает URL из кэша по хэшу"""
    return SHORT_LINKS_CACHE.get(url_hash)

def submit_complaint(url_hash, reason, user_id):
    """Обрабатывает жалобу на прокси и удаляет неисправный узел из базы"""
    url = retrieve_url(url_hash)
    if not url: return False
    
    # Удаление неисправного узла из оперативного кэша
    cached_db = load_json(CACHE_FILE)
    base_links = cached_db.get("lederg_base", [])
    if url in base_links:
        base_links.remove(url)
        cached_db["lederg_base"] = base_links
        save_json(CACHE_FILE, cached_db)

    # Запись жалобы в логи администратора
    reports = load_json(REPORTS_FILE)
    if not isinstance(reports, list): reports = []
    timestamp = time.strftime("%Y-%m-%d %H:%M")
    reports.insert(0, {"time": timestamp, "reason": reason, "link": url, "user_id": user_id})
    save_json(REPORTS_FILE, reports[:150]) # Храним последние 150 жалоб
    return True


# ==================== ДВИЖОК ВАЛИДАЦИИ И СБОРА MTPROTO (СУПЕР-ЯДРО) ====================
def is_valid_secret(secret):
    """Проверяет корректность секретного ключа (защита от мусорных ссылок)"""
    if not secret: return False
    clean_secret = secret.lower().strip()
    if clean_secret.startswith("ee") or clean_secret.startswith("dd"): clean_secret = clean_secret[2:]
    return bool(re.match(r"^[0-9a-f]{32,}", clean_secret))

def parse_mtproto_url(link):
    """Извлекает хост, порт и секрет из ссылки MTProto"""
    try:
        query = unquote(link).split("?")[1]
        params = parse_qs(query)
        return params.get('server',[''])[0], int(params.get('port',[0])[0]), params.get('secret',[''])[0]
    except: return None, None, None

def strict_tcp_ping(host, port, timeout=2.5):
    """Двойная проверка соединения TCP сокетом. Гарантирует отсев нестабильных прокси."""
    try:
        start_time = time.time()
        s1 = socket.create_connection((host, port), timeout=timeout)
        s1.close()
        ping1 = int((time.time() - start_time) * 1000)

        time.sleep(0.1) # Пауза для проверки стабильности канала (Защита от ТСПУ/DPI)
        
        start_time2 = time.time()
        s2 = socket.create_connection((host, port), timeout=timeout)
        s2.close()
        ping2 = int((time.time() - start_time2) * 1000)

        return True, (ping1 + ping2) // 2
    except:
        return False, 99999

def validate_and_fetch_proxies(raw_links, required_amount=1):
    """
    Интеллектуальный цикличный валидатор. 
    Гарантированно ищет указанное количество рабочих прокси, проверяя базу порциями.
    Даже при жестких блокировках он не остановится, пока не соберет нужное число!
    """
    if not raw_links: return []
    random.shuffle(raw_links)
    
    valid_proxies = []
    chunk_size = 150 # Захватываем по 150 прокси за раз
    
    for i in range(0, len(raw_links), chunk_size):
        chunk = raw_links[i : i + chunk_size]
        candidates = []
        
        # Отбор формально правильных ссылок
        for url in chunk:
            host, port, secret = parse_mtproto_url(url)
            if host and port and is_valid_secret(secret):
                candidates.append((host, port, url))
                
        # Многопоточная Socket-Атака
        with ThreadPoolExecutor(max_workers=100) as executor:
            futures = {executor.submit(strict_tcp_ping, c[0], c[1], 2.5): c[2] for c in candidates}
            
            for future in as_completed(futures):
                original_url = futures[future]
                try: 
                    success, latency = future.result()
                    if success: 
                        valid_proxies.append((latency, original_url))
                        # Если собрали нужное количество — прерываем цикл и возвращаем результат!
                        if len(valid_proxies) >= required_amount:
                             valid_proxies.sort(key=lambda x: x[0])
                             return valid_proxies[:required_amount]
                except: pass
                
    # Если база закончилась, возвращаем то, что смогли найти
    valid_proxies.sort(key=lambda x: x[0]) 
    return valid_proxies[:required_amount]


def scrape_global_database():
    """Сбор и дедупликация прокси со всех уголков GitHub"""
    collected_links = []
    def scrape(url):
        try:
            response_text = requests.get(url, timeout=5.0).text
            links = re.findall(r"(?:tg://proxy\?|https://t\.me/proxy\?)[^\s\"'<>]+", response_text)
            return [link.replace("https://t.me/proxy?", "tg://proxy?") for link in links]
        except: return []
        
    with ThreadPoolExecutor(max_workers=75) as executor:
        futures = [executor.submit(scrape, source) for source in PROXY_SOURCES]
        for f in as_completed(futures): collected_links.extend(f.result())

    try:
        api_data = requests.get("https://mtpro.xyz/api/?type=mtproto", timeout=8).json()
        for item in api_data: collected_links.append(f"tg://proxy?server={item['host']}&port={item['port']}&secret={item['secret']}")
    except: pass
         
    unique_links = list(set(collected_links))
    if len(unique_links) > 200: 
         save_json(CACHE_FILE, {"lederg_base": unique_links, "scraped_time_at": time.time()})
         
    print(f"[{time.strftime('%H:%M:%S')}] Сбор базы завершен. Сохранено {len(unique_links)} уникальных MTProto узлов.")
    return unique_links


# ==================== ИНТЕРФЕЙС ТЕЛЕГРАМ (ГЛАВНОЕ МЕНЮ И КЛАВИАТУРЫ) ====================

def generate_reply_keyboard(user_id):
    """Генерирует нижнюю клавиатуру. Скрывает Админ-Панель от обычных пользователей."""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(types.KeyboardButton("🚀 ЭКО-СИСТЕМА LEDERG PROXY"))
    if user_id in get_admins():
        keyboard.add(types.KeyboardButton("👑 АДМИН ПАНЕЛЬ"))
    return keyboard

def generate_main_menu(first_name):
    name = escape_html(first_name)
    text = (f"<b>🌟 СИСТЕМА ОБХОДА БЛОКИРОВОК LEDERG 👋</b>\n\n"
            f"Приветствую вас, <b>{name}</b>! Моя главная задача — обеспечить вам "
            f"бесперебойный, стабильный и сверхбыстрый доступ к Telegram.\n\n"
            f"🛡 <b>Наши алгоритмы:</b>\n"
            f"Я сканирую более 100 зарубежных репозиториев, пропускаю найденные узлы "
            f"через многопоточный сканер защиты DPI и предоставляю вам только те серверы, "
            f"которые обеспечивают минимальную задержку.\n\n"
            f"Пожалуйста, выберите нужный раздел меню:")
            
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("🔮 ПОЛУЧИТЬ MTPROTO ПРОКСИ", callback_data="menu_get_proxies"))
    markup.add(types.InlineKeyboardButton("🛠 Инструментарий", callback_data="menu_tools"),
               types.InlineKeyboardButton("📚 База знаний (Гайды)", callback_data="menu_guides"))
    markup.add(types.InlineKeyboardButton("⭐️ Моё Избранное", callback_data="menu_favorites"),
               types.InlineKeyboardButton("💎 Скачать базу (TXT)", callback_data="menu_download_db"))
    markup.add(types.InlineKeyboardButton("⚙️ Настройки рассылки", callback_data="menu_settings"))
    markup.add(types.InlineKeyboardButton("📡 Статистика системы", callback_data="menu_statistics"))
    return text, markup

@bot.message_handler(commands=["start", "menu"])
def handle_start(message):
    text, markup = generate_main_menu(message.from_user.first_name)
    bot.send_message(message.chat.id, "Система управления инициализирована. Используйте кнопки ниже для навигации.", reply_markup=generate_reply_keyboard(message.chat.id))
    bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=markup)
    os.makedirs(f"{USERS_DIR}/{message.chat.id}", exist_ok=True)
    USER_STATE.pop(message.chat.id, None)

@bot.message_handler(func=lambda msg: msg.text == "🚀 ЭКО-СИСТЕМА LEDERG PROXY")
def handle_home_button(message):
    handle_start(message)

@bot.callback_query_handler(func=lambda call: call.data in ["action_back", "action_close"])
def handle_navigation(call):
    try: bot.answer_callback_query(call.id)
    except: pass
    USER_STATE.pop(call.message.chat.id, None)
    
    if call.data == "action_back":
        text, markup = generate_main_menu(call.from_user.first_name)
        try: bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=markup)
        except: pass
    else:
        try: bot.delete_message(call.message.chat.id, call.message.message_id)
        except: pass


# 👑 ======================= АДМИН ПАНЕЛЬ И ПРАВА ДОСТУПА ========================== 
@bot.message_handler(commands=["claim_admin"])
def handle_claim_admin(message):
    admins = get_admins()
    if admins:
        bot.send_message(message.chat.id, f"🚫 <b>В доступе отказано.</b> Владелец проекта уже назначен. Операция невозможна.", parse_mode="HTML")
        return
    add_admin(message.chat.id)
    bot.send_message(message.chat.id, "🎆 <b>Права создателя успешно получены.</b>\nСистема признала вас владельцем. В нижней клавиатуре теперь доступна Админ-Панель.", parse_mode="HTML", reply_markup=generate_reply_keyboard(message.chat.id))

@bot.message_handler(func=lambda msg: msg.text == "👑 АДМИН ПАНЕЛЬ")
def handle_admin_panel_text(message):
   if message.chat.id in get_admins(): show_admin_panel(message)
   else: bot.send_message(message.chat.id, "🛑 У вас нет прав доступа к панели администратора.")

@bot.message_handler(commands=["admin"])
def handle_admin_command(message):
   if message.chat.id in get_admins(): show_admin_panel(message)
   else: bot.send_message(message.chat.id, "🛑 У вас нет прав доступа.")

def show_admin_panel(message_obj):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("🤬 Просмотр логов и жалоб", callback_data="admin_view_reports"))
    markup.add(types.InlineKeyboardButton("📢 Сделать глобальную рассылку", callback_data="admin_broadcast"))
    markup.add(types.InlineKeyboardButton("👥 Управление администраторами", callback_data="admin_manage_users"))
    markup.add(types.InlineKeyboardButton("✖ Закрыть", callback_data="action_close"))
    text = "👑 <b>ПАНЕЛЬ УПРАВЛЕНИЯ СИСТЕМОЙ</b>\n\nДобро пожаловать в конфигуратор. Выберите необходимое действие:"
    try: bot.send_message(message_obj.chat.id, text, parse_mode="HTML", reply_markup=markup)
    except: pass

@bot.callback_query_handler(func=lambda call: call.data == "admin_view_reports")
def admin_show_reports(call):
   if call.from_user.id not in get_admins(): return
   reports = load_json(REPORTS_FILE) if isinstance(load_json(REPORTS_FILE), list) else []
   
   markup = types.InlineKeyboardMarkup()
   markup.add(types.InlineKeyboardButton("🗑 Очистить базу жалоб", callback_data="admin_clear_reports"))
   markup.add(types.InlineKeyboardButton("❌ Закрыть", callback_data="action_close"))

   text = f"📋 <b>ЖАЛОБЫ ПОЛЬЗОВАТЕЛЕЙ (Последние 15): </b>\n\n"
   for rp in reports[:15]: 
       text += f"👤 ID пользователя: {rp.get('user_id')}\n⚡ <b>Проблема:</b> {rp.get('reason')}\n🔗 Линк: <code>{escape_html(rp.get('link'))}</code>\n\n"
   
   if not reports: text="☀️ Жалоб в базе не обнаружено! Система работает стабильно."

   bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "admin_clear_reports")
def admin_clear_reports(call):
     if call.from_user.id not in get_admins(): return
     try: 
        save_json(REPORTS_FILE, [])
        bot.answer_callback_query(call.id, "Логи жалоб успешно очищены.", show_alert=True)
     except: pass 
     admin_show_reports(call)

@bot.callback_query_handler(func=lambda call: call.data == "admin_broadcast")
def admin_broadcast_init(call):
     if call.from_user.id not in get_admins(): return
     markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 Отмена", callback_data="action_back"))
     bot.edit_message_text("📣 <b>МОДУЛЬ ГЛОБАЛЬНОЙ РАССЫЛКИ</b> \n\nПожалуйста, отправьте в чат текст сообщения. Оно будет немедленно доставлено всем пользователям бота.", call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=markup)
     USER_STATE[call.message.chat.id] = "STATE_BROADCAST_MSG"

@bot.callback_query_handler(func=lambda call: call.data == "admin_manage_users")
def admin_manage_users(call):
    if call.from_user.id not in get_admins(): return
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("➕ Добавить админа", callback_data="admin_add_user"),
               types.InlineKeyboardButton("➖ Удалить админа", callback_data="admin_remove_user"))
    markup.add(types.InlineKeyboardButton("✖ Закрыть", callback_data="action_close"))
    
    admins = get_admins()
    text = f"👥 <b>УПРАВЛЕНИЕ ПРАВАМИ ДОСТУПА</b>\n\nТекущие администраторы системы:\n"
    for a in admins: text += f"├ <code>{a}</code>\n"
    
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["admin_add_user", "admin_remove_user"])
def admin_modify_rights(call):
    if call.from_user.id not in get_admins(): return
    markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 Отмена", callback_data="action_back"))
    if call.data == "admin_add_user":
        text = "➕ Отправьте Telegram ID пользователя, которому хотите <b>выдать</b> права администратора:"
        USER_STATE[call.message.chat.id] = "STATE_ADD_ADMIN"
    else:
        text = "➖ Отправьте Telegram ID пользователя, которого хотите <b>лишить</b> прав администратора:"
        USER_STATE[call.message.chat.id] = "STATE_REMOVE_ADMIN"
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=markup)


# 1 =========== ВЫДАЧА ПРОКСИ И ГЕНЕРАТОР =============== 
@bot.callback_query_handler(func=lambda call: call.data == "menu_get_proxies")
def show_proxy_generator(call):
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(types.InlineKeyboardButton("1 прокси", callback_data="generate__1"), 
               types.InlineKeyboardButton("5 прокси", callback_data="generate__5"), 
               types.InlineKeyboardButton("10 прокси", callback_data="generate__10"))
    markup.add(types.InlineKeyboardButton("🔙 Назад в меню", callback_data="action_back"))
    text = (f"🪐 <b>ВЫДАЧА ПРОКСИ-СЕРВЕРОВ</b>\n\n"
            f"Укажите необходимое количество соединений.\n\n"
            f"⚠️ <i>Примечание: Система не выдаст вам нерабочие серверы. Мы будем сканировать "
            f"базу до тех пор, пока не найдем ровно запрошенное количество узлов с идеальным откликом. "
            f"Процесс может занять несколько секунд.</i>")
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("generate__") or call.data.startswith("req_more__"))
def process_proxy_generation(call):
    amount = 1
    if "generate__" in call.data: amount = int(call.data.split("__")[1])
    else: amount = int(call.data.split("req_more__")[1])
        
    try: bot.edit_message_text(f"⚙️ <b>Система в работе...</b>\nМногопоточный сканер проверяет доступность узлов связи. Ищем {amount} стабильных соединений... Пожалуйста, подождите ⏳", call.message.chat.id, call.message.message_id, parse_mode="HTML")
    except: pass
    
    db_cache = []
    if os.path.exists(CACHE_FILE): 
         try: db_cache = load_json(CACHE_FILE).get("lederg_base", [])
         except: pass
    if not db_cache: db_cache = scrape_global_database()
    
    # 100% ГАРАНТИРОВАННАЯ ВЫДАЧА
    valid_proxies = validate_and_fetch_proxies(db_cache, amount)
    
    if not valid_proxies: 
         try: bot.answer_callback_query(call.id, "К сожалению, в данный момент наблюдаются серьезные региональные блокировки. Попробуйте еще раз!", show_alert=True)
         except: pass
         return

    try: bot.delete_message(call.message.chat.id, call.message.message_id)
    except: pass

    for index, (ping_ms, proxy_link) in enumerate(valid_proxies):
        host, port, secret = parse_mtproto_url(proxy_link)
        url_hash = hash_url(proxy_link) 
        
        status_text = "Идеальное соединение 🟢" if ping_ms <= 300 else "Стабильное соединение 🟡" if ping_ms < 800 else "Приемлемое соединение 🟠"
        message_text = (f"💠 <b>МАГИСТРАЛЬНЫЙ УЗЕЛ LEDERG:</b>\n\n"
                  f"⚡️ Задержка (Ping) :: <code>{ping_ms} ms</code>\n"
                  f"🧿 Сервер (IP/Domain) : <code>{escape_html(host)}</code>\n"
                  f"🔰 Порт : <code>{port}</code>\n"
                  f"📊 Статус: <b>{status_text}</b>")

        markup = types.InlineKeyboardMarkup()
        clean_url = proxy_link.replace("tg://proxy?","https://t.me/proxy?")
        
        markup.add(types.InlineKeyboardButton("🚀 ПОДКЛЮЧИТЬСЯ", url=clean_url))
        markup.row(types.InlineKeyboardButton("⭐ В Избранное", callback_data="action_save_fav"), 
                   types.InlineKeyboardButton("⚠️ Пожаловаться", callback_data=f"report_proxy_{url_hash}"))
        
        if index == len(valid_proxies) - 1: 
             markup.add(types.InlineKeyboardButton(f"♻️ Выдать еще {amount} прокси", callback_data=f"req_more__{amount}"))
             markup.add(types.InlineKeyboardButton("✖ Скрыть", callback_data="action_close"))

        bot.send_message(call.message.chat.id, f"{message_text}\n\n<code>{escape_html(proxy_link)}</code>", reply_markup=markup, parse_mode="HTML")
        time.sleep(0.3)

@bot.callback_query_handler(func=lambda call: "report_proxy_" in call.data)
def handle_report_menu(call):
    url_hash = call.data.replace("report_proxy_", "") 
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔌 Сервер не отвечает (Мертв)", callback_data=f"send_rep_dead_{url_hash}"))
    markup.add(types.InlineKeyboardButton("📢 Рекламный/Спонсорский канал недопустим", callback_data=f"send_rep_spam_{url_hash}"))
    markup.add(types.InlineKeyboardButton("🐌 Очень низкая скорость", callback_data=f"send_rep_slow_{url_hash}"))
    markup.add(types.InlineKeyboardButton("🔙 Отмена", callback_data="action_close"))

    try: bot.edit_message_text("⚠️ <b>ОФОРМЛЕНИЕ ЖАЛОБЫ</b>\n\nПожалуйста, укажите причину вашей жалобы. Этот сервер будет немедленно исключен из нашей базы данных.", call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=markup)
    except: pass


@bot.callback_query_handler(func=lambda call: "send_rep_" in call.data)
def process_report_action(call):
    data_parts = call.data.split("_")
    reason_code = data_parts[2]
    url_hash = data_parts[3]
    
    reason_str = "Неизвестно"
    if reason_code == "dead": reason_str = "Сервер недоступен"
    elif reason_code == "spam": reason_str = "Нежелательная реклама"
    elif reason_code == "slow": reason_str = "Низкая скорость соединения"
        
    actual_url = retrieve_url(url_hash)
    if not actual_url:
         try: bot.answer_callback_query(call.id, "Ссылка устарела в кэше. Жалоба невозможна.", show_alert=True) 
         except: pass 
         return

    submit_complaint(url_hash, reason_str, call.from_user.id)
    markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🛑 Скрыть сообщение", callback_data="action_close"))
    try:
        bot.edit_message_text(f"✅ <b>Благодарим за помощь!</b>\n\nНеисправный прокси-сервер удален из базы данных. Ваша жалоба («{reason_str}») передана администраторам.", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="HTML")
        bot.answer_callback_query(call.id, "Успешно удалено из базы!", show_alert=False)
    except: pass 


# 2 ============= ИНСТРУМЕНТАРИЙ И БАЗА ЗНАНИЙ =======
@bot.callback_query_handler(func=lambda call: call.data == "menu_tools")
def show_tools_menu(call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("🛠 Расшифровать MTProto ссылку", callback_data="tool_decode"))
    markup.add(types.InlineKeyboardButton("🔳 Создать QR-код из ссылки", callback_data="tool_qr"))
    markup.add(types.InlineKeyboardButton("🔎 Узнать геолокацию по IP", callback_data="tool_geo"))
    markup.add(types.InlineKeyboardButton("⚡ Проверить пинг серверов Telegram", callback_data="tool_tg_ping"))
    markup.add(types.InlineKeyboardButton("🌐 DNS Lookup (Cloudflare DoH)", callback_data="tool_dns"))
    markup.add(types.InlineKeyboardButton("🔙 Назад в меню", callback_data="action_back"))
    text = ("🧰 <b>ИНСТРУМЕНТАРИЙ LEDERG</b>\n\nЗдесь собраны профессиональные утилиты для сетевой диагностики и работы с прокси-серверами.")
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "menu_guides")
def show_guides_menu(call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("📱 Инструкция для iPhone (iOS)", callback_data="guide_ios"))
    markup.add(types.InlineKeyboardButton("🤖 Инструкция для Android", callback_data="guide_android"))
    markup.add(types.InlineKeyboardButton("💻 Инструкция для ПК (Desktop)", callback_data="guide_pc"))
    markup.add(types.InlineKeyboardButton("🔙 Назад в меню", callback_data="action_back"))
    text = ("📚 <b>БАЗА ЗНАНИЙ СИСТЕМЫ</b>\n\nВыберите вашу платформу, чтобы получить подробную инструкцию по настройке и подключению:")
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("guide_"))
def show_specific_guide(call):
    topic = call.data.split("_")[1]
    markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 Назад к инструкциям", callback_data="menu_guides"))
    
    if topic == "ios":
        text = ("📱 <b>Подключение на iPhone / iPad:</b>\n\n1. Нажмите на кнопку «ПОДКЛЮЧИТЬСЯ» под любым сервером.\n2. В открывшемся окне Telegram нажмите «Разрешить» или «Добавить прокси».\n3. В верхней части экрана появится значок щита — это означает, что обход блокировки успешно активирован!")
    elif topic == "android":
        text = ("🤖 <b>Подключение на Android:</b>\n\n1. Нажмите на кнопку «ПОДКЛЮЧИТЬСЯ».\n2. Telegram автоматически предложит применить настройки. Подтвердите действие.\n\n<i>Совет: Периодически удаляйте нерабочие прокси из списка в настройках Telegram, чтобы приложение работало быстрее.</i>")
    elif topic == "pc":
        text = ("💻 <b>Подключение на ПК (Telegram Desktop):</b>\n\nСуществует два способа:\n1. Кликните по ссылке-кнопке, если клиент поддерживает прямые переходы.\n2. Если кнопка не срабатывает, скопируйте ссылку, начинающуюся на <code>tg://proxy...</code>, отправьте её себе в «Избранное» и кликните по ней прямо в чате.")
    else: text = "Информация не найдена."
    
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["tool_decode", "tool_qr", "tool_geo", "tool_dns"])
def process_tool_selection(call):
    markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🛑 Отмена операции", callback_data="h_tools_menu"))
    prompt = ""
    
    if call.data == "tool_decode":
        prompt = "🛠 Отправьте в чат ссылку на MTProto прокси, чтобы система разобрала её на IP, порт и секретный ключ:"
        USER_STATE[call.message.chat.id] = "STATE_DECODE_LINK"
    elif call.data == "tool_qr":
        prompt = "🔳 Отправьте любую ссылку, и я сгенерирую сканируемый QR-код:"
        USER_STATE[call.message.chat.id] = "STATE_GENERATE_QR"
    elif call.data == "tool_geo":
        prompt = "🗺 Отправьте IP-адрес (например: <code>8.8.8.8</code>), чтобы узнать страну и провайдера:"
        USER_STATE[call.message.chat.id] = "STATE_GEO_IP"
    elif call.data == "tool_dns":
        prompt = "🔍 Отправьте домен (например: <code>google.com</code>), чтобы узнать его защищенные IP-адреса:"
        USER_STATE[call.message.chat.id] = "STATE_DNS_LOOKUP"
    
    bot.edit_message_text(prompt, call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=markup)


# ============== ИНТЕРАКТИВНЫЙ ПЕРЕХВАТЧИК ТЕКСТА (ЖДЕМ ВВОДА) ======
@bot.message_handler(func=lambda msg: msg.chat.id in USER_STATE)
def handle_interactive_input(message):
     state = USER_STATE[message.chat.id]
     user_input = message.text.strip()
     USER_STATE.pop(message.chat.id, None)
     
     markup_close = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("✖ Скрыть сообщение", callback_data="action_close"))

     if state == "STATE_BROADCAST_MSG":
            if message.chat.id not in get_admins(): return
            users = []
            if os.path.exists(USERS_DIR): users = [int(u) for u in os.listdir(USERS_DIR) if os.path.isdir(os.path.join(USERS_DIR, u))]
            
            success_count = 0 
            bot.send_message(message.chat.id, f"🌋 <b>Рассылка инициирована.</b> Целевая аудитория: {len(users)} пользователей.", parse_mode="HTML")
            for uid in users:
                try: 
                    bot.send_message(uid, f"🚨 <b>ГЛОБАЛЬНОЕ УВЕДОМЛЕНИЕ:</b>\n\n{escape_html(user_input)}", parse_mode="HTML")
                    success_count += 1 
                    time.sleep(0.06) 
                except: pass 
            bot.send_message(message.chat.id, f"✅ <b>Рассылка успешно завершена!</b>\nДоставлено сообщений: {success_count}.", parse_mode="HTML", reply_markup=markup_close)
            
     elif state == "STATE_ADD_ADMIN":
         if message.chat.id not in get_admins(): return
         try:
             target_id = int(user_input)
             if add_admin(target_id): bot.send_message(message.chat.id, f"✅ Пользователь <code>{target_id}</code> назначен администратором.", parse_mode="HTML", reply_markup=markup_close)
             else: bot.send_message(message.chat.id, "Пользователь уже является администратором.", reply_markup=markup_close)
         except: bot.send_message(message.chat.id, "❌ Неверный формат ID.", reply_markup=markup_close)
         
     elif state == "STATE_REMOVE_ADMIN":
         if message.chat.id not in get_admins(): return
         try:
             target_id = int(user_input)
             if target_id == message.chat.id: bot.send_message(message.chat.id, "❌ Вы не можете удалить самого себя.", reply_markup=markup_close)
             elif remove_admin(target_id): bot.send_message(message.chat.id, f"✅ Пользователь <code>{target_id}</code> лишен прав администратора.", parse_mode="HTML", reply_markup=markup_close)
             else: bot.send_message(message.chat.id, "Пользователь не найден в списке администраторов.", reply_markup=markup_close)
         except: bot.send_message(message.chat.id, "❌ Неверный формат ID.", reply_markup=markup_close)

     elif state == "STATE_DECODE_LINK":
          host, port, secret = parse_mtproto_url(user_input)
          if host and is_valid_secret(secret):
                protection_type = "Ключ устойчив к проверкам DPI (Fake-TLS)" if "ee" in secret[:2] or "dd" in secret[:2] else "Базовое шифрование (Уязвимо)"
                bot.send_message(message.chat.id, f"🔍 <b>АНАЛИЗ ССЫЛКИ УСПЕШЕН:</b>\n\n IP сервера: <code>{escape_html(host)}</code>\n Порт: <code>{port}</code>\n Секретный ключ: <code>{escape_html(secret)}</code>\n\n Защита: <b>{protection_type}</b>", reply_markup=markup_close, parse_mode="HTML")
          else:
               bot.send_message(message.chat.id, "❌ Некорректный формат ссылки MTProto.", reply_markup=markup_close)

     elif state == "STATE_GEO_IP":
           geo_result = "Информация не найдена."
           try:
              data = requests.get(f"http://ip-api.com/json/{user_input}?lang=ru", timeout=3.5).json()
              if data.get('status') == 'success': 
                 country = data.get('country', 'Неизвестно')
                 city = data.get('city', 'Неизвестно')
                 isp = data.get('isp', 'Неизвестно')
                 geo_result = f"🌐 <b>ИНФОРМАЦИЯ О СЕТЕВОМ УЗЛЕ:</b>\n\n Страна: <code>{escape_html(country)}</code>\n Город: <code>{escape_html(city)}</code>\n Провайдер: <code>{escape_html(isp)}</code>" 
           except: pass
           bot.send_message(message.chat.id, geo_result, parse_mode="HTML", reply_markup=markup_close)

     elif state == "STATE_GENERATE_QR":
          safe_url = requests.utils.quote(user_input)
          api_url = f"https://api.qrserver.com/v1/create-qr-code/?size=380x380&data={safe_url}"
          bot.send_photo(message.chat.id, api_url, caption="⬛ Ваш QR-код успешно сгенерирован!", reply_markup=markup_close)

     elif state == "STATE_DNS_LOOKUP":
          try:
              response = requests.get(f"https://1.1.1.1/dns-query?name={user_input}&type=A", headers={'accept': 'application/dns-json'}, timeout=4)
              answers = response.json().get('Answer', [])
              ips = [ans['data'] for ans in answers if ans['type'] == 1]
              if ips: 
                  text_result = f"🔍 <b>Результаты DNS-запроса для {escape_html(user_input)}:</b>\n\n" + "\n".join([f"├ IP: <code>{escape_html(ip)}</code>" for ip in ips])
              else: 
                  text_result = f"❌ Не удалось разрешить домен <code>{escape_html(user_input)}</code>."
          except:
              text_result = "❌ Ошибка сетевого запроса к DNS-серверу."
          bot.send_message(message.chat.id, text_result, parse_mode="HTML", reply_markup=markup_close)


# =========== 3 ИЗБРАННЫЕ СОХРАНЕНИЯ ========== 
@bot.callback_query_handler(func=lambda call: call.data == "action_save_fav")
def save_favorite_proxy(call):
    extracted_link = None 
    for line in call.message.text.split("\n"):
        if "tg://" in line.strip(): extracted_link = line.strip() 

    if extracted_link: 
       update_user_setting(call.from_user.id, "favorite_proxies", extracted_link, is_list_append=True)
       try: bot.answer_callback_query(call.id, "✅ Прокси успешно добавлен в ваше Избранное!", show_alert=True)
       except: pass

@bot.callback_query_handler(func=lambda call: call.data == "menu_favorites")
def show_favorites(call):
   favs = get_user_setting(call.from_user.id, "favorite_proxies", [])
   markup = types.InlineKeyboardMarkup()
   if not favs: 
       text = "⭐ <b>ВАШИ ИЗБРАННЫЕ ПРОКСИ</b>\n\nВаш список пока пуст. Вы можете добавлять сюда сервера с помощью кнопки «В Избранное» при выдаче."
   else: 
       last_10 = favs[-10:]
       formatted_links = "\n\n".join([escape_html(link) for link in last_10])
       text = f"⭐️ <b>ВАШИ СОХРАНЕННЫЕ ПРОКСИ (Последние 10 шт):</b>\n\n{formatted_links}"
       markup.add(types.InlineKeyboardButton("🗑 Очистить Избранное", callback_data="action_clear_favs"))
       
   markup.add(types.InlineKeyboardButton("🔙 Назад в меню", callback_data="action_back"))
   bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "action_clear_favs")
def clear_favorites(call):
     update_user_setting(call.from_user.id, "favorite_proxies", [])
     try: bot.answer_callback_query(call.id, "Список успешно очищен.", show_alert=True)
     except: pass
     show_favorites(call)


# =========== 4 АНАЛИТИКА / ВЫГРУЗКА БАЗ ТЕКСТОМ  ==============
@bot.callback_query_handler(func=lambda call: call.data == "menu_download_db")
def download_database_txt(call):
      try: bot.answer_callback_query(call.id, "Генерирую текстовый файл с базой...", show_alert=False)
      except: pass
      
      cached_data = scrape_global_database()[:2500] 
      file_content = (f"🔥 ПОЛНАЯ БАЗА MTPROTO СЕРВЕРОВ — LEDERG PROXY 🔥\n"
                   f"Дата генерации дампа: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                   f"Всего выгружено активных серверов: {len(cached_data)}\n\n")
      
      for proxy in cached_data[:500]: 
           file_content += proxy + "\n\n"
      
      filename = f"LEDERG_PROXY_DB_{random.randint(11111,99999)}.txt"
      try:
         with open(filename, "w", encoding="utf-8") as f: f.write(file_content)
         markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🛑 Скрыть файл", callback_data="action_close"))
         bot.send_document(call.message.chat.id, open(filename, "rb"), caption="📂 Ваш запрошенный список сырой базы прокси (до 500 шт) в формате TXT.", reply_markup=markup)
         os.remove(filename)
      except: pass

@bot.callback_query_handler(func=lambda call: call.data == "menu_statistics")
def show_global_statistics(call):
       users_count = len(os.listdir(USERS_DIR)) if os.path.exists(USERS_DIR) else 0 
       db_count = 0 
       last_update = "-"
       
       if os.path.exists(CACHE_FILE):
          try:
            cached_data = load_json(CACHE_FILE)
            db_count = len(cached_data.get("lederg_base",[]))
            last_update = get_ago(cached_data.get("scraped_time_at", time.time()))
          except: pass
       
       markup = types.InlineKeyboardMarkup(row_width=1)
       markup.add(types.InlineKeyboardButton("♻️ Обновить кэш и перепроверить источники", callback_data="action_force_refresh"))
       markup.add(types.InlineKeyboardButton("🔙 Назад в меню", callback_data="action_back"))

       text = (f"📊 <b>СТАТИСТИКА УМНОЙ СИСТЕМЫ LEDERG</b>:\n\n"
             f"📡 Мониторинг: <code>{len(PROXY_SOURCES)}</code> Репозиториев\n"
             f"📦 Собрано серверов в кэше: <code>{db_count} шт.</code> \n"
             f"🔋 Последнее обновление: <code>{last_update}</code> \n\n"
             f"👥 Пользователей в системе: <code>{users_count} человек</code> \n\n"
             f"🛡️ Мощная Double-Проверка ТСПУ: <b>АКТИВНА 🟢</b>")
       bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "tool_tg_ping")
def ping_telegram_datacenters(call):
    bot.edit_message_text("🔄 Инициирую прямое подключение к магистральным датацентрам Telegram... Пожалуйста, подождите ⏳", call.message.chat.id, call.message.message_id)
    datacenters = [
        ("DC1 (Miami, US)", "149.154.175.50"), ("DC2 (Amsterdam, NL)", "149.154.167.51"),
        ("DC3 (Miami, US)", "149.154.175.100"),("DC4 (Amsterdam, NL)", "149.154.167.91"), ("DC5 (Singapore, SG)", "149.154.171.5")
    ]
    result = f"📊 <b>ПИНГ ДО ОФИЦИАЛЬНЫХ СЕРВЕРОВ TELEGRAM:</b>\n\n"
    for name, ip in datacenters:
        success, ms = strict_tcp_ping(ip, 443, 2.5)
        if success: result += f"├ <i>{name}</i>: <code>{ms} ms</code> 🟢\n"
        else: result += f"├ <i>{name}</i>: <code>Таймаут (Недоступен)</code> 🔴\n"
    
    markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 К инструментам", callback_data="menu_tools"))
    bot.edit_message_text(result, call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "action_force_refresh")
def force_cache_refresh(call):
     try: bot.answer_callback_query(call.id, "Запущено принудительное сканирование сети... ⏳")
     except: pass
     scrape_global_database()
     show_global_statistics(call)

# =========== 5 ЛИЧНЫЕ НАСТРОЙКИ (КОМФОРТ И РАССЫЛКА)  ===============
@bot.callback_query_handler(func=lambda call: call.data == "menu_settings")
def show_user_settings(call):
     is_mailing_active = get_user_setting(call.message.chat.id, "auto_mailing_enabled", True) 
     markup = types.InlineKeyboardMarkup(row_width=1)
     btn_text = "🔕 Отключить ежечасную рассылку" if is_mailing_active else "🔔 Включить ежечасную рассылку"
     markup.add(types.InlineKeyboardButton(btn_text, callback_data="toggle_mailing_status"))
     markup.add(types.InlineKeyboardButton("🔙 Назад в меню", callback_data="action_back"))
     
     status_text = "🔥 ВКЛЮЧЕНА (Бот каждый час присылает лучшие топ-прокси)" if is_mailing_active else "❌ ВЫКЛЮЧЕНА (Рассылки отключены)"
     text = (f"⚙️ <b>НАСТРОЙКИ РАССЫЛКИ LEDERG</b>\n\n"
             f"Рассылка прокси каждый час поможет тебе всегда оставаться онлайн без ручного поиска серверов. Бот будет заботиться о твоей связи автоматически.\n\n"
             f"Текущий статус: <b>{status_text}</b>")
     bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data=="toggle_mailing_status")
def toggle_mailing_settings(call):
    current_status = get_user_setting(call.message.chat.id, "auto_mailing_enabled", True) 
    update_user_setting(call.message.chat.id, "auto_mailing_enabled", not current_status) 
    try: bot.answer_callback_query(call.id, "Настройки успешно сохранены!")
    except: pass
    show_user_settings(call)


# ==================== 🔥 ЕЖЕЧАСОВЫЙ ФОНОВЫЙ РАССЫЛЬЩИК ====================
def background_hourly_broadcaster():
    """Рассылает 3 лучших прокси всем подписанным пользователям каждый час."""
    while True:
        time.sleep(3600) # Ожидание ровно 1 час
        print(f"[{time.strftime('%H:%M:%S')}] Запуск автоматической ежечасной рассылки...")
        fresh_database = scrape_global_database() 
        top_proxies = Fetch_Epic_Best_MTProtoss(fresh_database, rq_target=3) 

        if not top_proxies: continue
        
        users_list = []
        try: users_list = [int(u) for u in os.listdir(USERS_DIR) if os.path.isdir(os.path.join(USERS_DIR, u))]
        except: pass
        
        msg_text = (f"🕛 <b>АВТОМАТИЧЕСКАЯ ПОДДЕРЖКА СВЯЗИ LEDERG</b> \n\n"
                   f"Мы заботимся о том, чтобы вы всегда оставались в сети. Наш алгоритм только что проанализировал сотни серверов и отобрал для вас лучшие соединения.\n\n"
                   f"Ваши скоростные узлы связи на ближайший час ⬇️:")
                   
        for user_id in users_list: 
             is_subscribed = get_user_setting(user_id, "auto_mailing_enabled", True) 
             if is_subscribed:
                   try: 
                       bot.send_message(user_id, msg_text, parse_mode="HTML")
                       for latency, link in top_proxies: 
                            markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("⚡ ПОДКЛЮЧИТЬСЯ", url=link.replace('tg://', 'https://t.me/')))
                            bot.send_message(user_id, f"💠 <b>Задержка:</b> <code>{escape_html(latency)} ms</code>\n<code>{escape_html(link)}</code>", reply_markup=markup, parse_mode="HTML")
                            time.sleep(0.08) 
                   except: pass 


# ==================== ЗАПУСК ПРИЛОЖЕНИЯ ====================
if __name__ == "__main__":
    if not os.path.exists(USERS_DIR): os.makedirs(USERS_DIR, exist_ok=True)
    
    # 1. Запускаем первоначальный парсинг баз
    print(f"[{time.strftime('%H:%M:%S')}] Инициализация баз данных...")
    threading.Thread(target=scrape_global_database, daemon=True).start()
    
    # 2. Запускаем фоновую ежечасную рассылку
    threading.Thread(target=background_hourly_broadcaster, daemon=True).start()
    
    print(f"[{time.strftime('%H:%M:%S')}] Система успешно запущена и готова принимать команды.")
    while True:
        try: bot.infinity_polling(timeout=50, long_polling_timeout=45, skip_pending=True)
        except: time.sleep(2)

import threading
from flask import Flask
from telebot import TeleBot  # или как ты импортируешь бота

# Создаём Flask-приложение
app = Flask(__name__)

@app.route('/')
def health():
    return "OK", 200

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# Запускаем Flask в отдельном потоке (до бота)
threading.Thread(target=run_flask, daemon=True).start()

# А ТЕПЕРЬ ТВОЙ ОСНОВНОЙ КОД БОТА (polling)
if __name__ == '__main__':
    # Твой код запуска бота:
    # bot.infinity_polling() или bot.polling()
    bot.infinity_polling()
