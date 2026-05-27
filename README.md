# ⇄ Конвертер единиц США ↔ РФ

Telegram-бот + Mini App для быстрой конвертации единиц измерения.

🔗 **Mini App:** https://k22kot.github.io/unit-converter-bot
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
├── tests.py          # юнит-тесты (без токена)
├── requirements.txt  # python-telegram-bot==21.6
├── Procfile          # Для Railway: worker: python bot.py
├── .env.example      # Шаблон переменных окружения
├── database.sql      # SQL-схема + тестовые данные + 5 запросов
└── index.html        # Telegram Mini App
```

---

## Технологии

| Уровень | Технология |
|---|---|
| Backend | Python 3.11+, python-telegram-bot 21.6 |
| Frontend | HTML5 / CSS3 / Vanilla JS |
| Интеграция | Telegram Bot API, Telegram Web App SDK |
| Распознавание | difflib (fuzzy matching), таблица транслита |
| БД | SQLite |
| Деплой | GitHub Pages (frontend) + Railway (backend) |
