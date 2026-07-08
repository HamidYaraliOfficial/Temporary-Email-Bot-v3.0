# Temporary Email Bot v3.0

> Professional Multilingual Temporary Email Telegram Bot (Persian / English / Chinese)

---

# 🇬🇧 English

## Overview

Temporary Email Bot v3.0 is a professional Telegram bot that allows users to generate temporary email addresses, receive emails, manage inboxes, create custom email addresses, and use the bot in three languages: Persian, English, and Chinese.

### Features

- Random temporary email generation
- Custom email creation with multiple domains
- Receive and read incoming emails
- Email management and deletion
- Multi-language interface
  - Persian
  - English
  - Chinese
- Admin panel
- Forced channel membership system
- SQLite database support
- Fast API communication with retry mechanism
- User language persistence
- Email attachment support

---

## Installation

### Install Python Dependencies

```bash
pip install pyTelegramBotAPI requests urllib3
```

### Required Packages

| Package | Purpose |
|----------|----------|
| pyTelegramBotAPI | Telegram Bot Framework |
| requests | API Requests |
| urllib3 | Network & Retry Support |
| sqlite3 | Built into Python |
| json | Built into Python |
| os | Built into Python |
| re | Built into Python |
| html | Built into Python |

---

## Configuration

Edit the following variables inside the source code:

```python
TOKEN = "YOUR_BOT_TOKEN"
CHANNEL_USERNAME = "YOUR_CHANNEL"
ADMIN_IDS = [YOUR_ADMIN_ID]
API_URL = "YOUR_API_URL"
```

---

## Run

```bash
python "Temporary Email Bot.py"
```

---

## Project Structure

```text
Temporary Email Bot.py
channels.db
data/
 ├── data.json
 └── lang.json
```

---

## Main Functions

- Temporary Email Generation
- Custom Email Creation
- Message Retrieval
- Message Navigation
- Email Deletion
- Forced Subscription Check
- Multi-Language Support
- Admin Channel Management

---

## License

This project is provided for educational and development purposes.

---

# 🇮🇷 فارسی

## معرفی

ربات ایمیل موقت نسخه 3.0 یک ربات حرفه‌ای تلگرام است که امکان ساخت ایمیل موقت، دریافت پیام‌ها، مدیریت صندوق ایمیل، ساخت ایمیل دلخواه و استفاده به سه زبان فارسی، انگلیسی و چینی را فراهم می‌کند.

### امکانات

- ساخت ایمیل تصادفی
- ساخت ایمیل دلخواه با دامنه‌های مختلف
- دریافت و مشاهده ایمیل‌ها
- حذف ایمیل‌ها
- رابط کاربری سه‌زبانه
  - فارسی
  - انگلیسی
  - چینی
- پنل مدیریت
- سیستم عضویت اجباری کانال
- پایگاه داده SQLite
- ارتباط سریع با API
- ذخیره زبان کاربران
- پشتیبانی از فایل‌های ضمیمه

---

## نصب

### نصب کتابخانه‌های مورد نیاز

```bash
pip install pyTelegramBotAPI requests urllib3
```

### کتابخانه‌ها

| کتابخانه | کاربرد |
|-----------|---------|
| pyTelegramBotAPI | ساخت ربات تلگرام |
| requests | ارسال درخواست به API |
| urllib3 | مدیریت ارتباط و Retry |
| sqlite3 | داخلی پایتون |
| json | داخلی پایتون |
| os | داخلی پایتون |
| re | داخلی پایتون |
| html | داخلی پایتون |

---

## تنظیمات

در فایل اصلی مقادیر زیر را ویرایش کنید:

```python
TOKEN = "YOUR_BOT_TOKEN"
CHANNEL_USERNAME = "YOUR_CHANNEL"
ADMIN_IDS = [YOUR_ADMIN_ID]
API_URL = "YOUR_API_URL"
```

---

## اجرا

```bash
python "Temporary Email Bot.py"
```

---

## ساختار پروژه

```text
Temporary Email Bot.py
channels.db
data/
 ├── data.json
 └── lang.json
```

---

## قابلیت‌های اصلی

- ساخت ایمیل موقت
- ساخت ایمیل دلخواه
- دریافت پیام‌ها
- پیمایش بین پیام‌ها
- حذف ایمیل‌ها
- بررسی عضویت اجباری
- پشتیبانی چندزبانه
- مدیریت کانال‌ها توسط ادمین

---

## مجوز

این پروژه برای اهداف آموزشی و توسعه ارائه شده است.

---

# 🇨🇳 中文

## 项目介绍

Temporary Email Bot v3.0 是一个专业的 Telegram 临时邮箱机器人，支持创建临时邮箱、接收邮件、管理邮箱、自定义邮箱地址以及多语言操作。

### 功能特点

- 随机生成临时邮箱
- 自定义邮箱地址
- 接收和查看邮件
- 删除邮箱
- 三语言支持
  - 中文
  - English
  - فارسی
- 管理员面板
- 强制频道订阅系统
- SQLite 数据库支持
- 高速 API 通信
- 用户语言保存
- 附件支持

---

## 安装

### 安装依赖库

```bash
pip install pyTelegramBotAPI requests urllib3
```

### 依赖说明

| 库 | 作用 |
|-----|------|
| pyTelegramBotAPI | Telegram 机器人框架 |
| requests | API 请求 |
| urllib3 | 网络与重试机制 |
| sqlite3 | Python 内置 |
| json | Python 内置 |
| os | Python 内置 |
| re | Python 内置 |
| html | Python 内置 |

---

## 配置

修改源代码中的以下变量：

```python
TOKEN = "YOUR_BOT_TOKEN"
CHANNEL_USERNAME = "YOUR_CHANNEL"
ADMIN_IDS = [YOUR_ADMIN_ID]
API_URL = "YOUR_API_URL"
```

---

## 运行

```bash
python "Temporary Email Bot.py"
```

---

## 项目结构

```text
Temporary Email Bot.py
channels.db
data/
 ├── data.json
 └── lang.json
```

---

## 核心功能

- 临时邮箱生成
- 自定义邮箱创建
- 邮件接收
- 邮件浏览
- 邮箱删除
- 强制订阅验证
- 多语言支持
- 管理员频道管理

---

## 许可证

本项目仅供学习与开发使用。
