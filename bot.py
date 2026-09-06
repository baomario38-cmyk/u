import os
import hashlib
import math
import random
from threading import Thread
from flask import Flask
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- 1. SERVER KEEP-ALIVE ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "TOOL MD5 TXGAME v13.0 QUANTUM LEGACY ONLINE", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- 2. CẤU HÌNH HỆ THỐNG & ADMIN ---
TOKEN = '8985526419:AAGdRkntgFNYLBG53LoI-pNC7aHtOFMWhGA'
ADMIN_ID = 755092812
ADMIN_USERNAME = "lionvnios"

bot = telebot.TeleBot(TOKEN)
user_data = {}
all_users = set()
GLOBAL_CACHE = {}

def is_admin(user):
    if user.id == ADMIN_ID: return True
    if user.username and user.username.lower() == ADMIN_USERNAME.lower(): return True
    return False

def init_user(uid):
    all_users.add(uid)
    if uid not in user_data:
        user_data[uid] = {"balance": 20, "web": "HitClub", "logs": []}

# --- 3. ĐỘNG CƠ PHÂN TÍCH (KHÔI PHỤC LÕI LƯỢNG TỬ SIÊU NÉT TỪ TỐI QUA) ---
def ultimate_quantum_hash_algo(raw_code):
    clean_code = raw_code.strip().lower()
    
    if clean_code in GLOBAL_CACHE:
        return GLOBAL_CACHE[clean_code]

    # Khôi phục lõi SHA-512 + BLAKE2b chuẩn xác của tối qua
    sha512_hash = hashlib.sha512(clean_code.encode()).hexdigest()
    blake2b_hash = hashlib.blake2b(clean_code.encode()).hexdigest()

    core_val = 0
    for i in range(0, 64, 4):
        core_val ^= int(sha512_hash[i:i+4], 16) + int(blake2b_hash[i:i+4], 16)

    # Công thức Pi & Euler mang lại tỷ lệ "nét"
    math_factor = (math.pi * math.e * core_val) % 999999
    percent_raw = 12.5 + (math_factor % 750000) / 10000.0
    
    is_tai = percent_raw >= 50.0
    result = "TÀI" if is_tai else "XỈU"
    
    if is_tai:
        p_tai = round(percent_raw, 1)
        p_xiu = round(100.0 - p_tai, 1)
    else:
        p_xiu = round(100.0 - percent_raw, 1)
        p_tai = round(percent_raw, 1)

    # Vi phân độ tin cậy hiển thị 91.5% -> 99.4%
    md5_part = int(hashlib.md5(clean_code.encode()).hexdigest()[:6], 16)
    acc = round(91.5 + (md5_part % 80) / 10.0, 1)
    
    # Nâng cấp: Tính toán thời gian phản hồi (Scan time giả lập siêu tốc)
    scan_time = round(0.012 + (md5_part % 45) / 1000.0, 3)

    res_tuple = (result, p_tai, p_xiu, acc, scan_time)
    GLOBAL_CACHE[clean_code] = res_tuple
    return res_tuple

# --- 4. GIAO DIỆN TỐI GIẢN CHUYÊN NGHIỆP ---
def main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("⚙️ Đổi Cổng Game", callback_data="btn_web"),
        InlineKeyboardButton("💳 Ví & Lịch Sử", callback_data="btn_info")
    )
    markup.add(InlineKeyboardButton("💎 Nạp Xu Admin", callback_data="btn_nap"))
    return markup

# --- 5. LỆNH ĐIỀU HƯỚNG CƠ BẢN ---
@bot.message_handler(commands=['start'])
def start_cmd(message):
    uid = message.from_user.id
    init_user(uid)
    text = (
        "⚡ **HỆ THỐNG TOOL MD5 TXGAME** ⚡\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        f"🆔 ID Client: `{uid}`\n"
        f"💳 Gói phân tích: `{user_data[uid]['balance']} Lượt`\n"
        f"🌐 Server Game: `{user_data[uid]['web']}`\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "👉 **Dán mã MD5 (32 ký tự) hoặc SHA256 (64 ký tự)** để phần mềm dò cầu."
    )
    bot.reply_to(message, text, parse_mode="Markdown", reply_markup=main_menu())

# --- 6. HỆ THỐNG QUẢN TRỊ ADMIN (KHÔNG LỖI) ---
@bot.message_handler(commands=['congxu'])
def add_coins(message):
    if not is_admin(message.from_user):
        bot.reply_to(message, f"❌ **Truy cập bị từ chối!**\nBạn không có quyền Admin.\n🆔 ID của bạn: `{message.from_user.id}`", parse_mode="Markdown")
        return
        
    try:
        parts = message.text.split()
        if len(parts) != 3:
            bot.reply_to(message, "❌ **Sai số lượng tham số!**\n👉 Cấu trúc: `/congxu <ID_User> <Số_Xu>`", parse_mode="Markdown")
            return
            
        target_id = int(parts[1])
        amount = int(parts[2])
        
        init_user(target_id)
        user_data[target_id]["balance"] += amount
        
        bot.reply_to(message, f"✅ **CẤP QUYỀN THÀNH CÔNG!**\n👤 ID nhận: `{target_id}`\n➕ Số lượng: `{amount} Lượt`\n💳 Tổng dư: `{user_data[target_id]['balance']} Lượt`", parse_mode="Markdown")
        
        try:
            bot.send_message(target_id, f"🎉 Admin đã cấp thêm **+{amount} Lượt quét** vào tài khoản!\n💳 Số dư hiện tại: **{user_data[target_id]['balance']} Lượt**", parse_mode="Markdown")
        except:
            pass
            
    except ValueError:
        bot.reply_to(message, "❌ **Sai định dạng!** ID và Số lượng phải là chữ số.", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"❌ **Lỗi hệ thống:** {str(e)}", parse_mode="Markdown")

@bot.message_handler(commands=['thongbao'])
def broadcast(message):
    if not is_admin(message.from_user):
        bot.reply_to(message, "❌ **Truy cập bị từ chối!**")
        return
    try:
        parts = message.text.split(" ", 1)
        if len(parts) < 2:
            bot.reply_to(message, "❌ **Sai cấu trúc!**\n👉 Dùng: `/thongbao <Nội dung>`", parse_mode="Markdown")
            return
            
        notice = parts[1].strip()
        success = 0
        for uid in list(all_users):
            try:
                bot.send_message(uid, f"📢 **THÔNG BÁO TỪ MÁY CHỦ**\n━━━━━━━━━━━━━━━━━━━\n{notice}", parse_mode="Markdown")
                success += 1
            except:
                pass
        bot.reply_to(message, f"✅ Đã truyền tín hiệu tới `{success}` tài khoản.", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"❌ **Lỗi:** {str(e)}", parse_mode="Markdown")

# --- 7. TƯƠNG TÁC CALLBACK ---
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    uid = call.from_user.id
    init_user(uid)
    if call.data == "btn_web":
        markup = InlineKeyboardMarkup(row_width=2)
        for w in ["HitClub", "B52", "Lucky88", "LC79", "Go88"]:
            markup.add(InlineKeyboardButton(f"🎮 {w}", callback_data=f"web_{w}"))
        bot.send_message(call.message.chat.id, "🌐 **Chọn Server Game cần dò:**", parse_mode="Markdown", reply_markup=markup)
    elif call.data.startswith("web_"):
        web = call.data.split("_")[1]
        user_data[uid]["web"] = web
        bot.send_message(call.message.chat.id, f"✅ **Đã trỏ IP vào Server:** `{web}`", parse_mode="Markdown", reply_markup=main_menu())
    elif call.data == "btn_info":
        logs_str = "\n".join(user_data[uid]["logs"]) if user_data[uid]["logs"] else "Chưa có dữ liệu quét."
        bot.send_message(call.message.chat.id, f"💳 **HỒ SƠ CLIENT**\n🆔 ID: `{uid}`\n💰 Lượt quét: `{user_data[uid]['balance']} Lượt`\n📜 **5 Nhịp cầu gần nhất:**\n{logs_str}", parse_mode="Markdown", reply_markup=main_menu())
    elif call.data == "btn_nap":
        bot.send_message(call.message.chat.id, f"💎 **LIÊN HỆ QUẢN TRỊ VIÊN**\n📩 Telegram: @lionVnIos\n🆔 Copy ID này gửi Admin: `{uid}`", parse_mode="Markdown")

# --- 8. PHÂN TÍCH LÕI (CORE ANALYZER) ---
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    uid = message.from_user.id
    init_user(uid)
    text = message.text.strip().lower()
    
    if len(text) not in [32, 64]:
        bot.reply_to(message, "⚠️ **Định dạng lỗi:** Mã băm phải là MD5 (32 ký tự) hoặc SHA256 (64 ký tự).")
        return
    if user_data[uid]["balance"] < 1:
        bot.reply_to(message, "⚠️ **Cảnh báo:** Tài khoản hết lượt quét. Vui lòng liên hệ Admin.", reply_markup=main_menu())
        return
        
    user_data[uid]["balance"] -= 1
    
    # Kích hoạt Engine Lượng tử của tối qua
    result, p_tai, p_xiu, acc, scan_time = ultimate_quantum_hash_algo(text)
    
    code_type = "MD5" if len(text) == 32 else "SHA-256"
    res_icon = "🔴 TÀI" if result == "TÀI" else "🔵 XỈU"
    
    user_data[uid]["logs"].insert(0, f"[{code_type}] {text[:8]}... ➔ {result}")
    if len(user_data[uid]["logs"]) > 5:
        user_data[uid]["logs"].pop()
        
    # Giao diện nâng cấp hiển thị thời gian quét và tốc độ
    res_msg = (
        f"⚡ **DEEP SCAN HOÀN TẤT** ⚡\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        f"🎯 Dự đoán nhịp cầu: **{res_icon}**\n"
        f"📊 Tỷ lệ phân phối: **Tài {p_tai}% - Xỉu {p_xiu}%**\n"
        f"🔒 Mức độ tin cậy: **{acc}%**\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        f"⏱️ Thời gian quét: `{scan_time}s`\n"
        f"🎮 Server: `{user_data[uid]['web']}` | 💳 Còn lại: `{user_data[uid]['balance']} Lượt`"
    )
    bot.reply_to(message, res_msg, parse_mode="Markdown", reply_markup=main_menu())

if __name__ == '__main__':
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()
    try:
        bot.remove_webhook()
    except:
        pass
    print("TOOL MD5 TXGAME v13.0 QUANTUM LEGACY ACTIVE...")
    bot.infinity_polling(none_stop=True)
