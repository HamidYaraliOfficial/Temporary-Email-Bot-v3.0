# -*- coding: utf-8 -*-
# ============================================ #
#      حرفه‌ای - Professional - 专业版           #
#    ربات ایمیل موقت سه‌زبانه (فارسی/انگلیسی/چینی) #
#           Temporary Email Bot v3.0            #
# ============================================ #
# Developer: @HamidYaraliOfficial
# Telegram & Instagram: @HamidYaraliOfficial
# ============================================ #

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telebot import types
import requests
import telebot
import sqlite3
import html
import json
import os
import re
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ============================================ #
#              تنظیمات اولیه / Config           #
# ============================================ #
TOKEN = '000000'  # توکن ربات / Bot Token
CHANNEL_USERNAME = 'VeriaTeam'   # یوزر کانال بدون @ / Channel username without @
ADMIN_IDS = [5413202242, 0]     # آیدی عددی ادمین‌ها / Admin IDs
API_URL = "https://zecora0.serv00.net/fake.php"

bot = telebot.TeleBot(TOKEN)

# تنظیم سشن برای درخواست‌های سریعتر / Session for faster requests
session = requests.Session()
retry = Retry(total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry, pool_connections=20, pool_maxsize=20)
session.mount('http://', adapter)
session.mount('https://', adapter)

# ============================================ #
#              دیتابیس کانال‌ها / DB            #
# ============================================ #
conn = sqlite3.connect('channels.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS channels (id INTEGER PRIMARY KEY, channel_name TEXT, invite_link TEXT)''')

# ============================================ #
#         ذخیره اطلاعات کاربران / User Data    #
# ============================================ #
user_tokens = {}
current_messages = {}
current_message_index = {}
user_lang = {}  # ذخیره زبان کاربر / Store user language

if not os.path.exists('data'):
    os.makedirs('data')

if not os.path.exists('data/data.json'):
    with open('data/data.json', 'w') as f:
        json.dump({}, f)

with open('data/data.json', 'r') as f:
    try:
        user_tokens = json.load(f)
    except:
        user_tokens = {}

if not os.path.exists('data/lang.json'):
    with open('data/lang.json', 'w') as f:
        json.dump({}, f)

try:
    with open('data/lang.json', 'r') as f:
        user_lang = json.load(f)
except:
    user_lang = {}

# ============================================ #
#         متن‌های چندزبانه / Translations      #
# ============================================ #
TEXTS = {
    'fa': {
        'start': """
به ربات ایمیل موقت خوش اومدی {user_mention}

قابلیت‌های ربات:
- ساخت ایمیل تصادفی
- ساخت ایمیل دلخواه با دامنه‌های متنوع
- دریافت و مشاهده پیام‌ها
- حذف ایمیل‌های اضافی

کاملا رایگان و بدون محدودیت
        """,
        'random_email': """
ایمیل تصادفی ساخته شد

📧 {email}

می‌توانید هم اکنون از آن استفاده کنید
پیام‌ها به این ایمیل می‌آید
        """,
        'custom_email': """
ایمیل دلخواه ساخته شد

📧 {email}

می‌توانید هم اکنون از آن استفاده کنید
پیام‌ها به این ایمیل می‌آید
        """,
        'select_domain': "دامنه مورد نظر خود را انتخاب کنید:",
        'enter_email_name': """
دامنه انتخاب شد: {domain}

حالا اسم ایمیل را بفرستید
مثال: mymail
        """,
        'invalid_email_name': "⚠️ اسم ایمیل نامعتبر است\nفقط از حروف انگلیسی و اعداد استفاده کنید\nمثال: mymail123",
        'my_emails': "لیست ایمیل‌های شما:",
        'no_emails': "هیچ ایمیلی پیدا نشد\nبا دکمه‌های منوی اصلی ایمیل جدید بسازید",
        'email_selected': "ایمیل انتخاب شده:\n{email}\n\nحالا یکی از گزینه‌ها را انتخاب کنید",
        'fetching': "در حال دریافت پیام‌ها... لطفاً چند لحظه صبر کنید",
        'no_messages': "هیچ پیامی یافت نشد\nهنوز پیامی به این ایمیل نیامده است",
        'refreshing': "در حال بروزرسانی...",
        'still_no_messages': "هنوز پیامی دریافت نشده است\nدوباره تلاش کنید یا بعداً چک کنید",
        'delete_all_confirm': "⚠️ آیا از حذف همه ایمیل‌ها مطمئن هستید؟\n\nتعداد: {count} عدد\n\nاین کار قابل بازگشت نیست!",
        'no_emails_to_delete': "هیچ ایمیلی برای حذف وجود ندارد",
        'delete_all_success': "✅ همه ایمیل‌ها با موفقیت حذف شدند",
        'delete_all_error': "❌ خطا در حذف ایمیل‌ها:\n{error}",
        'delete_confirm': "⚠️ آیا از حذف این ایمیل مطمئن هستید؟\n\n{email}\n\nاین کار قابل بازگشت نیست!",
        'delete_success': "✅ ایمیل با موفقیت حذف شد\n\n{email}",
        'delete_error': "❌ خطا در حذف ایمیل:\n{error}",
        'admin_panel': """
👑 پنل مدیریت

سلام {user_link} عزیز
به پنل خودت خوش اومدی
        """,
        'add_channel_prompt': "یوزرنیم کانال را با @ بفرستید\nمثال: @my_channel",
        'not_channel': "❌ این یوزر متعلق به کانال یا گروه نیست",
        'bot_not_admin': "🚫 ربات باید در کانال ادمین باشد",
        'channel_exists': "⚠️ کانال از قبل وجود دارد\n{channel}",
        'channel_added': "✅ کانال با موفقیت اضافه شد\n\n{channel}\n{link}",
        'channel_error': "❌ خطا:\n{error}",
        'remove_channel_prompt': "یوزرنیم کانالی که میخواهید حذف کنید را بفرستید\nمثال: @my_channel",
        'channel_removed': "✅ کانال با موفقیت حذف شد\n{channel}",
        'channel_not_found': "❌ کانالی با این مشخصات پیدا نشد\n{channel}",
        'channel_list': "لیست کانال‌های اجباری:\n\n",
        'no_channels': "هیچ کانالی ثبت نشده است",
        'delete_all_channels_confirm': "⚠️ آیا از حذف همه کانال‌ها مطمئن هستید؟\nاین کار قابل بازگشت نیست!",
        'all_channels_deleted': "✅ همه کانال‌ها با موفقیت حذف شدند\n\n",
        'no_channels_to_delete': "هیچ کانالی برای حذف وجود نداشت",
        'subscription_required': """
⚠️ کاربر گرامی {name}

برای استفاده از ربات ابتدا باید در کانال ما عضو شوید

🔗 لینک عضویت: {link}

بعد از عضویت، دوباره /start رو بفرستید.
        """,
        'error_random': "❌ خطا در ساخت ایمیل\nلطفاً دوباره تلاش کنید",
        'error_domains': "❌ خطا در دریافت لیست دامنه‌ها\nلطفاً دوباره تلاش کنید",
        'error_custom': "❌ خطا در ساخت ایمیل دلخواه\nلطفاً دوباره تلاش کنید",
        'error_server': "خطا در ارتباط با سرور: {code}",
        'error_connection': "خطا در اتصال به سرور: {error}",
        'back': "بازگشت",
        'back_to_menu': "بازگشت به منو",
        'random_btn': "ایمیل تصادفی",
        'custom_btn': "ایمیل دلخواه",
        'list_btn': "لیست ایمیل‌ها",
        'delete_all_btn': "حذف همه ایمیل‌ها",
        'channel_btn': "کانال ربات",
        'receive_btn': "دریافت پیام‌ها",
        'delete_btn': "حذف ایمیل",
        'refresh_btn': "بروزرسانی",
        'confirm_yes': "بله، حذف کن",
        'cancel': "انصراف",
        'prev': "قبلی",
        'next': "بعدی",
        'admin_btn': "پنل مدیریت",
        'add_channel_btn': "افزودن کانال",
        'remove_channel_btn': "حذف کانال",
        'list_channels_btn': "لیست کانال‌ها",
        'delete_all_channels_btn': "حذف همه کانال‌ها",
        'access_denied': "❌ شما دسترسی به این بخش ندارید",
        'no_access': "❌ شما دسترسی به این بخش ندارید",
        'message_prefix': """
پیام {current} از {total}
====================================
از: {from}
به: {to}
زمان: {time}
موضوع: {subject}
متن پیام:
{body}
{attachments}
        """,
        'attachment_text': "\nپیوست‌ها:\n",
        'attachment_item': "{name} - {size}\n",
        'no_subject': 'بدون موضوع',
        'no_sender': 'فرستنده ناشناس',
        'no_body': 'بدون محتوا',
        'unknown_time': 'نامشخص',
        'lang_btn': "🌐 زبان / Language",
        'lang_select': "زبان خود را انتخاب کنید / Select your language / 选择您的语言",
        'lang_changed': "✅ زبان به فارسی تغییر کرد / Language changed to Persian",
        'lang_en': "English",
        'lang_zh': "中文",
        'lang_fa': "فارسی",
    },
    'en': {
        'start': """
Welcome to Temporary Email Bot {user_mention}

Features:
- Random email generation
- Custom email with various domains
- Receive and view messages
- Delete unnecessary emails

Completely free and unlimited
        """,
        'random_email': """
Random email created

📧 {email}

You can use it now
Messages will arrive at this email
        """,
        'custom_email': """
Custom email created

📧 {email}

You can use it now
Messages will arrive at this email
        """,
        'select_domain': "Select your desired domain:",
        'enter_email_name': """
Domain selected: {domain}

Now send the email name
Example: mymail
        """,
        'invalid_email_name': "⚠️ Invalid email name\nUse only English letters and numbers\nExample: mymail123",
        'my_emails': "Your email list:",
        'no_emails': "No emails found\nCreate a new email using the main menu buttons",
        'email_selected': "Selected email:\n{email}\n\nChoose an option",
        'fetching': "Fetching messages... Please wait",
        'no_messages': "No messages found\nNo messages have arrived yet",
        'refreshing': "Updating...",
        'still_no_messages': "No messages received yet\nTry again or check later",
        'delete_all_confirm': "⚠️ Are you sure you want to delete all emails?\n\nCount: {count}\n\nThis action cannot be undone!",
        'no_emails_to_delete': "No emails to delete",
        'delete_all_success': "✅ All emails deleted successfully",
        'delete_all_error': "❌ Error deleting emails:\n{error}",
        'delete_confirm': "⚠️ Are you sure you want to delete this email?\n\n{email}\n\nThis action cannot be undone!",
        'delete_success': "✅ Email deleted successfully\n\n{email}",
        'delete_error': "❌ Error deleting email:\n{error}",
        'admin_panel': """
👑 Admin Panel

Hello dear {user_link}
Welcome to your panel
        """,
        'add_channel_prompt': "Send the channel username with @\nExample: @my_channel",
        'not_channel': "❌ This username does not belong to a channel or group",
        'bot_not_admin': "🚫 Bot must be an admin in the channel",
        'channel_exists': "⚠️ Channel already exists\n{channel}",
        'channel_added': "✅ Channel added successfully\n\n{channel}\n{link}",
        'channel_error': "❌ Error:\n{error}",
        'remove_channel_prompt': "Send the channel username to remove\nExample: @my_channel",
        'channel_removed': "✅ Channel removed successfully\n{channel}",
        'channel_not_found': "❌ Channel not found\n{channel}",
        'channel_list': "Required channels list:\n\n",
        'no_channels': "No channels registered",
        'delete_all_channels_confirm': "⚠️ Are you sure you want to delete all channels?\nThis action cannot be undone!",
        'all_channels_deleted': "✅ All channels deleted successfully\n\n",
        'no_channels_to_delete': "No channels to delete",
        'subscription_required': """
⚠️ Dear {name}

To use this bot, you must first join our channel

🔗 Join link: {link}

After joining, send /start again.
        """,
        'error_random': "❌ Error creating email\nPlease try again",
        'error_domains': "❌ Error getting domain list\nPlease try again",
        'error_custom': "❌ Error creating custom email\nPlease try again",
        'error_server': "Server error: {code}",
        'error_connection': "Connection error: {error}",
        'back': "Back",
        'back_to_menu': "Back to menu",
        'random_btn': "Random Email",
        'custom_btn': "Custom Email",
        'list_btn': "Email List",
        'delete_all_btn': "Delete All Emails",
        'channel_btn': "Bot Channel",
        'receive_btn': "Receive Messages",
        'delete_btn': "Delete Email",
        'refresh_btn': "Refresh",
        'confirm_yes': "Yes, Delete",
        'cancel': "Cancel",
        'prev': "Previous",
        'next': "Next",
        'admin_btn': "Admin Panel",
        'add_channel_btn': "Add Channel",
        'remove_channel_btn': "Remove Channel",
        'list_channels_btn': "Channel List",
        'delete_all_channels_btn': "Delete All Channels",
        'access_denied': "❌ You do not have access to this section",
        'no_access': "❌ You do not have access to this section",
        'message_prefix': """
Message {current} of {total}
====================================
From: {from}
To: {to}
Time: {time}
Subject: {subject}
Body:
{body}
{attachments}
        """,
        'attachment_text': "\nAttachments:\n",
        'attachment_item': "{name} - {size}\n",
        'no_subject': 'No subject',
        'no_sender': 'Unknown sender',
        'no_body': 'No content',
        'unknown_time': 'Unknown',
        'lang_btn': "🌐 Language",
        'lang_select': "Select your language / زبان خود را انتخاب کنید / 选择您的语言",
        'lang_changed': "✅ Language changed to English",
        'lang_en': "English",
        'lang_zh': "中文",
        'lang_fa': "فارسی",
    },
    'zh': {
        'start': """
欢迎使用临时邮箱机器人 {user_mention}

功能：
- 生成随机邮箱
- 自定义域名邮箱
- 接收和查看邮件
- 删除多余邮箱

完全免费，无限制使用
        """,
        'random_email': """
随机邮箱已创建

📧 {email}

您现在就可以使用
邮件将发送到此邮箱
        """,
        'custom_email': """
自定义邮箱已创建

📧 {email}

您现在就可以使用
邮件将发送到此邮箱
        """,
        'select_domain': "请选择您想要的域名：",
        'enter_email_name': """
已选择域名：{domain}

现在请发送邮箱名称
示例：mymail
        """,
        'invalid_email_name': "⚠️ 邮箱名称无效\n请仅使用英文字母和数字\n示例：mymail123",
        'my_emails': "您的邮箱列表：",
        'no_emails': "未找到邮箱\n请使用主菜单按钮创建新邮箱",
        'email_selected': "已选择邮箱：\n{email}\n\n请选择一项操作",
        'fetching': "正在获取邮件...请稍候",
        'no_messages': "未找到邮件\n还没有邮件到达",
        'refreshing': "正在更新...",
        'still_no_messages': "尚未收到邮件\n请稍后再试或稍后查看",
        'delete_all_confirm': "⚠️ 您确定要删除所有邮箱吗？\n\n数量：{count}\n\n此操作不可撤销！",
        'no_emails_to_delete': "没有邮箱需要删除",
        'delete_all_success': "✅ 所有邮箱已成功删除",
        'delete_all_error': "❌ 删除邮箱时出错：\n{error}",
        'delete_confirm': "⚠️ 您确定要删除此邮箱吗？\n\n{email}\n\n此操作不可撤销！",
        'delete_success': "✅ 邮箱已成功删除\n\n{email}",
        'delete_error': "❌ 删除邮箱时出错：\n{error}",
        'admin_panel': """
👑 管理面板

你好 {user_link}
欢迎来到您的面板
        """,
        'add_channel_prompt': "请发送频道用户名（带@）\n示例：@my_channel",
        'not_channel': "❌ 此用户名不属于频道或群组",
        'bot_not_admin': "🚫 机器人必须是频道的管理员",
        'channel_exists': "⚠️ 频道已存在\n{channel}",
        'channel_added': "✅ 频道添加成功\n\n{channel}\n{link}",
        'channel_error': "❌ 错误：\n{error}",
        'remove_channel_prompt': "请发送要删除的频道用户名\n示例：@my_channel",
        'channel_removed': "✅ 频道已成功删除\n{channel}",
        'channel_not_found': "❌ 未找到此频道\n{channel}",
        'channel_list': "必需频道列表：\n\n",
        'no_channels': "没有注册频道",
        'delete_all_channels_confirm': "⚠️ 您确定要删除所有频道吗？\n此操作不可撤销！",
        'all_channels_deleted': "✅ 所有频道已成功删除\n\n",
        'no_channels_to_delete': "没有频道需要删除",
        'subscription_required': """
⚠️ 亲爱的 {name}

要使用此机器人，您必须先加入我们的频道

🔗 加入链接：{link}

加入后，请再次发送 /start。
        """,
        'error_random': "❌ 创建邮箱时出错\n请重试",
        'error_domains': "❌ 获取域名列表时出错\n请重试",
        'error_custom': "❌ 创建自定义邮箱时出错\n请重试",
        'error_server': "服务器错误：{code}",
        'error_connection': "连接错误：{error}",
        'back': "返回",
        'back_to_menu': "返回主菜单",
        'random_btn': "随机邮箱",
        'custom_btn': "自定义邮箱",
        'list_btn': "邮箱列表",
        'delete_all_btn': "删除所有邮箱",
        'channel_btn': "机器人频道",
        'receive_btn': "接收邮件",
        'delete_btn': "删除邮箱",
        'refresh_btn': "刷新",
        'confirm_yes': "是的，删除",
        'cancel': "取消",
        'prev': "上一封",
        'next': "下一封",
        'admin_btn': "管理面板",
        'add_channel_btn': "添加频道",
        'remove_channel_btn': "删除频道",
        'list_channels_btn': "频道列表",
        'delete_all_channels_btn': "删除所有频道",
        'access_denied': "❌ 您无权访问此部分",
        'no_access': "❌ 您无权访问此部分",
        'message_prefix': """
第 {current} 封，共 {total} 封
====================================
发件人：{from}
收件人：{to}
时间：{time}
主题：{subject}
正文：
{body}
{attachments}
        """,
        'attachment_text': "\n附件：\n",
        'attachment_item': "{name} - {size}\n",
        'no_subject': '无主题',
        'no_sender': '未知发件人',
        'no_body': '无内容',
        'unknown_time': '未知',
        'lang_btn': "🌐 语言",
        'lang_select': "选择您的语言 / Select your language / زبان خود را انتخاب کنید",
        'lang_changed': "✅ 语言已切换为中文",
        'lang_en': "English",
        'lang_zh': "中文",
        'lang_fa': "فارسی",
    }
}

# ============================================ #
#              توابع کمکی / Helpers             #
# ============================================ #

def get_lang(user_id):
    return user_lang.get(str(user_id), 'fa')

def set_lang(user_id, lang):
    user_lang[str(user_id)] = lang
    with open('data/lang.json', 'w') as f:
        json.dump(user_lang, f)

def t(user_id, key, **kwargs):
    lang = get_lang(user_id)
    text = TEXTS.get(lang, TEXTS['fa']).get(key, TEXTS['fa'].get(key, key))
    if kwargs:
        try:
            return text.format(**kwargs)
        except:
            return text
    return text

def call_api(endpoint, params=None, token=None):
    if params is None:
        params = {}
    url = f"{API_URL}?mail={endpoint}"
    if token:
        params['token'] = token
    if params:
        url += '&' + '&'.join([f"{k}={v}" for k, v in params.items()])
    try:
        response = session.get(url, verify=False, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return {'success': False, 'error': f'خطا در ارتباط با سرور: {response.status_code}'}
    except Exception as e:
        return {'success': False, 'error': f'خطا در اتصال به سرور: {str(e)}'}

def save_data():
    with open('data/data.json', 'w') as f:
        json.dump(user_tokens, f)

def format_file_size(bytes):
    if bytes == 0:
        return "0 B"
    sizes = ['B', 'KB', 'MB', 'GB']
    i = 0
    while bytes >= 1024 and i < len(sizes) - 1:
        bytes /= 1024.0
        i += 1
    return f"{round(bytes, 2)} {sizes[i]}"

# ============================================ #
#            بررسی عضویت / Membership Check     #
# ============================================ #

def is_user_member(user_id):
    channels = cursor.execute("SELECT channel_name, invite_link FROM channels").fetchall()
    for ch_name, invite_link in channels:
        try:
            status = bot.get_chat_member(chat_id=ch_name, user_id=user_id).status
            if status not in ["member", "administrator", "creator"]:
                return False, invite_link
        except:
            continue
    return True, None

def send_subscription_request(msg, invite_link):
    user_id = msg.from_user.id
    name = msg.from_user.first_name
    if invite_link:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(t(user_id, 'channel_btn'), url=f"{invite_link}"))
        bot.reply_to(
            msg,
            t(user_id, 'subscription_required', name=name, link=invite_link),
            disable_web_page_preview=True,
            reply_markup=markup
        )

def send_subscription_request_callback(call, invite_link):
    user_id = call.from_user.id
    name = call.from_user.first_name
    if invite_link:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(t(user_id, 'channel_btn'), url=f"{invite_link}"))
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=t(user_id, 'subscription_required', name=name, link=invite_link),
            disable_web_page_preview=True,
            reply_markup=markup
        )
        bot.clear_step_handler(call.message)

# ============================================ #
#           نمایش پیام‌ها / Display Messages    #
# ============================================ #

def display_message(chat_id, message_id, current_index, total_messages, message, email):
    user_id = str(chat_id)
    lang = get_lang(user_id)
    
    body_text = html.unescape(message.get('body_text', t(user_id, 'no_body')))
    from_email = html.unescape(message.get('from', t(user_id, 'no_sender')))
    subject = html.unescape(message.get('subject', t(user_id, 'no_subject')))
    to_email = message.get('to', email)
    created_at = message.get('created_at', t(user_id, 'unknown_time'))
    
    attachments_text = ""
    if message.get('attachments'):
        attachments_text = t(user_id, 'attachment_text')
        for attachment in message['attachments']:
            attachment_name = html.unescape(attachment.get('name', 'file'))
            attachment_size = format_file_size(attachment.get('size', 0))
            attachments_text += t(user_id, 'attachment_item', name=attachment_name, size=attachment_size)
    
    navigation_buttons = []
    if total_messages > 1:
        if current_index > 0:
            navigation_buttons.append(InlineKeyboardButton(t(user_id, 'prev'), callback_data=f'prevmsg:{current_index}'))
        navigation_buttons.append(InlineKeyboardButton(f'{current_index + 1}/{total_messages}', callback_data='none'))
        if current_index < total_messages - 1:
            navigation_buttons.append(InlineKeyboardButton(t(user_id, 'next'), callback_data=f'nextmsg:{current_index}'))
    
    keyboard = []
    if navigation_buttons:
        keyboard.append(navigation_buttons)
    keyboard.append([InlineKeyboardButton(t(user_id, 'refresh_btn'), callback_data=f'refresh:{email}')])
    keyboard.append([InlineKeyboardButton(t(user_id, 'back_to_menu'), callback_data='back_to_start')])
    
    message_text = t(user_id, 'message_prefix',
        current=current_index + 1,
        total=total_messages,
        from_email=from_email,
        to=to_email,
        time=created_at,
        subject=subject,
        body=body_text,
        attachments=attachments_text
    )
    
    markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(message_text, chat_id, message_id, reply_markup=markup)

# ============================================ #
#         دکمه‌های منو / Menu Buttons          #
# ============================================ #

def get_main_menu(user_id):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(t(user_id, 'random_btn'), callback_data='rndemail'),
        InlineKeyboardButton(t(user_id, 'custom_btn'), callback_data='specifemail')
    )
    markup.add(InlineKeyboardButton(t(user_id, 'list_btn'), callback_data='myemail'))
    markup.add(InlineKeyboardButton(t(user_id, 'delete_all_btn'), callback_data='deleteall1'))
    markup.add(
        InlineKeyboardButton(t(user_id, 'channel_btn'), url=f"https://t.me/{CHANNEL_USERNAME}"),
        InlineKeyboardButton(t(user_id, 'lang_btn'), callback_data='change_lang')
    )
    if user_id in ADMIN_IDS:
        markup.add(InlineKeyboardButton(t(user_id, 'admin_btn'), callback_data='admin_panel'))
    return markup

# ============================================ #
#          دستورات ربات / Bot Commands         #
# ============================================ #

@bot.message_handler(commands=['start', 'lang'])
def start_command(message):
    user_id = message.from_user.id
    is_member, invite_link = is_user_member(user_id)
    if not is_member:
        send_subscription_request(message, invite_link)
        return

    chat_id = message.chat.id
    if str(chat_id) not in user_tokens:
        res = call_api('token')
        if res.get('success'):
            user_tokens[str(chat_id)] = res['token']
            save_data()

    first_name = message.from_user.first_name
    user_mention = f"[{first_name}](tg://user?id={message.from_user.id})"
    
    # Check if it's a language change command
    if message.text == '/lang':
        show_lang_menu(message)
        return

    txt = t(user_id, 'start', user_mention=user_mention)
    markup = get_main_menu(user_id)
    bot.reply_to(message, txt, reply_markup=markup, parse_mode='Markdown')

# ============================================ #
#          منوی زبان / Language Menu           #
# ============================================ #

def show_lang_menu(message):
    user_id = message.from_user.id
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🇮🇷 فارسی", callback_data='setlang_fa'),
        InlineKeyboardButton("🇬🇧 English", callback_data='setlang_en'),
        InlineKeyboardButton("🇨🇳 中文", callback_data='setlang_zh')
    )
    markup.add(InlineKeyboardButton(t(user_id, 'back_to_menu'), callback_data='back_to_start'))
    bot.reply_to(message, t(user_id, 'lang_select'), reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('setlang_'))
def set_language(call):
    user_id = call.from_user.id
    lang = call.data.split('_')[1]
    set_lang(user_id, lang)
    
    # Update the message
    markup = get_main_menu(user_id)
    bot.edit_message_text(
        t(user_id, 'lang_changed'),
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )
    
    # Also update the main menu if user is admin
    if user_id in ADMIN_IDS:
        markup_admin = get_main_menu(user_id)
        # We'll just keep the current message

@bot.callback_query_handler(func=lambda call: call.data == 'change_lang')
def change_lang_callback(call):
    user_id = call.from_user.id
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🇮🇷 فارسی", callback_data='setlang_fa'),
        InlineKeyboardButton("🇬🇧 English", callback_data='setlang_en'),
        InlineKeyboardButton("🇨🇳 中文", callback_data='setlang_zh')
    )
    markup.add(InlineKeyboardButton(t(user_id, 'back_to_menu'), callback_data='back_to_start'))
    bot.edit_message_text(
        t(user_id, 'lang_select'),
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )

# ============================================ #
#          پنل مدیریت / Admin Panel            #
# ============================================ #

@bot.message_handler(commands=['admin'])
def admin_command(message):
    user_id = message.from_user.id
    
    if user_id not in ADMIN_IDS:
        bot.reply_to(message, t(user_id, 'access_denied'), parse_mode='Markdown')
        return
    
    is_member, invite_link = is_user_member(user_id)
    if not is_member:
        send_subscription_request(message, invite_link)
        return
    
    show_admin_panel(message, None)

def show_admin_panel(message, call):
    user_id = message.from_user.id if message else call.from_user.id
    markup = InlineKeyboardMarkup(row_width=2)
    user = bot.get_chat(user_id)
    user_link = f"[{user.first_name}](tg://user?id={user_id})"

    markup.add(
        InlineKeyboardButton(t(user_id, 'add_channel_btn'), callback_data='add_channel'),
        InlineKeyboardButton(t(user_id, 'remove_channel_btn'), callback_data='remove_channel')
    )
    markup.add(InlineKeyboardButton(t(user_id, 'list_channels_btn'), callback_data='show_channels'))
    markup.add(InlineKeyboardButton(t(user_id, 'delete_all_channels_btn'), callback_data='delete_all_channels'))
    markup.add(InlineKeyboardButton(t(user_id, 'back_to_menu'), callback_data='back_to_start'))

    text = t(user_id, 'admin_panel', user_link=user_link)
    
    if message:
        bot.reply_to(message, text, reply_markup=markup, parse_mode='Markdown')
    else:
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == 'admin_panel')
def admin_panel_callback(call):
    if call.from_user.id not in ADMIN_IDS:
        bot.answer_callback_query(call.id, t(call.from_user.id, 'access_denied'), show_alert=True)
        return
    show_admin_panel(None, call)

# ============================================ #
#          بازگشت به منو / Back to Menu        #
# ============================================ #

@bot.callback_query_handler(func=lambda call: call.data == 'back_to_start')
def back_to_main(call):
    user_id = call.from_user.id
    is_member, invite_link = is_user_member(user_id)
    if not is_member:
        send_subscription_request_callback(call, invite_link)
        return
    
    chat_id = call.message.chat.id
    if str(chat_id) not in user_tokens:
        res = call_api('token')
        if res.get('success'):
            user_tokens[str(chat_id)] = res['token']
            save_data()

    first_name = call.from_user.first_name
    user_mention = f"[{first_name}](tg://user?id={call.from_user.id})"

    txt = t(user_id, 'start', user_mention=user_mention)
    markup = get_main_menu(user_id)
    bot.edit_message_text(txt, chat_id, call.message.message_id, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == 'back_to_admin')
def back_to_admin(call):
    if call.from_user.id not in ADMIN_IDS:
        return
    show_admin_panel(None, call)

# ============================================ #
#          ایمیل تصادفی / Random Email         #
# ============================================ #

@bot.callback_query_handler(func=lambda call: call.data == 'rndemail')
def random_email(call):
    user_id = call.from_user.id
    is_member, invite_link = is_user_member(user_id)
    if not is_member:
        send_subscription_request_callback(call, invite_link)
        return

    chat_id = call.message.chat.id
    token = user_tokens.get(str(chat_id))
    res = call_api('random', {}, token)

    if res.get('success'):
        email = res['email']
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton(t(user_id, 'receive_btn'), callback_data=f'getemails:{email}'),
            InlineKeyboardButton(t(user_id, 'delete_btn'), callback_data=f'confirm_delete:{email}')
        )
        markup.add(InlineKeyboardButton(t(user_id, 'back_to_menu'), callback_data='back_to_start'))

        txt = t(user_id, 'random_email', email=email)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=txt,
            parse_mode='Markdown',
            reply_markup=markup
        )
    else:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(t(user_id, 'back_to_menu'), callback_data='back_to_start'))
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=t(user_id, 'error_random'),
            parse_mode='Markdown',
            reply_markup=markup
        )

# ============================================ #
#           ایمیل دلخواه / Custom Email        #
# ============================================ #

@bot.callback_query_handler(func=lambda call: call.data == 'specifemail')
def custom_email_domain(call):
    user_id = call.from_user.id
    is_member, invite_link = is_user_member(user_id)
    if not is_member:
        send_subscription_request_callback(call, invite_link)
        return

    chat_id = call.message.chat.id
    token = user_tokens.get(str(chat_id))
    res = call_api('domains', {}, token)

    if res.get('success') and res.get('domains'):
        markup = InlineKeyboardMarkup(row_width=2)
        buttons = []
        
        for domain in res['domains']:
            buttons.append(InlineKeyboardButton(domain['name'], callback_data=f'domainis:{domain["name"]}'))
        
        for i in range(0, len(buttons), 2):
            if i + 1 < len(buttons):
                markup.add(buttons[i], buttons[i+1])
            else:
                markup.add(buttons[i])
        
        markup.add(InlineKeyboardButton(t(user_id, 'back_to_menu'), callback_data='back_to_start'))
        
        bot.edit_message_text(
            t(user_id, 'select_domain'),
            chat_id=chat_id,
            message_id=call.message.message_id,
            parse_mode='Markdown',
            reply_markup=markup
        )
    else:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(t(user_id, 'back_to_menu'), callback_data='back_to_start'))
        bot.edit_message_text(
            t(user_id, 'error_domains'),
            chat_id=chat_id,
            message_id=call.message.message_id,
            parse_mode='Markdown',
            reply_markup=markup
        )

@bot.callback_query_handler(func=lambda call: call.data.startswith('domainis:'))
def get_custom_email(call):
    user_id = call.from_user.id
    is_member, invite_link = is_user_member(user_id)
    if not is_member:
        send_subscription_request_callback(call, invite_link)
        return

    chat_id = call.message.chat.id
    
    if str(chat_id) not in user_tokens:
        res = call_api('token')
        if res.get('success'):
            user_tokens[str(chat_id)] = res['token']
            save_data()
    
    domain = call.data.split(':', 1)[1]
    user_tokens[f'{chat_id}_domain'] = domain
    save_data()
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(t(user_id, 'cancel'), callback_data='back_to_start'))
    
    txt = t(user_id, 'enter_email_name', domain=domain)
    bot.edit_message_text(
        txt,
        chat_id=chat_id,
        message_id=call.message.message_id,
        parse_mode='Markdown',
        reply_markup=markup
    )

# ============================================ #
#          لیست ایمیل‌ها / Email List          #
# ============================================ #

@bot.callback_query_handler(func=lambda call: call.data == 'myemail')
def my_emails(call):
    user_id = call.from_user.id
    is_member, invite_link = is_user_member(user_id)
    if not is_member:
        send_subscription_request_callback(call, invite_link)
        return

    chat_id = call.message.chat.id
    token = user_tokens.get(str(chat_id))
    res = call_api('my-emails', {}, token)

    if res.get('success') and res.get('emails'):
        markup = InlineKeyboardMarkup()
        
        for email in res['emails']:
            markup.add(InlineKeyboardButton(email, callback_data=f'selectmail:{email}'))
        
        markup.add(InlineKeyboardButton(t(user_id, 'back_to_menu'), callback_data='back_to_start'))
        
        bot.edit_message_text(
            t(user_id, 'my_emails'),
            chat_id,
            call.message.message_id,
            parse_mode='Markdown',
            reply_markup=markup
        )
    else:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(t(user_id, 'back_to_menu'), callback_data='back_to_start'))
        bot.edit_message_text(
            t(user_id, 'no_emails'),
            chat_id,
            call.message.message_id,
            parse_mode='Markdown',
            reply_markup=markup
        )

@bot.callback_query_handler(func=lambda call: call.data.startswith('selectmail:'))
def select_email(call):
    user_id = call.from_user.id
    is_member, invite_link = is_user_member(user_id)
    if not is_member:
        send_subscription_request_callback(call, invite_link)
        return

    email = call.data.split(':', 1)[1]
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(t(user_id, 'receive_btn'), callback_data=f'getemails:{email}'),
        InlineKeyboardButton(t(user_id, 'delete_btn'), callback_data=f'confirm_delete:{email}')
    )
    markup.add(InlineKeyboardButton(t(user_id, 'back'), callback_data='myemail'))
    
    bot.edit_message_text(
        t(user_id, 'email_selected', email=email),
        call.message.chat.id,
        call.message.message_id,
        parse_mode='Markdown',
        reply_markup=markup
    )

# ============================================ #
#           دریافت پیام‌ها / Get Messages      #
# ============================================ #

@bot.callback_query_handler(func=lambda call: call.data.startswith('getemails:'))
def get_emails(call):
    user_id = call.from_user.id
    is_member, invite_link = is_user_member(user_id)
    if not is_member:
        send_subscription_request_callback(call, invite_link)
        return

    chat_id = call.message.chat.id
    email = call.data.split(':', 1)[1]
    token = user_tokens.get(str(chat_id))
    
    bot.edit_message_text(
        t(user_id, 'fetching'),
        chat_id,
        call.message.message_id,
        parse_mode='Markdown'
    )
    
    res = call_api('messages', {'email': email}, token)
    
    if res.get('success') and res.get('messages'):
        total = len(res['messages'])
        current_messages[str(chat_id)] = res['messages']
        current_message_index[str(chat_id)] = 0
        
        display_message(
            chat_id,
            call.message.message_id,
            0,
            total,
            res['messages'][0],
            email
        )
    else:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(t(user_id, 'refresh_btn'), callback_data=f'refresh:{email}'))
        markup.add(InlineKeyboardButton(t(user_id, 'back'), callback_data='myemail'))
        
        bot.edit_message_text(
            t(user_id, 'no_messages'),
            chat_id,
            call.message.message_id,
            parse_mode='Markdown',
            reply_markup=markup
        )

@bot.callback_query_handler(func=lambda call: call.data.startswith('refresh:'))
def refresh_emails(call):
    user_id = call.from_user.id
    is_member, invite_link = is_user_member(user_id)
    if not is_member:
        send_subscription_request_callback(call, invite_link)
        return

    chat_id = call.message.chat.id
    email = call.data.split(':', 1)[1]
    token = user_tokens.get(str(chat_id))
    
    bot.edit_message_text(
        t(user_id, 'refreshing'),
        chat_id,
        call.message.message_id,
        parse_mode='Markdown'
    )
    
    res = call_api('messages', {'email': email}, token)
    
    if res.get('success') and res.get('messages'):
        total = len(res['messages'])
        current_messages[str(chat_id)] = res['messages']
        current_message_index[str(chat_id)] = 0
        
        display_message(
            chat_id,
            call.message.message_id,
            0,
            total,
            res['messages'][0],
            email
        )
    else:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(t(user_id, 'refresh_btn'), callback_data=f'refresh:{email}'))
        markup.add(InlineKeyboardButton(t(user_id, 'back'), callback_data='myemail'))
        
        bot.edit_message_text(
            t(user_id, 'still_no_messages'),
            chat_id,
            call.message.message_id,
            parse_mode='Markdown',
            reply_markup=markup
        )

# ============================================ #
#          ناوبری پیام‌ها / Message Navigation #
# ============================================ #

@bot.callback_query_handler(func=lambda call: call.data.startswith('prevmsg:') or call.data.startswith('nextmsg:'))
def navigate_messages(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    if str(chat_id) in current_messages:
        messages = current_messages[str(chat_id)]
        current_index = current_message_index.get(str(chat_id), 0)
        
        if call.data.startswith('prevmsg:') and current_index > 0:
            current_index -= 1
        elif call.data.startswith('nextmsg:') and current_index < len(messages) - 1:
            current_index += 1
        
        current_message_index[str(chat_id)] = current_index
        email = messages[0].get('to', '')
        
        display_message(
            chat_id,
            call.message.message_id,
            current_index,
            len(messages),
            messages[current_index],
            email
        )

# ============================================ #
#           حذف ایمیل‌ها / Delete Emails       #
# ============================================ #

@bot.callback_query_handler(func=lambda call: call.data == 'deleteall1')
def confirm_delete_all(call):
    user_id = call.from_user.id
    is_member, invite_link = is_user_member(user_id)
    if not is_member:
        send_subscription_request_callback(call, invite_link)
        return

    chat_id = call.message.chat.id
    token = user_tokens.get(str(chat_id))
    res = call_api('my-emails', {}, token)
    
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(t(user_id, 'confirm_yes'), callback_data="deleteall2"),
        InlineKeyboardButton(t(user_id, 'cancel'), callback_data="back_to_start")
    )
    
    if res.get('success') and res.get('emails'):
        count = len(res['emails'])
        bot.edit_message_text(
            t(user_id, 'delete_all_confirm', count=count),
            chat_id,
            call.message.message_id,
            parse_mode='Markdown',
            reply_markup=markup
        )
    else:
        bot.edit_message_text(
            t(user_id, 'no_emails_to_delete'),
            chat_id,
            call.message.message_id,
            parse_mode='Markdown',
            reply_markup=markup
        )

@bot.callback_query_handler(func=lambda call: call.data == 'deleteall2')
def delete_all_emails(call):
    user_id = call.from_user.id
    is_member, invite_link = is_user_member(user_id)
    if not is_member:
        send_subscription_request_callback(call, invite_link)
        return

    chat_id = call.message.chat.id
    token = user_tokens.get(str(chat_id))
    res = call_api('delete-all', {}, token)
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(t(user_id, 'back_to_menu'), callback_data='back_to_start'))
    
    if res.get('success'):
        bot.edit_message_text(
            t(user_id, 'delete_all_success'),
            chat_id,
            call.message.message_id,
            parse_mode='Markdown',
            reply_markup=markup
        )
    else:
        error_msg = res.get('error', 'خطای ناشناخته')
        bot.edit_message_text(
            t(user_id, 'delete_all_error', error=error_msg),
            chat_id,
            call.message.message_id,
            parse_mode='Markdown',
            reply_markup=markup
        )

@bot.callback_query_handler(func=lambda call: call.data.startswith('confirm_delete:'))
def confirm_delete_email(call):
    user_id = call.from_user.id
    is_member, invite_link = is_user_member(user_id)
    if not is_member:
        send_subscription_request_callback(call, invite_link)
        return

    email = call.data.split(':', 1)[1]
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(t(user_id, 'confirm_yes'), callback_data=f'delete:{email}'),
        InlineKeyboardButton(t(user_id, 'cancel'), callback_data='back_to_start')
    )
    
    bot.edit_message_text(
        t(user_id, 'delete_confirm', email=email),
        call.message.chat.id,
        call.message.message_id,
        parse_mode='Markdown',
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('delete:'))
def delete_email(call):
    user_id = call.from_user.id
    is_member, invite_link = is_user_member(user_id)
    if not is_member:
        send_subscription_request_callback(call, invite_link)
        return

    chat_id = call.message.chat.id
    email = call.data.split(':', 1)[1]
    token = user_tokens.get(str(chat_id))
    res = call_api('delete-email', {'email': email}, token)
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(t(user_id, 'back'), callback_data='myemail'))
    
    if res.get('success'):
        bot.edit_message_text(
            t(user_id, 'delete_success', email=email),
            chat_id,
            call.message.message_id,
            parse_mode='Markdown',
            reply_markup=markup
        )
    else:
        error_msg = res.get('error', 'خطای ناشناخته')
        bot.edit_message_text(
            t(user_id, 'delete_error', error=error_msg),
            chat_id,
            call.message.message_id,
            parse_mode='Markdown',
            reply_markup=markup
        )

# ============================================ #
#           دریافت نام ایمیل دلخواه            #
#        Receive Custom Email Name             #
# ============================================ #

@bot.message_handler(func=lambda message: True)
def handle_custom_email_name(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    if f'{chat_id}_domain' in user_tokens:
        domain = user_tokens[f'{chat_id}_domain']
        email_name = message.text.strip()
        
        # بررسی کاراکترهای غیرمجاز / Check invalid characters
        if re.search("[\u0600-\u06FF\u2000-\u200F\u2028-\u202F]", email_name):
            bot.send_message(
                chat_id,
                t(user_id, 'invalid_email_name'),
                parse_mode='Markdown',
                reply_to_message_id=message.message_id
            )
            return
        
        token = user_tokens.get(str(chat_id))
        res = call_api('custom', {'name': email_name, 'domain': domain}, token)
        
        # پاک کردن دامنه موقت / Clear temp domain
        if f'{chat_id}_domain' in user_tokens:
            del user_tokens[f'{chat_id}_domain']
            save_data()
        
        if res.get('success'):
            email = res['email']
            markup = InlineKeyboardMarkup()
            markup.add(
                InlineKeyboardButton(t(user_id, 'receive_btn'), callback_data=f'getemails:{email}'),
                InlineKeyboardButton(t(user_id, 'delete_btn'), callback_data=f'confirm_delete:{email}')
            )
            markup.add(InlineKeyboardButton(t(user_id, 'back_to_menu'), callback_data='back_to_start'))
            
            txt = t(user_id, 'custom_email', email=email)
            bot.send_message(
                chat_id,
                txt,
                parse_mode='Markdown',
                reply_to_message_id=message.message_id,
                reply_markup=markup
            )
        else:
            bot.send_message(
                chat_id,
                t(user_id, 'error_custom'),
                parse_mode='Markdown',
                reply_to_message_id=message.message_id
            )

# ============================================ #
#           مدیریت کانال‌ها / Channel Mgmt     #
# ============================================ #

@bot.callback_query_handler(func=lambda call: call.data == 'add_channel')
def add_channel_step(call):
    user_id = call.from_user.id
    if user_id not in ADMIN_IDS:
        return
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(t(user_id, 'back'), callback_data='back_to_admin'))
    bot.edit_message_text(
        t(user_id, 'add_channel_prompt'),
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )
    bot.register_next_step_handler(call.message, add_channel)

def add_channel(message):
    user_id = message.from_user.id
    channel_name = message.text.strip()
    if not channel_name.startswith('@'):
        channel_name = '@' + channel_name
    
    try:
        chat_info = bot.get_chat(channel_name)
        if chat_info.type not in ['channel', 'supergroup', 'group']:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(t(user_id, 'back'), callback_data='back_to_admin'))
            bot.reply_to(message, t(user_id, 'not_channel'), reply_markup=markup)
            return
        
        admins = bot.get_chat_administrators(channel_name)
        bot_is_admin = any(admin.user.id == bot.get_me().id for admin in admins)
        
        if not bot_is_admin:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(t(user_id, 'back'), callback_data='back_to_admin'))
            bot.reply_to(message, t(user_id, 'bot_not_admin'), reply_markup=markup)
            return
        
        cursor.execute("SELECT * FROM channels WHERE channel_name = ?", (channel_name,))
        if cursor.fetchone():
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(t(user_id, 'back'), callback_data='back_to_admin'))
            bot.reply_to(message, t(user_id, 'channel_exists', channel=channel_name), reply_markup=markup)
        else:
            invite_link = bot.export_chat_invite_link(chat_info.id)
            cursor.execute("INSERT INTO channels (channel_name, invite_link) VALUES (?, ?)", (channel_name, invite_link))
            conn.commit()
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(t(user_id, 'back'), callback_data='back_to_admin'))
            bot.reply_to(
                message,
                t(user_id, 'channel_added', channel=channel_name, link=invite_link),
                reply_markup=markup
            )
    except Exception as e:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(t(user_id, 'back'), callback_data='back_to_admin'))
        bot.reply_to(message, t(user_id, 'channel_error', error=str(e)), reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'remove_channel')
def remove_channel_step(call):
    user_id = call.from_user.id
    if user_id not in ADMIN_IDS:
        return
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(t(user_id, 'back'), callback_data='back_to_admin'))
    bot.edit_message_text(
        t(user_id, 'remove_channel_prompt'),
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )
    bot.register_next_step_handler(call.message, remove_channel)

def remove_channel(message):
    user_id = message.from_user.id
    channel_name = message.text.strip()
    
    cursor.execute("SELECT * FROM channels WHERE channel_name = ?", (channel_name,))
    if cursor.fetchone():
        cursor.execute("DELETE FROM channels WHERE channel_name = ?", (channel_name,))
        conn.commit()
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(t(user_id, 'back'), callback_data='back_to_admin'))
        bot.reply_to(message, t(user_id, 'channel_removed', channel=channel_name), reply_markup=markup)
    else:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(t(user_id, 'back'), callback_data='back_to_admin'))
        bot.reply_to(message, t(user_id, 'channel_not_found', channel=channel_name), reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'show_channels')
def show_channels(call):
    user_id = call.from_user.id
    if user_id not in ADMIN_IDS:
        return
    cursor.execute("SELECT channel_name FROM channels")
    channels = cursor.fetchall()
    
    markup = InlineKeyboardMarkup()
    if channels:
        text = t(user_id, 'channel_list')
        for ch in channels:
            ch_name = ch[0].replace("@", "")
            text += f"🔹 @{ch_name}\n"
            markup.add(InlineKeyboardButton(f"🔹 {ch_name}", url=f"https://t.me/{ch_name}"))
        markup.add(InlineKeyboardButton(t(user_id, 'back'), callback_data='back_to_admin'))
    else:
        text = t(user_id, 'no_channels')
        markup.add(InlineKeyboardButton(t(user_id, 'back'), callback_data='back_to_admin'))
    
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'delete_all_channels')
def confirm_delete_all_channels(call):
    user_id = call.from_user.id
    if user_id not in ADMIN_IDS:
        return
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(t(user_id, 'confirm_yes'), callback_data='confirm_delete_all'),
        InlineKeyboardButton(t(user_id, 'cancel'), callback_data='back_to_admin')
    )
    
    bot.edit_message_text(
        t(user_id, 'delete_all_channels_confirm'),
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == 'confirm_delete_all')
def delete_all_channels(call):
    user_id = call.from_user.id
    if user_id not in ADMIN_IDS:
        return
    cursor.execute("SELECT channel_name FROM channels")
    channels = cursor.fetchall()
    
    if channels:
        cursor.execute("DELETE FROM channels")
        conn.commit()
        text = t(user_id, 'all_channels_deleted')
        for ch in channels:
            text += f"{ch[0]}\n"
    else:
        text = t(user_id, 'no_channels_to_delete')
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(t(user_id, 'back'), callback_data='back_to_admin'))
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

# ============================================ #
#            استارت ربات / Start Bot           #
# ============================================ #

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
print("=" * 50)
print("ربات ایمیل موقت سه‌زبانه با موفقیت استارت خورد")
print("Temporary Email Bot v3.0 started successfully")
print("开发者: @HamidYaraliOfficial")
print("Telegram & Instagram: @HamidYaraliOfficial")
print(f"ادمین‌ها / Admins: {ADMIN_IDS}")
print("=" * 50)

bot.delete_webhook()
bot.infinity_polling()

# Developer @HamidYaraliOfficial
# Telegram & Instagram: @HamidYaraliOfficial