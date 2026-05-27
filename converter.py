"""
converter.py — Конвертация единиц измерения и парсинг сообщений пользователя.
"""

from __future__ import annotations
import re
from typing import Optional

from fuzzy import detect_unit

# ─── Коэффициенты ─────────────────────────────────────────────────────────────

DISTANCE_TO_METERS: dict[str, float] = {
    "km": 1_000, "m": 1, "cm": 0.01,
    "mi": 1_609.344, "yd": 0.9144, "ft": 0.3048, "in": 0.0254,
}

WEIGHT_TO_GRAMS: dict[str, float] = {
    "kg": 1_000, "g": 1, "t": 1_000_000,
    "lb": 453.59237, "oz": 28.3495231, "st": 6_350.293,
}

# Объём: нормируем к миллилитрам
VOLUME_TO_ML: dict[str, float] = {
    "l":    1_000,
    "ml":   1,
    "gal":  3_785.41,   # US gallon
    "pt":   473.176,    # US pint
    "qt":   946.353,    # US quart
    "floz": 29.5735,    # US fl oz
    "cm3":  1,          # 1 cm³ = 1 ml
}

UNIT_NAMES: dict[str, str] = {
    "km": "км",    "m": "м",      "cm": "см",
    "mi": "миль",  "yd": "ярдов", "ft": "футов", "in": "дюймов",
    "kg": "кг",    "g": "г",      "t": "т",
    "lb": "фунтов","oz": "унций", "st": "стоунов",
    "C":  "°C",    "F":  "°F",    "K":  "K",
    "l":  "л",     "ml": "мл",
    "gal":"гал",   "pt": "пинт",  "qt": "кварт", "floz": "fl oz",
    "cm3":"мл",    # cm³ = ml — выводим как мл
}

DISTANCE_PAIRS = [("km","mi"), ("m","ft"), ("cm","in"), ("m","yd")]
WEIGHT_PAIRS   = [("kg","lb"), ("g","oz"), ("t","lb"), ("kg","oz"), ("st","kg")]
VOLUME_PAIRS   = [("l","gal"), ("ml","floz"), ("l","pt"), ("l","qt")]

DISTANCE_UNITS = set(DISTANCE_TO_METERS)
WEIGHT_UNITS   = set(WEIGHT_TO_GRAMS)
VOLUME_UNITS   = set(VOLUME_TO_ML)
TEMP_UNITS     = {"C", "F", "K"}


# ─── Форматирование ───────────────────────────────────────────────────────────

def _fmt(value: float) -> str:
    if abs(value) >= 1_000:
        return f"{value:,.2f}".replace(",", " ")
    if abs(value) >= 1:
        return f"{value:.4f}".rstrip("0").rstrip(".")
    return f"{value:.6f}".rstrip("0").rstrip(".")


def _pair_line(val: float, from_u: str, to_u: str, table: dict) -> str:
    result = val * table[from_u] / table[to_u]
    return (f"*{_fmt(val)} {UNIT_NAMES[from_u]}* = "
            f"*{_fmt(result)} {UNIT_NAMES[to_u]}*")


# ─── Конвертации ──────────────────────────────────────────────────────────────

def convert_distance(value: float, from_unit: str) -> str:
    base = value * DISTANCE_TO_METERS[from_unit]
    main = ""
    for a, b in DISTANCE_PAIRS:
        if from_unit == a:
            main = _pair_line(value, a, b, DISTANCE_TO_METERS); break
        if from_unit == b:
            main = _pair_line(value, b, a, DISTANCE_TO_METERS); break

    extras = []
    if from_unit in ("km", "mi"):
        for u in ("km", "mi", "m"):
            if u != from_unit:
                v = base / DISTANCE_TO_METERS[u]
                extras.append(f"{_fmt(v)} {UNIT_NAMES[u]}")
    elif from_unit in ("m", "ft", "yd"):
        for u in ("m", "ft", "yd"):
            if u != from_unit:
                v = base / DISTANCE_TO_METERS[u]
                extras.append(f"{_fmt(v)} {UNIT_NAMES[u]}")
    elif from_unit in ("cm", "in"):
        for u in ("cm", "in"):
            if u != from_unit:
                v = base / DISTANCE_TO_METERS[u]
                extras.append(f"{_fmt(v)} {UNIT_NAMES[u]}")

    out = main
    if extras:
        out += "\n\nТакже: " + " · ".join(extras)
    return out


def convert_weight(value: float, from_unit: str) -> str:
    base = value * WEIGHT_TO_GRAMS[from_unit]
    main = ""
    for a, b in WEIGHT_PAIRS:
        if from_unit == a:
            main = _pair_line(value, a, b, WEIGHT_TO_GRAMS); break
        if from_unit == b:
            main = _pair_line(value, b, a, WEIGHT_TO_GRAMS); break

    extras = []
    if from_unit in ("kg", "lb", "st"):
        for u in ("kg", "lb", "st"):
            if u != from_unit:
                v = base / WEIGHT_TO_GRAMS[u]
                extras.append(f"{_fmt(v)} {UNIT_NAMES[u]}")
    elif from_unit in ("g", "oz"):
        for u in ("g", "oz"):
            if u != from_unit:
                v = base / WEIGHT_TO_GRAMS[u]
                extras.append(f"{_fmt(v)} {UNIT_NAMES[u]}")

    out = main
    if extras:
        out += "\n\nТакже: " + " · ".join(extras)
    return out


def convert_volume(value: float, from_unit: str) -> str:
    """Конвертирует объём с основной парой и дополнительным контекстом."""
    # cm3 = ml для конвертации
    eff_unit = "ml" if from_unit == "cm3" else from_unit
    base_ml = value * VOLUME_TO_ML[from_unit]

    main = ""
    for a, b in VOLUME_PAIRS:
        if eff_unit == a:
            res = base_ml / VOLUME_TO_ML[b]
            main = (f"*{_fmt(value)} {UNIT_NAMES[from_unit]}* = "
                    f"*{_fmt(res)} {UNIT_NAMES[b]}*")
            break
        if eff_unit == b:
            res = base_ml / VOLUME_TO_ML[a]
            main = (f"*{_fmt(value)} {UNIT_NAMES[from_unit]}* = "
                    f"*{_fmt(res)} {UNIT_NAMES[a]}*")
            break

    # Дополнительный контекст
    extras = []
    if eff_unit in ("l", "gal", "qt", "pt"):
        for u in ("l", "gal", "qt", "pt"):
            u_eff = u
            if u_eff != eff_unit:
                v = base_ml / VOLUME_TO_ML[u_eff]
                extras.append(f"{_fmt(v)} {UNIT_NAMES[u_eff]}")
    elif eff_unit in ("ml", "floz", "cm3"):
        for u in ("ml", "floz"):
            if u != eff_unit and u != from_unit:
                v = base_ml / VOLUME_TO_ML[u]
                extras.append(f"{_fmt(v)} {UNIT_NAMES[u]}")

    out = main or (
        f"*{_fmt(value)} {UNIT_NAMES[from_unit]}* → "
        f"{_fmt(base_ml)} мл"
    )
    if extras:
        out += "\n\nТакже: " + " · ".join(extras)
    return out


def convert_temperature(value: float, from_unit: str) -> str:
    if from_unit == "C":
        f_val = value * 9 / 5 + 32
        k_val = value + 273.15
        return (f"*{_fmt(value)} °C* =\n"
                f"  🇺🇸 *{_fmt(f_val)} °F* (по Фаренгейту)\n"
                f"  🔬 *{_fmt(k_val)} K* (Кельвин)")
    elif from_unit == "F":
        c_val = (value - 32) * 5 / 9
        k_val = c_val + 273.15
        return (f"*{_fmt(value)} °F* =\n"
                f"  🇷🇺 *{_fmt(c_val)} °C* (по Цельсию)\n"
                f"  🔬 *{_fmt(k_val)} K* (Кельвин)")
    else:
        c_val = value - 273.15
        f_val = c_val * 9 / 5 + 32
        return (f"*{_fmt(value)} K* =\n"
                f"  🇷🇺 *{_fmt(c_val)} °C* (по Цельсию)\n"
                f"  🇺🇸 *{_fmt(f_val)} °F* (по Фаренгейту)")


# ─── Парсинг ─────────────────────────────────────────────────────────────────

_PATTERN = re.compile(
    r"(-?\s*\d+(?:[.,]\d+)?)"
    r"\s*"
    r"([^\d\-+=<>]+)",
    re.IGNORECASE,
)

_IS_NUMBER = re.compile(r"^-?\s*\d+(?:[.,]\d+)?\s*$")


def is_bare_number(text: str) -> bool:
    """True если пользователь отправил просто число без единицы."""
    return bool(_IS_NUMBER.match(text.strip()))


def _parse_value_and_unit(text: str) -> Optional[tuple[float, str]]:
    text = text.strip()
    text = re.sub(
        r"\b(переведи|конвертируй|convert|сколько|в|in|to|это|equals?)\b",
        " ", text, flags=re.IGNORECASE,
    )
    text = re.sub(r"\s{2,}", " ", text).strip()

    matches = _PATTERN.findall(text)
    if not matches:
        return None

    for raw_num, raw_unit in reversed(matches):
        raw_num = raw_num.replace(" ", "").replace(",", ".")
        try:
            value = float(raw_num)
        except ValueError:
            continue
        raw_unit = raw_unit.strip().rstrip(".")
        for token in raw_unit.split():
            code = detect_unit(token)
            if code:
                return value, code
    return None


def convert_message(text: str, category_hint: Optional[str] = None) -> Optional[str]:
    parsed = _parse_value_and_unit(text)
    if not parsed:
        return None
    value, unit = parsed
    if unit in DISTANCE_UNITS:
        return convert_distance(value, unit)
    elif unit in WEIGHT_UNITS:
        return convert_weight(value, unit)
    elif unit in VOLUME_UNITS:
        return convert_volume(value, unit)
    elif unit in TEMP_UNITS:
        return convert_temperature(value, unit)
    return None
