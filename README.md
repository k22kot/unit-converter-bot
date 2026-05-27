# ⇄ Конвертер единиц США ↔ РФ

Telegram-бот + Mini App для быстрой конвертации единиц измерения.

🔗 **Mini App:** https://k22kot.github.io/unit-converter-bot/mini_app/  
🤖 **Бот:** @conv_usru_bot

---

## Возможности

| Категория | Единицы |
|---|---|
| 📏 Расстояние | км ↔ мили, м ↔ футы/ярды, см ↔ дюймы |
| ⚖️ Вес | кг ↔ фунты, г ↔ унции, тонны, стоуны |
| 🌡 Температура | °C ↔ °F ↔ K |
| 🧴 Объём | литры ↔ галлоны (US), мл ↔ fl oz, пинты, кварты |

- Понимает **русский и английский** язык  
- Понимает **сокращения**: км, lbs, ft, oz, fl oz…  
- Понимает **опечатки и транслит**: форингейт, инч, кило, funt…  
- При вводе **просто числа** — предлагает кнопки выбора единицы  

---

## Структура проекта

```
unit-converter-bot/
├── bot.py            # Telegram-хэндлеры, Menu Button, /start /app
├── converter.py      # Математика конвертации, парсинг сообщений
├── fuzzy.py          # Словарь синонимов + difflib для опечаток
├── tests.py          # 71 юнит-тест (без токена)
├── requirements.txt  # python-telegram-bot==21.6
├── Procfile          # Для Railway: worker: python bot.py
├── .env.example      # Шаблон переменных окружения
├── database.sql      # SQL-схема + тестовые данные + 5 запросов
└── mini_app/
    └── index.html    # Telegram Mini App (всё в одном файле)
```

---

## Быстрый запуск локально

```bash
# 1. Клонировать
git clone https://github.com/ВАШ_ЛОГИН/unit-converter-bot.git
cd unit-converter-bot

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Запустить тесты (токен не нужен)
python tests.py

# 4. Задать переменные окружения
export TELEGRAM_BOT_TOKEN="токен_от_BotFather"
export MINI_APP_URL="https://ВАШ_ЛОГИН.github.io/unit-converter-bot/mini_app/"

# 5. Запустить бота
python bot.py
```

---

## Деплой

### Mini App → GitHub Pages (бесплатно)

1. Запушить репозиторий на GitHub  
2. Settings → Pages → Branch: `main` → папка: `/ (root)` → Save  
3. Mini App доступен по адресу:  
   `https://ВАШ_ЛОГИН.github.io/unit-converter-bot/mini_app/`

### Бот → Railway (бесплатно)

1. [railway.app](https://railway.app) → New Project → Deploy from GitHub  
2. Выбрать репозиторий `unit-converter-bot`  
3. В разделе Variables добавить:
   ```
   TELEGRAM_BOT_TOKEN = токен_от_BotFather
   MINI_APP_URL = https://ВАШ_ЛОГИН.github.io/unit-converter-bot/mini_app/
   ```
4. Railway автоматически найдёт `Procfile` и запустит бота  
5. При старте бот установит **Menu Button** — кнопка «⇄ Конвертер» появится рядом с полем ввода

---

## Технологии

| Уровень | Технология |
|---|---|
| Backend | Python 3.11+, python-telegram-bot 21.6 |
| Frontend | HTML5 / CSS3 / Vanilla JS (без фреймворков) |
| Интеграция | Telegram Bot API, Telegram Web App SDK |
| Распознавание | difflib (fuzzy matching), таблица транслита |
| БД | SQLite |
| Деплой | GitHub Pages (frontend) + Railway (backend) |
