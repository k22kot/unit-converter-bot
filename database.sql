-- ============================================================
-- База данных: unit_converter_bot
-- СУБД: SQLite (совместим с PostgreSQL / MySQL с минимальными правками)
-- Проект: Telegram Mini App «Конвертер единиц США ↔ РФ»
-- ============================================================

PRAGMA foreign_keys = ON;

-- ────────────────────────────────────────────────────────────
-- 1. ПОЛЬЗОВАТЕЛИ
-- ────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    user_id       INTEGER PRIMARY KEY,
    username      TEXT,
    first_name    TEXT    NOT NULL,
    last_name     TEXT,
    language_code TEXT    DEFAULT 'ru',
    created_at    TEXT    NOT NULL DEFAULT (datetime('now')),
    last_seen_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);

-- ────────────────────────────────────────────────────────────
-- 2. КАТЕГОРИИ ЕДИНИЦ
-- ────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS categories (
    category_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    code          TEXT    NOT NULL UNIQUE,
    name_ru       TEXT    NOT NULL,
    name_en       TEXT    NOT NULL,
    icon          TEXT
);

INSERT OR IGNORE INTO categories (code, name_ru, name_en, icon) VALUES
    ('distance',    'Расстояние',  'Distance',    '📏'),
    ('weight',      'Вес',         'Weight',      '⚖️'),
    ('temperature', 'Температура', 'Temperature', '🌡'),
    ('volume',      'Объём',       'Volume',      '🧴');

-- ────────────────────────────────────────────────────────────
-- 3. ЕДИНИЦЫ ИЗМЕРЕНИЯ
-- ────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS units (
    unit_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id      INTEGER NOT NULL REFERENCES categories(category_id) ON DELETE CASCADE,
    code             TEXT    NOT NULL UNIQUE,
    symbol           TEXT    NOT NULL,
    name_ru          TEXT    NOT NULL,
    name_en          TEXT    NOT NULL,
    to_base_factor   REAL    NOT NULL DEFAULT 1.0,
    base_unit_code   TEXT
);

INSERT OR IGNORE INTO units (category_id, code, symbol, name_ru, name_en, to_base_factor, base_unit_code) VALUES
    -- Расстояние (база = метр)
    (1, 'km',  'км',    'Километр',   'Kilometer',  1000.0,   'm'),
    (1, 'm',   'м',     'Метр',       'Meter',      1.0,      NULL),
    (1, 'cm',  'см',    'Сантиметр',  'Centimeter', 0.01,     'm'),
    (1, 'mi',  'миля',  'Миля',       'Mile',       1609.344, 'm'),
    (1, 'yd',  'ярд',   'Ярд',        'Yard',       0.9144,   'm'),
    (1, 'ft',  'фут',   'Фут',        'Foot',       0.3048,   'm'),
    (1, 'in',  'дюйм',  'Дюйм',       'Inch',       0.0254,   'm'),
    -- Вес (база = грамм)
    (2, 'kg',  'кг',    'Килограмм',  'Kilogram',   1000.0,   'g'),
    (2, 'g',   'г',     'Грамм',      'Gram',       1.0,      NULL),
    (2, 't',   'т',     'Тонна',      'Tonne',      1000000.0,'g'),
    (2, 'lb',  'фунт',  'Фунт',       'Pound',      453.592,  'g'),
    (2, 'oz',  'унц.',  'Унция',      'Ounce',      28.3495,  'g'),
    (2, 'st',  'ст.',   'Стоун',      'Stone',      6350.29,  'g'),
    -- Температура (нелинейная — to_base_factor не используется)
    (3, 'C',   '°C',    'Цельсий',    'Celsius',    0.0,      NULL),
    (3, 'F',   '°F',    'Фаренгейт',  'Fahrenheit', 0.0,      NULL),
    (3, 'K',   'K',     'Кельвин',    'Kelvin',     0.0,      NULL),
    -- Объём (база = мл)
    (4, 'l',   'л',     'Литр',       'Liter',      1000.0,   'ml'),
    (4, 'ml',  'мл',    'Миллилитр',  'Milliliter', 1.0,      NULL),
    (4, 'gal', 'гал.',  'Галлон (US)','Gallon',     3785.41,  'ml'),
    (4, 'pt',  'пинта', 'Пинта (US)', 'Pint',       473.176,  'ml'),
    (4, 'qt',  'кварта','Кварта (US)','Quart',      946.353,  'ml'),
    (4, 'floz','fl oz', 'Жидк. унция','Fl. Ounce',  29.5735,  'ml');

-- ────────────────────────────────────────────────────────────
-- 4. ИСТОРИЯ КОНВЕРТАЦИЙ
-- ────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS conversion_history (
    history_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id       INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    category_id   INTEGER NOT NULL REFERENCES categories(category_id),
    from_unit     TEXT    NOT NULL,
    to_unit       TEXT    NOT NULL,
    input_value   REAL    NOT NULL,
    result_value  REAL    NOT NULL,
    source        TEXT    NOT NULL DEFAULT 'miniapp',  -- 'miniapp' | 'bot'
    created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_history_user
    ON conversion_history(user_id, created_at DESC);

-- ────────────────────────────────────────────────────────────
-- ТЕСТОВЫЕ ДАННЫЕ
-- ────────────────────────────────────────────────────────────
INSERT INTO users (user_id, username, first_name, last_name, language_code) VALUES
    (100001, 'ivan_petrov',  'Иван',   'Петров',  'ru'),
    (100002, 'jane_smith',   'Jane',   'Smith',   'en'),
    (100003, 'aibek_k',      'Айбек',  'Кенесов', 'ru'),
    (100004, 'maria_test',   'Мария',  NULL,      'ru');

INSERT INTO conversion_history (user_id, category_id, from_unit, to_unit, input_value, result_value, source) VALUES
    (100001, 1, 'km',  'mi',  10.0,  6.2137,  'miniapp'),
    (100001, 2, 'kg',  'lb',  70.0,  154.32,  'bot'),
    (100002, 3, 'F',   'C',   98.6,  37.0,    'miniapp'),
    (100002, 4, 'l',   'gal', 2.0,   0.5283,  'miniapp'),
    (100003, 1, 'mi',  'km',  5.0,   8.0467,  'bot'),
    (100003, 2, 'lb',  'kg',  150.0, 68.039,  'bot'),
    (100004, 3, 'C',   'F',   36.6,  97.88,   'miniapp'),
    (100004, 4, 'ml',  'floz',500.0, 16.907,  'miniapp');

-- ────────────────────────────────────────────────────────────
-- SQL-ЗАПРОСЫ ДЛЯ ОТЧЁТА (5 штук)
-- ────────────────────────────────────────────────────────────

-- Запрос 1: SELECT с условием (WHERE)
-- Пользователи с конвертациями через Mini App
SELECT
    u.user_id,
    u.username,
    u.first_name || ' ' || COALESCE(u.last_name, '') AS full_name,
    COUNT(h.history_id)   AS total_conversions,
    MAX(h.created_at)     AS last_conversion
FROM users u
JOIN conversion_history h ON h.user_id = u.user_id
WHERE h.source = 'miniapp'
GROUP BY u.user_id
HAVING COUNT(h.history_id) >= 1
ORDER BY total_conversions DESC;

-- Запрос 2: INSERT — новый пользователь
INSERT INTO users (user_id, username, first_name, last_name, language_code)
VALUES (200001, 'new_user_alex', 'Алексей', 'Соколов', 'ru');

-- Запрос 3: UPDATE — обновить время последнего визита
UPDATE users
SET last_seen_at = datetime('now')
WHERE user_id = 100001;

-- Запрос 4: DELETE — удалить историю конкретного пользователя
DELETE FROM conversion_history
WHERE user_id = 200001;

-- Запрос 5: SELECT с JOIN — история с названиями категорий
SELECT
    h.history_id,
    u.first_name || ' ' || COALESCE(u.last_name, '') AS user_name,
    c.icon || ' ' || c.name_ru  AS category,
    h.from_unit,
    h.input_value,
    h.to_unit,
    ROUND(h.result_value, 4)    AS result,
    h.source,
    h.created_at
FROM conversion_history h
JOIN users      u ON u.user_id     = h.user_id
JOIN categories c ON c.category_id = h.category_id
ORDER BY h.created_at DESC
LIMIT 10;
