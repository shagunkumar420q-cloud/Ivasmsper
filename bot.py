# ╔══════════════════════════════════════════════════════════════╗
# ║     KITE OTP Bot — Full System Bot                        ║
# ║     Numbers + OTP Forwarding + Full Admin Suite             ║
# ║     Developed by Junaid (@payment_owner)                    ║
# ╚══════════════════════════════════════════════════════════════╝

import asyncio
import requests
import re
import ssl
import json
import os
import sys
import time
import logging
import sqlite3
import websockets
import phonenumbers
from phonenumbers import geocoder
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, KeyboardButton, CopyTextButton
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)

# ═══════════════════════════════════════════════════════════════
#  CONFIGURATION
# ═══════════════════════════════════════════════════════════════
BOT_TOKEN      = "8933245461:AAG8EHAntnbnTskEGhmI0eID4RGJX5feYPs"
OWNER_IDS      = [8129003140]
ADMIN_IDS      = [8129003140]
OTP_GROUP_LINK = "https://t.me/kiteotp"
BOT_NAME       = "IVASMS OTP"

REQUIRED_CHANNELS = []  # Force-join removed

DEV_CONTACT    = "@payment_owner"

DEFAULT_PANELS = {
    "KUMAIL HADI": {
        "url":     "http://147.135.212.197/crapi/had/viewstats",
        "token":   "SVVSRzRSQmhXkYuBilFYZw",
        "records": 20
    }
}

OTP_GROUP_IDS = [-1003652361706]

OTP_FILE      = "otp_store.json"
PANEL_FILE    = "panels.json"
IVAS_FILE     = "ivas.json"
USER_FILE     = "users.json"
GROUP_FILE    = "groups.json"
CONFIG_FILE   = "bot_config.json"
ADMINS_FILE   = "admins.json"
LOG_FILE      = "bot.log"
DB_FILE       = "bot_data.db"

# ═══════════════════════════════════════════════════════════════
#  CUSTOM EMOJI DICTIONARIES (Telegram Premium Custom Emojis)
#  All old emojis removed - replaced with custom emoji IDs
# ═══════════════════════════════════════════════════════════════
COUNTRY_EMOJI_ID = {
    "UA": "5222250679371839695", "UA_2": "5280587278828193324",
    "US": "5224321781321442532", "PL": "5224670399521892983",
    "KZ": "5222276376161171525", "AZ": "5224426544163728284",
    "EU": "5222108911091331711", "UN": "5451772687993031127",
    "AM": "5224369957969603463", "RU": "5280582975270963511",
    "CN": "5224435456220868088", "UZ": "5222404546575219535",
    "DE": "5222165617544542414", "JP": "5222390089715299207",
    "TR": "5224601903383457698", "BY": "5280820319458707404",
    "BY_2": "5222398507851199882", "GB": "5224518800061245598",
    "IN": "5222300011366200403", "BR": "5224688610183228070",
    "ZM": "5224646626877911277", "YE": "5222300655611294950",
    "VI": "5224395882392201810", "VN": "5222359651282071925",
    "VA": "5222420266155520507", "VU": "5222126748090512778",
    "UY": "5222466849370813232", "AE": "5224565851427976312",
    "US_2": "5222253007244113340", "UG": "5222464040462200940",
    "TM": "5224256935905208951", "TN": "5221991375016310330",
    "TT": "5224391883777651050", "TG": "5222408051268532030",
    "TH": "5224638530864556281", "TZ": "5224397364155923150",
    "TJ": "5222217865821696536", "CH": "5224707263226194753",
    "SE": "5222201098269373561", "SZ": "5224269666188274723",
    "SR": "5224567367551428669", "SD": "5224372990216514135",
    "ES": "5222024776976970940", "LK": "5224277294050192388",
    "SS": "5224618146949773268", "KR": "5222345550904439270",
    "ZA": "5224696216570309138", "SO": "5222370504664428325",
    "SI": "5224660718665607511", "SK": "5222401879400528047",
    "SG": "5224194023224257181", "SL": "5224420995065983217",
    "SC": "5224467496676896871", "RS": "5222145396838512729",
    "SN": "5224358988623130949", "SA": "5224698145010624573",
    "ST": "5221953304426198315", "WS": "5224660353593387686",
    "VC": "5224541228380467535", "LC": "5222000927023577045",
    "PS": "5222041677673282461", "PS_2": "5222370620628546719",
    "RW": "5222449197055227754", "RO": "5222273794885826118",
    "QA": "5222225596762830469", "PR": "5224220115150582423",
    "PT": "5224404094369672274", "PH": "5222065042295376892",
    "PE": "5224482026551258766", "PY": "5222152565138929235",
    "PG": "5224500164198149905", "PA": "5222111719999945107",
    "PK": "5224637061985742245", "OM": "5222396686785066306",
    "NO": "5224465228934163949", "NG": "5224723614166691638",
    "NE": "5222099049846420864", "NZ": "5224573595254009705",
    "NL": "5224516489368841614", "NP": "5222444378101925267",
    "NA": "5224690826386351746", "MZ": "5222470388423864826",
    "MA": "5224530035695693965", "ME": "5224463399278096980",
    "MN": "5224192257992701543", "MC": "5221937224068640464",
    "MD": "5224216473018314447", "FM": "5222280486444873367",
    "MX": "5221971386238514431", "MU": "5224238347286752315",
    "MH": "5224538449536624503", "MY": "5224312886444174057",
    "KE": "5222089648163009103", "KE_2": "5222279743415531561",
    "MG": "5222042605386217334", "MK": "5222470435668505656",
    "LU": "5224499567197700690", "LT": "5224245902134226386",
    "LY": "5222194286451242896", "LR": "5221998371518034740",
    "LS": "5224245850594619415", "LB": "5222244425899455269",
    "LV": "5224401229626484931", "LA": "5224200843632324642",
    "KG": "5224388147156102493", "KW": "5221949726718442491",
    "XK": "5222197129719592160", "KI": "5224652244695134610",
    "JO": "5222292177345853436", "JM": "5222007034467074185",
    "IE": "5224257017509588818", "IE_2": "5222233374948602940",
    "IT": "5222460101977190141", "IL": "5224720599099648709",
    "IQ": "5221980268230882832", "IR": "5224374154152653367",
    "ID": "5224405893960969756", "IS": "5222063229819172521",
    "HU": "5224691998912427164", "HN": "5222229234600130045",
    "HN_2": "5222434624231191289", "HT": "5224683146984831315",
    "GY": "5224570532942329532", "GW": "5224705704153066489",
    "GN": "5222337588035073000", "GT": "5222128302868672826",
    "GD": "5222234560359577687", "GR": "5222463490706389920",
    "GH": "5224511339703056124", "GE": "5222152195771742239",
    "GM": "5221949872747330159", "GA": "5224669733801963467",
    "FR": "5222029789203804982", "FI": "5224282903277482188",
    "FJ": "5221962676044838178", "ET": "5224467805914542024",
    "EE": "5222195463272281351", "GQ": "5222172811614762423",
    "SV": "5224337131534559907", "EG": "5222161185138292290",
    "EC": "5224191188545840926", "TL": "5224515905253291409",
    "DO": "5224286412265763450", "DM": "5222337489250824921",
    "DJ": "5224203012590810589", "DK": "5222297215342490217",
    "CY": "5222431454545327055", "HR": "5221967765581085099",
    "CR": "5222453801260168022", "CG": "5222104268231684600",
    "CD": "5224398158724871677", "KM": "5222398735484466247",
    "CO": "5224455152940886669", "CL": "5222350726340032308",
    "CZ": "5222073533445714675", "TD": "5222060468155204001",
    "CF": "5222073662294733523", "CV": "5222347737042792258",
    "CA": "5222001124592071204", "CM": "5222270788408717651",
    "KH": "5224189882875785448", "BI": "5224490444687158452",
    "BF": "5222356541725749790", "BG": "5222092074819530668",
    "BN": "5224435958732042406", "BW": "5224288456670196085",
    "BA": "5224496092569155254", "BO": "5224675484763170798",
    "BT": "5224541065171710147", "BJ": "5222024115552009151",
    "BZ": "5224316292353241916", "BE": "5224513182244024630",
    "BB": "5222156533688712094", "BD": "5224407289825340729",
    "BH": "5224492892818518587", "BS": "5224504167107668172",
    "AT": "5224520754271366661", "AU": "5224659803837574114",
    "AR": "5221980461504411710", "AG": "5224544866217765554",
    "AO": "5224379767674907895", "AD": "5221987861733061751",
    "DZ": "5224260376174015500", "AL": "5224312057515486246",
    "AF": "5222096009009575868", "ZW": "5222060442385397848",
    "VE": "5294476442854247878", "FO": "5280985770188885026",
    "MQ": "5281027792148909351",
    # Additional countries - all flags covered
    "TW": "5222345550904439270", "KP": "5222370504664428325",
    "MM": "5224638530864556281", "SY": "5222024776976970940",
    "CU": "5222453801260168022", "NI": "5222229234600130045",
    "MR": "5222099049846420864", "ML": "5222408051268532030",
    "MW": "5224467805914542024", "MV": "5224194023224257181",
    "LI": "5224499567197700690", "HK": "5224312886444174057",
    "MO": "5221971386238514431", "SB": "5224660353593387686",
    "TO": "5224541228380467535", "NR": "5222000927023577045",
    "PW": "5224220115150582423", "TV": "5224395882392201810",
    "GI": "5224516489368841614",
    "AW": "5224690826386351746", "CW": "5224500164198149905",
    "SX": "5224391883777651050", "BQ": "5224683146984831315",
    "CK": "5224570532942329532", "NU": "5222449197055227754",
    "TK": "5224256935905208951", "AS": "5222253007244113340",
    "GU": "5224397364155923150", "MP": "5224358988623130949",
    "IM": "5224245902134226386", "JE": "5224401229626484931",
    "GG": "5224200843632324642", "AX": "5224282903277482188",
    "SJ": "5224465228934163949", "NC": "5224573595254009705",
    "PF": "5224404094369672274", "GP": "5224686610183228070",
    "RE": "5224337131534559907", "YT": "5221949726718442491",
    "PM": "5222197129719592160", "GF": "5221962676044838178",
    "TF": "5222060468155204001", "IO": "5224318292353241916",
    "SH": "5224541065171710147", "FK": "5224316292353241916",
    "AI": "5224544866217765554", "MS": "5224379767674907895",
    "TC": "5221987861733061751", "VG": "5224260376174015500",
    "KY": "5224312057515486246", "BM": "5224288456670196085",
    "GL": "5222280486444873367", "MF": "5224463399278096980",
    "BL": "5221937224068640464", "CX": "5224238347286752315",
    "CC": "5224538449536624503", "NF": "5224696216570309138",
    "HM": "5222042605386217334", "BV": "5222470435668505656",
    "AQ": "5222201098269373561", "GS": "5222024115552009151",
    "PN": "5222356541725749790",
    "EH": "5222041677673282461",
    "DEFAULT": "5222250679371839695",
}

APP_EMOJI_ID = {
    "tiktok":    "5327982530702359565",  "whatsapp":  "5334998226636390258",
    "instagram": "5319160079465857105",  "facebook":  "5323261730283863478",
    "telegram":  "5330237710655306682",  "twitter":   "5330337435500951363",
    "snapchat":  "5330248916224983855",  "google":    "5359758030198031389",
    "gmail":     "5359758030198031389",  "youtube":   "5373026167722876724",
    "discord":   "5373026167722876724",  "netflix":   "5373026167722876724",
    "amazon":    "5373026167722876724",  "paypal":    "5364111181415996352",
    "spotify":   "5373026167722876724",  "binance":   "5359437015752401733",
    "bybit":     "5359437015752401733",  "hsbc":      "6249045530119249807",
    "gochat":    "5332524123610430820",  "imo":       "5920204030570667999",
    "apple":     "5334955749409834455",
    "DEFAULT":   "5332524123610430820",
}

SERVICE_HASHTAGS = {
    "whatsapp": "WS", "telegram": "TG", "instagram": "IG", "facebook": "FB",
    "google": "GG", "gmail": "GG", "twitter": "TW", "tiktok": "TT",
    "snapchat": "SC", "netflix": "NF", "amazon": "AM", "paypal": "PP",
    "binance": "BN", "bybit": "BB", "discord": "DC", "microsoft": "MS",
    "yahoo": "YH", "apple": "AP", "spotify": "SP", "vk": "VK", "line": "LN",
    "wechat": "WC", "viber": "VB", "imo": "IM", "kakaotalk": "KT",
    "truecaller": "TC", "linkedin": "LI", "shopee": "SH", "lazada": "LZ",
    "gojek": "GJ", "grab": "GR", "foodpanda": "FP", "deliveroo": "DR",
    "uber": "UB", "bolt": "BL", "indriver": "IDR", "careem": "CR",
    "tinder": "TN", "bumble": "BM", "okcupid": "OK", "hinge": "HG",
}

# File handler - DEBUG and above
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

# Console handler - ERROR only (no spam)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[file_handler, console_handler]
)
logger = logging.getLogger(__name__)

# Suppress noisy HTTP 200 OK logs
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("telegram.ext.Application").setLevel(logging.WARNING)
logging.getLogger("telegram.ext.Updater").setLevel(logging.WARNING)

STATS = {"start_time": time.time(), "otps_sent": 0, "otps_dropped": 0,
         "errors": 0, "panel_hits": {}, "ivas_hits": {}}

# ── OTP Send Queue ─────────────────────────────────────────────
OTP_QUEUE: asyncio.Queue = asyncio.Queue()

PANEL_ADD_STATES = {}
IVAS_ADD_STATES  = {}
BROADCAST_STATES = {}
SETTING_STATES   = {}
NB_STATE         = {}
FETCH_STATES     = {}
STATE_TIMEOUT    = 300

IVAS_TASKS: Dict[str, asyncio.Task] = {}
REST_TASKS: Dict[str, asyncio.Task] = {}

OTP_LOG: List[dict] = []
OTP_LOG_MAX = 200

# ═══════════════════════════════════════════════════════════════
#  SQLITE DATABASE
# ═══════════════════════════════════════════════════════════════
def init_db():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS numbers
                 (id INTEGER PRIMARY KEY, country TEXT, phone TEXT,
                  added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
    c.execute("""CREATE TABLE IF NOT EXISTS tg_users
                 (user_id INTEGER PRIMARY KEY, first_seen TEXT,
                  last_seen TEXT, total_commands INTEGER DEFAULT 0)""")
    c.execute("""CREATE TABLE IF NOT EXISTS otp_history
                 (id INTEGER PRIMARY KEY, number TEXT, service TEXT,
                  otp TEXT, source TEXT,
                  received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
    c.execute("""CREATE TABLE IF NOT EXISTS assigned_numbers
                 (phone TEXT PRIMARY KEY, user_id INTEGER NOT NULL,
                  assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
    conn.commit()
    return conn

db = init_db()

def db_add_user(user_id: int):
    db_touch_user(user_id)

def db_touch_user(user_id: int):
    now = datetime.now().isoformat()
    c = db.cursor()
    c.execute(
        """
        INSERT INTO tg_users (user_id, first_seen, last_seen, total_commands)
        VALUES (?, ?, ?, 1)
        ON CONFLICT(user_id) DO UPDATE SET
            last_seen = excluded.last_seen,
            total_commands = tg_users.total_commands + 1
        """,
        (user_id, now, now),
    )
    db.commit()

def db_get_countries():
    c = db.cursor()
    c.execute("SELECT country,COUNT(*) FROM numbers GROUP BY country ORDER BY COUNT(*) DESC")
    return c.fetchall()

def db_get_country_numbers(country: str, limit: int = 9999):
    c = db.cursor()
    c.execute("SELECT phone FROM numbers WHERE country=? LIMIT ?", (country, limit))
    return [r[0] for r in c.fetchall()]

def db_pop_number(country: str):
    c = db.cursor()
    c.execute("SELECT id,phone FROM numbers WHERE country=? LIMIT 1", (country,))
    row = c.fetchone()
    if row:
        c.execute("DELETE FROM numbers WHERE id=?", (row[0],))
        db.commit()
        return row[1]
    return None

def db_pop_numbers(country: str, count: int = 3):
    c = db.cursor()
    c.execute("SELECT id,phone FROM numbers WHERE country=? LIMIT ?", (country, count))
    rows = c.fetchall()
    if rows:
        ids = [r[0] for r in rows]
        c.execute(f"DELETE FROM numbers WHERE id IN ({','.join('?'*len(ids))})", ids)
        db.commit()
        return [r[1] for r in rows]
    return []

def db_delete_country(country: str):
    c = db.cursor()
    c.execute("DELETE FROM numbers WHERE country=?", (country,))
    db.commit()

def db_add_numbers(country: str, nums: list):
    c = db.cursor()
    c.executemany("INSERT INTO numbers (country,phone) VALUES (?,?)",
                  [(country, n) for n in nums])
    db.commit()

def db_total_numbers():
    c = db.cursor()
    c.execute("SELECT COUNT(*) FROM numbers")
    return c.fetchone()[0]

def db_save_otp_history(number: str, service: str, otp: str, source: str):
    c = db.cursor()
    c.execute("INSERT INTO otp_history (number,service,otp,source) VALUES (?,?,?,?)",
              (number, service, otp or "N/A", source))
    db.commit()

def db_assign_numbers(user_id: int, phones: list):
    c = db.cursor()
    for phone in phones:
        clean = re.sub(r"[^0-9]", "", phone)
        c.execute("INSERT OR REPLACE INTO assigned_numbers (phone, user_id) VALUES (?,?)",
                  (clean, user_id))
    db.commit()

def db_get_owner_of_number(number: str) -> Optional[int]:
    clean = re.sub(r"[^0-9]", "", number)
    c = db.cursor()
    c.execute("SELECT user_id FROM assigned_numbers WHERE phone=?", (clean,))
    row = c.fetchone()
    if row:
        return row[0]
    if len(clean) >= 5:
        suffix = clean[-5:]
        c.execute("SELECT user_id FROM assigned_numbers WHERE phone LIKE ?", (f"%{suffix}",))
        row = c.fetchone()
        if row:
            return row[0]
    return None

def db_clear_old_assignments(days: int = 2):
    c = db.cursor()
    c.execute("DELETE FROM assigned_numbers WHERE assigned_at < datetime('now', ?)",
              (f"-{days} days",))
    db.commit()

def db_get_otp_history(limit: int = 20):
    c = db.cursor()
    c.execute("""SELECT number,service,otp,source,received_at FROM otp_history
                 ORDER BY id DESC LIMIT ?""", (limit,))
    return c.fetchall()

def db_search_otp_by_number(target: str):
    c = db.cursor()
    c.execute("""SELECT number,service,otp,source,received_at FROM otp_history
                 WHERE number LIKE ? ORDER BY id DESC LIMIT 10""", (f"%{target}%",))
    return c.fetchall()

def db_clear_otp_history():
    c = db.cursor()
    c.execute("DELETE FROM otp_history")
    db.commit()

def db_user_stats():
    c = db.cursor()
    today    = datetime.now().date().isoformat()
    week_ago = (datetime.now() - timedelta(days=7)).isoformat()
    c.execute("SELECT COUNT(*) FROM tg_users")
    total = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM tg_users WHERE last_seen LIKE ?", (f"{today}%",))
    active_today = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM tg_users WHERE last_seen >= ?", (week_ago,))
    active_week = c.fetchone()[0]
    return total, active_today, active_week

def get_broadcast_user_ids():
    user_ids = set()
    c = db.cursor()
    c.execute("SELECT user_id FROM tg_users")
    user_ids.update(int(row[0]) for row in c.fetchall())
    try:
        for user_id in GN_DATA.get("users", {}):
            try:
                user_ids.add(int(user_id))
            except (TypeError, ValueError):
                logger.warning("Invalid broadcast user ID: %r", user_id)
    except NameError:
        pass  # GN_DATA not loaded yet
    return sorted(user_ids)

# ═══════════════════════════════════════════════════════════════
#  JSON HELPERS
# ═══════════════════════════════════════════════════════════════
def load_json(file: str, default: Any = None) -> Any:
    if default is None:
        default = {}
    if not os.path.exists(file):
        return default
    try:
        with open(file, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading {file}: {e}")
        return default

def save_json(file: str, data: Any) -> None:
    try:
        with open(file, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        logger.error(f"Error saving {file}: {e}")

def load_panels():      return load_json(PANEL_FILE, DEFAULT_PANELS.copy())
def save_panels(d):     save_json(PANEL_FILE, d)
def load_ivas():        return load_json(IVAS_FILE, {})
def save_ivas(d):       save_json(IVAS_FILE, d)
def load_otp_store():   return load_json(OTP_FILE, {})
def save_otp_store(d):  save_json(OTP_FILE, d)
def load_users():       return load_json(USER_FILE, {})
def save_users(d):      save_json(USER_FILE, d)
def load_groups():      return load_json(GROUP_FILE, OTP_GROUP_IDS.copy())
def save_groups(d):     save_json(GROUP_FILE, d)

# ═══════════════════════════════════════════════════════════════
#  PERMISSION SYSTEM
# ═══════════════════════════════════════════════════════════════

ALL_PERMISSIONS = {
    "numbers":    "📦 Add/Delete Numbers",
    "panels":     "📡 Manage Panels",
    "ivas":       "🔌 Manage IVAS",
    "groups":     "👥 Manage Groups",
    "broadcast":  "📢 Broadcast",
    "otp_history":"📋 OTP History",
    "fetch_sms":  "🔄 Fetch SMS",
    "files":      "📂 File Manager",
    "settings":   "⚙️ Settings",
    "advanced":   "🔧 Advanced Tools",
    "stats":      "📊 Stats/Status",
}

def load_staff() -> dict:
    data = load_json(ADMINS_FILE, {"owners": list(OWNER_IDS), "staff": {}})
    return data.get("staff", {})

def save_staff(staff: dict):
    data = load_json(ADMINS_FILE, {"owners": list(OWNER_IDS), "staff": {}})
    data["staff"] = staff
    save_json(ADMINS_FILE, data)

def load_admins() -> list:
    staff = load_staff()
    return [int(k) for k in staff.keys()] + list(OWNER_IDS)

def get_staff_perms(uid: int) -> list:
    if is_owner(uid):
        return list(ALL_PERMISSIONS.keys())
    staff = load_staff()
    return staff.get(str(uid), {}).get("perms", [])

def has_perm(uid: int, perm: str) -> bool:
    if is_owner(uid):
        return True
    return perm in get_staff_perms(uid)

def add_staff(uid: int, name: str, perms: list):
    staff = load_staff()
    staff[str(uid)] = {"name": name, "perms": perms}
    save_staff(staff)

def remove_staff(uid: int):
    staff = load_staff()
    staff.pop(str(uid), None)
    save_staff(staff)

def update_staff_perms(uid: int, perms: list):
    staff = load_staff()
    if str(uid) in staff:
        staff[str(uid)]["perms"] = perms
        save_staff(staff)

def load_config():
    return load_json(CONFIG_FILE, {
        "channel_link":    "https://t.me/kitenumbers",
        "number_bot_link": "https://t.me/IVASMSotps_bot",
        "otp_forward":     True,
        "forward_delay":   0,
        "log_group":       None,
    })

def save_config(c): save_json(CONFIG_FILE, c)

def is_owner(uid: int) -> bool:
    return uid in OWNER_IDS

def is_admin(uid: int) -> bool:
    if is_owner(uid):
        return True
    staff = load_staff()
    return str(uid) in staff

def get_role_label(uid: int) -> str:
    if is_owner(uid):
        return "👑 Owner"
    staff = load_staff()
    entry = staff.get(str(uid))
    if entry:
        perms = entry.get("perms", [])
        return f"🛡️ Staff ({len(perms)} perms)"
    return "👤 User"

API_PANELS = load_panels()

# ═══════════════════════════════════════════════════════════════
#  OTP HELPERS WITH CUSTOM EMOJIS (NO OLD EMOJIS)
# ═══════════════════════════════════════════════════════════════

REGION_LANGUAGE = {
    "DE":"German","AT":"German","CH":"German","FR":"French","BE":"French",
    "ES":"Spanish","MX":"Spanish","AR":"Spanish","PT":"Portuguese","BR":"Portuguese",
    "RU":"Russian","UA":"Russian","BY":"Russian","TR":"Turkish",
    "SA":"Arabic","AE":"Arabic","EG":"Arabic","CN":"Chinese","TW":"Chinese",
    "JP":"Japanese","KR":"Korean","IN":"Hindi","PK":"Urdu","IT":"Italian",
    "NL":"Dutch","PL":"Polish","SE":"Swedish","NO":"Norwegian","DK":"Danish",
    "FI":"Finnish","GR":"Greek","IR":"Persian","TH":"Thai","VN":"Vietnamese",
    "ID":"Indonesian","NG":"English","PH":"Filipino",
}

def get_service_short(service: str) -> str:
    """Get service hashtag using SERVICE_HASHTAGS dictionary. Returns empty string if unknown."""
    s = service.lower().strip()
    for key, tag in SERVICE_HASHTAGS.items():
        if key in s:
            return tag
    return ""

def _flag_emoji(code: str) -> str:
    """Convert ISO 3166-1 alpha-2 country code to Unicode regional flag emoji."""
    try:
        c = code.upper()
        if len(c) == 2 and c.isalpha():
            return chr(0x1F1E6 + ord(c[0]) - ord('A')) + chr(0x1F1E6 + ord(c[1]) - ord('A'))
    except Exception:
        pass
    return "🌍"

APP_EMOJI_FALLBACK = {
    "whatsapp":  "💬",
    "telegram":  "✈️",
    "instagram": "📷",
    "facebook":  "👥",
    "google":    "📧",
    "gmail":     "📧",
    "twitter":   "🐦",
    "tiktok":    "🎵",
    "snapchat":  "👻",
    "binance":   "💰",
    "bybit":     "💰",
    "discord":   "🎮",
    "netflix":   "🎬",
    "amazon":    "📦",
    "paypal":    "💳",
    "spotify":   "🎧",
    "microsoft": "🖥️",
    "apple":     "🍎",
    "DEFAULT":   "📱",
}

def get_custom_country_emoji(region_code: str) -> str:
    """
    Get custom emoji HTML tag for country flag.
    Uses <tg-emoji> with the emoji-id — works with parse_mode=HTML on Bot API.
    """
    if not region_code:
        return f"<tg-emoji emoji-id=\"{COUNTRY_EMOJI_ID['DEFAULT']}\">🌍</tg-emoji>"
    if region_code in COUNTRY_EMOJI_ID:
        return f"<tg-emoji emoji-id=\"{COUNTRY_EMOJI_ID[region_code]}\">🌍</tg-emoji>"
    if f"{region_code}_2" in COUNTRY_EMOJI_ID:
        return f"<tg-emoji emoji-id=\"{COUNTRY_EMOJI_ID[f'{region_code}_2']}\">🌍</tg-emoji>"
    if region_code.upper() in COUNTRY_EMOJI_ID:
        return f"<tg-emoji emoji-id=\"{COUNTRY_EMOJI_ID[region_code.upper()]}\">🌍</tg-emoji>"
    return f"<tg-emoji emoji-id=\"{COUNTRY_EMOJI_ID['DEFAULT']}\">🌍</tg-emoji>"

def get_app_emoji(service: str) -> str:
    """
    Get custom emoji HTML tag for app/service icon.
    Uses <tg-emoji> with the emoji-id — works with parse_mode=HTML on Bot API.
    """
    s = service.lower().strip()
    for key, emoji_id in APP_EMOJI_ID.items():
        if key in s:
            return f"<tg-emoji emoji-id=\"{emoji_id}\">📱</tg-emoji>"
    return f"<tg-emoji emoji-id=\"{APP_EMOJI_ID['DEFAULT']}\">📱</tg-emoji>"

def extract_otp(message: str) -> Optional[str]:
    """
    Extract OTP from SMS text.
    """
    # Split OTP: 3–4 digits, dash or space, 3–4 digits
    m = re.search(r'(?<!\d)(\d{3,4})[\- ](\d{3,4})(?!\d)', message)
    if m:
        combined = m.group(1) + m.group(2)
        if 6 <= len(combined) <= 8:
            return combined

    # Straight 4–6 digit OTP
    for pat in [r'(?<!\d)\d{6}(?!\d)',
                r'(?<!\d)\d{5}(?!\d)',
                r'(?<!\d)\d{4}(?!\d)']:
        m = re.search(pat, message)
        if m:
            return m.group(0)

    return None

def get_country_info(number_str: str) -> tuple:
    """Returns country name and region code (no flag emoji - using custom emojis now)"""
    try:
        if not number_str.startswith("+"):
            number_str = "+" + number_str
        parsed  = phonenumbers.parse(number_str)
        country = geocoder.description_for_number(parsed, "en")
        region  = phonenumbers.region_code_for_number(parsed)
        return country or "Unknown", region or ""
    except:
        return "Unknown", ""

def get_region_code(number_str: str) -> str:
    try:
        n = number_str if number_str.startswith("+") else "+" + number_str
        return phonenumbers.region_code_for_number(phonenumbers.parse(n)) or ""
    except:
        return ""

def get_country_code_str(number_str: str) -> str:
    try:
        n = number_str if number_str.startswith("+") else "+" + number_str
        return f"+{phonenumbers.parse(n).country_code}"
    except:
        return ""

def get_last5(number_str: str) -> str:
    digits = re.sub(r"[^0-9]", "", number_str)
    return digits[-5:] if len(digits) >= 5 else digits

def detect_language_from_text(text: str) -> str:
    """Detect language from SMS message content."""
    if not text:
        return None
    if re.search(r'[\u3041-\u3096\u30A1-\u30FA]', text): return "Japanese"
    if re.search(r'[\uAC00-\uD7AF]', text):               return "Korean"
    if re.search(r'[\u4e00-\u9fff\u3400-\u4DBF]', text):  return "Chinese"
    if re.search(r'[\u0600-\u06FF]', text):                return "Arabic"
    if re.search(r'[\u0400-\u04FF]', text):                return "Russian"
    if re.search(r'[\u0900-\u097F]', text):                return "Hindi"
    if re.search(r'[\u0E00-\u0E7F]', text):                return "Thai"
    if re.search(r'[\u0370-\u03FF]', text):                return "Greek"
    if re.search(r'[\u06A9\u06AF\u06CC\u06BE]', text):    return "Persian"
    if re.search(r'[\u0590-\u05FF]', text):                return "Hebrew"
    return None

def mask_phone_for_dm(phone: str) -> str:
    """Exact same as main.go maskPhoneForDM — first 5 digits + *** + last 3 digits."""
    import re as _re
    cleaned = _re.sub(r'\D', '', phone)
    if len(cleaned) >= 8:
        return f"{cleaned[:5]}***{cleaned[-3:]}"
    return phone

def format_otp_code(code: str) -> str:
    """Splits OTP into two halves with dash. e.g. '313963' → '313-963'"""
    if not code or code == "------":
        return code
    n = len(code)
    if n < 4:
        return code
    mid = n // 2
    return code[:mid] + "-" + code[mid:]

def format_number_Kite_OTP(number: str) -> str:
    """Format full number as: 4915511-Junaid-03543"""
    digits = re.sub(r"[^0-9]", "", number)
    if len(digits) >= 12:
        return f"{digits[:7]}-Junaid-{digits[-5:]}"
    elif len(digits) >= 7:
        mid = len(digits) - 5
        return f"{digits[:mid]}-KITE-{digits[-5:]}"
    return digits

def format_otp_message(number: str, service: str, otp: str,
                        source_label: str = "", sms_text: str = "") -> str:
    """
    Format OTP message with <tg-emoji> HTML tags for Telegram Premium custom emojis.
    send_message must use parse_mode='HTML'.
    """
    region = get_region_code(number)
    svc    = get_service_short(service)

    country_custom_emoji = get_custom_country_emoji(region)
    app_custom_emoji     = get_app_emoji(service)

    Junaid_OTP_number = format_number_Junaid_OTP(number)
    lang = detect_language_from_text(sms_text) or REGION_LANGUAGE.get(region, "English")

    lang_emoji = '<tg-emoji emoji-id="5388632425314140043">🌐</tg-emoji>'
    # Bold Junaid number using Unicode bold chars
    bold_num = "".join(
        chr(ord(c) + 0x1D400 - ord('A')) if 'A' <= c <= 'Z' else
        chr(ord(c) + 0x1D41A - ord('a')) if 'a' <= c <= 'z' else
        chr(ord(c) + 0x1D7CE - ord('0')) if '0' <= c <= '9' else c
        for c in Junaid_OTP_number
    )
    base = (f"{country_custom_emoji} ┃ {app_custom_emoji}"
            f"  <b>#{region}</b>  {bold_num}  {lang_emoji}<b>#{lang}</b>")

    # If no OTP, append truncated raw SMS
    if not otp or otp == "N/A":
        if sms_text:
            snippet = sms_text[:120].replace("<", "&lt;").replace(">", "&gt;")
            base += f"\n💬 <code>{snippet}</code>"

    return base

def get_otp_keyboard(number: str, otp: str) -> dict:
    """Raw dict so icon_custom_emoji_id/style/copy_text survive make_request."""
    OTP_EMOJI   = "6319056439096644016"
    PHONE_EMOJI = "5282843764451195532"
    CHAT_EMOJI  = "6206497372176913599"
    if otp:
        clean = re.sub(r"[^0-9]", "", otp)
        otp_row = [{"text": f" {clean}", "icon_custom_emoji_id": OTP_EMOJI,
                    "copy_text": {"text": clean}, "style": "danger"}]
    else:
        otp_row = [{"text": "No OTP Detected", "callback_data": "no_otp"}]
    return {"inline_keyboard": [
        otp_row,
        [{"text": " 𝗡𝘂𝗺𝗯𝗲𝗿𝘀", "url": "https://t.me/junaidaliniz",
          "icon_custom_emoji_id": PHONE_EMOJI, "style": "danger"},
         {"text": " 𝗖𝗵𝗮𝘁",    "url": "https://t.me/+DrBDJM9-nvAyMjRk",
          "icon_custom_emoji_id": CHAT_EMOJI,  "style": "primary"}],
    ]}

# Shared persistent Bot instance
_shared_bot: Optional[Bot] = None

def get_shared_bot() -> Bot:
    global _shared_bot
    if _shared_bot is None:
        _shared_bot = Bot(token=BOT_TOKEN)
    return _shared_bot

# In-memory caches
_CONFIG_CACHE: dict = {}
_CONFIG_CACHE_TS: float = 0.0
_GROUPS_CACHE: list = []
_GROUPS_CACHE_TS: float = 0.0
_CACHE_TTL: float = 5.0

def get_cached_config() -> dict:
    global _CONFIG_CACHE, _CONFIG_CACHE_TS
    if time.time() - _CONFIG_CACHE_TS > _CACHE_TTL:
        _CONFIG_CACHE = load_config()
        _CONFIG_CACHE_TS = time.time()
    return _CONFIG_CACHE

def get_cached_groups() -> list:
    global _GROUPS_CACHE, _GROUPS_CACHE_TS
    if time.time() - _GROUPS_CACHE_TS > _CACHE_TTL:
        _GROUPS_CACHE = load_groups()
        _GROUPS_CACHE_TS = time.time()
    return _GROUPS_CACHE

async def send_to_all_groups(msg: str, reply_markup=None):
    """Enqueue OTP"""
    config = get_cached_config()
    if not config.get("otp_forward", True):
        STATS["otps_dropped"] += 1
        return
    await OTP_QUEUE.put((msg, reply_markup))

async def _otp_sender_task():
    """Dedicated queue-draining task"""
    bot = get_shared_bot()
    logger.info("📤 OTP sender task started.")
    while True:
        try:
            msg, reply_markup = await OTP_QUEUE.get()
            groups = get_cached_groups()
            if not groups:
                OTP_QUEUE.task_done()
                continue

            async def _send_one(gid):
                for attempt in range(3):
                    try:
                        import json as _json
                        _p = {"chat_id": str(gid), "text": msg, "parse_mode": "HTML",
                              "disable_web_page_preview": True}
                        if reply_markup is not None:
                            _p["reply_markup"] = _json.dumps(reply_markup) if isinstance(reply_markup, dict) else _json.dumps(reply_markup.to_dict())
                        import aiohttp as _aiohttp
                        _url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                        async with _aiohttp.ClientSession() as _sess:
                            async with _sess.post(_url, json=_p) as _resp:
                                _result = await _resp.json()
                                if not _result.get("ok"):
                                    raise Exception(_result.get("description", "Unknown error"))
                        STATS["otps_sent"] += 1
                        logger.info(f"✅ OTP sent to group {gid}")
                        return
                    except Exception as e:
                        err = str(e)
                        if "RetryAfter" in err or "Too Many Requests" in err:
                            m = re.search(r"retry after (\d+)", err, re.I)
                            wait = int(m.group(1)) if m else 5
                            logger.warning(f"Flood wait {wait}s for group {gid}")
                            await asyncio.sleep(wait)
                        else:
                            STATS["errors"] += 1
                            logger.error(f"Send failed {gid} attempt {attempt+1}: {e}")
                            if attempt < 2:
                                await asyncio.sleep(1)
                            else:
                                break

            await asyncio.gather(*[_send_one(gid) for gid in groups])
            OTP_QUEUE.task_done()
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.error(f"_otp_sender_task error: {e}")

async def send_otp_to_owner(number: str, service: str, otp: str,
                             sms_text: str = "", source_label: str = ""):
    """
    Send OTP privately to holder — mirrors Go mainBotDMMessage.
    Uses find_holder_for_phone() (GN_HOLDS scan) then make_request raw JSON
    so <tg-emoji> and styled button fields work in private DMs.
    """
    logger.info(f"[DM] ▶ called: number=...{number[-5:]} service={service!r} otp={otp!r} source={source_label!r}")

    # ── Find holder via GN_HOLDS scan (mirrors Go findHolderForPhone) ──
    owner_id, hold = find_holder_for_phone(number)
    if not owner_id:
        logger.warning(f"[DM] ⚠️ no holder for ...{number[-5:]} — DM skipped. GN_HOLDS size={len(GN_HOLDS)}")
        return
    hold = hold or {}
    logger.info(f"[DM] holder found: owner_id={owner_id} numbers={hold.get('numbers')} msg_id={hold.get('message_id')}")

    # ── OTP limit check — mirrors Go holdsMu block ───────────
    otp_limit       = hold.get("otp_limit", 0)
    num_key         = re.sub(r'\D', '', number)
    hold_otp_counts = hold.get("number_otp_count", {})
    current_count   = hold_otp_counts.get(num_key, 0) + 1
    logger.info(f"[DM] otp_limit={otp_limit} current_count={current_count}")
    if otp_limit > 0 and current_count > otp_limit:
        logger.warning(f"[DM] ⚠️ limit {otp_limit} reached for ...{number[-5:]} — skip DM")
        return
    # Update count in hold
    hold_otp_counts[num_key] = current_count
    hold["number_otp_count"] = hold_otp_counts
    if otp_limit > 0 and current_count >= otp_limit:
        hold.setdefault("used", {})[num_key] = True
    GN_HOLDS[str(owner_id)] = hold
    gn_save_holds()

    # ── Price and balance ─────────────────────────────────────
    rate  = GN_DATA.get("usd_to_pkr", GN_USD_RATE) or GN_USD_RATE
    price = 0.0

    # STEP 1: Always prefer the hold's own service/country keys — these are the
    # exact keys stored in GN_DATA["services"] when the number was assigned.
    # The incoming `service` arg is the raw SMS originator (e.g. "Apple ID")
    # and almost never matches the admin panel key (e.g. "apple").
    hold_svc_key = hold.get("service", "")
    hold_cnt_key = hold.get("country", "")

    # STEP 2: Look up price using hold's keys (exact match first)
    svc = GN_DATA["services"].get(hold_svc_key, {})
    cnt = hold_cnt_key

    if svc and cnt:
        price = svc.get("countries", {}).get(cnt, {}).get("price", 0.0)

    # STEP 3: If still 0, try case-insensitive match on service key
    if price == 0.0 and hold_svc_key:
        _hold_svc_lower = hold_svc_key.lower().strip()
        for _k, _v in GN_DATA["services"].items():
            if _k.lower().strip() == _hold_svc_lower:
                svc = _v
                if cnt:
                    price = svc.get("countries", {}).get(cnt, {}).get("price", 0.0)
                if price == 0.0 and cnt:
                    # case-insensitive country key match
                    for _ck, _cv in svc.get("countries", {}).items():
                        if _ck.lower().strip() == cnt.lower().strip():
                            price = _cv.get("price", 0.0)
                            break
                if price > 0.0:
                    break

    # STEP 4: Last resort — try the raw incoming service name against admin keys
    if price == 0.0 and service:
        _raw_lower = service.lower().strip()
        for _k, _v in GN_DATA["services"].items():
            if _k.lower().strip() == _raw_lower or _raw_lower in _k.lower() or _k.lower() in _raw_lower:
                if cnt:
                    price = _v.get("countries", {}).get(cnt, {}).get("price", 0.0)
                    if price == 0.0:
                        for _ck, _cv in _v.get("countries", {}).items():
                            if _ck.lower().strip() == cnt.lower().strip():
                                price = _cv.get("price", 0.0)
                                break
                if price > 0.0:
                    break

    logger.info(
        f"[DM][BALANCE] hold_svc={hold_svc_key!r} hold_cnt={hold_cnt_key!r} "
        f"sms_svc={service!r} price={price} owner={owner_id}"
    )
    # Always call gn_credit_otp so OTP counters increment; adds 0 if price not found
    balance = gn_credit_otp(owner_id, price)
    price_as_usdt = price   / rate
    total_w_usdt  = balance / rate

    # ── Country info ──────────────────────────────────────────
    country_code = ""
    country_name = cnt
    if svc and cnt:
        c_data       = svc.get("countries", {}).get(cnt, {})
        country_code = c_data.get("code", "")
        country_name = c_data.get("name", cnt)
    flag     = gn_flag(country_code) if country_code else "🌍"
    svc_name = service or hold.get("service", "Service")
    svc_em   = gn_svc_emoji(svc_name)

    # ── Phone / OTP ───────────────────────────────────────────
    masked_phone = mask_phone_for_dm(number)
    raw_otp      = re.sub(r'[^0-9]', '', otp) if otp and otp != "N/A" else ""
    fmt_otp      = format_otp_code(raw_otp) if raw_otp else "------"
    logger.info(f"[DM] raw_otp={raw_otp!r} fmt_otp={fmt_otp!r} masked_phone={masked_phone!r}")

    # ── OTP count line ────────────────────────────────────────
    otp_count_line = ""
    if otp_limit > 0:
        otp_count_line = (
            f'\n<tg-emoji emoji-id="6235417186572178718">➡️</tg-emoji>'
            f" <b>OTP Count: {current_count}/{otp_limit}</b>"
        )

    # ── Message text — mirrors Go mainBotDMMessage ────────────
    price_line = (
        f'<tg-emoji emoji-id="6001526766714227911">💰</tg-emoji>'
        f" <b>+{price:.2f} {GN_CURRENCY} / +{price_as_usdt:.6f} {GN_DOLLAR}</b>"
    )
    balance_line = (
        f'<tg-emoji emoji-id="6001434068435079689">💎</tg-emoji>'
        f" <b>{balance:.2f} {GN_CURRENCY} / {total_w_usdt:.4f} {GN_DOLLAR}</b>"
    )
    text = (
        f"{svc_em} <b>{svc_name}</b>\n"
        f"{flag} <b>{country_name}</b>\n"
        f'<tg-emoji emoji-id="5954078884310814346">📱</tg-emoji>'
        f" <b>{masked_phone}</b>{otp_count_line}\n"
        f"{price_line}\n"
        f"{balance_line}"
    )

    # ── OTP button as raw dict — copy_text + styled icon ─────
    if raw_otp:
        dm_keyboard = {"inline_keyboard": [[{
            "text":                 f" {fmt_otp}",
            "icon_custom_emoji_id": "6204162490515855272",
            "copy_text":            {"text": raw_otp},
            "style":                "danger",
        }]]}
    else:
        dm_keyboard = {"inline_keyboard": [[{"text": "No OTP Detected", "callback_data": "no_otp"}]]}

    # ── Send via make_request (raw JSON) ─────────────────────
    # Bypasses PTB serialization so <tg-emoji> and styled buttons reach Telegram
    import json as _json
    bot = get_shared_bot()
    logger.info(f"[DM] 📤 sending to owner_id={owner_id}")
    try:
        import aiohttp as _aiohttp_dm
        _url_dm = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        _payload_dm = {
            "chat_id": str(owner_id),
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
            "reply_markup": _json.dumps(dm_keyboard),
        }
        async with _aiohttp_dm.ClientSession() as _sess_dm:
            async with _sess_dm.post(_url_dm, json=_payload_dm) as _resp_dm:
                _result_dm = await _resp_dm.json()
                if not _result_dm.get("ok"):
                    raise Exception(_result_dm.get("description", "Unknown error"))
        logger.info(f"[DM] ✅ sent to uid={owner_id} for ...{number[-5:]}")
    except Exception as e:
        logger.error(f"[DM] ❌ make_request FAILED uid={owner_id}: {e}")

def log_otp_memory(number: str, service: str, otp: str, source: str):
    global OTP_LOG
    OTP_LOG.append({"number": number, "service": service, "otp": otp or "N/A",
                    "source": source, "time": datetime.now().strftime("%H:%M:%S")})
    if len(OTP_LOG) > OTP_LOG_MAX:
        OTP_LOG = OTP_LOG[-OTP_LOG_MAX:]
    db_save_otp_history(number, service, otp, source)

# ═══════════════════════════════════════════════════════════════
#  REST PANEL FETCH
# ═══════════════════════════════════════════════════════════════
def fetch_latest(panel_name: str) -> Optional[Dict]:
    rows = fetch_latest_batch(panel_name, limit=1)
    return rows[0] if rows else None

def fetch_latest_batch(panel_name: str, limit: int = 20) -> List[Dict]:
    if panel_name not in API_PANELS:
        return []
    cfg = API_PANELS[panel_name]
    try:
        r  = requests.get(cfg["url"],
                          params={"token": cfg["token"], "records": limit},
                          timeout=10)
        ct = r.headers.get('content-type', '')
        if 'application/json' not in ct:
            return []
        data = r.json()
        results = []
        if isinstance(data, dict) and data.get("status") == "success":
            for row in data.get("data", [])[:limit]:
                results.append({"time": row.get("dt",""), "number": row.get("num",""),
                                 "service": row.get("cli",""), "message": row.get("message","")})
        elif isinstance(data, list):
            for row in data[:limit]:
                if len(row) >= 4:
                    results.append({"time": row[3], "number": row[1],
                                    "service": row[0] or "Unknown", "message": row[2]})
        return results
    except Exception as e:
        STATS["errors"] += 1
        logger.error(f"Fetch error {panel_name}: {e}")
        return []

def fetch_all_panels(limit: int = 5) -> list:
    results = []
    for panel_name, cfg in API_PANELS.items():
        try:
            r  = requests.get(cfg["url"],
                              params={"token": cfg["token"], "records": limit},
                              timeout=10)
            ct = r.headers.get('content-type', '')
            if 'application/json' not in ct:
                continue
            data = r.json()
            if isinstance(data, dict) and data.get("status") == "success":
                for row in data.get("data", [])[:limit]:
                    results.append({"panel": panel_name, "time": row.get("dt",""),
                                    "number": row.get("num",""), "service": row.get("cli",""),
                                    "message": row.get("message","")})
            elif isinstance(data, list):
                for row in data[:limit]:
                    if len(row) >= 4:
                        results.append({"panel": panel_name, "time": row[3], "number": row[1],
                                        "service": row[0] or "Unknown", "message": row[2]})
        except Exception as e:
            logger.error(f"fetch_all_panels error {panel_name}: {e}")
    return results

# ═══════════════════════════════════════════════════════════════
#  EXCEPTION HANDLER
# ═══════════════════════════════════════════════════════════════
def handle_task_exception(task: asyncio.Task):
    try:
        task.result()
    except asyncio.CancelledError:
        pass
    except Exception as e:
        logger.error(f"Task {task.get_name()} exception: {e}", exc_info=True)

# ═══════════════════════════════════════════════════════════════
#  IVAS WEBSOCKET WORKER
# ═══════════════════════════════════════════════════════════════
async def _ivas_ping(ws, interval_ms):
    while True:
        await asyncio.sleep(interval_ms / 1000)
        try:
            await ws.send("3")
        except:
            break

async def ivas_worker(name: str):
    logger.info(f"🔌 IVAS worker starting: {name}")
    seen = set()
    while True:
        try:
            accounts = load_ivas()
            if name not in accounts:
                logger.info(f"IVAS '{name}' removed — stopping.")
                break
            uri = accounts[name].get("uri", "")
            if not uri:
                await asyncio.sleep(10)
                continue
            ssl_ctx = ssl._create_unverified_context()
            try:
                async with websockets.connect(uri, ssl=ssl_ctx) as ws:
                    logger.info(f"✅ IVAS [{name}] connected.")
                    initial = await ws.recv()
                    ping_interval = 25000
                    try:
                        if initial.startswith("0{"):
                            ping_interval = json.loads(initial[1:]).get("pingInterval", 25000)
                    except:
                        pass
                    await ws.send("40/livesms,")
                    ping_task = asyncio.create_task(_ivas_ping(ws, ping_interval))
                    try:
                        check_counter = 0
                        while True:
                            check_counter += 1
                            if check_counter % 100 == 0:
                                if name not in load_ivas():
                                    break
                            msg = await ws.recv()
                            if not msg.startswith("42/livesms,"):
                                continue
                            try:
                                data = json.loads(msg[msg.find("["):])
                                if not (isinstance(data, list) and len(data) > 1
                                        and isinstance(data[1], dict)):
                                    continue
                                sms     = data[1]
                                number  = sms.get("recipient", "")
                                text    = sms.get("message", "") or ""
                                service = sms.get("originator", "Unknown")
                                country = sms.get("range", "")
                                otp     = extract_otp(text)
                                uniq    = f"{number}-{text[:20]}"
                                if uniq in seen:
                                    continue
                                seen.add(uniq)
                                if len(seen) > 1000:
                                    seen = set(list(seen)[-500:])
                                STATS["ivas_hits"][name] = STATS["ivas_hits"].get(name, 0) + 1
                                log_otp_memory(number, service, otp, f"IVAS:{name}")
                                if otp and number:
                                    store = load_otp_store()
                                    store[number] = otp
                                    save_otp_store(store)
                                formatted = format_otp_message(number, service, otp or "N/A",
                                    source_label=f"IVAS:{name}", sms_text=text)
                                keyboard = get_otp_keyboard(number, otp)
                                await send_to_all_groups(formatted, reply_markup=keyboard)
                                if otp:
                                    await send_otp_to_owner(number, service, otp,
                                        sms_text=text, source_label=f"IVAS:{name}")
                            except Exception as e:
                                logger.error(f"IVAS [{name}] parse error: {e}")
                    finally:
                        ping_task.cancel()
            except websockets.exceptions.WebSocketException as e:
                logger.error(f"IVAS [{name}] WS error: {e}. Retry in 5s...")
                await asyncio.sleep(5)
            except Exception as e:
                logger.error(f"IVAS [{name}] error: {e}. Retry in 5s...")
                await asyncio.sleep(5)
        except Exception as e:
            logger.error(f"IVAS [{name}] critical: {e}. Retry in 10s...")
            await asyncio.sleep(10)

# ═══════════════════════════════════════════════════════════════
#  REST API WORKER
# ═══════════════════════════════════════════════════════════════
async def api_worker(panel: str):
    seen: set = set()
    logger.info(f"📡 REST worker starting: {panel}")
    loop = asyncio.get_event_loop()
    while True:
        try:
            if panel not in API_PANELS:
                break
            rows = await loop.run_in_executor(None, lambda: fetch_latest_batch(panel, limit=20))
            for data in rows:
                uniq = f"{data['number']}-{data['message'][:30]}"
                if uniq in seen:
                    continue
                seen.add(uniq)
                if len(seen) > 1000:
                    seen = set(list(seen)[-500:])
                otp = extract_otp(data["message"])
                STATS["panel_hits"][panel] = STATS["panel_hits"].get(panel, 0) + 1
                log_otp_memory(data["number"], data["service"], otp, f"REST:{panel}")
                if otp and data["number"]:
                    store = load_otp_store()
                    store[data["number"]] = otp
                    save_otp_store(store)
                formatted = format_otp_message(
                    data["number"], data["service"], otp or "N/A",
                    source_label=f"REST:{panel}", sms_text=data.get("message", ""))
                keyboard = get_otp_keyboard(data["number"], otp)
                await send_to_all_groups(formatted, reply_markup=keyboard)
                if otp:
                    await send_otp_to_owner(data["number"], data["service"], otp,
                        sms_text=data.get("message",""), source_label=f"REST:{panel}")
        except Exception as e:
            logger.error(f"REST worker error {panel}: {e}")
        await asyncio.sleep(2)

# ═══════════════════════════════════════════════════════════════
#  MONITOR & CLEANUP
# ═══════════════════════════════════════════════════════════════
async def monitor_tasks():
    while True:
        await asyncio.sleep(60)
        for name in load_ivas():
            if name not in IVAS_TASKS or IVAS_TASKS[name].done():
                logger.warning(f"IVAS '{name}' dead — restarting...")
                task = asyncio.create_task(ivas_worker(name), name=f"IVAS-{name}")
                task.add_done_callback(handle_task_exception)
                IVAS_TASKS[name] = task
        for panel in list(API_PANELS.keys()):
            if panel not in REST_TASKS or REST_TASKS[panel].done():
                logger.warning(f"REST '{panel}' dead — restarting...")
                task = asyncio.create_task(api_worker(panel), name=f"REST-{panel}")
                task.add_done_callback(handle_task_exception)
                REST_TASKS[panel] = task

async def cleanup_states():
    while True:
        await asyncio.sleep(60)
        now = time.time()
        for d in [PANEL_ADD_STATES, IVAS_ADD_STATES, BROADCAST_STATES,
                  SETTING_STATES, FETCH_STATES]:
            for uid in list(d.keys()):
                if now - d[uid].get("timestamp", 0) > STATE_TIMEOUT:
                    del d[uid]

# ═══════════════════════════════════════════════════════════════
#  KEYBOARDS
# ═══════════════════════════════════════════════════════════════
def b(text, cb=None, url=None):
    return InlineKeyboardButton(text, callback_data=cb) if cb else InlineKeyboardButton(text, url=url)

def bc(text, cb=None, url=None, style=None, icon=None):
    """Inline button with Bot API color style + optional premium emoji icon."""
    api_kw = {}
    if style:   api_kw["style"] = style
    if icon:    api_kw["icon_custom_emoji_id"] = icon
    kwargs = {"api_kwargs": api_kw} if api_kw else {}
    if cb:
        return InlineKeyboardButton(text, callback_data=cb, **kwargs)
    return InlineKeyboardButton(text, url=url, **kwargs)

def gn_btn(text, cb=None, url=None, style=None, icon=None):
    """Same as bc() — inline button with style + emoji icon."""
    return bc(text, cb=cb, url=url, style=style, icon=icon)

# ── Emoji IDs for reply keyboard buttons (from main.go consts) ───────────────
_KB_EMOJI = {
    "get_number":  "5296369303661067030",
    "my_account":  "6237864166879663987",
    "balance":     "5778204036578678218",
    "withdraw":    "5409048419211682843",
    "top_users":   "6235252066554484059",
    "developer":   "6235572922086331108",
    "admin_panel": "6205965994528086727",
    "add_numbers": "4956507094124594921",
    "list":        "5197219609970758159",
    "remove":      "5445267414562389170",
    "users":       "4958832114540741368",
    "back":        "5255703720078879038",
    "announce":    "6206080502651164081",
    "join":        "6206080502651164081",
    "referral":    "6242498410822244114",
    "chart":       "5225414461080685066",
    "panels":      "5217824874487101321",
    "refresh":     "4956287101604725699",
    "money":       "6190336264940559752",
    "crown":       "6206096153511990389",
    "rocket":      "5235575317191474172",
    "gift":        "6206027872121918710",
}

def skb(text: str, emoji_key: str, style: str) -> KeyboardButton:
    """Styled KeyboardButton with color + premium emoji icon.
    PTB 21.7 passes api_kwargs directly to Bot API JSON payload.
    Bot API 9.4 supports icon_custom_emoji_id for KeyboardButton."""
    eid = _KB_EMOJI.get(emoji_key, "")
    api_kw: dict = {"style": style}
    if eid:
        api_kw["icon_custom_emoji_id"] = eid
    return KeyboardButton(text, api_kwargs=api_kw)


def get_main_menu_keyboard():
    """Main user reply keyboard — colored + premium emoji icon from main.go."""
    return ReplyKeyboardMarkup([
        [skb("𝗚𝗲𝘁 𝗡𝘂𝗺𝗯𝗲𝗿",        "get_number",  "primary"),
         skb("𝗠𝘆 𝗔𝗰𝗰𝗼𝘂𝗻𝘁",        "my_account",  "primary")],
        [skb("𝗕𝗮𝗹𝗮𝗻𝗰𝗲",             "balance",     "success"),
         skb("𝗪𝗶𝘁𝗵𝗱𝗿𝗮𝘄",           "withdraw",    "danger")],
        [skb("𝗧𝗼𝗽 𝗨𝘀𝗲𝗿𝘀",           "top_users",   "success"),
         skb("𝗗𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗿",          "developer",   "primary")],
        [skb("𝗥𝗲𝗳𝗲𝗿𝗿𝗮𝗹",             "referral",    "success")],
        [skb("𝗝𝗼𝗶𝗻 𝗢𝘂𝗿 𝗖𝗵𝗮𝗻𝗻𝗲𝗹𝘀",  "join",        "primary")],
    ], resize_keyboard=True)


def get_admin_menu_keyboard():
    """Admin reply keyboard — same as user (Admin Panel removed)."""
    return ReplyKeyboardMarkup([
        [skb("𝗚𝗲𝘁 𝗡𝘂𝗺𝗯𝗲𝗿",        "get_number",  "primary"),
         skb("𝗠𝘆 𝗔𝗰𝗰𝗼𝘂𝗻𝘁",        "my_account",  "primary")],
        [skb("𝗕𝗮𝗹𝗮𝗻𝗰𝗲",             "balance",     "success"),
         skb("𝗪𝗶𝘁𝗵𝗱𝗿𝗮𝘄",           "withdraw",    "danger")],
        [skb("𝗧𝗼𝗽 𝗨𝘀𝗲𝗿𝘀",           "top_users",   "success"),
         skb("𝗗𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗿",          "developer",   "primary")],
        [skb("𝗥𝗲𝗳𝗲𝗿𝗿𝗮𝗹",             "referral",    "success")],
        [skb("𝗝𝗼𝗶𝗻 𝗢𝘂𝗿 𝗖𝗵𝗮𝗻𝗻𝗲𝗹𝘀",  "join",        "primary")],
    ], resize_keyboard=True)


def get_admin_action_keyboard():
    """Admin Numbers panel quick keyboard."""
    return ReplyKeyboardMarkup([
        [skb("𝗔𝗱𝗱 𝗡𝘂𝗺𝗯𝗲𝗿𝘀",  "add_numbers", "success"),
         skb("𝗦𝘆𝘀𝘁𝗲𝗺 𝗦𝘁𝗮𝘁𝘀",  "chart",       "primary")],
        [skb("𝗕𝗮𝗰𝗸",           "back",        "primary")],
    ], resize_keyboard=True)


def get_back_keyboard():
    """Back only keyboard."""
    return ReplyKeyboardMarkup([
        [skb("𝗕𝗮𝗰𝗸", "back", "primary")],
    ], resize_keyboard=True)


def smart_kb(uid: int):
    """Returns admin menu if admin, else main menu."""
    if is_admin(uid):
        return get_admin_menu_keyboard()
    return get_main_menu_keyboard()

def get_admin_keyboard(uid: int = 0):
    """Build /admin inline panel buttons — each button has its own colour + icon."""
    rows = []
    row = []
    if has_perm(uid, "numbers"): row.append(bc("𝗡𝘂𝗺𝗯𝗲𝗿𝘀",    cb="menu_numbers",    style="success", icon="5296369303661067030"))
    if has_perm(uid, "files"):   row.append(bc("𝗙𝗶𝗹𝗲𝘀",      cb="menu_files",      style="primary", icon="5197219609970758159"))
    if row: rows.append(row); row = []
    if has_perm(uid, "panels"):  row.append(bc("𝗣𝗮𝗻𝗲𝗹𝘀",     cb="menu_panels",     style="primary", icon="5217824874487101321"))
    if has_perm(uid, "ivas"):    row.append(bc("𝗜𝗩𝗔𝗦",       cb="menu_ivas",       style="success", icon="5352564488258200671"))
    if row: rows.append(row); row = []
    if has_perm(uid, "fetch_sms"):   row.append(bc("𝗙𝗲𝘁𝗰𝗵 𝗦𝗠𝗦",   cb="menu_fetch",       style="primary", icon="4956287101604725699"))
    if has_perm(uid, "otp_history"): row.append(bc("𝗢𝗧𝗣 𝗛𝗶𝘀𝘁𝗼𝗿𝘆", cb="menu_otp_history", style="success", icon="5197219609970758159"))
    if row: rows.append(row); row = []
    if has_perm(uid, "groups"):    row.append(bc("𝗚𝗿𝗼𝘂𝗽𝘀",    cb="menu_groups",    style="primary", icon="4958832114540741368"))
    if has_perm(uid, "broadcast"): row.append(bc("𝗕𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁", cb="nb_broadcast",    style="danger",  icon="6206080502651164081"))
    if row: rows.append(row); row = []
    if has_perm(uid, "settings"):  row.append(bc("𝗦𝗲𝘁𝘁𝗶𝗻𝗴𝘀",  cb="menu_settings",  style="primary", icon="6205965994528086727"))
    if has_perm(uid, "advanced"):  row.append(bc("𝗔𝗱𝘃𝗮𝗻𝗰𝗲𝗱",  cb="menu_advanced",  style="danger",  icon="6176966310920983412"))
    if row: rows.append(row)
    if has_perm(uid, "stats"):
        rows.append([
            bc("𝗦𝘁𝗮𝘁𝘀",  cb="stats",  style="success", icon="5225414461080685066"),
            bc("𝗦𝘁𝗮𝘁𝘂𝘀", cb="status", style="primary", icon="5319310205752717294"),
        ])
    rows.append([
        bc("𝗥𝗲𝗳𝗿𝗲𝘀𝗵", cb="refresh_admin", style="primary", icon="4956287101604725699"),
        bc("𝗖𝗹𝗼𝘀𝗲",   cb="close_admin",   style="danger",  icon="5974083768233760323"),
    ])
    return InlineKeyboardMarkup(rows)

def get_numbers_menu():
    return InlineKeyboardMarkup([
        [bc("𝗔𝗱𝗱 𝗡𝘂𝗺𝗯𝗲𝗿𝘀",     cb="nb_add_numbers",   style="success", icon="4956507094124594921"),
         bc("𝗟𝗶𝘀𝘁 𝗦𝗲𝗿𝘃𝗶𝗰𝗲𝘀",    cb="nb_list_services", style="primary", icon="5197219609970758159")],
        [bc("𝗦𝘆𝘀𝘁𝗲𝗺 𝗦𝘁𝗮𝘁𝘀",    cb="nb_system_stats",  style="primary", icon="5225414461080685066"),
         bc("𝗧𝗼𝘁𝗮𝗹 𝗨𝘀𝗲𝗿𝘀",     cb="nb_total_users",   style="primary", icon="4958832114540741368")],
        [bc("𝗥𝗲𝗺𝗼𝘃𝗲 𝗦𝗲𝗿𝘃𝗶𝗰𝗲",  cb="nb_remove_svc",    style="danger",  icon="5445267414562389170"),
         bc("𝗥𝗲𝗺𝗼𝘃𝗲 𝗖𝗼𝘂𝗻𝘁𝗿𝘆", cb="nb_remove_cnt",    style="danger",  icon="5445267414562389170")],
        [bc("𝗔𝗱𝗱 𝗕𝗮𝗹𝗮𝗻𝗰𝗲",     cb="nb_add_balance",   style="success", icon="6190336264940559752"),
         bc("𝗪𝗶𝘁𝗵𝗱𝗿𝗮𝘄𝗮𝗹𝘀",    cb="nb_withdrawals",   style="primary", icon="6206155797722830770")],
        [bc("𝗨𝘀𝗲𝗿 𝗜𝗻𝗳𝗼",       cb="nb_user_info",     style="primary", icon="5242442819573927209"),
         bc("𝗧𝗼𝗴𝗴𝗹𝗲 𝗪𝗱𝗿𝗮𝘄",   cb="nb_toggle_wd",     style="danger",  icon="6206479140040743133")],
        [bc("💰 𝗠𝗶𝗻 𝗪𝗶𝘁𝗵𝗱𝗿𝗮𝘄𝗮𝗹",  cb="nb_min_wd",        style="primary", icon="6206155797722830770")],
        [bc("𝗕𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁",       cb="nb_broadcast",     style="primary", icon="6206080502651164081")],
        [bc("𝗕𝗮𝗰𝗸",             cb="back_to_admin",    style="primary", icon="5255703720078879038")],
    ])

def get_files_menu():
    return InlineKeyboardMarkup([
        [b("📂 List Files","fm_list"),          b("📥 Download Log","fm_download_log")],
        [b("📥 Download OTP Store","fm_download_otp"),b("📥 Download DB","fm_download_db")],
        [b("🗑️ Clear Log","fm_clear_log"),      b("🔙 Back","back_to_admin")],
    ])

def get_panels_menu():
    return InlineKeyboardMarkup([
        [b("📋 List Panels","list_panels"),     b("➕ Add Panel","add_panel")],
        [b("🗑️ Remove Panel","remove_panel"),  b("🧪 Test All","test_panels_menu")],
        [b("🔄 Fetch Latest","panel_fetch_all"),b("🔙 Back","back_to_admin")],
    ])

def get_panels_keyboard(action="view"):
    panels  = load_panels()
    keyboard = []
    for name in panels:
        active = (name in REST_TASKS and not REST_TASKS[name].done())
        st     = "🟢" if active else "🔴"
        cb     = f"remove_panel_{name}" if action == "remove" else f"view_panel_{name}"
        label  = f"{st} {name.upper()}" + (" 🗑️" if action == "remove" else "")
        keyboard.append([b(label, cb)])
    keyboard.append([b("🔙 Back","menu_panels")])
    return InlineKeyboardMarkup(keyboard)

def get_ivas_menu():
    return InlineKeyboardMarkup([
        [b("📋 List IVAS","list_ivas"),         b("➕ Add IVAS","add_ivas")],
        [b("🗑️ Remove IVAS","remove_ivas"),     b("🔄 Restart All","ivas_restart_all")],
        [b("🔙 Back","back_to_admin")],
    ])

def get_ivas_keyboard(action="view"):
    accounts = load_ivas()
    keyboard = []
    for name in accounts:
        active = (name in IVAS_TASKS and not IVAS_TASKS[name].done())
        st     = "🟢" if active else "🔴"
        cb     = f"remove_ivas_{name}" if action == "remove" else f"view_ivas_{name}"
        label  = f"{st} {name.upper()}" + (" 🗑️" if action == "remove" else "")
        keyboard.append([b(label, cb)])
    keyboard.append([b("🔙 Back","menu_ivas")])
    return InlineKeyboardMarkup(keyboard)

def get_groups_menu():
    groups  = load_groups()
    config  = load_config()
    keyboard = []
    for gid in groups:
        keyboard.append([b(f"🗑️ Remove {gid}", f"del_group_{gid}")])
    keyboard.append([b("➕ Add Group","add_group_prompt")])
    keyboard.append([b("📋 Set Log Group","set_log_group"),
                     b("❌ Clear Log Group","clear_log_group")])
    keyboard.append([b("🔙 Back","back_to_admin")])
    return InlineKeyboardMarkup(keyboard)

def get_otp_history_menu():
    return InlineKeyboardMarkup([
        [b("📋 Last 10","otp_hist_10"),         b("📋 Last 20","otp_hist_20")],
        [b("🔍 Search by Number","otp_search_num"),b("📤 Export CSV","otp_export_hist")],
        [b("🗑️ Clear History","otp_clear_hist"),b("🔙 Back","back_to_admin")],
    ])

def get_fetch_menu():
    return InlineKeyboardMarkup([
        [b("🔄 Fetch All Panels","fetch_all_now")],
        [b("🔍 Fetch by Number","fetch_by_number")],
        [b("📡 Fetch Single Panel","fetch_single_panel")],
        [b("🔙 Back","back_to_admin")],
    ])

def get_settings_menu():
    config = load_config()
    fwd    = "✅ ON" if config.get("otp_forward", True) else "❌ OFF"
    delay  = config.get("forward_delay", 0)
    lg     = str(config.get("log_group") or "None")[:12]
    return InlineKeyboardMarkup([
        [b(f"📤 OTP Forward: {fwd}","toggle_otp_forward")],
        [b(f"⏱ Delay: {delay}s","set_forward_delay"),
         b("📢 Channel Link","set_channel")],
        [b("🤖 NumberBot Link","set_numberbot"),
         b(f"📋 Log Group: {lg}","set_log_group")],
        [b("🔗 OTP Group Link","set_otp_group_link"),
         b("👤 Admin Manager","menu_admin_manager")],
        [b("🔙 Back","back_to_admin")],
    ])

def get_admin_manager_keyboard():
    staff    = load_staff()
    keyboard = []
    for aid in OWNER_IDS:
        keyboard.append([b(f"👑 {aid}  (Owner)", "noop")])
    for uid_str, info in staff.items():
        uid_int = int(uid_str)
        if uid_int in OWNER_IDS:
            continue
        name  = info.get("name", uid_str)
        perms = info.get("perms", [])
        keyboard.append([
            b(f"🛡️ {name} ({len(perms)} perms)", f"edit_staff_{uid_str}"),
            b("🗑️", f"remove_staff_{uid_str}")
        ])
    keyboard.append([b("➕ Add Staff Member", "add_staff_prompt")])
    keyboard.append([b("🔙 Back", "menu_settings")])
    return InlineKeyboardMarkup(keyboard)

def get_staff_perms_keyboard(uid_str: str):
    staff   = load_staff()
    info    = staff.get(uid_str, {})
    cur     = info.get("perms", [])
    keyboard = []
    for perm_key, perm_label in ALL_PERMISSIONS.items():
        has = perm_key in cur
        icon = "✅" if has else "☑️"
        keyboard.append([b(f"{icon} {perm_label}", f"toggle_perm_{uid_str}_{perm_key}")])
    keyboard.append([
        b("✅ Grant All",  f"grant_all_{uid_str}"),
        b("❌ Revoke All", f"revoke_all_{uid_str}")
    ])
    keyboard.append([b("🔙 Back", "menu_admin_manager")])
    return InlineKeyboardMarkup(keyboard)

def get_advanced_keyboard():
    return InlineKeyboardMarkup([
        [b("🔄 Restart All Workers","restart_workers"),
         b("🛑 Stop Forwarding","stop_forward")],
        [b("▶️ Start Forwarding","start_forward"),
         b("🔄 Reload Config","reload_config")],
        [b("🗑️ Clear OTP Store","clear_all_otps"),
         b("📤 Export OTP Store","export_otps")],
        [b("📋 View Logs","view_logs"),
         b("🔁 Restart Bot","restart_bot")],
        [b("🧪 Test All Panels","test_panels_adv"),
         b("📊 Worker Status","worker_status")],
        [b("🔙 Back","back_to_admin")],
    ])

def get_confirmation_keyboard(action: str, extra: str = ""):
    cd = f"confirm_{action}" + (f"_{extra}" if extra else "")
    return InlineKeyboardMarkup([
        [b("✅ Confirm", cd), b("❌ Cancel","cancel_action")]
    ])

def get_broadcast_keyboard():
    return InlineKeyboardMarkup([
        [b("📝 Text Only","broadcast_text"),
         b("🔘 With Buttons","broadcast_with_buttons")],
        [b("🔙 Back","back_to_admin")]
    ])

def get_countries_keyboard():
    rows = db_get_countries()
    if not rows:
        return None
    # Use custom emojis for country buttons
    buttons = []
    for c, n in rows:
        region_code = c[:2].upper() if len(c) >= 2 else "DEFAULT"
        custom_emoji = get_custom_country_emoji(region_code)
        # Strip HTML tags for button text, just show emoji representation
        emoji_display = "🌍"  # fallback
        buttons.append(b(f"{emoji_display} {c} ({n})", f"nb_get|{c}"))
    kb = [buttons[i:i+2] for i in range(0, len(buttons), 2)]
    kb.append([b("🔄 Refresh","show_countries")])
    return InlineKeyboardMarkup(kb)

def get_nb_stock_keyboard():
    rows     = db_get_countries()
    keyboard = [[b(f"❌ {c} ({n})  Delete", f"nb_del|{c}")] for c, n in rows]
    keyboard.append([b("🔙 Back","menu_numbers")])
    return InlineKeyboardMarkup(keyboard)

# ═══════════════════════════════════════════════════════════════
#  COMMANDS
# ═══════════════════════════════════════════════════════════════

# Force-join fully removed

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from html import escape
    uid   = update.effective_user.id
    uname = update.effective_user.username or ""
    first = escape(update.effective_user.first_name or "User")
    last  = escape(update.effective_user.last_name  or "")
    db_add_user(uid)
    gn_upsert_user(uid, uname, first, last)

    # ── Handle referral deep-link (/start ref123456) ──────────
    args = context.args or []
    if args and args[0].startswith("ref"):
        try:
            ref_by = int(args[0][3:])
            if ref_by != uid:
                uk = str(uid)
                if uk in GN_DATA["users"] and not GN_DATA["users"][uk].get("referred_by"):
                    GN_DATA["users"][uk]["referred_by"] = ref_by
                    gn_save()
        except:
            pass

    name_line = f"{first} {last}".strip()
    admin_note = "\n\n🛡️ <b>ADMIN MODE ACTIVE</b> — use /admin" if is_admin(uid) else ""

    welcome = (
        f"<tg-emoji emoji-id=\"6204104220694550861\">☄️</tg-emoji> "
        f"<b>Welcome, {name_line}!</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"<tg-emoji emoji-id=\"6205965994528086727\">💠</tg-emoji> <b>Junaid OTP</b>\n\n"
        f"<tg-emoji emoji-id=\"5411590687663608498\">⚡️</tg-emoji> Fastest OTP Service in Pakistan\n"
        f"<tg-emoji emoji-id=\"5339267587337370029\">🤖</tg-emoji> Auto-Assign Number System\n"
        f"<tg-emoji emoji-id=\"5352564488258200671\">📡</tg-emoji> Multi-Panel + IVAS Support\n"
        f"<tg-emoji emoji-id=\"6242498410822244114\">🎁</tg-emoji> Referral Reward System\n"
        f"<tg-emoji emoji-id=\"6206155797722830770\">💵</tg-emoji> PKR + USDT Withdrawal\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"<tg-emoji emoji-id=\"6206096153511990389\">👑</tg-emoji> <b>Version 7.0</b>  •  "
        f"<tg-emoji emoji-id=\"6235572922086331108\">🧑‍💻</tg-emoji> Dev: Junaid Ali\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"👆 <b>Select an option below:</b>"
        f"{admin_note}"
    )
    await update.message.reply_text(welcome, parse_mode="HTML",
                                    reply_markup=smart_kb(uid))

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🔔 <b>{BOT_NAME}</b> - Help\n━━━━━━━━━━━━━━━━━━━━━━\n"
        f"/start — Start\n/admin — Admin panel\n"
        f"/otpfor [num] — Search OTP\n/fetchsms — Fetch latest SMS\n"
        f"/status — Bot status\n/stats — Statistics\n"
        f"/addgroup [id] — Add OTP group\n/removegroup [id] — Remove group\n"
        f"/reload — Reload workers\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n🤖 Dev: {DEV_CONTACT}",
        parse_mode="HTML", reply_markup=smart_kb(uid))

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if is_admin(uid):
        await update.message.reply_text(
            f"<tg-emoji emoji-id=\"6205965994528086727\">💠</tg-emoji> <b>ADMIN PANEL</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<tg-emoji emoji-id=\"6235572922086331108\">🧑‍💻</tg-emoji> Select an option:",
            parse_mode="HTML", reply_markup=get_admin_keyboard(uid))
    else:
        await update.message.reply_text("❌ Unauthorized!")

async def otpfor_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Use: /otpfor 447123456789")
        return
    target = context.args[0].replace("+", "")
    wait   = await update.message.reply_text(f"🔄 Scanning <code>{target}</code>...", parse_mode="HTML")
    found  = None
    store  = load_otp_store()
    for k, v in store.items():
        if target in k:
            found = v
            break
    if not found:
        rows = db_search_otp_by_number(target)
        if rows:
            found = rows[0][2]
    if not found:
        for panel in API_PANELS:
            d2 = fetch_latest(panel)
            if d2 and target in d2["number"]:
                found = extract_otp(d2["message"])
                if found:
                    break
    if found:
        await wait.edit_text(
            f"✅ <b>OTP FOUND</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📞 <code>{target}</code>\n🔑 <code>{found}</code>", parse_mode="HTML")
    else:
        await wait.edit_text(
            f"❌ <b>No OTP found</b> for <code>{target}</code>", parse_mode="HTML")

async def fetchsms_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Unauthorized!")
        return
    wait    = await update.message.reply_text("🔄 Fetching...")
    results = fetch_all_panels(limit=5)
    if not results:
        await wait.edit_text("❌ No SMS fetched.")
        return
    text = f"📨 <b>LATEST SMS ({len(results)})</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
    for r in results[:10]:
        otp  = extract_otp(r["message"]) or "N/A"
        text += (f"\n📡 <b>{r['panel']}</b> | {r['service']}\n"
                 f"📞 <code>{r['number']}</code>\n"
                 f"🔑 OTP: <code>{otp}</code>\n"
                 f"💬 {r['message'][:80]}\n──────────────────────\n")
    await wait.edit_text(text[:4000], parse_mode="HTML")

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Unauthorized!")
        return
    await update.message.reply_text(_build_status(), parse_mode="HTML")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Unauthorized!")
        return
    total, active_today, active_week = db_user_stats()
    uptime = str(datetime.now() - datetime.fromtimestamp(STATS['start_time'])).split('.')[0]
    await update.message.reply_text(
        f"📊 <b>BOT STATS</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
        f"⏱ Uptime: <code>{uptime}</code>\n"
        f"👤 Total Users: <code>{total}</code>\n"
        f"🟢 Active Today: <code>{active_today}</code>\n"
        f"📅 This Week: <code>{active_week}</code>\n"
        f"📊 OTPs Sent: <code>{STATS['otps_sent']}</code>\n"
        f"🚫 Dropped: <code>{STATS['otps_dropped']}</code>\n"
        f"❌ Errors: <code>{STATS['errors']}</code>\n"
        f"📦 Numbers in DB: <code>{db_total_numbers()}</code>\n"
        f"🗄 OTP Store: <code>{len(load_otp_store())}</code>\n"
        f"📡 REST Panels: <code>{len(load_panels())}</code>\n"
        f"🔌 IVAS Accounts: <code>{len(load_ivas())}</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━", parse_mode="HTML")

async def addgroup_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Unauthorized!")
        return
    if not context.args:
        await update.message.reply_text("Usage: /addgroup <chat_id>")
        return
    try:
        gid    = int(context.args[0])
        groups = load_groups()
        if gid in groups:
            await update.message.reply_text("🟡 Already exists.")
            return
        groups.append(gid)
        save_groups(groups)
        await update.message.reply_text(f"✅ Group <code>{gid}</code> added.", parse_mode="HTML")
    except ValueError:
        await update.message.reply_text("❌ Invalid chat ID.")

async def removegroup_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Unauthorized!")
        return
    if not context.args:
        await update.message.reply_text("Usage: /removegroup <chat_id>")
        return
    try:
        gid    = int(context.args[0])
        groups = load_groups()
        if gid not in groups:
            await update.message.reply_text("❌ Not found.")
            return
        groups.remove(gid)
        save_groups(groups)
        await update.message.reply_text("✅ Group removed.")
    except ValueError:
        await update.message.reply_text("❌ Invalid chat ID.")

async def reload_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Unauthorized!")
        return
    await _restart_all_workers()
    await update.message.reply_text(
        f"✅ Reloaded — REST: {len(API_PANELS)}, IVAS: {len(load_ivas())}, Groups: {len(load_groups())}")

async def do_broadcast(bot, message: str, keyboard=None) -> dict:
    """Send message to ALL users (tg_users + GN_DATA). Returns stats dict."""
    user_ids = get_broadcast_user_ids()
    success = 0
    fail = 0
    for uid in user_ids:
        try:
            await bot.send_message(
                chat_id=uid, text=message,
                parse_mode="HTML", reply_markup=keyboard)
            success += 1
            await asyncio.sleep(0.05)  # avoid flood
        except Exception:
            fail += 1
    return {"total": len(user_ids), "success": success, "fail": fail}

async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Unauthorized!")
        return
    if not context.args:
        await update.message.reply_text("Usage: /broadcast <message>")
        return
    wait = await update.message.reply_text("📢 Broadcasting...")
    stats = await do_broadcast(context.bot, " ".join(context.args))
    await wait.edit_text(
        f"📢 <b>BROADCAST COMPLETE</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👥 Total Users: <code>{stats['total']}</code>\n"
        f"✅ Success: <code>{stats['success']}</code>\n"
        f"❌ Failed: <code>{stats['fail']}</code>",
        parse_mode="HTML")

# ═══════════════════════════════════════════════════════════════
#  INTERNAL HELPERS
# ═══════════════════════════════════════════════════════════════
def _build_status() -> str:
    uptime = str(datetime.now() - datetime.fromtimestamp(STATS['start_time'])).split('.')[0]
    config = load_config()
    fwd_st = "✅ ON" if config.get("otp_forward", True) else "❌ OFF"
    panels = load_panels()
    ivas   = load_ivas()
    plines = "\n".join([
        f"  {'🟢' if (p in REST_TASKS and not REST_TASKS[p].done()) else '🔴'} "
        f"{p} (hits:{STATS['panel_hits'].get(p,0)})"
        for p in panels]) or "  None"
    ilines = "\n".join([
        f"  {'🟢' if (n in IVAS_TASKS and not IVAS_TASKS[n].done()) else '🔴'} "
        f"{n} (hits:{STATS['ivas_hits'].get(n,0)})"
        for n in ivas]) or "  None"
    return (
        f"🖥 <b>BOT STATUS</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
        f"⏱ Uptime: <code>{uptime}</code>\n"
        f"📊 OTPs Sent: <code>{STATS['otps_sent']}</code>\n"
        f"❌ Errors: <code>{STATS['errors']}</code>\n"
        f"📤 Forward: {fwd_st} | Groups: {len(load_groups())}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📡 <b>REST Panels:</b>\n{plines}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🔌 <b>IVAS Accounts:</b>\n{ilines}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━"
    )

async def _restart_all_workers():
    global API_PANELS
    API_PANELS = load_panels()
    for panel in list(REST_TASKS.keys()):
        REST_TASKS[panel].cancel()
        del REST_TASKS[panel]
    for panel in API_PANELS:
        task = asyncio.create_task(api_worker(panel), name=f"REST-{panel}")
        task.add_done_callback(handle_task_exception)
        REST_TASKS[panel] = task
    for name in list(IVAS_TASKS.keys()):
        IVAS_TASKS[name].cancel()
        del IVAS_TASKS[name]
    for name in load_ivas():
        task = asyncio.create_task(ivas_worker(name), name=f"IVAS-{name}")
        task.add_done_callback(handle_task_exception)
        IVAS_TASKS[name] = task

# ═══════════════════════════════════════════════════════════════
#  CALLBACK QUERY HANDLER
# ═══════════════════════════════════════════════════════════════
async def callback_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global API_PANELS
    query = update.callback_query
    uid  = query.from_user.id
    data = query.data

    # ── GN Feature Callbacks (from main.go) ──────────────────
    if await gn_callback_handler(update, context):
        return

    await query.answer()

    if data == "noop":
        return

    # ── Public ────────────────────────────────────────────────
    if data.startswith("copy_"):
        # copy_text button handles native copy; this is fallback only
        await query.answer(f"OTP: {data[5:]}", show_alert=True)
        return

    if data == "show_help":
        await help_command(update, context)
        return

    if data == "public_stats":
        total, today, _ = db_user_stats()
        await query.edit_message_text(
            f"📊 <b>PUBLIC STATS</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Users: {total} | Active Today: {today}\n"
            f"OTPs in DB: {len(load_otp_store())}\n"
            f"Numbers: {db_total_numbers()}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━", parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","back_to_main")]]))
        return

    if data == "search_otp":
        await query.edit_message_text(
            "ℹ️ Use: <code>/otpfor [number]</code>", parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","back_to_main")]]))
        return

    if data == "user_profile":
        from html import escape
        user       = query.from_user
        first      = escape(user.first_name or "")
        last       = escape(user.last_name or "")
        username   = f"@{user.username}" if user.username else "N/A"
        uid_val    = user.id
        c_cur = db.cursor()
        c_cur.execute("SELECT first_seen, last_seen, total_commands FROM tg_users WHERE user_id=?",
                      (uid_val,))
        row    = c_cur.fetchone()
        joined = row[0][:10] if row else "Unknown"
        cmds   = row[2] if row else 0
        total_users, today_u, _ = db_user_stats()
        await query.edit_message_text(
            f"🫁 <b>YOUR PROFILE</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 <b>Name:</b> {first} {last}\n"
            f"🔖 <b>Username:</b> {username}\n"
            f"🆔 <b>User ID:</b> <code>{uid_val}</code>\n"
            f"📅 <b>Joined:</b> {joined}\n"
            f"📊 <b>Commands Used:</b> {cmds}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📦 <b>Numbers Available:</b> {db_total_numbers()}\n"
            f"👥 <b>Total Bot Users:</b> {total_users}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 𝗕𝗮𝗰𝗸", "back_to_main")]]))
        return

    if data == "back_to_main":
        from html import escape
        first = escape(query.from_user.first_name or "User")
        msg = (
            f"🚀 <b>Main Menu</b>\n"
            f"👆 Select an option below:"
        )
        await query.message.reply_text(msg, parse_mode="HTML",
                                       reply_markup=smart_kb(uid))
        return

    # check_join callback removed (force-join disabled)

    if data == "show_countries":
        rows = db_get_countries()
        if not rows:
            await query.edit_message_text("❌ No numbers available.",
                reply_markup=InlineKeyboardMarkup([[b("🔙 Back","back_to_main")]]))
            return
        await query.edit_message_text("🌍 <b>Select Country:</b>",
            parse_mode="HTML", reply_markup=get_countries_keyboard())
        return

    if data.startswith("nb_get|"):
        country = data.split("|", 1)[1]
        phones  = db_pop_numbers(country, 3)
        if phones:
            remaining = db_get_countries()
            rem_count = next((n for c, n in remaining if c == country), 0)

            db_assign_numbers(uid, phones)

            num_lines = ""
            for i, ph in enumerate(phones, 1):
                num_lines += f"📱 <b>0{i}</b>  ›  <code>{ph}</code>\n"

            msg = (
                f"🌍 <b>YOUR NUMBERS</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"🌍 <b>Country:</b> {country}\n"
                f"📦 <b>Remaining:</b> {rem_count}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"{num_lines}"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"⏳ <b>Waiting for OTP...</b>\n"
                f"🔔 OTP will be sent here and in the group!"
            )
            await query.edit_message_text(
                msg,
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([
                    [b("🔄 Get 3 More Numbers", f"nb_get|{country}"),
                     b("🌍 Change Country",      "show_countries")],
                    [b("📢 OTP Group", url="https://t.me/junaidniz110")],
                    [b("🔙 Back",               "back_to_main")],
                ]))
        else:
            await query.answer("❌ Out of stock!", show_alert=True)
        return

    # ── Admin gate ────────────────────────────────────────────
    if not is_admin(uid):
        await query.edit_message_text("❌ Unauthorized!")
        return

    # ── Admin nav ─────────────────────────────────────────────
    if data in ("back_to_admin", "refresh_admin"):
        await query.message.reply_text(
            f'<tg-emoji emoji-id="6205965994528086727">💠</tg-emoji> <b>ADMIN PANEL</b>\n'
            f'━━━━━━━━━━━━━━━━━━━━━━\n'
            f'<tg-emoji emoji-id="6235572922086331108">🧑‍💻</tg-emoji> Select an option:',
            parse_mode="HTML", reply_markup=get_admin_keyboard(uid))
        return

    if data == "close_admin":
        await query.delete_message()
        return

    # ══ NUMBERS — Full GN System from main.go ════════════════
    if data == "menu_numbers":
        if not has_perm(uid,"numbers"): await query.answer("❌ No permission.",show_alert=True); return
        grand = sum(len(c.get("numbers",[])) for svc in GN_DATA["services"].values() for c in svc.get("countries",{}).values())
        svc_count = len(GN_DATA["services"])
        user_count = len(GN_DATA["users"])
        await query.edit_message_text(
            f'<tg-emoji emoji-id="5296369303661067030">📲</tg-emoji> <b>NUMBER MANAGER</b>\n'
            f'━━━━━━━━━━━━━━━━━━━━━━\n'
            f'<tg-emoji emoji-id="5343862721307748990">📊</tg-emoji> Services: <b>{svc_count}</b>\n'
            f'<tg-emoji emoji-id="5312310156384557787">📱</tg-emoji> Total Numbers: <b>{grand}</b>\n'
            f'<tg-emoji emoji-id="4958832114540741368">👥</tg-emoji> Total Users: <b>{user_count}</b>',
            parse_mode="HTML", reply_markup=get_numbers_menu())
        return

    if data == "nb_add_numbers":
        if not has_perm(uid,"numbers"): await query.answer("❌ No permission.",show_alert=True); return
        GN_WIZARD_STATES[uid] = {"step": "svc", "staged": []}
        await query.edit_message_text(
            f'{gn_icon("addnum")} <b>Step 1/7 — Service Name</b>\n\n'
            f'Enter service name:\n<i>Example: TikTok, WhatsApp, Instagram</i>',
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[bc("𝗖𝗮𝗻𝗰𝗲𝗹",cb="menu_numbers",style="danger",icon="5974083768233760323")]]))
        return

    if data == "nb_list_services":
        if not has_perm(uid,"numbers"): await query.answer("❌ No permission.",show_alert=True); return
        txt = f'<tg-emoji emoji-id="5197219609970758159">📋</tg-emoji> <b>Services</b>\n\n'
        if not GN_DATA["services"]: txt += "No services yet."
        for sn, svc in GN_DATA["services"].items():
            em = gn_svc_emoji(sn); txt += f"{em} <b>{sn}</b>\n"
            for cn, c in svc.get("countries",{}).items():
                flag = gn_flag(c.get("code",""))
                txt += f"  {flag} {cn} — {c.get('price',0):.0f}{GN_CURRENCY} — {len(c.get('numbers',[]))} nums\n"
        await query.edit_message_text(txt[:4000], parse_mode="HTML", reply_markup=get_numbers_menu())
        return

    if data == "nb_system_stats":
        if not has_perm(uid,"numbers"): await query.answer("❌ No permission.",show_alert=True); return
        grand = 0
        txt = f'<tg-emoji emoji-id="5225414461080685066">📊</tg-emoji> <b>System Statistics</b>\n\n'
        for sn, svc in GN_DATA["services"].items():
            em = gn_svc_emoji(sn); txt += f"{em} <b>{sn}</b>\n"
            for cn, c in svc.get("countries",{}).items():
                flag = gn_flag(c.get("code",""))
                n = len(c.get("numbers",[])); grand += n
                st = "❌ Out" if n==0 else ("⚠️ Low" if n<5 else "✅ OK")
                txt += f"  {flag} {cn} — {c.get('price',0):.0f}{GN_CURRENCY} — {n} — {st}\n"
            txt += "\n"
        ty = sum(u.get("today_otps",0) for u in GN_DATA["users"].values())
        ta = sum(u.get("total_otps",0) for u in GN_DATA["users"].values())
        txt += (f'━━━━━━━━━━━━━━━━━━━━━━\n'
                f'<tg-emoji emoji-id="5312310156384557787">📱</tg-emoji> Total Numbers: <b>{grand}</b>\n'
                f'<tg-emoji emoji-id="4958832114540741368">👥</tg-emoji> Total Users: <b>{len(GN_DATA["users"])}</b>\n'
                f'<tg-emoji emoji-id="6176966310920983412">🔑</tg-emoji> Total OTPs: <b>{ta}</b>\n'
                f'<tg-emoji emoji-id="6206508629286196237">🔔</tg-emoji> Today OTPs: <b>{ty}</b>')
        await query.edit_message_text(txt[:4000], parse_mode="HTML", reply_markup=get_numbers_menu())
        return

    if data == "nb_total_users":
        if not has_perm(uid,"numbers"): await query.answer("❌ No permission.",show_alert=True); return
        _cu = db.cursor(); _cu.execute("SELECT COUNT(*) FROM tg_users"); total = _cu.fetchone()[0]
        lines = ["Username,UserID,TotalOTPs,TodayOTPs,Balance,JoinedAt"]
        for u in GN_DATA["users"].values():
            lines.append(f"{u.get('username','')},{u.get('id','')},{u.get('total_otps',0)},"
                         f"{u.get('today_otps',0)},{u.get('balance',0.0):.2f},{u.get('joined_at','')}")
        fname = f"/tmp/gn_users_{int(time.time())}.csv"
        with open(fname,"w") as f_: f_.write("\n".join(lines))
        await context.bot.send_document(chat_id=chat, document=open(fname,"rb"),
            caption=f'✅ Users Export — {total} users')
        import os as _os; _os.remove(fname)
        await query.answer("✅ Exported!")
        return

    if data == "nb_remove_svc":
        if not has_perm(uid,"numbers"): await query.answer("❌ No permission.",show_alert=True); return
        rows = [[bc(f"{sn}", cb=f"nb_do_rmsvc:{sn}", style="danger", icon="5445267414562389170")]
                for sn in GN_DATA["services"]]
        if not rows: rows = [[bc("❌ No Services", cb="noop", style="danger")]]
        rows.append([bc("𝗕𝗮𝗰𝗸", cb="menu_numbers", style="primary", icon="5255703720078879038")])
        await query.edit_message_text(
            f'<tg-emoji emoji-id="5445267414562389170">🗑</tg-emoji> <b>Select Service to Remove:</b>',
            parse_mode="HTML", reply_markup=InlineKeyboardMarkup(rows))
        return

    if data.startswith("nb_do_rmsvc:"):
        if not has_perm(uid,"numbers"): return
        sn = data[12:]; GN_DATA["services"].pop(sn,None); gn_save()
        await query.edit_message_text(
            f'<tg-emoji emoji-id="6206479140040743133">✅</tg-emoji> Service <b>{sn}</b> removed.',
            parse_mode="HTML", reply_markup=get_numbers_menu())
        return

    if data == "nb_remove_cnt":
        if not has_perm(uid,"numbers"): await query.answer("❌ No permission.",show_alert=True); return
        rows = []
        for sn, svc in GN_DATA["services"].items():
            for cn in svc.get("countries",{}):
                rows.append([bc(f"{sn} → {cn}", cb=f"nb_do_rmcnt:{sn}:{cn}", style="danger", icon="5445267414562389170")])
        if not rows: rows = [[bc("❌ No Countries", cb="noop", style="danger")]]
        rows.append([bc("𝗕𝗮𝗰𝗸", cb="menu_numbers", style="primary", icon="5255703720078879038")])
        await query.edit_message_text(
            f'<tg-emoji emoji-id="5445267414562389170">🗑</tg-emoji> <b>Select Country to Remove:</b>',
            parse_mode="HTML", reply_markup=InlineKeyboardMarkup(rows))
        return

    if data.startswith("nb_do_rmcnt:"):
        if not has_perm(uid,"numbers"): return
        parts = data[12:].split(":",1)
        if len(parts)==2:
            sn,cn=parts
            if sn in GN_DATA["services"]: GN_DATA["services"][sn].get("countries",{}).pop(cn,None); gn_save()
        await query.edit_message_text(
            f'<tg-emoji emoji-id="6206479140040743133">✅</tg-emoji> Country removed.',
            parse_mode="HTML", reply_markup=get_numbers_menu())
        return

    if data == "nb_add_balance":
        if not has_perm(uid,"numbers"): await query.answer("❌ No permission.",show_alert=True); return
        GN_WIZARD_STATES[uid] = {"step":"bal_uid"}
        await query.edit_message_text(
            f'<tg-emoji emoji-id="6190336264940559752">💰</tg-emoji> Enter User ID to add balance:',
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[bc("𝗖𝗮𝗻𝗰𝗲𝗹",cb="menu_numbers",style="danger",icon="5974083768233760323")]]))
        return

    if data == "nb_withdrawals":
        if not has_perm(uid,"numbers"): await query.answer("❌ No permission.",show_alert=True); return
        pending = [w for w in GN_DATA.get("withdrawals",{}).values() if w.get("status")=="pending"]
        if not pending:
            await query.edit_message_text(
                f'<tg-emoji emoji-id="6206155797722830770">💵</tg-emoji> <b>No pending withdrawals.</b>',
                parse_mode="HTML", reply_markup=get_numbers_menu()); return
        for req in pending[:10]:
            meth = req.get("method","pkr")
            amt_str = (f"{req.get('amount',0):.2f} {GN_CURRENCY}" if meth=="pkr" else f"{req.get('amount_usd',0):.4f} $")
            txt = (f'<tg-emoji emoji-id="6206155797722830770">💵</tg-emoji> <b>Withdrawal Request</b>\n\n'
                   f'👤 {req.get("first_name","")} (@{req.get("username","")})\n'
                   f'🆔 <code>{req.get("user_id","")}</code>\n'
                   f'💰 {amt_str}\n💳 <code>{req.get("details","")}</code>\n'
                   f'🕐 {req.get("created_at","")}')
            kb = InlineKeyboardMarkup([[
                bc("𝗔𝗽𝗽𝗿𝗼𝘃𝗲",cb=f"gnadm_wd_ok:{req['id']}",style="success",icon="6206479140040743133"),
                bc("𝗥𝗲𝗷𝗲𝗰𝘁",  cb=f"gnadm_wd_rej:{req['id']}",style="danger", icon="5974083768233760323")]])
            await context.bot.send_message(chat_id=chat,text=txt,parse_mode="HTML",reply_markup=kb)
        await query.answer()
        return

    if data == "nb_user_info":
        if not has_perm(uid,"numbers"): await query.answer("❌ No permission.",show_alert=True); return
        GN_WIZARD_STATES[uid] = {"step":"user_info"}
        await query.edit_message_text(
            f'<tg-emoji emoji-id="5242442819573927209">👤</tg-emoji> <b>User Info</b>\n\nEnter Telegram User ID:',
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[bc("𝗖𝗮𝗻𝗰𝗲𝗹",cb="menu_numbers",style="danger",icon="5974083768233760323")]]))
        return

    if data == "nb_toggle_wd":
        if not has_perm(uid,"numbers"): await query.answer("❌ No permission.",show_alert=True); return
        cur = GN_DATA.get("withdraw_enabled",True)
        GN_DATA["withdraw_enabled"] = not cur; gn_save()
        status = "✅ ENABLED" if not cur else "❌ DISABLED"
        await query.edit_message_text(
            f'<tg-emoji emoji-id="6206155797722830770">💵</tg-emoji> Withdrawals: <b>{status}</b>',
            parse_mode="HTML", reply_markup=get_numbers_menu())
        return

    if data == "nb_min_wd":
        if not has_perm(uid,"numbers"): await query.answer("❌ No permission.",show_alert=True); return
        minw = GN_DATA.get("min_withdrawal", GN_MIN_WITHDRAW)
        minu = GN_DATA.get("min_withdrawal_usd", GN_MIN_USD)
        rate = GN_DATA.get("usd_to_pkr", GN_USD_RATE)
        GN_WIZARD_STATES[uid] = {"step": "minwd"}
        await query.edit_message_text(
            f'<tg-emoji emoji-id="6206155797722830770">💵</tg-emoji> <b>Set Minimum Withdrawal</b>\n\n'
            f'Current values:\n'
            f'  💵 PKR minimum: <b>{minw:.0f} {GN_CURRENCY}</b>\n'
            f'  💲 USDT minimum: <b>{minu:.4f} $</b>\n'
            f'  📈 Rate: <b>1 USDT = {rate:.0f} {GN_CURRENCY}</b>\n\n'
            f'Send new values in this format (all optional):\n'
            f'<code>PKR:500 USDT:0.5 RATE:280</code>\n\n'
            f'<i>Example to only change PKR min: <code>PKR:200</code></i>',
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[bc("𝗖𝗮𝗻𝗰𝗲𝗹", cb="menu_numbers", style="danger", icon="5974083768233760323")]]))
        return

    if data == "nb_broadcast":
        if not has_perm(uid,"broadcast"): await query.answer("❌ No permission.",show_alert=True); return
        GN_BCAST_STATES[uid] = {"step":"await"}
        await query.edit_message_text(
            f'<tg-emoji emoji-id="6206080502651164081">📣</tg-emoji> <b>Broadcast Message</b>\n\n'
            f'Write here what you want to broadcast to users\n\n'
            f'You can send: Text, Image 🖼, Video 🎬, or Voice Note 🎤\n\n'
            f'<i>Supports premium emojis, bold, italic, code formatting</i>',
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[bc("𝗖𝗮𝗻𝗰𝗲𝗹",cb="nb_cancel_bcast",style="danger",icon="5974083768233760323")]]))
        return

    if data == "nb_cancel_bcast":
        GN_BCAST_STATES.pop(uid,None)
        await query.edit_message_text(
            f'<tg-emoji emoji-id="5974083768233760323">❌</tg-emoji> Broadcast cancelled.',
            parse_mode="HTML", reply_markup=get_numbers_menu())
        return

    if data == "nb_do_broadcast":
        state = GN_BCAST_STATES.pop(uid, None)
        logger.info(f"[broadcast] nb_do_broadcast clicked uid={uid} state_found={state is not None}")
        if not state or "payload" not in state:
            logger.warning(f"[broadcast] ⚠️ no pending state for uid={uid}")
            await query.edit_message_text("❌ No pending broadcast.", parse_mode="HTML"); return
        logger.info(f"[broadcast] payload={state['payload']}")
        await query.edit_message_text("📣 Sending broadcast to all users…", parse_mode="HTML")
        asyncio.create_task(nb_run_broadcast(context.bot, update.effective_chat.id, state["payload"]))
        logger.info(f"[broadcast] ✅ task created for uid={uid}")
        return

    # ══ FILE MANAGER ══════════════════════════════════════════
    if data == "menu_files":
        if not has_perm(uid,"files"): await query.answer("❌ No permission.",show_alert=True); return
        flist = []

        for f in [LOG_FILE, OTP_FILE, DB_FILE, PANEL_FILE, IVAS_FILE,
                  CONFIG_FILE, ADMINS_FILE, GROUP_FILE]:
            if os.path.exists(f):
                flist.append(f"{f} — {os.path.getsize(f):,}b")
        await query.edit_message_text(
            f"📂 <b>FILE MANAGER</b>\n━━━━━━━━━━━━━━━━━━━━━━\n<code>"
            + "\n".join(flist) + "</code>",
            parse_mode="HTML", reply_markup=get_files_menu())
        return

    if data == "fm_list":
        flist = []
        for f in [LOG_FILE, OTP_FILE, DB_FILE, PANEL_FILE, IVAS_FILE,
                  CONFIG_FILE, ADMINS_FILE, GROUP_FILE]:
            if os.path.exists(f):
                flist.append(f"{f} ({os.path.getsize(f):,}b)")
        await query.edit_message_text(
            "📂 <b>FILES:</b>\n<code>" + "\n".join(flist) + "</code>",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_files")]]))
        return

    for file_data, file_path, caption in [
        ("fm_download_log", LOG_FILE, "📋 Bot Log"),
        ("fm_download_otp", OTP_FILE, "🗄 OTP Store"),
        ("fm_download_db",  DB_FILE,  "🗄 SQLite DB"),
    ]:
        if data == file_data:
            if not os.path.exists(file_path):
                await query.answer("File not found", show_alert=True)
                return
            async with Bot(token=BOT_TOKEN) as bot_inst:
                await bot_inst.send_document(chat_id=query.message.chat_id,
                    document=open(file_path, "rb"), caption=caption)
            await query.answer("✅ Sent", show_alert=True)
            return

    if data == "fm_clear_log":
        await query.edit_message_text("🗑️ Clear the bot log file?",
            reply_markup=get_confirmation_keyboard("clear_log"))
        return

    if data == "confirm_clear_log":
        open(LOG_FILE, "w").close()
        await query.edit_message_text("✅ Log cleared.",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_files")]]))
        return

    # ══ PANEL MANAGER ═════════════════════════════════════════
    if data == "menu_panels":
        if not has_perm(uid,"panels"): await query.answer("❌ No permission.",show_alert=True); return
        await query.edit_message_text(
            "📡 <b>PANEL MANAGER</b>\n━━━━━━━━━━━━━━━━━━━━━━\nSelect option:",
            parse_mode="HTML", reply_markup=get_panels_menu())
        return

    if data == "list_panels":
        panels = load_panels()
        text   = "📋 <b>REST PANELS</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
        for name, pd in panels.items():
            active = (name in REST_TASKS and not REST_TASKS[name].done())
            hits   = STATS["panel_hits"].get(name, 0)
            st     = "🟢" if active else "🔴"
            text  += f"\n{st} <b>{name}</b>\n   {pd['url'][:50]}\n   Hits: {hits}\n"
        await query.edit_message_text(text or "No panels.", parse_mode="HTML",
            reply_markup=get_panels_keyboard("view"))
        return

    if data == "add_panel":
        PANEL_ADD_STATES[uid] = {"step":"name","data":{},"timestamp":time.time()}
        await query.edit_message_text(
            "➕ <b>ADD REST PANEL</b>\n━━━━━━━━━━━━━━━━━━━━━━\nStep 1: Panel name:",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("❌ Cancel","cancel_action")]]))
        return

    if data == "remove_panel":
        await query.edit_message_text("🗑️ <b>SELECT PANEL TO REMOVE:</b>",
            parse_mode="HTML", reply_markup=get_panels_keyboard("remove"))
        return

    if data.startswith("view_panel_"):
        panel  = data.replace("view_panel_", "")
        panels = load_panels()
        if panel not in panels:
            await query.answer("Not found", show_alert=True)
            return
        pd     = panels[panel]
        active = (panel in REST_TASKS and not REST_TASKS[panel].done())
        await query.edit_message_text(
            f"{'🟢' if active else '🔴'} <b>{panel.upper()}</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
            f"URL: <code>{pd['url']}</code>\n"
            f"Token: <code>{pd['token'][:30]}...</code>\n"
            f"Records: <code>{pd.get('records',20)}</code>\n"
            f"Hits: <code>{STATS['panel_hits'].get(panel,0)}</code>",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","list_panels")]]))
        return

    if data.startswith("remove_panel_"):
        panel = data.replace("remove_panel_", "")
        await query.edit_message_text(f"🟡 Remove panel <b>{panel}</b>?", parse_mode="HTML",
            reply_markup=get_confirmation_keyboard("remove_panel", panel))
        return

    if data.startswith("confirm_remove_panel_"):
        panel  = data.replace("confirm_remove_panel_", "")
        panels = load_panels()
        if panel in panels:
            del panels[panel]
            save_panels(panels)
            API_PANELS = panels
        if panel in REST_TASKS:
            REST_TASKS[panel].cancel()
            del REST_TASKS[panel]
        await query.edit_message_text(f"✅ Panel <b>{panel}</b> removed.", parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_panels")]]))
        return

    if data == "confirm_add_panel":
        if uid not in PANEL_ADD_STATES or PANEL_ADD_STATES[uid]["step"] != "confirm":
            await query.edit_message_text("❌ No pending panel.")
            return
        pd = PANEL_ADD_STATES[uid]["data"]
        API_PANELS[pd["name"]] = {"url":pd["url"],"token":pd["token"],
                                   "records":pd.get("records",20)}
        save_panels(API_PANELS)
        task = asyncio.create_task(api_worker(pd["name"]), name=f"REST-{pd['name']}")
        task.add_done_callback(handle_task_exception)
        REST_TASKS[pd["name"]] = task
        del PANEL_ADD_STATES[uid]
        await query.edit_message_text(f"✅ Panel <b>{pd['name']}</b> added and started!",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_panels")]]))
        return

    if data == "panel_fetch_all":
        wait    = await context.bot.send_message(chat_id=query.message.chat_id, text="🔄 Fetching...")
        results = fetch_all_panels(limit=3)
        if not results:
            await wait.edit_text("❌ Nothing fetched.")
            return
        text = f"📨 <b>FETCHED {len(results)}</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
        for r in results[:8]:
            otp  = extract_otp(r["message"]) or "N/A"
            text += (f"📡 <b>{r['panel']}</b> | {r['service']}\n"
                     f"📞 <code>{r['number']}</code>  🔑 <code>{otp}</code>\n"
                     f"💬 {r['message'][:60]}\n──────────────────────\n")
        await wait.edit_text(text[:4000], parse_mode="HTML")
        return

    # ══ IVAS MANAGER ══════════════════════════════════════════
    if data == "menu_ivas":
        if not has_perm(uid,"ivas"): await query.answer("❌ No permission.",show_alert=True); return
        await query.edit_message_text(
            "🔌 <b>IVAS MANAGER</b>\n━━━━━━━━━━━━━━━━━━━━━━\nSelect option:",
            parse_mode="HTML", reply_markup=get_ivas_menu())
        return

    if data == "list_ivas":
        accounts = load_ivas()
        if not accounts:
            await query.edit_message_text("🟡 No IVAS accounts yet.",
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([
                    [b("➕ Add IVAS","add_ivas")],
                    [b("🔙 Back","menu_ivas")]]))
            return
        text = "🔌 <b>IVAS ACCOUNTS</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
        for name in accounts:
            active = (name in IVAS_TASKS and not IVAS_TASKS[name].done())
            hits   = STATS["ivas_hits"].get(name, 0)
            st     = "🟢" if active else "🔴"
            text  += f"\n{st} <b>{name}</b> (hits:{hits})\n"
        await query.edit_message_text(text, parse_mode="HTML",
            reply_markup=get_ivas_keyboard("view"))
        return

    if data == "add_ivas":
        IVAS_ADD_STATES[uid] = {"step":"name","data":{},"timestamp":time.time()}
        await query.edit_message_text(
            "🔌 <b>ADD IVAS</b>\n━━━━━━━━━━━━━━━━━━━━━━\nStep 1: Account name:",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("❌ Cancel","cancel_action")]]))
        return

    if data == "remove_ivas":
        await query.edit_message_text("🗑️ <b>SELECT IVAS TO REMOVE:</b>",
            parse_mode="HTML", reply_markup=get_ivas_keyboard("remove"))
        return

    if data == "ivas_restart_all":
        for name in list(IVAS_TASKS.keys()):
            IVAS_TASKS[name].cancel()
            del IVAS_TASKS[name]
        for name in load_ivas():
            task = asyncio.create_task(ivas_worker(name), name=f"IVAS-{name}")
            task.add_done_callback(handle_task_exception)
            IVAS_TASKS[name] = task
        await query.edit_message_text("✅ All IVAS workers restarted.",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_ivas")]]))
        return

    if data.startswith("view_ivas_"):
        name     = data.replace("view_ivas_", "")
        accounts = load_ivas()
        if name not in accounts:
            await query.answer("Not found", show_alert=True)
            return
        active = (name in IVAS_TASKS and not IVAS_TASKS[name].done())
        hits   = STATS["ivas_hits"].get(name, 0)
        uri    = accounts[name].get("uri", "N/A")
        await query.edit_message_text(
            f"{'🟢' if active else '🔴'} <b>IVAS: {name.upper()}</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Status: {'Running' if active else 'Stopped'}\n"
            f"Hits: <code>{hits}</code>\n"
            f"URI: <code>{uri[:80]}...</code>",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","list_ivas")]]))
        return

    if data.startswith("remove_ivas_"):
        name = data.replace("remove_ivas_", "")
        await query.edit_message_text(f"🟡 Remove IVAS <b>{name}</b>?", parse_mode="HTML",
            reply_markup=get_confirmation_keyboard("remove_ivas", name))
        return

    if data.startswith("confirm_remove_ivas_"):
        name     = data.replace("confirm_remove_ivas_", "")
        accounts = load_ivas()
        if name in accounts:
            del accounts[name]
            save_ivas(accounts)
        if name in IVAS_TASKS:
            IVAS_TASKS[name].cancel()
            del IVAS_TASKS[name]
        await query.edit_message_text(f"✅ IVAS <b>{name}</b> removed.", parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_ivas")]]))
        return

    if data == "confirm_add_ivas":
        if uid not in IVAS_ADD_STATES or IVAS_ADD_STATES[uid]["step"] != "confirm":
            await query.edit_message_text("❌ No pending IVAS.")
            return
        pd       = IVAS_ADD_STATES[uid]["data"]
        accounts = load_ivas()
        accounts[pd["name"]] = {"uri": pd["uri"]}
        save_ivas(accounts)
        task = asyncio.create_task(ivas_worker(pd["name"]), name=f"IVAS-{pd['name']}")
        task.add_done_callback(handle_task_exception)
        IVAS_TASKS[pd["name"]] = task
        del IVAS_ADD_STATES[uid]
        await query.edit_message_text(f"✅ IVAS <b>{pd['name']}</b> added!",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_ivas")]]))
        return

    # ══ FETCH SMS ══════════════════════════════════════════════
    if data == "menu_fetch":
        if not has_perm(uid,"fetch_sms"): await query.answer("❌ No permission.",show_alert=True); return
        await query.edit_message_text(
            "🔄 <b>FETCH SMS</b>\n━━━━━━━━━━━━━━━━━━━━━━\nSelect method:",
            parse_mode="HTML", reply_markup=get_fetch_menu())
        return

    if data == "fetch_all_now":
        wait    = await context.bot.send_message(chat_id=query.message.chat_id, text="🔄 Fetching...")
        results = fetch_all_panels(limit=5)
        if not results:
            await wait.edit_text("❌ Nothing fetched.")
            return
        text = f"📨 <b>LATEST SMS ({len(results)})</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
        for r in results[:10]:
            otp  = extract_otp(r["message"]) or "N/A"
            text += (f"📡 <b>{r['panel']}</b> | {r['service']}\n"
                     f"📞 <code>{r['number']}</code>\n"
                     f"🔑 OTP: <code>{otp}</code>\n"
                     f"💬 {r['message'][:80]}\n──────────────────────\n")
        await wait.edit_text(text[:4000], parse_mode="HTML")
        return

    if data == "fetch_by_number":
        FETCH_STATES[uid] = {"step":"waiting_number","timestamp":time.time()}
        await query.edit_message_text(
            "🔍 <b>FETCH BY NUMBER</b>\n━━━━━━━━━━━━━━━━━━━━━━\nSend the phone number:",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("❌ Cancel","cancel_action")]]))
        return

    if data == "fetch_single_panel":
        panels = load_panels()
        kb     = [[b(name.upper(), f"fetch_panel_{name}")] for name in panels]
        kb.append([b("🔙 Back","menu_fetch")])
        await query.edit_message_text("📡 <b>SELECT PANEL:</b>",
            parse_mode="HTML", reply_markup=InlineKeyboardMarkup(kb))
        return

    if data.startswith("fetch_panel_"):
        panel  = data.replace("fetch_panel_", "")
        result = fetch_latest(panel)
        if result:
            otp = extract_otp(result["message"]) or "N/A"
            await query.edit_message_text(
                f"📡 <b>Panel: {panel}</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
                f"📞 <code>{result['number']}</code>\n"
                f"🔑 OTP: <code>{otp}</code>\n"
                f"📱 Service: {result['service']}\n"
                f"💬 {result['message'][:200]}\n"
                f"⏱ {result['time']}",
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_fetch")]]))
        else:
            await query.edit_message_text(f"❌ No data from <b>{panel}</b>.", parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_fetch")]]))
        return

    # ══ OTP HISTORY ═══════════════════════════════════════════
    if data == "menu_otp_history":
        if not has_perm(uid,"otp_history"): await query.answer("❌ No permission.",show_alert=True); return
        last    = db_get_otp_history(5)
        preview = "".join([f"📞 <code>{r[0]}</code> 🔑 <code>{r[2]}</code> {r[3]}\n"
                           for r in last]) or "No history yet"
        await query.edit_message_text(
            f"📋 <b>OTP HISTORY</b>\n━━━━━━━━━━━━━━━━━━━━━━\n{preview}",
            parse_mode="HTML", reply_markup=get_otp_history_menu())
        return

    if data in ("otp_hist_10","otp_hist_20"):
        limit = 10 if data == "otp_hist_10" else 20
        rows  = db_get_otp_history(limit)
        if not rows:
            await query.answer("No history", show_alert=True)
            return
        text = f"📋 <b>LAST {limit} OTPs</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
        for row in rows:
            text += (f"📞 <code>{row[0]}</code> | <b>{row[1]}</b>\n"
                     f"🔑 <code>{row[2]}</code> | {row[3]} | {row[4]}\n──────────\n")
        await query.edit_message_text(text[:4000], parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_otp_history")]]))
        return

    if data == "otp_export_hist":
        rows = db_get_otp_history(9999)
        if not rows:
            await query.answer("No history", show_alert=True)
            return
        fname = f"otp_history_{int(time.time())}.csv"
        with open(fname, "w") as f:
            f.write("number,service,otp,source,time\n")
            for row in rows:
                f.write(",".join(str(x) for x in row) + "\n")
        async with Bot(token=BOT_TOKEN) as bot_inst:
            await bot_inst.send_document(chat_id=query.message.chat_id,
                document=open(fname,"rb"),
                caption=f"📤 OTP History — {len(rows)} records")
        os.remove(fname)
        await query.answer("✅ Exported", show_alert=True)
        return

    if data == "otp_search_num":
        FETCH_STATES[uid] = {"step":"waiting_number","timestamp":time.time()}
        await query.edit_message_text(
            "🔍 <b>SEARCH OTP BY NUMBER</b>\n━━━━━━━━━━━━━━━━━━━━━━\nSend the number:",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("❌ Cancel","cancel_action")]]))
        return

    if data == "otp_clear_hist":
        await query.edit_message_text("🗑️ Clear ALL OTP history?",
            reply_markup=get_confirmation_keyboard("otp_clear_hist"))
        return

    if data == "confirm_otp_clear_hist":
        db_clear_otp_history()
        await query.edit_message_text("✅ History cleared.",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_otp_history")]]))
        return

    # ══ GROUP MANAGER ═════════════════════════════════════════
    if data == "menu_groups":
        if not has_perm(uid,"groups"): await query.answer("❌ No permission.",show_alert=True); return
        groups = load_groups()
        config = load_config()
        lg     = config.get("log_group") or "Not set"
        await query.edit_message_text(
            f"👥 <b>GROUP MANAGER</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
            f"OTP Groups: <b>{len(groups)}</b>\n"
            f"Log Group: <code>{lg}</code>",
            parse_mode="HTML", reply_markup=get_groups_menu())
        return

    if data == "add_group_prompt":
        SETTING_STATES[uid] = {"step":"waiting_group_id","timestamp":time.time()}
        await query.edit_message_text(
            "➕ <b>ADD OTP GROUP</b>\n━━━━━━━━━━━━━━━━━━━━━━\nSend the group chat ID:",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("❌ Cancel","cancel_action")]]))
        return

    if data.startswith("del_group_"):
        try:
            gid    = int(data.replace("del_group_", ""))
            groups = load_groups()
            if gid in groups:
                groups.remove(gid)
                save_groups(groups)
            await query.edit_message_text(f"✅ Group <code>{gid}</code> removed.", parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_groups")]]))
        except:
            await query.answer("Error", show_alert=True)
        return

    if data in ("set_log_group","set_log_group_settings"):
        SETTING_STATES[uid] = {"step":"waiting_log_group","timestamp":time.time()}
        await query.edit_message_text(
            "📋 <b>SET LOG GROUP</b>\n━━━━━━━━━━━━━━━━━━━━━━\nSend log group chat ID:",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("❌ Cancel","cancel_action")]]))
        return

    if data == "clear_log_group":
        config = load_config()
        config["log_group"] = None
        save_config(config)
        await query.edit_message_text("✅ Log group cleared.",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_groups")]]))
        return

    # ══ STATS / STATUS ════════════════════════════════════════
    if data == "stats":
        if not has_perm(uid,"stats"): await query.answer("❌ No permission.",show_alert=True); return
        total, active_today, active_week = db_user_stats()
        uptime = str(datetime.now() - datetime.fromtimestamp(STATS['start_time'])).split('.')[0]
        await query.edit_message_text(
            f"📊 <b>BOT STATS</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
            f"⏱ Uptime: <code>{uptime}</code>\n"
            f"👤 Users: <code>{total}</code> | Today: <code>{active_today}</code>\n"
            f"📊 OTPs Sent: <code>{STATS['otps_sent']}</code>\n"
            f"🚫 Dropped: <code>{STATS['otps_dropped']}</code>\n"
            f"❌ Errors: <code>{STATS['errors']}</code>\n"
            f"📦 Numbers: <code>{db_total_numbers()}</code>\n"
            f"🗄 OTP Store: <code>{len(load_otp_store())}</code>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━", parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","back_to_admin")]]))
        return

    if data == "status":
        if not has_perm(uid,"stats"): await query.answer("❌ No permission.",show_alert=True); return
        await query.edit_message_text(_build_status(), parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","back_to_admin")]]))
        return

    # ══ BROADCAST ═════════════════════════════════════════════
    if data == "broadcast":
        if not has_perm(uid,"broadcast"): await query.answer("❌ No permission.",show_alert=True); return
        await query.edit_message_text("📢 <b>BROADCAST</b>\n━━━━━━━━━━━━━━━━━━━━━━\nChoose type:",
            parse_mode="HTML", reply_markup=get_broadcast_keyboard())
        return

    if data == "broadcast_text":
        BROADCAST_STATES[uid] = {"type":"text","step":"waiting_message","timestamp":time.time()}
        await query.edit_message_text("📢 Send your broadcast message:",
            reply_markup=InlineKeyboardMarkup([[b("❌ Cancel","cancel_action")]]))
        return

    if data == "broadcast_with_buttons":
        BROADCAST_STATES[uid] = {"type":"with_buttons","step":"waiting_message","timestamp":time.time()}
        await query.edit_message_text(
            "📢 Send text + buttons.\nFormat:\nYour message\n[Button Label|https://url]",
            reply_markup=InlineKeyboardMarkup([[b("❌ Cancel","cancel_action")]]))
        return

    if data == "confirm_broadcast":
        if uid not in BROADCAST_STATES or BROADCAST_STATES[uid]["step"] != "confirm":
            await query.edit_message_text("❌ No pending broadcast.")
            return
        msg_text = BROADCAST_STATES[uid]["message"]
        del BROADCAST_STATES[uid]
        await query.edit_message_text("📢 Broadcasting to all users...")
        stats = await do_broadcast(context.bot, msg_text)
        await query.edit_message_text(
            f"📢 <b>BROADCAST COMPLETE</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"👥 Total: <code>{stats['total']}</code>\n"
            f"✅ Success: <code>{stats['success']}</code>\n"
            f"❌ Failed: <code>{stats['fail']}</code>",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","back_to_admin")]]))
        return

    if data == "confirm_broadcast_buttons":
        if uid not in BROADCAST_STATES or BROADCAST_STATES[uid]["step"] != "confirm":
            await query.edit_message_text("❌ No pending broadcast.")
            return
        state   = BROADCAST_STATES[uid]
        buttons = state.get("buttons", [])
        kb      = InlineKeyboardMarkup([[btn_] for btn_ in buttons]) if buttons else None
        msg_text = state["message"]
        del BROADCAST_STATES[uid]
        await query.edit_message_text("📢 Broadcasting to all users...")
        stats = await do_broadcast(context.bot, msg_text, kb)
        await query.edit_message_text(
            f"📢 <b>BROADCAST COMPLETE</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"👥 Total Users: <code>{stats['total']}</code>\n"
            f"✅ Success: <code>{stats['success']}</code>\n"
            f"❌ Failed: <code>{stats['fail']}</code>",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","back_to_admin")]]))
        return

    # ══ SETTINGS ══════════════════════════════════════════════
    if data == "menu_settings":
        if not has_perm(uid,"settings"): await query.answer("❌ No permission.",show_alert=True); return
        await query.edit_message_text(
            "⚙️ <b>SETTINGS</b>\n━━━━━━━━━━━━━━━━━━━━━━\nSelect option:",
            parse_mode="HTML", reply_markup=get_settings_menu())
        return

    if data == "toggle_otp_forward":
        config = load_config()
        config["otp_forward"] = not config.get("otp_forward", True)
        save_config(config)
        st = "✅ ENABLED" if config["otp_forward"] else "❌ DISABLED"
        await query.edit_message_text(f"📤 OTP Forwarding: <b>{st}</b>", parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_settings")]]))
        return

    if data in ("set_forward_delay","set_channel","set_numberbot",
                "set_otp_group_link","set_log_group"):
        step_map = {
            "set_forward_delay": ("waiting_delay",    "⏱ SET FORWARD DELAY\nSend seconds (0-60):"),
            "set_channel":       ("waiting_channel",  "📢 SET CHANNEL LINK\nSend the URL:"),
            "set_numberbot":     ("waiting_numberbot","🤖 SET NUMBER BOT LINK\nSend the URL:"),
            "set_otp_group_link":("waiting_otp_link", "🔗 SET OTP GROUP LINK\nSend the URL:"),
            "set_log_group":     ("waiting_log_group","📋 SET LOG GROUP\nSend the chat ID:"),
        }
        step, prompt = step_map[data]
        SETTING_STATES[uid] = {"step": step, "timestamp": time.time()}
        await query.edit_message_text(
            f"⚙️ <b>{prompt}</b>", parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("❌ Cancel","cancel_action")]]))
        return

    if data == "menu_admin_manager":
        if not is_owner(uid):
            await query.answer("❌ Owner only!", show_alert=True)
            return
        staff = load_staff()
        await query.edit_message_text(
            f"👤 <b>STAFF MANAGER</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
            f"👑 Owners: <b>{len(OWNER_IDS)}</b>\n"
            f"🛡️ Staff Members: <b>{len(staff)}</b>\n\n"
            f"Tap a staff member to edit their permissions.\n"
            f"Each permission can be toggled ON/OFF individually.",
            parse_mode="HTML", reply_markup=get_admin_manager_keyboard())
        return

    if data == "add_staff_prompt":
        if not is_owner(uid):
            await query.answer("❌ Owner only!", show_alert=True)
            return
        SETTING_STATES[uid] = {"step": "waiting_staff_id", "timestamp": time.time()}
        await query.edit_message_text(
            "➕ <b>ADD STAFF MEMBER</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
            "Send the Telegram <b>User ID</b> of the new staff member:",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("❌ Cancel", "cancel_action")]]))
        return

    if data.startswith("edit_staff_"):
        if not is_owner(uid):
            await query.answer("❌ Owner only!", show_alert=True)
            return
        target_str = data.replace("edit_staff_", "")
        staff      = load_staff()
        info       = staff.get(target_str, {})
        name       = info.get("name", target_str)
        perms      = info.get("perms", [])
        perm_lines = "\n".join([
            f"  {'✅' if p in perms else '☑️'} {ALL_PERMISSIONS[p]}"
            for p in ALL_PERMISSIONS
        ])
        await query.edit_message_text(
            f"🛡️ <b>EDIT PERMISSIONS</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"User: <code>{target_str}</code> ({name})\n"
            f"Active Perms: <b>{len(perms)}/{len(ALL_PERMISSIONS)}</b>\n\n"
            f"{perm_lines}",
            parse_mode="HTML",
            reply_markup=get_staff_perms_keyboard(target_str))
        return

    if data.startswith("toggle_perm_"):
        if not is_owner(uid):
            await query.answer("❌ Owner only!", show_alert=True)
            return
        rest       = data.replace("toggle_perm_", "", 1)
        perm_key   = None
        target_str = None
        for pk in ALL_PERMISSIONS:
            if rest.endswith("_" + pk):
                perm_key   = pk
                target_str = rest[:-(len(pk)+1)]
                break
        if not perm_key or not target_str:
            await query.answer("Error parsing perm", show_alert=True)
            return
        staff = load_staff()
        if target_str not in staff:
            await query.answer("Staff not found", show_alert=True)
            return
        perms = staff[target_str].get("perms", [])
        if perm_key in perms:
            perms.remove(perm_key)
            action = "Removed"
        else:
            perms.append(perm_key)
            action = "Added"
        staff[target_str]["perms"] = perms
        save_staff(staff)
        await query.answer(f"{action}: {ALL_PERMISSIONS[perm_key]}", show_alert=False)
        info       = staff[target_str]
        name       = info.get("name", target_str)
        perm_lines = "\n".join([
            f"  {'✅' if p in perms else '☑️'} {ALL_PERMISSIONS[p]}"
            for p in ALL_PERMISSIONS
        ])
        await query.edit_message_text(
            f"🛡️ <b>EDIT PERMISSIONS</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"User: <code>{target_str}</code> ({name})\n"
            f"Active Perms: <b>{len(perms)}/{len(ALL_PERMISSIONS)}</b>\n\n"
            f"{perm_lines}",
            parse_mode="HTML",
            reply_markup=get_staff_perms_keyboard(target_str))
        return

    if data.startswith("grant_all_"):
        if not is_owner(uid):
            await query.answer("❌ Owner only!", show_alert=True)
            return
        target_str = data.replace("grant_all_", "")
        staff      = load_staff()
        if target_str in staff:
            staff[target_str]["perms"] = list(ALL_PERMISSIONS.keys())
            save_staff(staff)
        await query.answer("✅ All permissions granted", show_alert=True)
        await query.edit_message_text(
            f"✅ All permissions granted to <code>{target_str}</code>.",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back", "menu_admin_manager")]]))
        return

    if data.startswith("revoke_all_"):
        if not is_owner(uid):
            await query.answer("❌ Owner only!", show_alert=True)
            return
        target_str = data.replace("revoke_all_", "")
        staff      = load_staff()
        if target_str in staff:
            staff[target_str]["perms"] = []
            save_staff(staff)
        await query.answer("❌ All permissions revoked", show_alert=True)
        await query.edit_message_text(
            f"❌ All permissions revoked from <code>{target_str}</code>.",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back", "menu_admin_manager")]]))
        return

    if data.startswith("remove_staff_"):
        if not is_owner(uid):
            await query.answer("❌ Owner only!", show_alert=True)
            return
        target_str = data.replace("remove_staff_", "")
        try:
            target_int = int(target_str)
            if target_int in OWNER_IDS:
                await query.answer("❌ Cannot remove owner!", show_alert=True)
                return
            remove_staff(target_int)
            await query.edit_message_text(
                f"✅ Staff member <code>{target_str}</code> removed.",
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([[b("🔙 Back", "menu_admin_manager")]]))
        except:
            await query.answer("Error", show_alert=True)
        return

    # ══ ADVANCED ══════════════════════════════════════════════
    if data == "menu_advanced":
        if not has_perm(uid,"advanced"): await query.answer("❌ No permission.",show_alert=True); return
        await query.edit_message_text(
            "🔧 <b>ADVANCED TOOLS</b>\n━━━━━━━━━━━━━━━━━━━━━━\nSelect option:",
            parse_mode="HTML", reply_markup=get_advanced_keyboard())
        return

    if data == "restart_workers":
        await _restart_all_workers()
        await query.edit_message_text("✅ All workers restarted.",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_advanced")]]))
        return

    if data == "restart_bot":
        if not is_owner(uid):
            await query.answer("❌ Owner only!", show_alert=True)
            return
        await query.edit_message_text("🔁 Restarting bot...")
        await asyncio.sleep(1)
        os.execv(sys.executable, [sys.executable] + sys.argv)
        return

    if data in ("stop_forward","start_forward"):
        config = load_config()
        config["otp_forward"] = (data == "start_forward")
        save_config(config)
        st = "✅ ENABLED" if config["otp_forward"] else "❌ DISABLED"
        await query.edit_message_text(f"📤 OTP Forwarding: <b>{st}</b>", parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_advanced")]]))
        return

    if data == "reload_config":
        API_PANELS = load_panels()
        await query.edit_message_text("✅ Config reloaded from all JSON files.",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_advanced")]]))
        return

    if data == "clear_all_otps":
        await query.edit_message_text("🗑️ Delete ALL stored OTPs?",
            reply_markup=get_confirmation_keyboard("clear_all_otps"))
        return

    if data == "confirm_clear_all_otps":
        save_otp_store({})
        await query.edit_message_text("✅ OTP store cleared.",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_advanced")]]))
        return

    if data == "export_otps":
        store = load_otp_store()
        if not store:
            await query.answer("No OTPs to export", show_alert=True)
            return
        fname = f"otp_export_{int(time.time())}.json"
        with open(fname, "w") as f:
            json.dump(store, f, indent=4)
        async with Bot(token=BOT_TOKEN) as bot_inst:
            await bot_inst.send_document(chat_id=query.message.chat_id,
                document=open(fname,"rb"),
                caption=f"📤 OTP Store — {len(store)} entries")
        os.remove(fname)
        await query.answer("✅ Exported", show_alert=True)
        return

    if data == "view_logs":
        try:
            with open(LOG_FILE, "r") as f:
                lines = f.readlines()[-25:]
            log_text = "".join(lines)
            if len(log_text) > 3500:
                log_text = log_text[-3500:]
            await query.edit_message_text(
                f"<b>Last 25 log lines:</b>\n<pre>{log_text}</pre>",
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_advanced")]]))
        except Exception as e:
            await query.edit_message_text(f"Error reading logs: {e}")
        return

    if data in ("test_panels_menu","test_panels_adv"):
        panels = load_panels()
        if not panels:
            await query.edit_message_text("No panels configured.")
            return
        results = []
        for name in panels:
            try:
                d2 = fetch_latest(name)
                results.append(f"{'✅' if d2 else '❌'} {name}: {'Online' if d2 else 'Offline'}")
            except Exception as e:
                results.append(f"❌ {name}: {e}")
        await query.edit_message_text(
            "🧪 <b>Panel Test Results</b>\n━━━━━━━━━━━━━━━━━━━━━━\n" + "\n".join(results),
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_advanced")]]))
        return

    if data == "worker_status":
        lines = []
        for p in load_panels():
            alive = (p in REST_TASKS and not REST_TASKS[p].done())
            lines.append(f"{'🟢' if alive else '🔴'} REST: {p} (hits:{STATS['panel_hits'].get(p,0)})")
        for n in load_ivas():
            alive = (n in IVAS_TASKS and not IVAS_TASKS[n].done())
            lines.append(f"{'🟢' if alive else '🔴'} IVAS: {n} (hits:{STATS['ivas_hits'].get(n,0)})")
        await query.edit_message_text(
            "📊 <b>WORKER STATUS</b>\n━━━━━━━━━━━━━━━━━━━━━━\n" + "\n".join(lines or ["No workers"]),
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_advanced")]]))
        return

    if data == "confirm_clear_otps":
        save_otp_store({})
        await query.edit_message_text("✅ OTP store cleared.",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","back_to_admin")]]))
        return

    if data == "cancel_action":
        for d in [PANEL_ADD_STATES, IVAS_ADD_STATES, BROADCAST_STATES,
                  SETTING_STATES, FETCH_STATES, NB_STATE]:
            d.pop(uid, None)
        await query.edit_message_text("❌ Action cancelled.",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","back_to_admin")]]))
        return

# ═══════════════════════════════════════════════════════════════
#  MESSAGE HANDLER
# ═══════════════════════════════════════════════════════════════
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid  = update.effective_user.id
    text = update.message.text or ""

    # ── Track every user interaction ──────────────────────────
    if update.effective_user:
        db_touch_user(update.effective_user.id)

    # ── GN Feature Text Handlers (from main.go) ───────────────
    if await gn_withdraw_text(update, context):
        return
    if await gn_admin_wizard_text(update, context):
        return
    if await gn_broadcast_text(update, context):
        return

    # ── Reply keyboard button handlers — exact match from main.go ──
    # User buttons
    if text == "𝗚𝗲𝘁 𝗡𝘂𝗺𝗯𝗲𝗿":
        await gn_cmd_get_number(update, context); return
    if text == "𝗠𝘆 𝗔𝗰𝗰𝗼𝘂𝗻𝘁":
        await gn_cmd_my_account(update, context); return
    if text == "𝗕𝗮𝗹𝗮𝗻𝗰𝗲":
        await gn_cmd_balance(update, context); return
    if text == "𝗪𝗶𝘁𝗵𝗱𝗿𝗮𝘄":
        await gn_cmd_withdraw(update, context); return
    if text == "𝗧𝗼𝗽 𝗨𝘀𝗲𝗿𝘀":
        await gn_cmd_top_users(update, context); return
    if text == "𝗗𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗿":
        await update.message.reply_text(
            f'<tg-emoji emoji-id="6235572922086331108">😒</tg-emoji> 𝘿𝙚𝙫𝙚𝙡𝙤𝙥𝙚𝙧 𝘽𝙮: <b>KITE DEVELOPER</b>\n\n'
            f'<tg-emoji emoji-id="6206096153511990389">👑</tg-emoji> 𝙊𝙬𝙣𝙚𝙧: @payment_owner',
            parse_mode="HTML"); return
    if text == "𝗥𝗲𝗳𝗲𝗿𝗿𝗮𝗹":
        await gn_cmd_referral(update, context); return
    if text == "𝗝𝗼𝗶𝗻 𝗢𝘂𝗿 𝗖𝗵𝗮𝗻𝗻𝗲𝗹𝘀":
        await gn_cmd_join_channels(update, context); return

    # ── Admin Panel button → shows only Add Numbers + System Stats ──
    if text in ("𝗔𝗱𝗺𝗶𝗻 𝗣𝗮𝗻𝗲𝗹", "💠 𝗔𝗱𝗺𝗶𝗻 𝗣𝗮𝗻𝗲𝗹"):  # kept for backward compat
        if is_admin(uid):
            await update.message.reply_text(
                f'<tg-emoji emoji-id="6205965994528086727">💠</tg-emoji> <b>ADMIN PANEL</b>\n'
                f'━━━━━━━━━━━━━━━━━━━━━━\n\n'
                f'<tg-emoji emoji-id="4956507094124594921">➕</tg-emoji> <b>Add Numbers</b> — Add new numbers to any service\n'
                f'<tg-emoji emoji-id="5225414461080685066">📊</tg-emoji> <b>System Stats</b> — View all stock & OTP stats\n\n'
                f'<tg-emoji emoji-id="5235575317191474172">🚀</tg-emoji> <i>Use /admin for full admin panel</i>',
                parse_mode="HTML", reply_markup=get_admin_keyboard(uid))
        return

    # ── Admin Panel reply keyboard buttons ───────────────────
    if text == "𝗔𝗱𝗱 𝗡𝘂𝗺𝗯𝗲𝗿𝘀":
        if is_admin(uid):
            GN_WIZARD_STATES[uid] = {"step": "svc", "staged": []}
            await update.message.reply_text(
                f"{gn_icon('addnum')} <b>Step 1/7 — Service Name</b>\n\n"
                f"Enter service name:\n<i>Example: TikTok, WhatsApp, Instagram</i>",
                parse_mode="HTML", reply_markup=get_back_keyboard())
        return

    if text == "𝗦𝘆𝘀𝘁𝗲𝗺 𝗦𝘁𝗮𝘁𝘀":
        if is_admin(uid):
            grand = 0
            txt2 = (f"<tg-emoji emoji-id=\"5225414461080685066\">📊</tg-emoji> "
                    f"<b>System Statistics</b>\n\n")
            for sn, svc in GN_DATA["services"].items():
                em = gn_svc_emoji(sn); txt2 += f"{em} <b>{sn}</b>\n"
                for cn, c in svc.get("countries", {}).items():
                    flag = gn_flag(c.get("code", ""))
                    n = len(c.get("numbers", [])); grand += n
                    st = "❌ Out of Stock" if n == 0 else ("⚠️ Low" if n < 5 else "✅ OK")
                    txt2 += f"  {flag} {cn} — {c.get('price',0):.0f}{GN_CURRENCY} — {n} nums — {st}\n"
                txt2 += "\n"
            ty = sum(u.get("today_otps", 0) for u in GN_DATA["users"].values())
            ta = sum(u.get("total_otps", 0) for u in GN_DATA["users"].values())
            txt2 += (f"━━━━━━━━━━━━━━━━━━━━━━\n"
                     f"<tg-emoji emoji-id=\"5312310156384557787\">📱</tg-emoji> Total Numbers: <b>{grand}</b>\n"
                     f"<tg-emoji emoji-id=\"4958832114540741368\">👥</tg-emoji> Total Users: <b>{len(GN_DATA['users'])}</b>\n"
                     f"<tg-emoji emoji-id=\"6176966310920983412\">🔑</tg-emoji> Total OTPs: <b>{ta}</b>\n"
                     f"<tg-emoji emoji-id=\"6206508629286196237\">🔔</tg-emoji> Today OTPs: <b>{ty}</b>")
            await update.message.reply_text(txt2[:4000], parse_mode="HTML",
                reply_markup=get_admin_keyboard(uid))
        return

    # ── Back button ───────────────────────────────────────────
    if text in ("𝗕𝗮𝗰𝗸", "Back", "🔙 Back"):
        # If in a wizard, wizard handler already caught this above.
        # This handles the plain Back from Admin Panel → main menu.
        await update.message.reply_text(
            f"<tg-emoji emoji-id=\"5235575317191474172\">🚀</tg-emoji> <b>Main Menu</b>",
            parse_mode="HTML", reply_markup=smart_kb(uid))
        return

    if text == "/cancel":
        for d in [PANEL_ADD_STATES, IVAS_ADD_STATES, BROADCAST_STATES,
                  SETTING_STATES, FETCH_STATES, NB_STATE]:
            d.pop(uid, None)
        await update.message.reply_text("❌ Cancelled.")
        return

    # ── Number add flow ───────────────────────────────────────
    if uid in NB_STATE:
        state = NB_STATE[uid]
        if isinstance(state, dict) and state.get("step") == "waiting_country":
            NB_STATE[uid] = {"step":"waiting_file","country":text,"timestamp":time.time()}
            await update.message.reply_text(
                f"📄 Now send a <b>.txt file</b> (one number per line) for <b>{text}</b>:",
                parse_mode="HTML")
        return

    # ── Settings wizard ───────────────────────────────────────
    if uid in SETTING_STATES:
        state = SETTING_STATES[uid]
        state["timestamp"] = time.time()
        step  = state.get("step")

        if step == "waiting_group_id":
            try:
                gid = int(text.strip())
                groups = load_groups()
                if gid not in groups:
                    groups.append(gid)
                    save_groups(groups)
                    await update.message.reply_text(f"✅ Group <code>{gid}</code> added.", parse_mode="HTML")
                else:
                    await update.message.reply_text("🟡 Already exists.")
            except:
                await update.message.reply_text("❌ Invalid chat ID.")
            del SETTING_STATES[uid]

        elif step == "waiting_log_group":
            try:
                gid = int(text.strip())
                config = load_config()
                config["log_group"] = gid
                save_config(config)
                await update.message.reply_text(f"✅ Log group set to <code>{gid}</code>.", parse_mode="HTML")
            except:
                await update.message.reply_text("❌ Invalid chat ID.")
            del SETTING_STATES[uid]

        elif step == "waiting_delay":
            try:
                delay = int(text.strip())
                if not 0 <= delay <= 60:
                    raise ValueError
                config = load_config()
                config["forward_delay"] = delay
                save_config(config)
                await update.message.reply_text(f"✅ Forward delay set to <b>{delay}s</b>.", parse_mode="HTML")
            except:
                await update.message.reply_text("❌ Enter a number 0-60.")
            del SETTING_STATES[uid]

        elif step == "waiting_channel":
            config = load_config()
            config["channel_link"] = text.strip()
            save_config(config)
            await update.message.reply_text("✅ Channel link updated.")
            del SETTING_STATES[uid]

        elif step == "waiting_numberbot":
            config = load_config()
            config["number_bot_link"] = text.strip()
            save_config(config)
            await update.message.reply_text("✅ Number bot link updated.")
            del SETTING_STATES[uid]

        elif step == "waiting_otp_link":
            config = load_config()
            config["channel_link"] = text.strip()
            save_config(config)
            await update.message.reply_text("✅ OTP group link updated.")
            del SETTING_STATES[uid]

        elif step == "waiting_staff_id":
            if not is_owner(uid):
                await update.message.reply_text("❌ Owner only!")
                del SETTING_STATES[uid]
                return
            try:
                new_uid = int(text.strip())
                if new_uid in OWNER_IDS:
                    await update.message.reply_text("🟡 That user is already an owner.")
                    del SETTING_STATES[uid]
                    return
                staff = load_staff()
                if str(new_uid) in staff:
                    await update.message.reply_text("🟡 Already a staff member. Use edit to change permissions.")
                    del SETTING_STATES[uid]
                    return
                add_staff(new_uid, str(new_uid), [])
                await update.message.reply_text(
                    f"✅ Staff member <code>{new_uid}</code> added with no permissions.\n\n"
                    f"Now go to Staff Manager and tap their name to assign permissions.",
                    parse_mode="HTML",
                    reply_markup=InlineKeyboardMarkup([[b("👤 Open Staff Manager", "menu_admin_manager")]]))
            except ValueError:
                await update.message.reply_text("❌ Invalid user ID. Send a numeric Telegram user ID.")
            del SETTING_STATES[uid]
        return

    # ── Fetch by number ───────────────────────────────────────
    if uid in FETCH_STATES:
        state = FETCH_STATES[uid]
        state["timestamp"] = time.time()
        if state.get("step") == "waiting_number":
            target = text.strip().replace("+", "")
            found  = None
            store  = load_otp_store()
            for k, v in store.items():
                if target in k:
                    found = v
                    break
            if not found:
                rows = db_search_otp_by_number(target)
                if rows:
                    found = rows[0][2]
            if not found:
                for panel in API_PANELS:
                    d2 = fetch_latest(panel)
                    if d2 and target in d2["number"]:
                        found = extract_otp(d2["message"])
                        break
            if found:
                await update.message.reply_text(
                    f"✅ <b>OTP FOUND</b>\n📞 <code>{target}</code>\n🔑 <code>{found}</code>",
                    parse_mode="HTML")
            else:
                await update.message.reply_text(
                    f"❌ No OTP found for <code>{target}</code>", parse_mode="HTML")
            del FETCH_STATES[uid]
        return

    # ── Panel add wizard ──────────────────────────────────────
    if uid in PANEL_ADD_STATES:
        state = PANEL_ADD_STATES[uid]
        state["timestamp"] = time.time()
        if state["step"] == "name":
            state["data"]["name"] = text
            state["step"] = "url"
            await update.message.reply_text("Step 2: API URL (http://...):")
        elif state["step"] == "url":
            if not text.startswith("http"):
                await update.message.reply_text("❌ Must start with http:")
                return
            state["data"]["url"] = text
            state["step"] = "token"
            await update.message.reply_text("Step 3: API Token:")
        elif state["step"] == "token":
            state["data"]["token"] = text
            state["step"] = "records"
            await update.message.reply_text("Step 4: Records count (1-50):")
        elif state["step"] == "records":
            try:
                rec = int(text)
                if not 1 <= rec <= 50:
                    raise ValueError
            except:
                await update.message.reply_text("❌ Enter 1-50:")
                return
            state["data"]["records"] = rec
            state["step"] = "confirm"
            await update.message.reply_text(
                f"➕ <b>CONFIRM ADD PANEL</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
                f"Name: <code>{state['data']['name']}</code>\n"
                f"URL: <code>{state['data']['url']}</code>\n"
                f"Token: <code>{state['data']['token'][:30]}...</code>\n"
                f"Records: <code>{rec}</code>\n━━━━━━━━━━━━━━━━━━━━━━\nConfirm?",
                parse_mode="HTML", reply_markup=get_confirmation_keyboard("add_panel"))
        return

    # ── IVAS add wizard ───────────────────────────────────────
    if uid in IVAS_ADD_STATES:
        state = IVAS_ADD_STATES[uid]
        state["timestamp"] = time.time()
        if state["step"] == "name":
            state["data"]["name"] = text
            state["step"] = "uri"
            await update.message.reply_text(
                "Step 2: IVAS WebSocket URI (<code>wss://...</code>):", parse_mode="HTML")
        elif state["step"] == "uri":
            if not text.startswith("wss://"):
                await update.message.reply_text("❌ Must start with <code>wss://</code>", parse_mode="HTML")
                return
            state["data"]["uri"] = text
            state["step"] = "confirm"
            await update.message.reply_text(
                f"🔌 <b>CONFIRM ADD IVAS</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
                f"Name: <code>{state['data']['name']}</code>\n"
                f"URI: <code>{state['data']['uri'][:80]}...</code>\n━━━━━━━━━━━━━━━━━━━━━━\nConfirm?",
                parse_mode="HTML", reply_markup=get_confirmation_keyboard("add_ivas"))
        return

    # ── Broadcast wizard ──────────────────────────────────────
    if uid in BROADCAST_STATES:
        state = BROADCAST_STATES[uid]
        state["timestamp"] = time.time()
        if state["step"] == "waiting_message":
            if state["type"] == "text":
                state["message"] = text
                state["step"]    = "confirm"
                await update.message.reply_text(
                    f"Preview:\n{text[:200]}{'...' if len(text)>200 else ''}\n\nSend?",
                    reply_markup=get_confirmation_keyboard("broadcast"))
            elif state["type"] == "with_buttons":
                lines    = text.split('\n')
                msg_text = ""
                buttons  = []
                for line in lines:
                    if line.startswith('[') and line.endswith(']') and '|' in line:
                        parts = line[1:-1].split('|', 1)
                        buttons.append(InlineKeyboardButton(parts[0].strip(), url=parts[1].strip()))
                    else:
                        msg_text += line + '\n'
                state["message"] = msg_text.strip()
                state["buttons"] = buttons
                state["step"]    = "confirm"
                await update.message.reply_text(
                    f"Preview with {len(buttons)} button(s). Send?",
                    reply_markup=get_confirmation_keyboard("broadcast_buttons"))
        return

# ═══════════════════════════════════════════════════════════════
#  ██████╗ ███╗   ██╗    ███████╗███████╗ █████╗ ████████╗██╗   ██╗██████╗ ███████╗███████╗
#  ██╔════╝████╗  ██║    ██╔════╝██╔════╝██╔══██╗╚══██╔══╝██║   ██║██╔══██╗██╔════╝██╔════╝
#  ██║  ███╗██╔██╗ ██║    █████╗  █████╗  ███████║   ██║   ██║   ██║██████╔╝█████╗  ███████╗
#  ██║   ██║██║╚██╗██║    ██╔══╝  ██╔══╝  ██╔══██║   ██║   ██║   ██║██╔══██╗██╔══╝  ╚════██║
#  ╚██████╔╝██║ ╚████║    ██║     ███████╗██║  ██║   ██║   ╚██████╔╝██║  ██║███████╗███████║
#   ╚═════╝ ╚═╝  ╚═══╝    ╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝
#  PORTED FROM main.go — Get Number, My Account, Balance, Withdraw, Top Users,
#  Referral, Admin Add Numbers (7-step), Remove Service, Remove Country, Auto Broadcast
# ═══════════════════════════════════════════════════════════════

import random as _random

# ── Premium UI Emoji IDs (from main.go uiEmojis) ─────────────────────────────
GN_UI_EMOJI = {
    "fire":       ("6204104220694550861", "☄️"),   "bolt":       ("6206405459876779229", "💸"),
    "crown":      ("6206096153511990389", "👑"),   "diamond":    ("6205965994528086727", "💠"),
    "star":       ("6204104220694550861", "☄️"),   "key":        ("6176966310920983412", "🔑"),
    "lock":       ("5291873529464122510", "🔒"),   "robot":      ("5339267587337370029", "🤖"),
    "shield":     ("5339163352776058483", "🛡"),   "rocket":     ("5235575317191474172", "🚀"),
    "chart":      ("5343862721307748990", "📊"),   "bell":       ("6206508629286196237", "🔔"),
    "skull":      ("5807631052251861399", "💀"),   "zap":        ("5411590687663608498", "⚡️"),
    "check":      ("6206479140040743133", "✅"),   "earth":      ("5224450179368767019", "🌍"),
    "phone":      ("5312310156384557787", "📱"),   "chat":       ("5040036030414062506", "💬"),
    "speak":      ("5850449436651556295", "🗣"),   "receiver":   ("6204108584381322968", "📞"),
    "satellite":  ("5352564488258200671", "📡"),   "clock":      ("6206508629286196237", "🔔"),
    "pushpin":    ("5397782960512444700", "📍"),   "megaphone":  ("6206080502651164081", "📣"),
    "document":   ("5258079129051356005", "📄"),   "notepad":    ("5262974657329394511", "📝"),
    "laptop":     ("5321154224191462061", "💻"),   "people":     ("5242442819573927209", "👋"),
    "globe":      ("6204058135695464033", "🌐"),   "copy":       ("5197219609970758159", "📋"),
    "envelope":   ("6206112371308500200", "✉️"),  "download":   ("6204177183598974956", "⬇️"),
    "hourglass":  ("6206118633370818254", "⌛"),   "money":      ("6190336264940559752", "💰"),
    "link":       ("6206497372176913599", "🔗"),   "gift":       ("6206027872121918710", "🎁"),
    "user_alt":   ("5242442819573927209", "👤"),   "dev":        ("5215263059639017128", "🧑‍💻"),
    "focus":      ("5226851658792717025", "🎯"),   "user":       ("5321154224191462061", "👤"),
    "book":       ("5411369574157286161", "📖"),   "help":       ("5436113877181941026", "❓"),
    "back":       ("5255703720078879038", "🔙"),   "trash":      ("6206108815075579644", "🗑"),
    "cancel":     ("5974083768233760323", "❌"),   "online":     ("5319310205752717294", "🟢"),
    "offline":    ("5319238892115733906", "🔴"),   "info":       ("5467889436807157272", "ℹ️"),
    "refresh":    ("5285347429737055549", "🔄"),   "announce":   ("6206080502651164081", "📣"),
    "trophy":     ("6190336264940559752", "💰"),   "withdraw":   ("6206155797722830770", "💵"),
    "account":    ("6237864166879663987", "🤖"),   "addnum":     ("4956507094124594921", "➕"),
    "otp":        ("6206508629286196237", "🔔"),   "comet":      ("6204104220694550861", "☄️"),
    "timer":      ("",                    "⏱"),   "target":     ("6206479140040743133", "✅"),
    "list":       ("5197219609970758159", "📋"),   "remove":     ("5445267414562389170", "🗑️"),
    "users":      ("4958832114540741368", "👥"),   "get_number": ("5296369303661067030", "📲"),
    "my_account": ("6237864166879663987", "🤖"),   "balance":    ("5778204036578678218", "💰"),
    "top_users":  ("6235252066554484059", "🏆"),   "developer":  ("6235572922086331108", "🧑‍💻"),
    "admin":      ("6205965994528086727", "💠"),   "join":       ("6206080502651164081", "📣"),
    "referral":   ("6242498410822244114", "🎁"),   "settings":   ("6205965994528086727", "💠"),
    "shield2":    ("5197288647275071607", "🛡️"),
}

# ── Additional Service Emoji IDs (from main.go serviceEmojiIDs) ───────────────
GN_SERVICE_EMOJIS = {
    "tiktok":    "5327982530702359565",  "whatsapp":  "5334998226636390258",
    "instagram": "5319160079465857105",  "facebook":  "5323261730283863478",
    "telegram":  "5330237710655306682",  "twitter":   "5330337435500951363",
    "snapchat":  "5330248916224983855",  "google":    "5359758030198031389",
    "gmail":     "5359758030198031389",  "youtube":   "5373026167722876724",
    "discord":   "5373026167722876724",  "netflix":   "5373026167722876724",
    "amazon":    "5373026167722876724",  "paypal":    "5364111181415996352",
    "spotify":   "5373026167722876724",  "binance":   "5359437015752401733",
    "bybit":     "5359437015752401733",  "hsbc":      "6249045530119249807",
    "gochat":    "5332524123610430820",  "imo":       "5920204030570667999",
    "apple":     "5334955749409834455",
    "DEFAULT":   "5332524123610430820",
}

# ── Full Country Flag IDs (from main.go countryFlagIDs) ───────────────────────
GN_FLAG_IDS = {
    "AD":"5221987861733061751","AE":"5224565851427976312","AF":"5222096009009575868",
    "AG":"5224544866217765554","AL":"5224312057515486246","AM":"5224369957969603463",
    "AO":"5224379767674907895","AR":"5221980461504411710","AT":"5224520754271366661",
    "AU":"5224659803837574114","AZ":"5224426544163728284","BA":"5224496092569155254",
    "BB":"5222156533688712094","BD":"5224407289825340729","BE":"5224513182244024630",
    "BF":"5222356541725749790","BG":"5222092074819530668","BH":"5224492892818518587",
    "BI":"5224490444687158452","BJ":"5222024115552009151","BN":"5224435958732042406",
    "BO":"5224675484763170798","BR":"5224688610183228070","BS":"5224504167107668172",
    "BT":"5224541065171710147","BW":"5224288456670196085","BY":"5280820319458707404",
    "BZ":"5224316292353241916","CA":"5222001124592071204","CD":"5224398158724871677",
    "CF":"5222073662294733523","CG":"5222104268231684600","CH":"5224707263226194753",
    "CL":"5222350726340032308","CM":"5222270788408717651","CN":"5224435456220868088",
    "CO":"5224455152940886669","CR":"5222453801260168022","CV":"5222347737042792258",
    "CY":"5222431454545327055","CZ":"5222073533445714675","DE":"5222165617544542414",
    "DJ":"5224203012590810589","DK":"5222297215342490217","DM":"5222337489250824921",
    "DO":"5224286412265763450","DZ":"5224260376174015500","EC":"5224191188545840926",
    "EE":"5222195463272281351","EG":"5222161185138292290","ES":"5222024776976970940",
    "ET":"5224467805914542024","EU":"5222108911091331711","FI":"5224282903277482188",
    "FJ":"5221962676044838178","FM":"5222280486444873367","FR":"5222029789203804982",
    "GA":"5224669733801963467","GB":"5224518800061245598","GD":"5222234560359577687",
    "GE":"5222152195771742239","GH":"5224511339703056124","GM":"5221949872747330159",
    "GN":"5222337588035073000","GQ":"5222172811614762423","GR":"5222463490706389920",
    "GT":"5222128302868672826","GW":"5224705704153066489","GY":"5224570532942329532",
    "HK":"5292166459118606932","HN":"5222229234600130045","HR":"5221967765581085099",
    "HT":"5224683146984831315","HU":"5224691998912427164","ID":"5224405893960969756",
    "IE":"5224257017509588818","IL":"5224720599099648709","IN":"5222300011366200403",
    "IQ":"5221980268230882832","IR":"5224374154152653367","IS":"5222063229819172521",
    "IT":"5222460101977190141","JM":"5222007034467074185","JO":"5222292177345853436",
    "JP":"5222390089715299207","KE":"5222089648163009103","KG":"5224388147156102493",
    "KH":"5224189882875785448","KI":"5224652244695134610","KM":"5222398735484466247",
    "KP":"5294193812531333564","KR":"5222345550904439270","KW":"5221949726718442491",
    "KZ":"5222276376161171525","LA":"5224200843632324642","LB":"5222244425899455269",
    "LC":"5222000927023577045","LK":"5224277294050192388","LR":"5221998371518034740",
    "LS":"5224245850594619415","LT":"5224245902134226386","LU":"5224499567197700690",
    "LV":"5224401229626484931","LY":"5222194286451242896","MA":"5224530035695693965",
    "MC":"5221937224068640464","MD":"5224216473018314447","ME":"5224463399278096980",
    "MG":"5222042605386217334","MH":"5224538449536624503","MK":"5222470435668505656",
    "ML":"5224322352552096671","MM":"5294254478944393569","MN":"5224192257992701543",
    "MT":"5224731388057497620","MU":"5224238347286752315","MV":"5224393700548814960",
    "MX":"5221971386238514431","MY":"5224312886444174057","MZ":"5222470388423864826",
    "NA":"5224690826386351746","NE":"5222099049846420864","NG":"5224723614166691638",
    "NL":"5224516489368841614","NO":"5224465228934163949","NP":"5222444378101925267",
    "NZ":"5224573595254009705","OM":"5222396686785066306","PA":"5222111719999945107",
    "PE":"5224482026551258766","PG":"5224500164198149905","PH":"5222065042295376892",
    "PK":"5224637061985742245","PL":"5224670399521892983","PS":"5222041677673282461",
    "PT":"5224404094369672274","PY":"5222152565138929235","QA":"5222225596762830469",
    "RO":"5222273794885826118","RS":"5222145396838512729","RU":"5294335323113807278",
    "RW":"5222449197055227754","SA":"5224698145010624573","SC":"5224467496676896871",
    "SD":"5224372990216514135","SE":"5222201098269373561","SG":"5224194023224257181",
    "SI":"5294279359689938006","SL":"5224420995065983217","SN":"5224358988623130949",
    "SR":"5224567367551428669","SS":"5224618146949773268","ST":"5221953304426198315",
    "SY":"5294013428199869487","SZ":"5224269666188274723","TD":"5222060468155204001",
    "TG":"5222408051268532030","TH":"5224638530864556281","TJ":"5222217865821696536",
    "TL":"5224515905253291409","TM":"5224256935905208951","TN":"5221991375016310330",
    "TR":"5224601903383457698","TT":"5224391883777651050","TW":"5294095745543069603",
    "TZ":"5224397364155923150","UA":"5222250679371839695","UG":"5222464040462200940",
    "UN":"5451772687993031127","US":"5224321781321442532","UY":"5222466849370813232",
    "UZ":"5222404546575219535","VA":"5222420266155520507","VC":"5224541228380467535",
    "VE":"5294476442854247878","VN":"5222359651282071925","VU":"5222126748090512778",
    "WS":"5224660353593387686","XK":"5222197129719592160","YE":"5222300655611294950",
    "ZA":"5294325281480266304","ZM":"5224646626877911277","ZW":"5222060442385397848",
    "DEFAULT":"5929108859279907956",
}

# ── Constants ─────────────────────────────────────────────────
GN_CURRENCY      = "Rs"
GN_DOLLAR        = "$"
GN_HOLD_SECS     = 20 * 60        # 20 min hold
GN_CYCLE_DEFAULT = 3
GN_MIN_WITHDRAW  = 10.0
GN_MIN_USD       = 0.0045
GN_USD_RATE      = 280.0
GN_REF_MILESTONE = 20
GN_REF_REWARD    = 10.0
GN_OTP_GROUP_URL = "https://t.me/kiteotp"

GN_DATA_FILE      = "gn_data.json"
GN_HOLDS_FILE     = "gn_holds.json"
GN_REFERRALS_FILE = "gn_referrals.json"

# ── In-memory stores ─────────────────────────────────────────
GN_DATA            = {}
GN_HOLDS           = {}
GN_HOLD_SEQ        = 0
GN_WIZARD_STATES   = {}   # admin add-number wizard
GN_WDRAW_STATES    = {}   # user withdraw wizard
GN_BCAST_STATES    = {}   # admin broadcast wizard


# ── Helpers ───────────────────────────────────────────────────
def gn_icon(name: str) -> str:
    eid, fb = GN_UI_EMOJI.get(name, ("", name))
    return f'<tg-emoji emoji-id="{eid}">{fb}</tg-emoji>' if eid else fb

def gn_ce(eid: str, fb: str) -> str:
    return f'<tg-emoji emoji-id="{eid}">{fb}</tg-emoji>' if eid else fb

def gn_flag(code: str) -> str:
    """Returns HTML tg-emoji tag — for use in message text only."""
    c = (code or "DEFAULT").upper()
    eid = GN_FLAG_IDS.get(c, GN_FLAG_IDS["DEFAULT"])
    return f'<tg-emoji emoji-id="{eid}">🏳</tg-emoji>'

def gn_flag_plain(code: str) -> str:
    """Returns Unicode flag emoji — for use in button labels (no HTML supported)."""
    c = (code or "").upper()
    if len(c) == 2:
        return chr(ord(c[0]) + 127397) + chr(ord(c[1]) + 127397)
    return "🌍"

def gn_svc_emoji(service: str) -> str:
    """Returns HTML tg-emoji tag — for use in message text only."""
    s = service.lower().strip()
    for k, eid in GN_SERVICE_EMOJIS.items():
        if k != "DEFAULT" and k in s:
            return f'<tg-emoji emoji-id="{eid}">📱</tg-emoji>'
    return f'<tg-emoji emoji-id="{GN_SERVICE_EMOJIS["DEFAULT"]}">📱</tg-emoji>'

def gn_svc_emoji_plain(service: str) -> str:
    """Returns plain emoji fallback — for use in button labels."""
    s = service.lower().strip()
    plain_map = {
        "tiktok": "🎵", "whatsapp": "💬", "instagram": "📸",
        "facebook": "👤", "telegram": "✈️", "twitter": "🐦",
        "snapchat": "👻", "google": "🔍", "gmail": "📧",
        "youtube": "▶️", "discord": "🎮", "netflix": "🎬",
        "amazon": "📦", "paypal": "💳", "spotify": "🎧",
        "binance": "💰", "bybit": "📊",
        "imo": "💬", "paypal": "💳", "apple": "🍎",
    }
    for k, em in plain_map.items():
        if k in s:
            return em
    return "📱"

def gn_btn(text, cb=None, url=None, style=None):
    """Colored inline button — same as bc() but always uses InlineKeyboardButton."""
    if url:
        return InlineKeyboardButton(text, url=url)
    return InlineKeyboardButton(text, callback_data=cb or "noop")


# ── Data persistence ─────────────────────────────────────────
def gn_load():
    global GN_DATA
    try:
        with open(GN_DATA_FILE) as f:
            GN_DATA = json.load(f)
    except:
        GN_DATA = {}
    for k, v in [("services",{}),("users",{}),("withdrawals",{}),("withdraw_seq",0),
                 ("min_withdrawal",GN_MIN_WITHDRAW),("min_withdrawal_usd",GN_MIN_USD),
                 ("usd_to_pkr",GN_USD_RATE),("withdraw_enabled",True)]:
        GN_DATA.setdefault(k, v)

def gn_save():
    try:
        with open(GN_DATA_FILE,"w") as f: json.dump(GN_DATA, f, indent=2)
    except Exception as e: logger.error(f"gn_save: {e}")

def gn_load_holds():
    """
    Load holds.json on startup — mirrors Go loadHolds().
    Keys are str(chat_id), values are hold dicts with:
      chat_id, message_id, service, country, numbers[],
      token, otp_limit, number_otp_count{}, used{}, expires_at (unix float)
    """
    global GN_HOLDS
    try:
        with open(GN_HOLDS_FILE) as f:
            loaded = json.load(f)
        if not isinstance(loaded, dict):
            GN_HOLDS = {}
            return
        now = time.time()
        expired = [k for k, h in loaded.items() if h.get("expires_at", 0) < now]
        for k in expired:
            del loaded[k]
        GN_HOLDS = loaded
        logger.info(f"[holds] Loaded {len(GN_HOLDS)} active holds from {GN_HOLDS_FILE} ({len(expired)} expired dropped)")
    except FileNotFoundError:
        GN_HOLDS = {}
        logger.info(f"[holds] {GN_HOLDS_FILE} not found — starting fresh")
    except Exception as e:
        GN_HOLDS = {}
        logger.error(f"[holds] load error: {e}")

def gn_save_holds():
    """Save GN_HOLDS to holds.json — mirrors Go saveHolds()."""
    try:
        with open(GN_HOLDS_FILE, "w") as f:
            json.dump(GN_HOLDS, f, indent=2)
    except Exception as e:
        logger.error(f"[holds] save error: {e}")

def find_holder_for_phone(phone: str):
    """
    Python port of Go findHolderForPhone().
    Scans GN_HOLDS for an active (non-expired) hold whose Numbers[] contains phone.
    Uses suffix matching — mirrors Go strings.HasSuffix logic to tolerate
    country-code prefix differences (e.g. 263783... vs 0783...).
    Falls back to SQLite assigned_numbers for old nb_get flow.
    Returns (chat_id: int, hold: dict) or (None, None).
    """
    target = re.sub(r'\D', '', phone)
    if not target:
        logger.warning(f"[find_holder] empty target for phone={phone!r}")
        return None, None

    now = time.time()
    active = 0
    for key, hold in list(GN_HOLDS.items()):
        if not hold:
            continue
        exp = hold.get("expires_at", 0)
        if exp < now:
            logger.debug(f"[find_holder] skip key={key} — expired")
            continue
        active += 1
        for n in hold.get("numbers", []):
            nd = re.sub(r'\D', '', n)
            if not nd:
                continue
            # Suffix match — mirrors Go: nd==target || HasSuffix(nd,target) || HasSuffix(target,nd)
            if nd == target or nd.endswith(target) or target.endswith(nd):
                logger.info(f"[find_holder] ✅ MATCH phone={phone} target={target} matched_num={nd} chat_id={key}")
                try:
                    return int(hold.get("chat_id", key)), hold
                except (ValueError, TypeError):
                    return int(key), hold

    logger.info(f"[find_holder] no match in GN_HOLDS (active={active}) for target={target}")

    # Fallback: SQLite assigned_numbers (nb_get flow)
    owner_id = db_get_owner_of_number(phone)
    if owner_id:
        logger.info(f"[find_holder] ✅ SQLite fallback match owner_id={owner_id}")
        return owner_id, GN_HOLDS.get(str(owner_id))

    logger.warning(f"[find_holder] ❌ no holder found for {phone!r} (target={target})")
    return None, None

# ── User management ───────────────────────────────────────────
def gn_upsert_user(uid, uname="", first="", last=""):
    key = str(uid)
    if key not in GN_DATA["users"]:
        GN_DATA["users"][key] = {
            "id":uid,"username":uname,"first_name":first,"last_name":last,
            "balance":0.0,"total_otps":0,"today_otps":0,
            "joined_at":datetime.now().strftime("%Y-%m-%d"),
            "referred_by":0,"referral_count":0,
            "otps_since_last_reward":0,"referral_reward_given":False,
        }
        gn_save()
    u = GN_DATA["users"][key]
    chg = False
    for attr,val in [("first_name",first),("last_name",last),("username",uname)]:
        if val and u.get(attr) != val: u[attr]=val; chg=True
    if chg: gn_save()
    return GN_DATA["users"][key]

def gn_credit_otp(uid, price):
    key = str(uid)
    u = GN_DATA["users"].get(key); 
    if not u: return 0.0
    u["total_otps"]   = u.get("total_otps",0)+1
    u["today_otps"]   = u.get("today_otps",0)+1
    u["otps_since_last_reward"] = u.get("otps_since_last_reward",0)+1
    u["balance"]      = u.get("balance",0.0) + price
    ref = u.get("referred_by",0)
    if u["total_otps"] == GN_REF_MILESTONE and ref and not u.get("referral_reward_given"):
        rk = str(ref)
        if rk in GN_DATA["users"]:
            GN_DATA["users"][rk]["balance"] = GN_DATA["users"][rk].get("balance",0.0)+GN_REF_REWARD
            GN_DATA["users"][rk]["referral_count"] = GN_DATA["users"][rk].get("referral_count",0)+1
        u["referral_reward_given"]=True
    gn_save()
    return u["balance"]

def gn_ref_stats(uid):
    total=qual=pend=0
    for u in GN_DATA["users"].values():
        if u.get("referred_by")==uid:
            total+=1
            if u.get("referral_reward_given"): qual+=1
            else: pend+=1
    return total, qual, pend, qual*GN_REF_REWARD

def gn_ref_link(bot_username, uid):
    return f"https://t.me/{bot_username}?start=ref{uid}"

# ── Hold management ───────────────────────────────────────────
def gn_pick_numbers(pool, n):
    n = min(n, len(pool))
    if n<=0: return [],pool
    idxs = _random.sample(range(len(pool)),n)
    iset = set(idxs)
    return [pool[i] for i in idxs],[pool[i] for i in range(len(pool)) if i not in iset]

def gn_clear_hold(chat_id):
    key = str(chat_id)
    old = GN_HOLDS.pop(key,None)
    if not old: return
    sn = old.get("service"); cn = old.get("country")
    old_set = {re.sub(r'\D','',x) for x in old.get("numbers",[])}
    svc = GN_DATA["services"].get(sn)
    if svc and cn in svc.get("countries",{}):
        c = svc["countries"][cn]
        before = c.get("numbers",[])
        c["numbers"] = [x for x in before if re.sub(r'\D','',x) not in old_set]
        c["total_stock"] = max(0,c.get("total_stock",0)-( len(before)-len(c["numbers"])))
    gn_save_holds()

def gn_release_hold(hold):
    if not hold or not hold.get("numbers"): return
    used = hold.get("used",{})
    to_ret = [n for n in hold["numbers"] if not used.get(re.sub(r'\D','',n))]
    if not to_ret: return
    svc = GN_DATA["services"].get(hold.get("service"))
    cn  = hold.get("country")
    if svc and cn in svc.get("countries",{}):
        svc["countries"][cn]["numbers"].extend(to_ret)
        svc["countries"][cn]["total_stock"] = svc["countries"][cn].get("total_stock",0)+len(to_ret)
        gn_save()

# ── Keyboards ─────────────────────────────────────────────────
def gn_main_menu_kb():
    """Main user menu — same-to-same from main.go mainMenuKB."""
    return InlineKeyboardMarkup([
        [gn_btn(f"📲 𝗚𝗲𝘁 𝗡𝘂𝗺𝗯𝗲𝗿",  cb="gn_services"),
         gn_btn(f"🤖 𝗠𝘆 𝗔𝗰𝗰𝗼𝘂𝗻𝘁", cb="gn_myacc")],
        [gn_btn(f"💰 𝗕𝗮𝗹𝗮𝗻𝗰𝗲",    cb="gn_balance"),
         gn_btn(f"💵 𝗪𝗶𝘁𝗵𝗱𝗿𝗮𝘄",   cb="gn_withdraw")],
        [gn_btn(f"🏆 𝗧𝗼𝗽 𝗨𝘀𝗲𝗿𝘀",   cb="gn_topusers"),
         gn_btn(f"🧑‍💻 𝗗𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗿",  url="https://t.me/payment_owner")],
        [gn_btn(f"🎁 𝗥𝗲𝗳𝗲𝗿𝗿𝗮𝗹",    cb="gn_referral")],
        [gn_btn(f"📣 𝗝𝗼𝗶𝗻 𝗢𝘂𝗿 𝗖𝗵𝗮𝗻𝗻𝗲𝗹𝘀", cb="gn_joinchan")],
    ])

def gn_admin_action_kb(uid=0):
    """Admin action keyboard — same-to-same from main.go adminActionKB."""
    rows=[]
    if has_perm(uid,"numbers"):
        rows.append([gn_btn("➕ 𝗔𝗱𝗱 𝗡𝘂𝗺𝗯𝗲𝗿𝘀",  cb="gnadm_addnums"),
                     gn_btn("📋 𝗟𝗶𝘀𝘁 𝗦𝗲𝗿𝘃𝗶𝗰𝗲𝘀",  cb="gnadm_listsvc")])
    if has_perm(uid,"stats"):
        rows.append([gn_btn("📊 𝗦𝘆𝘀𝘁𝗲𝗺 𝗦𝘁𝗮𝘁𝘀",  cb="gnadm_stats"),
                     gn_btn("👥 𝗧𝗼𝘁𝗮𝗹 𝗨𝘀𝗲𝗿𝘀",   cb="gnadm_users")])
    if has_perm(uid,"numbers"):
        rows.append([gn_btn("🗑 𝗥𝗲𝗺𝗼𝘃𝗲 𝗦𝗲𝗿𝘃𝗶𝗰𝗲",cb="gnadm_rmsvc"),
                     gn_btn("🗑 𝗥𝗲𝗺𝗼𝘃𝗲 𝗖𝗼𝘂𝗻𝘁𝗿𝘆",cb="gnadm_rmcnt")])
    if has_perm(uid,"broadcast"):
        rows.append([bc("📣 𝗕𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁", cb="nb_broadcast", style="primary", icon="6206080502651164081")])
    rows.append([gn_btn("🔙 𝗕𝗮𝗰𝗸",             cb="back_to_admin")])
    return InlineKeyboardMarkup(rows)

def gn_services_kb():
    rows = []
    styles = ["danger", "success", "primary"]
    for i, (sn, svc) in enumerate(GN_DATA["services"].items()):
        total = sum(len(c.get("numbers", [])) for c in svc.get("countries", {}).values())
        stock = f"({total})" if total > 0 else "(❌ Empty)"
        # Get premium emoji ID for this service
        s_lower = sn.lower().strip()
        svc_icon_id = None
        for k, eid in GN_SERVICE_EMOJIS.items():
            if k != "DEFAULT" and k in s_lower:
                svc_icon_id = eid
                break
        if not svc_icon_id:
            svc_icon_id = GN_SERVICE_EMOJIS["DEFAULT"]
        rows.append([InlineKeyboardButton(
            f"{sn} {stock}",
            callback_data=f"gnsvc:{sn}",
            api_kwargs={"style": styles[i % 3], "icon_custom_emoji_id": svc_icon_id}
        )])
    if not rows:
        rows.append([bc("❌ 𝗡𝗼 𝗦𝗲𝗿𝘃𝗶𝗰𝗲𝘀 𝗔𝘃𝗮𝗶𝗹𝗮𝗯𝗹𝗲", cb="noop", style="danger")])
    rows.append([bc("𝗕𝗮𝗰𝗸", cb="gn_backmain", style="primary", icon="5255703720078879038")])
    return InlineKeyboardMarkup(rows)

def gn_countries_kb(sn):
    rows = []
    svc = GN_DATA["services"].get(sn, {})
    styles = ["success", "primary", "danger"]
    for i, (cn, c) in enumerate(svc.get("countries", {}).items()):
        code = (c.get("code") or "").upper()
        n = len(c.get("numbers", [])); p = c.get("price", 0)
        if n > 0:
            lbl = f"{cn} — {p:.0f}{GN_CURRENCY} • {n} nums"
        else:
            lbl = f"{cn} — {p:.0f}{GN_CURRENCY} • ❌ Out"
        # Premium flag emoji ID for button icon
        flag_icon_id = GN_FLAG_IDS.get(code, GN_FLAG_IDS.get("DEFAULT", "5222250679371839695"))
        rows.append([InlineKeyboardButton(
            lbl,
            callback_data=f"gncnt:{sn}:{cn}",
            api_kwargs={"style": styles[i % 3], "icon_custom_emoji_id": flag_icon_id}
        )])
    rows.append([bc("𝗕𝗮𝗰𝗸", cb="gn_services", style="primary", icon="5255703720078879038")])
    return InlineKeyboardMarkup(rows)

def gn_numbers_kb(sn, cn, nums, otp_group=""):
    rows = []
    for n in nums:
        rows.append([InlineKeyboardButton(
            n,
            copy_text=CopyTextButton(text=n),
            api_kwargs={
                "style": "success",
                "icon_custom_emoji_id": "5312310156384557787"
            }
        )])
    rows.append([bc("𝗖𝗵𝗮𝗻𝗴𝗲 𝗖𝗼𝘂𝗻𝘁𝗿𝘆",   cb=f"gnchcnt:{sn}",        style="primary", icon="6204058135695464033")])
    rows.append([bc("𝗥𝗲𝗳𝗿𝗲𝘀𝗵 𝗡𝘂𝗺𝗯𝗲𝗿𝘀", cb=f"gnrefresh:{sn}:{cn}", style="success", icon="4956287101604725699")])
    if otp_group:
        rows.append([bc("𝗢𝗧𝗣 𝗚𝗿𝗼𝘂𝗽", url=otp_group, style="danger", icon="6206508629286196237")])
    rows.append([bc("🔙 𝗕𝗮𝗰𝗸", cb=f"gnchcnt:{sn}", style="primary", icon="5255703720078879038")])
    return InlineKeyboardMarkup(rows)

def gn_rm_service_kb():
    rows = [[bc(f"{sn}", cb=f"gnrmsvc:{sn}", style="danger", icon="5445267414562389170")]
            for sn in GN_DATA["services"]]
    if not rows:
        rows = [[bc("❌ No Services", cb="noop", style="danger")]]
    rows.append([bc("𝗕𝗮𝗰𝗸", cb="back_to_admin", style="primary", icon="5255703720078879038")])
    return InlineKeyboardMarkup(rows)

def gn_rm_country_kb():
    rows = []
    for sn, svc in GN_DATA["services"].items():
        for cn in svc.get("countries", {}):
            rows.append([bc(f"{sn} → {cn}", cb=f"gnrmcnt:{sn}:{cn}",
                            style="danger", icon="5445267414562389170")])
    if not rows:
        rows = [[bc("❌ No Countries", cb="noop", style="danger")]]
    rows.append([bc("𝗕𝗮𝗰𝗸", cb="back_to_admin", style="primary", icon="5255703720078879038")])
    return InlineKeyboardMarkup(rows)


# ── Assign numbers to user (from main.go assignNumbersToUser) ─────────────────
async def gn_assign_numbers(bot, chat_id, msg_id, sn, cn):
    global GN_HOLD_SEQ
    gn_clear_hold(chat_id)
    svc = GN_DATA["services"].get(sn)
    if not svc:
        await bot.edit_message_text(chat_id=chat_id,message_id=msg_id,
            text="❌ Service no longer exists.",parse_mode="HTML"); return
    c = svc.get("countries",{}).get(cn)
    if not c:
        await bot.edit_message_text(chat_id=chat_id,message_id=msg_id,
            text="❌ Country no longer exists.",parse_mode="HTML"); return
    if not c.get("numbers"):
        await bot.edit_message_text(chat_id=chat_id,message_id=msg_id,
            text="❌ No numbers available right now.",parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [bc("𝗖𝗵𝗮𝗻𝗴𝗲 𝗖𝗼𝘂𝗻𝘁𝗿𝘆",cb=f"gnchcnt:{sn}",style="success",icon="6204058135695464033")],
                [bc("𝗥𝗲𝗳𝗿𝗲𝘀𝗵",cb=f"gnrefresh:{sn}:{cn}",style="primary",icon="4956287101604725699")]])); return
    cycle = c.get("numbers_per_cycle",0) or GN_CYCLE_DEFAULT
    picked,remaining = gn_pick_numbers(c["numbers"],cycle)
    c["numbers"]=remaining; c["total_stock"]=max(0,c.get("total_stock",0)-len(picked))
    GN_DATA["services"][sn]["countries"][cn]=c; gn_save()
    GN_HOLD_SEQ+=1; tok=GN_HOLD_SEQ
    GN_HOLDS[str(chat_id)]={"chat_id":chat_id,"message_id":msg_id,"service":sn,"country":cn,
        "numbers":picked,"token":tok,"otp_limit":c.get("otp_limit",0),
        "number_otp_count":{},"used":{},"expires_at":time.time()+GN_HOLD_SECS}
    gn_save_holds()
    flag=gn_flag(c.get("code","")); em=gn_svc_emoji(sn)
    hdr=(f"{flag} {em} <b>{c.get('name',cn)} Numbers Assigned</b> "
         f'<tg-emoji emoji-id="6206479140040743133">✅</tg-emoji>\n\n'
         f'<tg-emoji emoji-id="6206508629286196237">🔔</tg-emoji> '
         f"<b>Waiting for OTP........ "
         f'<tg-emoji emoji-id="6206118633370818254">⌛</tg-emoji> 20min</b>')
    await bot.edit_message_text(chat_id=chat_id,message_id=msg_id,text=hdr,
        parse_mode="HTML",reply_markup=gn_numbers_kb(sn,cn,picked,c.get("otp_group","")))
    asyncio.get_event_loop().call_later(GN_HOLD_SECS,
        lambda: asyncio.ensure_future(gn_expire_hold(bot,chat_id,tok)))

async def gn_expire_hold(bot,chat_id,tok):
    key=str(chat_id)
    hold=GN_HOLDS.get(key)
    if not hold or hold.get("token")!=tok: return
    GN_HOLDS.pop(key,None)
    used=hold.get("used",{}); used_c=sum(1 for n in hold.get("numbers",[]) if used.get(re.sub(r'\D','',n)))
    gn_release_hold(hold); gn_save_holds()
    ret=len(hold.get("numbers",[]))-used_c
    if used_c==0:   txt="⏱ <b>Time expired</b> — no OTP received. Numbers returned to stock."
    elif ret==0:    txt="✅ <b>Session ended</b> — OTP delivered for all assigned numbers."
    else:           txt=(f"⏱ <b>Time expired</b> — OTP received for {used_c} number(s); "
                         f"{ret} returned to stock.")
    try:
        await bot.edit_message_text(chat_id=chat_id,message_id=hold["message_id"],
            text=txt,parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[bc("𝗚𝗲𝘁 𝗡𝘂𝗺𝗯𝗲𝗿 𝗔𝗴𝗮𝗶𝗻",cb=f"gnchcnt:{hold['service']}",style="success",icon="5296369303661067030")]]))
    except: pass


# ═══════════════════════════════════════════════════════════════
#  USER BUTTON REPLY HANDLERS (from main.go)
# ═══════════════════════════════════════════════════════════════
async def gn_cmd_get_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id
    gn_upsert_user(uid,update.effective_user.username or "",
        update.effective_user.first_name or "","")
    if not GN_DATA["services"]:
        await update.message.reply_text("❌ No services available yet.",parse_mode="HTML"); return
    await update.message.reply_text(
        f'<tg-emoji emoji-id="6206090539989734881">🔝</tg-emoji> <b>Select Service</b>\n'
        f'━━━━━━━━━━━━━━━━━━━━━━\n'
        f'<tg-emoji emoji-id="6204177183598974956">⬇️</tg-emoji> Choose a service below:',
        parse_mode="HTML",reply_markup=gn_services_kb())

async def gn_cmd_my_account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from html import escape
    uid=update.effective_user.id
    u=gn_upsert_user(uid,update.effective_user.username or "",
        escape(update.effective_user.first_name or ""),
        escape(update.effective_user.last_name or ""))
    rate=GN_DATA.get("usd_to_pkr",GN_USD_RATE) or GN_USD_RATE
    usdt=u.get("balance",0.0)/rate
    await update.message.reply_text(
        f'<tg-emoji emoji-id="6237864166879663987">🤖</tg-emoji> <b>𝗠𝘆 𝗔𝗰𝗰𝗼𝘂𝗻𝘁</b>\n\n'
        f'<tg-emoji emoji-id="5242442819573927209">👤</tg-emoji> 𝗡𝗮𝗺𝗲: {u.get("first_name","")} {u.get("last_name","")}\n'
        f'<tg-emoji emoji-id="5467889436807157272">ℹ️</tg-emoji> 𝗜𝗗: <code>{uid}</code>\n'
        f'<tg-emoji emoji-id="6176966310920983412">🔑</tg-emoji> 𝗧𝗼𝘁𝗮𝗹 𝗢𝗧𝗣𝘀: <b>{u.get("total_otps",0)}</b>\n'
        f'<tg-emoji emoji-id="6190336264940559752">💰</tg-emoji> 𝗕𝗮𝗹𝗮𝗻𝗰𝗲: <b>{u.get("balance",0.0):.2f} {GN_CURRENCY}</b>\n'
        f'<tg-emoji emoji-id="6206405459876779229">💸</tg-emoji> 𝗨𝗦𝗗𝗧: <b>{usdt:.4f} {GN_DOLLAR}</b>',
        parse_mode="HTML")

async def gn_cmd_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id
    u=gn_upsert_user(uid)
    rate=GN_DATA.get("usd_to_pkr",GN_USD_RATE) or GN_USD_RATE
    usdt=u.get("balance",0.0)/rate
    await update.message.reply_text(
        f'<tg-emoji emoji-id="6190336264940559752">💰</tg-emoji> <b>Your Balance</b>\n\n'
        f'<tg-emoji emoji-id="6206155797722830770">💵</tg-emoji> PKR Balance: <b>{u.get("balance",0.0):.2f} {GN_CURRENCY}</b>\n'
        f'   ≈ <b>{usdt:.4f} USDT</b>\n\n'
        f'<tg-emoji emoji-id="6204058135695464033">🌐</tg-emoji> 1 USDT = {rate:.0f} {GN_CURRENCY}\n\n'
        f'<tg-emoji emoji-id="6206479140040743133">✅</tg-emoji> <b>Total Withdrawable USDT: {usdt:.4f} $</b>',
        parse_mode="HTML")

async def gn_cmd_top_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    medals=[
        '<tg-emoji emoji-id="6206096153511990389">👑</tg-emoji>',
        '<tg-emoji emoji-id="6205965994528086727">💠</tg-emoji>',
        '<tg-emoji emoji-id="6204104220694550861">☄️</tg-emoji>',
    ]
    entries=[]
    for u in GN_DATA["users"].values():
        if u.get("total_otps",0)>0:
            name=(u.get("first_name","")+" "+u.get("last_name","")).strip() or u.get("username","") or "User"
            entries.append((name,u["total_otps"]))
    entries.sort(key=lambda x:x[1],reverse=True); entries=entries[:10]
    txt=(f'<tg-emoji emoji-id="6235252066554484059">🏆</tg-emoji>'
         f" <b>𝗧𝗼𝗽 𝟭𝟬 𝗨𝘀𝗲𝗿𝘀 — 𝗔𝗹𝗹 𝗧𝗶𝗺𝗲</b>\n\n")
    if not entries:
        txt+="𝗡𝗼 𝗢𝗧𝗣𝘀 𝗱𝗲𝗹𝗶𝘃𝗲𝗿𝗲𝗱 𝘆𝗲𝘁."
    else:
        for i,(name,otps) in enumerate(entries):
            m=medals[i] if i<3 else '<tg-emoji emoji-id="6206479140040743133">✅</tg-emoji>'
            txt+=f"{m} <b>{name}</b> — 𝗢𝗧𝗣𝘀: {otps}\n"
    await update.message.reply_text(txt,parse_mode="HTML")

async def gn_cmd_referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id
    u=gn_upsert_user(uid)
    ref_link=gn_ref_link(context.bot.username or "",uid)
    total,qual,pend,earned=gn_ref_stats(uid)
    await update.message.reply_text(
        f'<tg-emoji emoji-id="6190336264940559752">💰</tg-emoji> Balance: <b>{u.get("balance",0.0):.2f} {GN_CURRENCY}</b>\n'
        f'<tg-emoji emoji-id="6206497372176913599">🔗</tg-emoji> Referral link: {ref_link}\n'
        f'<tg-emoji emoji-id="5242442819573927209">👤</tg-emoji> Qualified: <b>{qual}</b> | ⏳ Pending: <b>{pend}</b>\n\n'
        f'<tg-emoji emoji-id="5343862721307748990">📊</tg-emoji> <b>Your Stats:</b>\n'
        f'▸ Total Referrals: <b>{total}</b>\n'
        f'▸ Qualified (Paid): <b>{qual}</b>\n'
        f'▸ Total Earned: <b>{earned:.2f} {GN_CURRENCY}</b>\n\n'
        f'━━━ <tg-emoji emoji-id="5262974657329394511">📝</tg-emoji> <b>Rules</b> ━━━\n'
        f'▸ Share your link with friends\n'
        f'▸ They must join via your link\n'
        f'▸ They get <b>{GN_REF_MILESTONE} OTPs</b> → you earn <b>{GN_REF_REWARD:.0f} {GN_CURRENCY}</b>\n'
        f'▸ Added to balance automatically',
        parse_mode="HTML")

async def gn_cmd_join_channels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f'<tg-emoji emoji-id="6206080502651164081">📣</tg-emoji> <b>𝗖𝗹𝗶𝗰𝗸 𝘁𝗼 𝗝𝗼𝗶𝗻 𝗢𝘂𝗿 𝗖𝗵𝗮𝗻𝗻𝗲𝗹𝘀</b> <tg-emoji emoji-id="6206027872121918710">🎁</tg-emoji>\n\n'
        f'<tg-emoji emoji-id="6235373579769222419">➡️</tg-emoji> 𝗦𝘁𝗮𝘆 𝘂𝗽𝗱𝗮𝘁𝗲𝗱 𝘄𝗶𝘁𝗵 𝗼𝘂𝗿 𝗹𝗮𝘁𝗲𝘀𝘁 𝗻𝗲𝘄𝘀!',
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [bc("𝗡𝘂𝗺𝗯𝗲𝗿𝘀 𝗖𝗵𝗮𝗻𝗻𝗲𝗹", url="https://t.me/junaidaliniz",    style="danger",  icon="6206497372176913599")],
            [bc("𝗖𝗵𝗮𝘁 𝗚𝗿𝗼𝘂𝗽",        url="https://t.me/+DrBDJM9-nvAyMjRk",   style="success", icon="6206080502651164081")],
            [bc("𝗢𝗧𝗣 𝗚𝗿𝗼𝘂𝗽",         url="https://t.me/junaidniz110", style="primary", icon="6206508629286196237")],
        ]))

async def gn_cmd_withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id
    u=gn_upsert_user(uid)
    if not GN_DATA.get("withdraw_enabled",True):
        await update.message.reply_text(
            f'<tg-emoji emoji-id="5974083768233760323">❌</tg-emoji> <b>Withdrawals Disabled</b>\n\n'
            f'<tg-emoji emoji-id="6206508629286196237">🔔</tg-emoji> Withdrawals are currently disabled.\n<i>Please check back later.</i>',
            parse_mode="HTML"); return
    rate=GN_DATA.get("usd_to_pkr",GN_USD_RATE) or GN_USD_RATE
    minw=GN_DATA.get("min_withdrawal",GN_MIN_WITHDRAW)
    minu=GN_DATA.get("min_withdrawal_usd",GN_MIN_USD)
    usdt=u.get("balance",0.0)/rate
    has_pkr=u.get("balance",0.0)>=minw; has_usd=usdt>=minu
    if not has_pkr and not has_usd:
        await update.message.reply_text(
            f'<tg-emoji emoji-id="5974083768233760323">❌</tg-emoji> <b>Insufficient Balance</b>\n\n'
            f'<tg-emoji emoji-id="6206155797722830770">💵</tg-emoji> PKR Balance: <b>{u.get("balance",0.0):.2f} {GN_CURRENCY}</b> (Min: {minw:.0f})\n'
            f'   ≈ <b>{usdt:.4f} USDT</b> (Min: {minu:.4f} $)',
            parse_mode="HTML"); return
    GN_WDRAW_STATES[uid]={"step":0}
    await update.message.reply_text(
        f'<tg-emoji emoji-id="6206155797722830770">💵</tg-emoji> <b>Withdraw Request</b>\n\n'
        f'<tg-emoji emoji-id="6190336264940559752">💰</tg-emoji> PKR Balance: <b>{u.get("balance",0.0):.2f} {GN_CURRENCY}</b>\n'
        f'   ≈ <b>{usdt:.4f} USDT</b>\n\n'
        f'<tg-emoji emoji-id="6204058135695464033">🌐</tg-emoji> 1 USDT = {rate:.0f} {GN_CURRENCY}\n\n'
        f'<tg-emoji emoji-id="6206479140040743133">✅</tg-emoji> <b>Total Withdrawable USDT: {usdt:.4f} $</b>\n\n'
        f'Which method do you want to withdraw?',
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [bc("𝗣𝗞𝗥 — 𝗘𝗮𝘀𝘆𝗣𝗮𝗶𝘀𝗮 / 𝗝𝗮𝘇𝘇𝗖𝗮𝘀𝗵",cb="gn_wd_pkr",style="success",icon="5778204036578678218")],
            [bc("𝗨𝗦𝗗𝗧 — 𝗕𝗶𝗻𝗮𝗻𝗰𝗲",cb="gn_wd_usdt",style="primary",icon="5409048419211682843")],
        ]))


# ═══════════════════════════════════════════════════════════════
#  WITHDRAW TEXT FLOW (multi-step)
# ═══════════════════════════════════════════════════════════════
async def gn_withdraw_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    uid=update.effective_user.id; txt=(update.message.text or "").strip()
    if uid not in GN_WDRAW_STATES: return False
    state=GN_WDRAW_STATES[uid]
    if txt in ("𝗕𝗮𝗰𝗸", "Back", "🔙 Back"):
        GN_WDRAW_STATES.pop(uid,None)
        await update.message.reply_text("🚀 <b>Main Menu</b>",parse_mode="HTML",
            reply_markup=smart_kb(uid)); return True
    step=state.get("step",0)
    if step==0: return True
    if step==1:
        try: amt=float(txt.replace(",",".")); assert amt>0
        except:
            await update.message.reply_text("❌ <b>Invalid amount.</b> Enter a number like <code>10</code>.",parse_mode="HTML"); return True
        u=gn_upsert_user(uid); rate=GN_DATA.get("usd_to_pkr",GN_USD_RATE) or GN_USD_RATE
        minw=GN_DATA.get("min_withdrawal",GN_MIN_WITHDRAW); minu=GN_DATA.get("min_withdrawal_usd",GN_MIN_USD)
        meth=state.get("method","pkr")
        if meth=="pkr":
            if amt<minw:
                await update.message.reply_text(f"❌ Amount too low. Minimum: <b>{minw:.0f} {GN_CURRENCY}</b>",parse_mode="HTML"); return True
            if amt>u.get("balance",0.0):
                await update.message.reply_text(f"❌ Insufficient PKR balance. Your balance: <b>{u.get('balance',0.0):.2f} {GN_CURRENCY}</b>",parse_mode="HTML"); return True
            state["step"]=2; state["amount"]=amt
            await update.message.reply_text(
                f"💵 <b>Withdraw — Step 2/3</b>\n\n💵 PKR Amount: <b>{amt:.2f} {GN_CURRENCY}</b>\n\n"
                f"📋 Send your payment details:\n<i>Example: <code>JazzCash 03001234567 - John Doe</code></i>",
                parse_mode="HTML")
        else:
            usdt=u.get("balance",0.0)/rate
            if amt<minu:
                await update.message.reply_text(f"❌ Amount too low. Minimum: <b>{minu:.4f} $</b>",parse_mode="HTML"); return True
            if amt>usdt:
                await update.message.reply_text(f"❌ Insufficient balance. Withdrawable USDT: <b>{usdt:.4f} $</b>",parse_mode="HTML"); return True
            state["step"]=2; state["amount_usd"]=amt
            await update.message.reply_text(
                f"💵 <b>Withdraw — Step 2/3</b>\n\n💲 USDT Amount: <b>{amt:.4f} $</b>\n\n"
                f"📋 Send your <b>Binance ID</b>:\n<i>Example: <code>123456789</code></i>",
                parse_mode="HTML")
        return True
    if step==2:
        if not txt:
            await update.message.reply_text("❌ Please send your payment details.",parse_mode="HTML"); return True
        state["step"]=3; state["details"]=txt; meth=state.get("method","pkr")
        amt=state.get("amount",0.0); amt_usd=state.get("amount_usd",0.0)
        if meth=="pkr":
            sm=(f"💵 <b>Withdraw — Step 3/3</b>\n\n📋 <b>Review:</b>\n\n"
                f"💵 Method: <b>PKR (EasyPaisa / JazzCash)</b>\n💰 Amount: <b>{amt:.2f} {GN_CURRENCY}</b>\n\n"
                f"📞 Payment Details:\n<code>{txt}</code>\n\n⚠️ Balance deducted on confirm.")
        else:
            rate=GN_DATA.get("usd_to_pkr",GN_USD_RATE) or GN_USD_RATE
            sm=(f"💵 <b>Withdraw — Step 3/3</b>\n\n📋 <b>Review:</b>\n\n"
                f"💲 Method: <b>USDT (Binance)</b>\n💰 Amount: <b>{amt_usd:.4f} $</b>"
                f" (≈ {amt_usd*rate:.2f} {GN_CURRENCY})\n\n"
                f"🆔 Binance ID:\n<code>{txt}</code>")
        await update.message.reply_text(sm,parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [bc("𝗖𝗼𝗻𝗳𝗶𝗿𝗺",cb="gn_wd_confirm",style="success",icon="6206479140040743133"),
                 bc("𝗖𝗮𝗻𝗰𝗲𝗹",cb="gn_wd_cancel",style="danger",icon="5974083768233760323")]])); return True
    return False


# ═══════════════════════════════════════════════════════════════
#  ADMIN WIZARD: ADD NUMBERS (7-step) + BROADCAST TEXT HANDLER
# ═══════════════════════════════════════════════════════════════
async def gn_admin_wizard_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    uid=update.effective_user.id; txt=(update.message.text or "").strip()
    if uid not in GN_WIZARD_STATES or not is_admin(uid): return False
    state=GN_WIZARD_STATES[uid]
    if txt in ("𝗕𝗮𝗰𝗸", "Back", "🔙 Back") or txt == "menu_numbers":
        GN_WIZARD_STATES.pop(uid,None)
        await update.message.reply_text(
            f'<tg-emoji emoji-id="6205965994528086727">💠</tg-emoji> <b>ADMIN PANEL</b>\n'
            f'━━━━━━━━━━━━━━━━━━━━━━\n'
            f'<tg-emoji emoji-id="6235572922086331108">🧑‍💻</tg-emoji> Select an option:',
            parse_mode="HTML", reply_markup=get_admin_keyboard(uid)); return True
    step=state.get("step")
    cancel_kb=InlineKeyboardMarkup([[bc("𝗖𝗮𝗻𝗰𝗲𝗹",cb="gnadm_cancel",style="danger",icon="5974083768233760323")]])

    if step == "svc":
        state["svc"] = txt; state["step"] = "cnt"
        await update.message.reply_text(
            f"{gn_icon('check')} Service: <b>{txt}</b>\n\n"
            f"{gn_icon('globe')} <b>Step 2/7 — Country Name</b>\n\n"
            f"Enter country name:\n<i>Example: Slovenia, Algeria, France</i>",
            parse_mode="HTML", reply_markup=get_back_keyboard()); return True

    if step == "cnt":
        state["cnt"] = txt; state["step"] = "code"
        await update.message.reply_text(
            f"{gn_icon('check')} Country: <b>{txt}</b>\n\n"
            f"{gn_icon('earth')} <b>Step 3/7 — Country Code</b>\n\n"
            f"Enter 2-letter country code:\n<i>Example: SI, DZ, FR, PK, US</i>",
            parse_mode="HTML", reply_markup=get_back_keyboard()); return True

    if step == "code":
        state["code"] = txt.upper(); state["step"] = "price"
        flag = gn_flag(txt.upper())
        await update.message.reply_text(
            f"{gn_icon('check')} Code: <b>{txt.upper()}</b> {flag}\n\n"
            f"{gn_icon('money')} <b>Step 4/7 — Price in Rs</b>\n\n"
            f"Enter price:\n<i>Example: 1 or 2 or 1.5</i>",
            parse_mode="HTML", reply_markup=get_back_keyboard()); return True

    if step == "price":
        try: price = float(txt)
        except:
            await update.message.reply_text(
                f"{gn_icon('cancel')} Invalid price. Enter a number like <code>1</code>",
                parse_mode="HTML"); return True
        state["price"] = price; state["step"] = "cycle"
        await update.message.reply_text(
            f"{gn_icon('check')} PKR Price: <b>{price:.2f} {GN_CURRENCY}</b>\n\n"
            f"{gn_icon('people')} <b>Step 5/7 — Numbers Per Cycle</b>\n\n"
            f"How many numbers should each user receive per session?\n"
            f"<i>Example: 3 or 5 or 10</i>",
            parse_mode="HTML", reply_markup=get_back_keyboard()); return True

    if step == "cycle":
        try: n = int(txt); assert n >= 1
        except:
            await update.message.reply_text(
                f"{gn_icon('cancel')} Invalid number. Enter a whole number like <code>3</code>",
                parse_mode="HTML"); return True
        state["cycle"] = n; state["step"] = "otplim"
        await update.message.reply_text(
            f"{gn_icon('check')} Numbers per cycle: <b>{n}</b>\n\n"
            f"{gn_icon('otp')} <b>Step 6/7 — OTP Limit Per Number</b>\n\n"
            f"How many OTPs should be sent to user DM per number?\n\n"
            f"<i>Example: 1 = only 1 OTP per number, 3 = 3 OTPs then stop DMing\n"
            f"Send 0 for unlimited</i>",
            parse_mode="HTML", reply_markup=get_back_keyboard()); return True

    if step == "otplim":
        try: n = int(txt); assert n >= 0
        except:
            await update.message.reply_text(
                f"{gn_icon('cancel')} Invalid. Enter 0 for unlimited or a number like <code>1</code>",
                parse_mode="HTML"); return True
        state["otplim"] = n; state["staged"] = state.get("staged", []); state["step"] = "nums"
        lim = "Unlimited" if n == 0 else f"{n} OTP(s) per number"
        await update.message.reply_text(
            f"{gn_icon('check')} OTP limit: <b>{lim}</b>\n\n"
            f"{gn_icon('phone')} <b>Step 7/7 — Phone Numbers</b>\n\n"
            f"Send numbers one per line:\n\n"
            f"<code>+38665761402\n+38665884088\n+38665703698</code>\n\n"
            f"OR upload a <b>.txt file</b>",
            parse_mode="HTML", reply_markup=get_back_keyboard()); return True

    if step == "nums":
        new = [l.strip() for l in txt.splitlines() if l.strip()]
        if not new:
            await update.message.reply_text(
                f"{gn_icon('cancel')} No numbers found. Try again or upload .txt",
                parse_mode="HTML"); return True
        state.setdefault("staged", []).extend(new)
        await gn_staged_preview(update.message, uid, state); return True

    # Balance add
    if step=="bal_uid":
        state["buid"]=txt; state["step"]="bal_amt"
        await update.message.reply_text(f"User ID: <code>{txt}</code>\n\nEnter amount to add ({GN_CURRENCY}):",parse_mode="HTML"); return True
    if step=="bal_amt":
        try: amt=float(txt)
        except:
            await update.message.reply_text("❌ Invalid amount.",parse_mode="HTML"); return True
        uk=state.get("buid",""); GN_WIZARD_STATES.pop(uid,None)
        if uk in GN_DATA["users"]:
            GN_DATA["users"][uk]["balance"]=GN_DATA["users"][uk].get("balance",0.0)+amt; gn_save()
            nb=GN_DATA["users"][uk]["balance"]
            await update.message.reply_text(f"✅ Added <b>{amt:.0f} {GN_CURRENCY}</b> to <code>{uk}</code>\nNew balance: <b>{nb:.0f} {GN_CURRENCY}</b>",
                parse_mode="HTML",reply_markup=get_admin_keyboard(uid))
        else:
            await update.message.reply_text("❌ User not found.",parse_mode="HTML",reply_markup=get_admin_keyboard(uid))
        return True

    # ── User info lookup ──────────────────────────────────────
    if step == "user_info":
        GN_WIZARD_STATES.pop(uid, None)
        try: target = int(txt.strip())
        except:
            await update.message.reply_text("❌ Invalid User ID.",parse_mode="HTML",
                reply_markup=get_admin_keyboard(uid)); return True
        key = str(target); u = GN_DATA["users"].get(key)
        if not u:
            await update.message.reply_text(f"❌ User <code>{target}</code> not found.",
                parse_mode="HTML",reply_markup=get_admin_keyboard(uid)); return True
        name = u.get("first_name","")
        if u.get("username"): name += f" (@{u['username']})"
        total_ref=qual_ref=0
        for uu in GN_DATA["users"].values():
            if uu.get("referred_by")==target:
                total_ref+=1
                if uu.get("referral_reward_given"): qual_ref+=1
        rate = GN_DATA.get("usd_to_pkr", GN_USD_RATE) or GN_USD_RATE
        bal = u.get("balance",0.0); usdt = bal/rate
        txt2=(f"ℹ️ <b>User Info</b>\n\n"
             f"👤 <b>Name:</b> {name}\n🆔 <b>ID:</b> <code>{target}</code>\n\n"
             f"🔔 <b>Today OTPs:</b> {u.get('today_otps',0)}\n"
             f"📊 <b>Total OTPs:</b> {u.get('total_otps',0)}\n\n"
             f"💰 <b>Balance:</b> {bal:.2f} {GN_CURRENCY} (≈ {usdt:.4f} USDT)\n\n"
             f"🔗 <b>Total Referrals:</b> {total_ref}\n"
             f"✅ <b>Qualified:</b> {qual_ref}\n"
             f"📅 <b>Joined:</b> {u.get('joined_at','Unknown')}")
        await update.message.reply_text(txt2,parse_mode="HTML",
            reply_markup=get_admin_keyboard(uid)); return True

    # ── Min withdrawal settings ───────────────────────────────
    if step == "minwd":
        GN_WIZARD_STATES.pop(uid, None)
        parts = dict(p.split(":") for p in txt.upper().split() if ":" in p)
        changed = []
        if "PKR" in parts:
            try: GN_DATA["min_withdrawal"]=float(parts["PKR"]); changed.append(f"PKR min: {parts['PKR']}")
            except: pass
        if "USDT" in parts:
            try: GN_DATA["min_withdrawal_usd"]=float(parts["USDT"]); changed.append(f"USDT min: {parts['USDT']}")
            except: pass
        if "RATE" in parts:
            try: GN_DATA["usd_to_pkr"]=float(parts["RATE"]); changed.append(f"Rate: {parts['RATE']}")
            except: pass
        if changed: gn_save()
        res = "\n".join(f"✅ {c}" for c in changed) if changed else "❌ Nothing changed."
        await update.message.reply_text(f"💰 <b>Settings Updated</b>\n\n{res}",
            parse_mode="HTML", reply_markup=get_admin_keyboard(uid)); return True

    return False

async def gn_staged_preview(msg, uid, state):
    total = len(state.get("staged", []))
    nums  = state["staged"]
    if total <= 5:
        preview = "\n".join(nums)
    else:
        preview = "\n".join(nums[:3]) + f"\n... and {total-3} more"
    await msg.reply_text(
        f"{gn_icon('check')} <b>Staged: {total} numbers</b>\n\n"
        f"Send more files/lines to add more, or confirm:\n\n"
        f"<code>{preview}</code>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(
                f"𝗖𝗼𝗻𝗳𝗶𝗿𝗺 — {total} Numbers",
                callback_data="gnadm_confirm_nums",
                api_kwargs={"icon_custom_emoji_id": "6206479140040743133", "style": "success"}
            )],
            [InlineKeyboardButton(
                "𝗖𝗹𝗲𝗮𝗿 𝗔𝗹𝗹",
                callback_data="gnadm_clear_staged",
                api_kwargs={"icon_custom_emoji_id": "6206488264914703123", "style": "danger"}
            )],
        ])
    )

async def gn_commit_numbers(bot, chat_id, uid):
    state = GN_WIZARD_STATES.get(uid)
    if not state: return
    nums   = state.get("staged", []); sn = state.get("svc", ""); cn = state.get("cnt", "")
    code   = state.get("code", "");   price  = state.get("price", 0.0)
    cycle  = state.get("cycle", GN_CYCLE_DEFAULT); otplim = state.get("otplim", 0)
    GN_WIZARD_STATES.pop(uid, None)

    if sn not in GN_DATA["services"]:
        GN_DATA["services"][sn] = {"name": sn, "emoji": "", "countries": {}}
    svc = GN_DATA["services"][sn]; svc.setdefault("countries", {})
    c = svc["countries"].get(cn, {})
    c.update({"name": cn, "code": code, "price": price,
               "otp_group": GN_OTP_GROUP_URL, "numbers_per_cycle": cycle, "otp_limit": otplim})
    c.setdefault("numbers", []).extend(nums)
    c["total_stock"] = len(c["numbers"])
    svc["countries"][cn] = c; gn_save()

    rate   = GN_DATA.get("usd_to_pkr", GN_USD_RATE) or GN_USD_RATE
    pu     = price / rate
    lim    = "Unlimited" if otplim == 0 else f"{otplim} per number"
    total  = len(c["numbers"])
    flag   = gn_flag(code); em = gn_svc_emoji(sn)

    # ── Admin confirmation — exact main.go commitNumbers format ──
    await bot.send_message(chat_id=chat_id, parse_mode="HTML",
        reply_markup=get_admin_action_keyboard(),
        text=(
            f"{gn_icon('check')} <b>Numbers Added!</b>\n\n"
            f"{em} Service: <b>{sn}</b>\n"
            f"{flag} Country: <b>{cn}</b>\n"
            f"{gn_icon('money')} Price: <b>{price:.2f} {GN_CURRENCY}</b> / <b>{pu:.6f} $</b>\n"
            f"{gn_icon('people')} Per cycle: <b>{cycle} numbers</b>\n"
            f"{gn_icon('otp')} OTP limit: <b>{lim}</b>\n"
            f"{gn_icon('phone')} Added now: <b>{len(nums)}</b>\n"
            f"{gn_icon('chart')} Total in pool: <b>{total}</b>"
        ))

    # ── Auto Broadcast — exact main.go broadcastText format ──
    bcast = (
        f'<tg-emoji emoji-id="6206479140040743133">✅</tg-emoji> <b>Numbers Added!</b>\n\n'
        f'{em} <b>Service:</b> {sn}\n'
        f'{flag} <b>Country:</b> {cn}\n'
        f'<tg-emoji emoji-id="6190336264940559752">💰</tg-emoji> <b>Price:</b> {price:.2f} {GN_CURRENCY} / {pu:.6f} $\n'
        f'<tg-emoji emoji-id="5242442819573927209">👋</tg-emoji> <b>Per cycle:</b> {cycle} numbers\n'
        f'<tg-emoji emoji-id="6206508629286196237">🔔</tg-emoji> <b>OTP limit:</b> {lim}\n'
        f'<tg-emoji emoji-id="5312310156384557787">📱</tg-emoji> <b>Added now:</b> {len(nums)}\n'
        f'<tg-emoji emoji-id="5343862721307748990">📊</tg-emoji> <b>Total in pool:</b> {total}'
    )
    # Get Number button — emoji 5427168083074628963, style success
    get_num_kb = InlineKeyboardMarkup([[
        InlineKeyboardButton(
            "𝗚𝗲𝘁 𝗡𝘂𝗺𝗯𝗲𝗿",
            callback_data=f"gnsvc:{sn}",
            api_kwargs={"icon_custom_emoji_id": "5427168083074628963", "style": "success"}
        )
    ]])
    asyncio.create_task(gn_auto_broadcast(bot, bcast, get_num_kb))
    for gid in load_groups():
        try: await bot.send_message(chat_id=gid, text=bcast, parse_mode="HTML", reply_markup=get_num_kb)
        except: pass

async def gn_auto_broadcast(bot, text, kb=None):
    """Auto-broadcast added numbers to all users (from main.go)."""
    sent=failed=0
    for key in list(GN_DATA["users"].keys()):
        try:
            await bot.send_message(chat_id=int(key),text=text,parse_mode="HTML",reply_markup=kb)
            sent+=1; await asyncio.sleep(0.05)
        except: failed+=1
    logger.info(f"[GN] Auto-broadcast: sent={sent} failed={failed}")


# ═══════════════════════════════════════════════════════════════
#  ADMIN DOCUMENT HANDLER: .txt upload for numbers
# ═══════════════════════════════════════════════════════════════
async def gn_admin_doc_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    uid=update.effective_user.id
    if uid not in GN_WIZARD_STATES or not is_admin(uid): return False
    state=GN_WIZARD_STATES[uid]
    if state.get("step")!="nums": return False
    doc=update.message.document
    if not doc or not doc.file_name.lower().endswith(".txt"):
        await update.message.reply_text("❌ Please upload a .txt file.",parse_mode="HTML"); return True
    try:
        f=await context.bot.get_file(doc.file_id); data=await f.download_as_bytearray()
        new=[l.strip() for l in data.decode("utf-8").splitlines() if l.strip()]
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}",parse_mode="HTML"); return True
    if not new:
        await update.message.reply_text("❌ File is empty.",parse_mode="HTML"); return True
    state.setdefault("staged",[]).extend(new)
    await gn_staged_preview(update.message,uid,state); return True


# ═══════════════════════════════════════════════════════════════
#  MANUAL BROADCAST HANDLER (admin → Broadcast button)
# ═══════════════════════════════════════════════════════════════
def _entities_to_html(text: str, entities: list) -> str:
    """Convert message entities to HTML — exact main.go entitiesToHTML.
    Preserves bold, italic, code, custom_emoji (premium emojis), text_links, etc."""
    if not text or not entities:
        from html import escape as _esc
        return _esc(text or "")
    import html as _html
    tags = []
    for e in entities:
        etype  = e.type; offset = e.offset; length = e.length
        if etype == "bold":            tags += [(offset,True,"<b>"),(offset+length,False,"</b>")]
        elif etype == "italic":        tags += [(offset,True,"<i>"),(offset+length,False,"</i>")]
        elif etype == "underline":     tags += [(offset,True,"<u>"),(offset+length,False,"</u>")]
        elif etype == "strikethrough": tags += [(offset,True,"<s>"),(offset+length,False,"</s>")]
        elif etype == "spoiler":       tags += [(offset,True,"<tg-spoiler>"),(offset+length,False,"</tg-spoiler>")]
        elif etype == "code":          tags += [(offset,True,"<code>"),(offset+length,False,"</code>")]
        elif etype == "pre":           tags += [(offset,True,"<pre>"),(offset+length,False,"</pre>")]
        elif etype == "text_link":
            url = _html.escape(e.url or "")
            tags += [(offset,True,f'<a href="{url}">'),(offset+length,False,"</a>")]
        elif etype == "custom_emoji":
            eid = e.custom_emoji_id or ""
            if eid:
                tags += [(offset,True,f'<tg-emoji emoji-id="{eid}">'),(offset+length,False,"</tg-emoji>")]
    tags.sort(key=lambda x:(x[0],not x[1]))
    utf16 = text.encode("utf-16-le")
    def s16(a,b): return utf16[a*2:b*2].decode("utf-16-le")
    result=""; last=0
    for pos,is_open,tag in tags:
        if pos>last: result+=_html.escape(s16(last,pos))
        result+=tag; last=pos
    total=len(utf16)//2
    if last<total: result+=_html.escape(s16(last,total))
    return result

async def media_broadcast_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle photo/video/voice messages for broadcast."""
    uid = update.effective_user.id
    if uid not in GN_BCAST_STATES or not is_admin(uid):
        return
    await gn_broadcast_text(update, context)


async def gn_broadcast_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Broadcast handler — supports text/photo/video/voice + premium emoji preservation."""
    uid = update.effective_user.id
    if uid not in GN_BCAST_STATES or not is_admin(uid): return False
    state = GN_BCAST_STATES[uid]
    msg   = update.message
    txt   = (msg.text or msg.caption or "").strip()

    # Back / cancel
    if txt in ("Back","🔙 Back","𝗕𝗮𝗰𝗸","🔙 𝗕𝗮𝗰𝗸") and msg.text:
        GN_BCAST_STATES.pop(uid, None)
        await msg.reply_text(
            f'<tg-emoji emoji-id="5974083768233760323">❌</tg-emoji> Broadcast cancelled.',
            parse_mode="HTML", reply_markup=get_numbers_menu()); return True

    if state.get("step") == "await":
        payload = {}
        _cu = db.cursor(); _cu.execute("SELECT COUNT(*) FROM tg_users"); total = _cu.fetchone()[0]
        confirm_kb = InlineKeyboardMarkup([
            [bc("📣 𝗦𝗲𝗻𝗱 𝘁𝗼 𝗔𝗹𝗹", cb="nb_do_broadcast",  style="success", icon="6206080502651164081"),
             bc("❌ 𝗖𝗮𝗻𝗰𝗲𝗹",      cb="nb_cancel_bcast", style="danger",  icon="5974083768233760323")]
        ])

        if msg.photo:
            # Caption HTML is safe — it's plain HTML we built without custom_emoji tags
            cap = _entities_to_html(msg.caption or "", list(msg.caption_entities or []))
            payload = {"media_id": msg.photo[-1].file_id, "media_type": "photo", "text": cap}
            prev_hdr = (f'<tg-emoji emoji-id="6206080502651164081">📣</tg-emoji>'
                        f' <b>Preview</b> — {total} users\n\n🖼 <b>Image + caption below</b>'
                        + (f"\n\n{cap}" if cap else ""))
            GN_BCAST_STATES[uid] = {"step": "confirm", "payload": payload}
            await msg.reply_text(prev_hdr, parse_mode="HTML", reply_markup=confirm_kb)

        elif msg.video:
            cap = _entities_to_html(msg.caption or "", list(msg.caption_entities or []))
            payload = {"media_id": msg.video.file_id, "media_type": "video", "text": cap}
            prev_hdr = (f'<tg-emoji emoji-id="6206080502651164081">📣</tg-emoji>'
                        f' <b>Preview</b> — {total} users\n\n🎬 <b>Video + caption below</b>'
                        + (f"\n\n{cap}" if cap else ""))
            GN_BCAST_STATES[uid] = {"step": "confirm", "payload": payload}
            await msg.reply_text(prev_hdr, parse_mode="HTML", reply_markup=confirm_kb)

        elif msg.voice:
            payload = {"media_id": msg.voice.file_id, "media_type": "voice", "text": ""}
            GN_BCAST_STATES[uid] = {"step": "confirm", "payload": payload}
            await msg.reply_text(
                f'<tg-emoji emoji-id="6206080502651164081">📣</tg-emoji>'
                f' <b>Preview</b> — {total} users\n\n🎤 <b>Voice Note</b>',
                parse_mode="HTML", reply_markup=confirm_kb)

        else:
            # ── TEXT broadcast ──────────────────────────────────────────────────
            # Store orig_chat + orig_mid so nb_run_broadcast uses copy_message.
            # NEVER put the rendered HTML into the preview message — Telegram
            # will reject <tg-emoji> tags the bot itself sends (Entity_text_invalid).
            # We forward the original message as the preview instead.
            rendered = _entities_to_html(msg.text or "", list(msg.entities or []))
            payload  = {
                "media_type": "text",
                "text":       rendered,
                "orig_chat":  msg.chat_id,
                "orig_mid":   msg.message_id,
            }
            GN_BCAST_STATES[uid] = {"step": "confirm", "payload": payload}

            # Send a plain header first (no embedded HTML from user message)
            await msg.reply_text(
                f'<tg-emoji emoji-id="6206080502651164081">📣</tg-emoji>'
                f' <b>Broadcast Preview</b> — {total} users\n\n'
                f'<tg-emoji emoji-id="6204177183598974956">⬇️</tg-emoji>'
                f' Your message is shown above ☝️\n\n'
                f'<tg-emoji emoji-id="6206479140040743133">✅</tg-emoji>'
                f' Confirm below to send to all users.',
                parse_mode="HTML", reply_markup=confirm_kb)

        return True
    return False


async def nb_run_broadcast(bot, admin_chat_id: int, payload: dict):
    """
    Broadcast to ALL users — merges tg_users SQLite + GN_DATA users.
    Uses copy_message for text (preserves <tg-emoji> and all entities).
    Detailed debug logging so every step is visible in logs.
    """
    media_type = payload.get("media_type", "text")
    user_ids = get_broadcast_user_ids()

    sent = failed = 0
    removed = []

    logger.info(
        "[broadcast] START type=%s users=%d",
        media_type,
        len(user_ids),
    )

    if not user_ids:
        logger.warning("[broadcast] ⚠️ no users found in tg_users or GN_DATA")
        try:
            await bot.send_message(
                chat_id=admin_chat_id,
                text=(
                    "⚠️ <b>Broadcast failed</b>\n\n"
                    "No users are registered yet."
                ),
                parse_mode="HTML",
            )
        except Exception:
            pass
        return

    for user_id in user_ids:
        try:
            if media_type == "text":
                source_chat = payload.get("orig_chat")
                source_message = payload.get("orig_mid")
                if source_chat and source_message:
                    await bot.copy_message(
                        chat_id=user_id,
                        from_chat_id=source_chat,
                        message_id=source_message,
                    )
                else:
                    await bot.send_message(
                        chat_id=user_id,
                        text=payload.get("text", ""),
                        parse_mode="HTML",
                    )
            elif media_type == "photo":
                await bot.send_photo(
                    chat_id=user_id,
                    photo=payload["media_id"],
                    caption=payload.get("text") or None,
                    parse_mode="HTML" if payload.get("text") else None,
                )
            elif media_type == "video":
                await bot.send_video(
                    chat_id=user_id,
                    video=payload["media_id"],
                    caption=payload.get("text") or None,
                    parse_mode="HTML" if payload.get("text") else None,
                )
            elif media_type == "voice":
                await bot.send_voice(
                    chat_id=user_id,
                    voice=payload["media_id"],
                )

            sent += 1
            logger.info("[broadcast] sent to %s", user_id)

        except Exception as error:
            failed += 1
            error_text = str(error).lower()

            logger.error(
                "[broadcast] failed for %s: %s",
                user_id,
                error,
            )

            if any(
                phrase in error_text
                for phrase in (
                    "blocked",
                    "deactivated",
                    "chat not found",
                    "forbidden",
                    "user is deactivated",
                    "403",
                )
            ):
                removed.append(user_id)

        await asyncio.sleep(0.1)

    if removed:
        c = db.cursor()
        c.executemany(
            "DELETE FROM tg_users WHERE user_id = ?",
            [(user_id,) for user_id in removed],
        )
        db.commit()

    logger.info(
        "[broadcast] COMPLETE sent=%d failed=%d removed=%d",
        sent,
        failed,
        len(removed),
    )

    try:
        await bot.send_message(
            chat_id=admin_chat_id,
            text=(
                "✅ <b>Broadcast Complete</b>\n\n"
                f"✅ Sent: <code>{sent}</code>\n"
                f"❌ Failed: <code>{failed}</code>\n"
                f"🗑 Removed: <code>{len(removed)}</code>"
            ),
            parse_mode="HTML",
        )
    except Exception as e:
        logger.warning(f"[broadcast] summary failed: {e}")






# ═══════════════════════════════════════════════════════════════
#  GN CALLBACK HANDLER — all new callbacks from main.go
# ═══════════════════════════════════════════════════════════════
async def gn_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Returns True if callback was consumed by GN system."""
    query=update.callback_query; data=query.data
    uid=query.from_user.id; chat=query.message.chat_id; mid=query.message.message_id

    # ── Service / Country navigation ─────────────────────────
    if data=="gn_services":
        await query.answer()
        await query.edit_message_text(
            f'<tg-emoji emoji-id="6206090539989734881">🔝</tg-emoji> <b>Select Service</b>\n'
            f'━━━━━━━━━━━━━━━━━━━━━━\n'
            f'<tg-emoji emoji-id="6204177183598974956">⬇️</tg-emoji> Choose a service below:',
            parse_mode="HTML",reply_markup=gn_services_kb()); return True

    if data=="gn_backmain":
        await query.answer()
        from html import escape; first=escape(query.from_user.first_name or "User")
        await query.edit_message_text(
            f"👋 <b>HI {first}</b>\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"💎 <b>Junaid OTP</b>\n⚡ Fastest OTP Service\n"
            f"🤖 Auto-Assign System\n\n👆 <b>Select an option:</b>",
            parse_mode="HTML",reply_markup=smart_kb(uid)); return True

    if data.startswith("gnsvc:"):
        await query.answer()
        sn=data[6:]
        svc_em = gn_svc_emoji(sn)
        await query.edit_message_text(
            f'<tg-emoji emoji-id="6206090539989734881">🔝</tg-emoji> {svc_em} <b>{sn}</b>\n'
            f'━━━━━━━━━━━━━━━━━━━━━━\n'
            f'<tg-emoji emoji-id="6204177183598974956">⬇️</tg-emoji> <b>Select Country:</b>\n'
            f'<tg-emoji emoji-id="6206112371308500200">✉️</tg-emoji> <i>OTP will be sent to your DM</i>',
            parse_mode="HTML",reply_markup=gn_countries_kb(sn)); return True

    if data.startswith("gncnt:"):
        await query.answer()
        parts=data[6:].split(":",1)
        if len(parts)==2: await gn_assign_numbers(context.bot,chat,mid,parts[0],parts[1])
        return True

    if data.startswith("gnchcnt:"):
        await query.answer()
        sn=data[8:]; gn_clear_hold(chat)
        svc_em = gn_svc_emoji(sn)
        await query.edit_message_text(
            f'<tg-emoji emoji-id="6206090539989734881">🔝</tg-emoji> {svc_em} <b>{sn}</b>\n'
            f'━━━━━━━━━━━━━━━━━━━━━━\n'
            f'<tg-emoji emoji-id="6204177183598974956">⬇️</tg-emoji> <b>Select Country:</b>\n'
            f'<tg-emoji emoji-id="6206112371308500200">✉️</tg-emoji> <i>OTP will be sent to your DM</i>',
            parse_mode="HTML",reply_markup=gn_countries_kb(sn)); return True

    if data.startswith("gnrefresh:"):
        await query.answer()
        parts=data[10:].split(":",1)
        if len(parts)==2: await gn_assign_numbers(context.bot,chat,mid,parts[0],parts[1])
        return True

    if data.startswith("gncopy:"):
        num=data[7:]
        await query.answer(f"📋 Number: {num}",show_alert=True); return True

    # ── My Account / Balance / Top Users / Referral inline ───
    if data=="gn_myacc":
        await query.answer()
        from html import escape
        u=gn_upsert_user(uid,query.from_user.username or "",
            escape(query.from_user.first_name or ""),escape(query.from_user.last_name or ""))
        rate=GN_DATA.get("usd_to_pkr",GN_USD_RATE) or GN_USD_RATE; usdt=u.get("balance",0.0)/rate
        await query.edit_message_text(
            f"🤖 <b>𝗠𝘆 𝗔𝗰𝗰𝗼𝘂𝗻𝘁</b>\n\n"
            f"👤 𝗡𝗮𝗺𝗲: {u.get('first_name','')} {u.get('last_name','')}\n"
            f"ℹ️ 𝗜𝗗: <code>{uid}</code>\n"
            f"🔑 𝗧𝗼𝘁𝗮𝗹 𝗢𝗧𝗣𝘀: {u.get('total_otps',0)}\n"
            f"💰 𝗕𝗮𝗹𝗮𝗻𝗰𝗲: <b>{u.get('balance',0.0):.2f} {GN_CURRENCY}</b>\n"
            f"💸 𝗨𝗦𝗗𝗧: <b>{usdt:.4f} {GN_DOLLAR}</b>",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[bc("𝗕𝗮𝗰𝗸",cb="gn_backmain",style="primary",icon="5255703720078879038")]])); return True

    if data=="gn_balance":
        await query.answer()
        u=gn_upsert_user(uid); rate=GN_DATA.get("usd_to_pkr",GN_USD_RATE) or GN_USD_RATE; usdt=u.get("balance",0.0)/rate
        await query.edit_message_text(
            f"💰 <b>Your Balance</b>\n\n"
            f"💵 PKR: <b>{u.get('balance',0.0):.2f} {GN_CURRENCY}</b>\n   ≈ <b>{usdt:.4f} USDT</b>\n\n"
            f"1 USDT = {rate:.0f} {GN_CURRENCY}\n\n✅ <b>Withdrawable USDT: {usdt:.4f} $</b>",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[bc("𝗕𝗮𝗰𝗸",cb="gn_backmain",style="primary",icon="5255703720078879038")]])); return True

    if data=="gn_topusers":
        await query.answer()
        medals=["👑","💠","☄️"]; entries=[]
        for u in GN_DATA["users"].values():
            if u.get("total_otps",0)>0:
                name=(u.get("first_name","")+" "+u.get("last_name","")).strip() or u.get("username","") or "User"
                entries.append((name,u["total_otps"]))
        entries.sort(key=lambda x:x[1],reverse=True); entries=entries[:10]
        txt=f"🏆 <b>𝗧𝗼𝗽 𝟭𝟬 𝗨𝘀𝗲𝗿𝘀</b>\n\n"
        if not entries: txt+="𝗡𝗼 𝗢𝗧𝗣𝘀 𝗱𝗲𝗹𝗶𝘃𝗲𝗿𝗲𝗱 𝘆𝗲𝘁."
        else:
            for i,(name,otps) in enumerate(entries):
                m=medals[i] if i<3 else "✅"
                txt+=f"{m} <b>{name}</b> — 𝗢𝗧𝗣𝘀: {otps}\n"
        await query.edit_message_text(txt,parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[bc("𝗕𝗮𝗰𝗸",cb="gn_backmain",style="primary",icon="5255703720078879038")]])); return True

    if data=="gn_referral":
        await query.answer()
        u=gn_upsert_user(uid); ref_link=gn_ref_link(context.bot.username or "",uid)
        total,qual,pend,earned=gn_ref_stats(uid)
        await query.edit_message_text(
            f"💰 Balance: {u.get('balance',0.0):.2f} {GN_CURRENCY}\n"
            f"🔗 Referral link: {ref_link}\n"
            f"👤 Qualified: {qual} | ⏳ Pending: {pend}\n\n"
            f"📊 Total Referrals: {total} | Earned: {earned:.2f}\n\n"
            f"━━━ 📝 Rules ━━━\n"
            f"▸ They get {GN_REF_MILESTONE} OTPs → you earn {GN_REF_REWARD:.0f} {GN_CURRENCY}",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[bc("𝗕𝗮𝗰𝗸",cb="gn_backmain",style="primary",icon="5255703720078879038")]])); return True

    if data=="gn_joinchan":
        await query.answer()
        await query.edit_message_text(
            "📣 <b>𝗖𝗹𝗶𝗰𝗸 𝘁𝗼 𝗝𝗼𝗶𝗻 𝗢𝘂𝗿 𝗖𝗵𝗮𝗻𝗻𝗲𝗹𝘀</b> 🎉\n\n➡️ Stay updated!",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [bc("𝗡𝘂𝗺𝗯𝗲𝗿𝘀 𝗖𝗵𝗮𝗻𝗻𝗲𝗹",url="https://t.me/junaidaliniz",style="danger",icon="6206497372176913599")],
                [bc("𝗖𝗵𝗮𝘁 𝗚𝗿𝗼𝘂𝗽",url="https://t.me/+DrBDJM9-nvAyMjRk",style="success",icon="6206080502651164081")],
                [bc("𝗢𝗧𝗣 𝗚𝗿𝗼𝘂𝗽",url="https://t.me/junaidniz110",style="primary",icon="6206508629286196237")],
                [bc("𝗕𝗮𝗰𝗸",cb="gn_backmain",style="primary",icon="5255703720078879038")],
            ])); return True

    if data=="gn_withdraw":
        await query.answer()
        u=gn_upsert_user(uid)
        if not GN_DATA.get("withdraw_enabled",True):
            await query.edit_message_text("❌ <b>Withdrawals Disabled</b>\n\nWithdrawal requests are currently disabled.",
                parse_mode="HTML"); return True
        rate=GN_DATA.get("usd_to_pkr",GN_USD_RATE) or GN_USD_RATE
        minw=GN_DATA.get("min_withdrawal",GN_MIN_WITHDRAW)
        usdt=u.get("balance",0.0)/rate
        GN_WDRAW_STATES[uid]={"step":0}
        await query.edit_message_text(
            f"💵 <b>Withdraw Request</b>\n\n"
            f"💵 PKR: <b>{u.get('balance',0.0):.2f} {GN_CURRENCY}</b>\n   ≈ <b>{usdt:.4f} USDT</b>\n\n"
            f"1 USDT = {rate:.0f} {GN_CURRENCY}\n✅ Withdrawable USDT: <b>{usdt:.4f} $</b>\n\n"
            f"Which method?",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [gn_btn("💵 PKR — EasyPaisa / JazzCash",cb="gn_wd_pkr")],
                [gn_btn("💲 USDT — Binance",            cb="gn_wd_usdt")],
            ])); return True

    if data in ("gn_wd_pkr","gn_wd_usdt"):
        await query.answer()
        meth="pkr" if data=="gn_wd_pkr" else "usdt"
        if uid not in GN_WDRAW_STATES: GN_WDRAW_STATES[uid]={"step":0}
        u=gn_upsert_user(uid); rate=GN_DATA.get("usd_to_pkr",GN_USD_RATE) or GN_USD_RATE
        minw=GN_DATA.get("min_withdrawal",GN_MIN_WITHDRAW); minu=GN_DATA.get("min_withdrawal_usd",GN_MIN_USD)
        GN_WDRAW_STATES[uid]={"step":1,"method":meth}
        if meth=="pkr":
            await query.edit_message_text(
                f"💵 <b>Withdraw — Step 1/3</b>\n\n"
                f"💵 Balance: <b>{u.get('balance',0.0):.2f} {GN_CURRENCY}</b>\n"
                f"ℹ️ Minimum: <b>{minw:.0f} {GN_CURRENCY}</b>\n\n"
                f"💬 How much PKR to withdraw?\n<i>Example: <code>10</code></i>",
                parse_mode="HTML"); return True
        else:
            usdt=u.get("balance",0.0)/rate
            await query.edit_message_text(
                f"💵 <b>Withdraw — Step 1/3</b>\n\n"
                f"✅ Withdrawable: <b>{usdt:.4f} USDT</b>\n"
                f"ℹ️ Minimum: <b>{minu:.4f} $</b>\n\n"
                f"💬 How much USDT?\n<i>Example: <code>0.004</code></i>",
                parse_mode="HTML"); return True

    if data=="gn_wd_confirm":
        await query.answer()
        state=GN_WDRAW_STATES.pop(uid,None)
        if not state or state.get("step")!=3:
            await query.answer("⚠️ Expired. Tap Withdraw again.",show_alert=True); return True
        meth=state.get("method","pkr"); amt=state.get("amount",0.0); amt_usd=state.get("amount_usd",0.0)
        details=state.get("details",""); rate=GN_DATA.get("usd_to_pkr",GN_USD_RATE) or GN_USD_RATE
        uk=str(uid)
        if uk in GN_DATA["users"]:
            uu=GN_DATA["users"][uk]
            if meth=="pkr": uu["balance"]=max(0.0,uu.get("balance",0.0)-amt)
            else: uu["balance"]=max(0.0,uu.get("balance",0.0)-(amt_usd*rate))
            GN_DATA["users"][uk]=uu
        GN_DATA["withdraw_seq"]=GN_DATA.get("withdraw_seq",0)+1; rid=GN_DATA["withdraw_seq"]
        req={"id":rid,"user_id":uid,"username":query.from_user.username or "",
             "first_name":query.from_user.first_name or "","method":meth,
             "amount":amt,"amount_usd":amt_usd,"details":details,"status":"pending",
             "created_at":datetime.now().strftime("%Y-%m-%d %H:%M")}
        GN_DATA["withdrawals"][str(rid)]=req; gn_save()
        et=(f"✅ <b>Withdrawal Submitted!</b>\n\n💵 PKR: <b>{amt:.2f} {GN_CURRENCY}</b> deducted.\n💳 Details: <code>{details}</code>\n\n⏳ Admin will review shortly."
            if meth=="pkr" else
            f"✅ <b>Withdrawal Submitted!</b>\n\n💲 USDT: <b>{amt_usd:.4f} $</b> deducted.\n🆔 Binance ID: <code>{details}</code>\n\n⏳ Admin will review shortly.")
        await query.edit_message_text(et,parse_mode="HTML")
        as_=(f"{amt:.2f} {GN_CURRENCY} (PKR)" if meth=="pkr" else f"{amt_usd:.4f} $ (USDT)")
        at=(f"💵 <b>New Withdrawal Request</b>\n\n"
            f"👤 User: <b>{req['first_name']}</b> (@{req['username']})\n"
            f"🆔 ID: <code>{uid}</code>\n💰 Amount: <b>{as_}</b>\n"
            f"💳 Details: <code>{details}</code>\n\n⚠️ Balance already deducted.")
        ak=InlineKeyboardMarkup([
            [bc("𝗔𝗽𝗽𝗿𝗼𝘃𝗲 𝗣𝗮𝘆𝗼𝘂𝘁",cb=f"gnadm_wd_ok:{rid}",style="success",icon="6206479140040743133"),
             bc("𝗥𝗲𝗷𝗲𝗰𝘁 & 𝗥𝗲𝗳𝘂𝗻𝗱",cb=f"gnadm_wd_rej:{rid}",style="danger",icon="5974083768233760323")]])
        for aid in list(OWNER_IDS)+load_admins():
            try: await context.bot.send_message(chat_id=aid,text=at,parse_mode="HTML",reply_markup=ak)
            except: pass
        return True

    if data=="gn_wd_cancel":
        await query.answer(); GN_WDRAW_STATES.pop(uid,None)
        await query.edit_message_text("❌ <b>Withdrawal Cancelled</b>\n\nBalance not affected.",parse_mode="HTML"); return True

    # ── Admin withdraw approve/reject ────────────────────────
    if data.startswith("gnadm_wd_ok:"):
        if not is_admin(uid): return False
        await query.answer()
        rid=data.split(":")[1]; req=GN_DATA["withdrawals"].get(rid)
        if req and req.get("status")=="pending":
            req["status"]="approved"; gn_save()
            as_=(f"{req.get('amount',0):.2f} {GN_CURRENCY}" if req.get("method")=="pkr" else f"{req.get('amount_usd',0):.4f} $")
            await query.edit_message_text(f"✅ <b>Withdrawal Approved</b>\n\n👤 {req.get('first_name','')} (@{req.get('username','')})\n💰 {as_}",parse_mode="HTML")
            try: await context.bot.send_message(chat_id=req["user_id"],text=f"✅ <b>Withdrawal Approved!</b>\n\n💰 Amount: <b>{as_}</b> approved for payout.\n💳 Details:\n<code>{req.get('details','')}</code>",parse_mode="HTML")
            except: pass
        return True

    if data.startswith("gnadm_wd_rej:"):
        if not is_admin(uid): return False
        await query.answer()
        rid=data.split(":")[1]; req=GN_DATA["withdrawals"].get(rid)
        rate=GN_DATA.get("usd_to_pkr",GN_USD_RATE) or GN_USD_RATE
        if req and req.get("status")=="pending":
            req["status"]="rejected"; uk=str(req["user_id"])
            if uk in GN_DATA["users"]: GN_DATA["users"][uk]["balance"]=GN_DATA["users"][uk].get("balance",0.0)+req.get("amount",0.0)
            gn_save()
            as_=(f"{req.get('amount',0):.2f} {GN_CURRENCY}" if req.get("method")=="pkr" else f"{req.get('amount_usd',0):.4f} $")
            await query.edit_message_text(f"❌ <b>Withdrawal Rejected & Refunded</b>\n\n👤 {req.get('first_name','')} | 💰 {as_} refunded.",parse_mode="HTML")
            try: await context.bot.send_message(chat_id=req["user_id"],text=f"❌ <b>Withdrawal Declined</b>\n\n💰 <b>{as_}</b> has been refunded to your balance.\n📣 Contact admin if you have questions.",parse_mode="HTML")
            except: pass
        return True

    # ── Admin panel action callbacks ─────────────────────────
    if data=="gnadm_addnums":
        if not is_admin(uid): return False
        await query.answer()
        GN_WIZARD_STATES[uid]={"step":"svc","staged":[]}
        await query.edit_message_text(
            "➕ <b>Step 1/7 — Service Name</b>\n\nEnter service name:\n<i>Example: TikTok, WhatsApp, Instagram</i>",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[bc("𝗖𝗮𝗻𝗰𝗲𝗹",cb="gnadm_cancel",style="danger",icon="5974083768233760323")]])); return True

    if data=="gnadm_listsvc":
        if not is_admin(uid): return False
        await query.answer()
        txt="📋 <b>Services</b>\n\n"
        if not GN_DATA["services"]: txt+="No services yet."
        for sn,svc in GN_DATA["services"].items():
            em=gn_svc_emoji(sn); txt+=f"{em} <b>{sn}</b>\n"
            for cn,c in svc.get("countries",{}).items():
                flag=gn_flag(c.get("code","")); n=len(c.get("numbers",[]))
                txt+=f"   {flag} {cn} — {c.get('price',0):.0f}{GN_CURRENCY} — {n} nums\n"
        await query.edit_message_text(txt[:4000],parse_mode="HTML"); return True

    if data=="gnadm_stats":
        if not is_admin(uid): return False
        await query.answer()
        grand=0; txt="📊 <b>System Statistics</b>\n\n"
        for sn,svc in GN_DATA["services"].items():
            em=gn_svc_emoji(sn); txt+=f"{em} <b>{sn}</b>\n"
            for cn,c in svc.get("countries",{}).items():
                flag=gn_flag(c.get("code","")); n=len(c.get("numbers",[])); grand+=n
                st="❌ Out of Stock" if n==0 else ("⚠️ Low" if n<5 else "✅ OK")
                txt+=f"  {flag} {cn} — {c.get('price',0):.0f}{GN_CURRENCY} — {n} nums — {st}\n"
            txt+="\n"
        ty=sum(u.get("today_otps",0) for u in GN_DATA["users"].values())
        ta=sum(u.get("total_otps",0) for u in GN_DATA["users"].values())
        txt+=(f"━━━━━━━━━━━━━━━━━━━━━━\n"
              f"📱 Total Numbers: <b>{grand}</b>\n👥 Total Users: <b>{len(GN_DATA['users'])}</b>\n"
              f"🔑 Total OTPs: <b>{ta}</b>\n🔔 Today OTPs: <b>{ty}</b>")
        await query.edit_message_text(txt[:4000],parse_mode="HTML"); return True

    if data=="gnadm_users":
        if not is_admin(uid): return False
        await query.answer()
        _cu = db.cursor(); _cu.execute("SELECT COUNT(*) FROM tg_users"); total = _cu.fetchone()[0]
        lines=["Username,UserID,TotalOTPs,TodayOTPs,Balance,JoinedAt"]
        for u in GN_DATA["users"].values():
            lines.append(f"{u.get('username','')},{u.get('id','')},{u.get('total_otps',0)},"
                         f"{u.get('today_otps',0)},{u.get('balance',0.0):.2f},{u.get('joined_at','')}")
        fname=f"/tmp/gn_users_{int(time.time())}.csv"
        with open(fname,"w") as f_: f_.write("\n".join(lines))
        await context.bot.send_document(chat_id=chat,document=open(fname,"rb"),
            caption=f"✅ Users Export\nTotal: {total} users",parse_mode="HTML")
        import os as _os; _os.remove(fname); return True

    if data=="gnadm_rmsvc":
        if not is_admin(uid): return False
        await query.answer()
        await query.edit_message_text("🗑 <b>Select service to remove:</b>",
            parse_mode="HTML",reply_markup=gn_rm_service_kb()); return True

    if data=="gnadm_rmcnt":
        if not is_admin(uid): return False
        await query.answer()
        await query.edit_message_text("🗑 <b>Select country to remove:</b>",
            parse_mode="HTML",reply_markup=gn_rm_country_kb()); return True

    if data.startswith("gnrmsvc:"):
        if not is_admin(uid): return False
        await query.answer()
        sn=data[8:]; GN_DATA["services"].pop(sn,None); gn_save()
        await query.edit_message_text(f"✅ Service <b>{sn}</b> removed.",parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[bc("𝗕𝗮𝗰𝗸",cb="back_to_admin",style="primary",icon="5255703720078879038")]])); return True

    if data.startswith("gnrmcnt:"):
        if not is_admin(uid): return False
        await query.answer()
        parts=data[8:].split(":",1)
        if len(parts)==2:
            sn,cn=parts
            if sn in GN_DATA["services"]: GN_DATA["services"][sn].get("countries",{}).pop(cn,None); gn_save()
            await query.edit_message_text(f"✅ Country <b>{cn}</b> removed from <b>{sn}</b>.",parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([[bc("𝗕𝗮𝗰𝗸",cb="back_to_admin",style="primary",icon="5255703720078879038")]]))
        return True

    # gnadm_bcast/do/cancel removed — all broadcast now uses nb_ system

    if data=="gnadm_confirm_nums":
        if not is_admin(uid): return False
        await query.answer()
        state=GN_WIZARD_STATES.get(uid)
        if not state or state.get("step")!="nums" or not state.get("staged"):
            await query.edit_message_text("❌ No staged numbers found.",parse_mode="HTML"); return True
        await gn_commit_numbers(context.bot,chat,uid)
        return True

    if data=="gnadm_clear_staged":
        await query.answer()
        if uid in GN_WIZARD_STATES: GN_WIZARD_STATES[uid]["staged"]=[]
        await query.edit_message_text("🗑 Staged numbers cleared. Send new numbers or files.",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[bc("𝗖𝗮𝗻𝗰𝗲𝗹",cb="gnadm_cancel",style="danger",icon="5974083768233760323")]])); return True

    if data=="gnadm_cancel":
        await query.answer(); GN_WIZARD_STATES.pop(uid,None)
        await query.message.reply_text(
            f'<tg-emoji emoji-id="6205965994528086727">💠</tg-emoji> <b>ADMIN PANEL</b>\n'
            f'━━━━━━━━━━━━━━━━━━━━━━\n'
            f'<tg-emoji emoji-id="6235572922086331108">🧑‍💻</tg-emoji> Select an option:',
            parse_mode="HTML", reply_markup=get_admin_keyboard(uid)); return True

    if data=="gnadm_add_balance":
        if not is_admin(uid): return False
        await query.answer()
        GN_WIZARD_STATES[uid]={"step":"bal_uid"}
        await query.edit_message_text("💰 Enter user ID to add balance:",parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[bc("𝗖𝗮𝗻𝗰𝗲𝗹",cb="gnadm_cancel",style="danger",icon="5974083768233760323")]])); return True

    return False


# ── Load GN data on startup ───────────────────────────────────
gn_load(); gn_load_holds()
logger.info(f"[GN] Loaded {len(GN_DATA['services'])} services, {len(GN_DATA['users'])} users")

# ═══════════════════════════════════════════════════════════════
#  DOCUMENT HANDLER
# ═══════════════════════════════════════════════════════════════
async def document_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    # ── GN Admin .txt upload for numbers (from main.go) ──────
    if await gn_admin_doc_handler(update, context):
        return
    if uid not in NB_STATE or not isinstance(NB_STATE[uid], dict):
        return
    state = NB_STATE[uid]
    if state.get("step") != "waiting_file":
        return
    country = state["country"]
    try:
        file       = await update.message.document.get_file()
        file_bytes = await file.download_as_bytearray()
        file_text  = file_bytes.decode("utf-8")
        all_lines  = [n.strip() for n in file_text.splitlines() if n.strip()]
        nums       = [n for n in all_lines if n.isdigit()] or all_lines
        db_add_numbers(country, nums)
        await update.message.reply_text(
            f"✅ <b>{len(nums)}</b> numbers added to <b>{country}</b>!",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back to Admin","back_to_admin")]]))
        del NB_STATE[uid]
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

# ═══════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════
async def main():
    logger.info(f"🚀 {BOT_NAME} starting...")
    logger.info(f"📡 OTP Groups: {load_groups()}")
    logger.info(f"🔌 IVAS accounts: {list(load_ivas().keys())}")
    logger.info(f"📋 REST panels: {list(API_PANELS.keys())}")
    logger.info(f"⚙️  OTP forward: {load_config().get('otp_forward', True)}")

    asyncio.create_task(cleanup_states())
    asyncio.create_task(monitor_tasks())
    asyncio.create_task(_otp_sender_task())

    for panel in API_PANELS:
        task = asyncio.create_task(api_worker(panel), name=f"REST-{panel}")
        task.add_done_callback(handle_task_exception)
        REST_TASKS[panel] = task

    for name in load_ivas():
        task = asyncio.create_task(ivas_worker(name), name=f"IVAS-{name}")
        task.add_done_callback(handle_task_exception)
        IVAS_TASKS[name] = task

    app = Application.builder().token(BOT_TOKEN).build()

    for cmd, handler in [
        ("start",       start_command),
        ("help",        help_command),
        ("admin",       admin_command),
        ("otpfor",      otpfor_command),
        ("fetchsms",    fetchsms_command),
        ("status",      status_command),
        ("stats",       stats_command),
        ("broadcast",   broadcast_command),
        ("addgroup",    addgroup_command),
        ("removegroup", removegroup_command),
        ("reload",      reload_command),
    ]:
        app.add_handler(CommandHandler(cmd, handler))

    app.add_handler(CallbackQueryHandler(callback_query_handler))
    app.add_handler(MessageHandler(filters.Document.ALL, document_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    # ── Broadcast media handlers ──────────────────────────────
    app.add_handler(MessageHandler(filters.PHOTO, media_broadcast_handler))
    app.add_handler(MessageHandler(filters.VIDEO, media_broadcast_handler))
    app.add_handler(MessageHandler(filters.VOICE, media_broadcast_handler))

    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)
    logger.info("🟢 Bot is online.")
    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
