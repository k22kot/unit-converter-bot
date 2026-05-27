# ⇄ Unit Converter Bot (US ↔ RU)

Telegram-бот и Mini App для конвертации американских и метрических единиц измерения.

## Demo

🔗 Mini App:  

https://k22kot.github.io/unit-converter-bot/

🤖 Telegram Bot:  

https://t.me/conv_usru_bot

---

## Возможности

### 📏 Расстояние

- километры ↔ мили

- метры ↔ футы / ярды

- сантиметры ↔ дюймы

### ⚖️ Вес

- килограммы ↔ фунты

- граммы ↔ унции

- тонны ↔ стоуны

### 🌡 Температура

- °C ↔ °F ↔ K

### 🧴 Объём

- литры ↔ галлоны (US)

- мл ↔ fl oz

- пинты ↔ кварты

---

## Особенности

- Поддерживает русский и английский язык

- Понимает сокращения (`км`, `lbs`, `ft`, `oz`)

- Обрабатывает транслит и опечатки (`funt`, `inch`, `фаренгейт`)

- При вводе только числа предлагает выбор единиц через кнопки

- Работает как Telegram-бот и как Mini App

---

## Примеры запросов

```text

10 km to miles

5 кг в фунты

72 f

100 oz

2 галлона в литры

```

---

## Структура проекта

```text

unit-converter-bot/

├── bot.py            # Telegram bot handlers

├── converter.py      # Логика конвертации и парсинг запросов

├── fuzzy.py          # Обработка опечаток и fuzzy matching

├── tests.py          # Юнит-тесты

├── requirements.txt

├── Procfile          # Railway deploy

├── .env.example

├── database.sql      # SQL-схема и тестовые запросы

└── index.html        # Telegram Mini App

```

---

## Технологии

### Backend

- Python 3.11+

- python-telegram-bot 21.6

### Frontend

- HTML5

- CSS3

- Vanilla JavaScript

### Интеграции

- Telegram Bot API

- Telegram Web Apps SDK

### Дополнительно

- SQLite

- difflib (fuzzy matching)

- GitHub Pages

- Railway

---

## Локальный запуск

```bash

git clone https://github.com/k22kot/unit-converter-bot.git

cd unit-converter-bot

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

```

Создать `.env`:

```env

BOT_TOKEN=your_token

```

Запуск:

```bash

python bot.py

```

---

## Цель проекта

Учебный pet-project для практики и личного пользования
