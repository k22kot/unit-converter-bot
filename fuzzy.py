"""
fuzzy.py — Нечёткое распознавание единиц измерения.
"""

from __future__ import annotations
from difflib import get_close_matches
from typing import Optional

_TRANSLIT_TABLE: dict[str, str] = {
    "dyuym": "дюйм", "dyujm": "дюйм", "dyuim": "дюйм", "diuim": "дюйм",
    "dyujmy": "дюймы", "inchi": "дюйм", "inchy": "дюйм",
    "fut": "фут", "futa": "фута", "futov": "футов",
    "metr": "метр", "metry": "метры", "metrov": "метров",
    "kilometr": "километр", "kilometrov": "километров",
    "milya": "миля", "milj": "миля", "milei": "миль",
    "kilogram": "кг", "kilogramm": "кг", "gramm": "г",
    "funt": "фунт", "funtov": "фунтов",
    "unciya": "унция", "uncii": "унции",
    "tonna": "тонна", "tonn": "тонн",
    "celciy": "цельсий",
    "farengejt": "фаренгейт", "farengeyt": "фаренгейт",
    "litr": "литр", "litrov": "литров",
    "galon": "галлон", "gallons": "галлон",
    "pinta": "пинта", "pint": "пинта", "pints": "пинта",
    "floz": "fl oz",
    "millilitr": "мл", "mililiter": "мл", "milliliter": "мл",
}

ALIASES: dict[str, str] = {
    # ── РАССТОЯНИЕ
    "км": "km", "километр": "km", "километра": "km", "километров": "km",
    "километры": "km", "kilom": "km", "kilometer": "km", "kilometres": "km",
    "kilometers": "km", "km": "km",
    "м": "m", "метр": "m", "метра": "m", "метров": "m", "метры": "m",
    "meter": "m", "meters": "m", "metre": "m", "metres": "m", "m": "m",
    "см": "cm", "сантиметр": "cm", "сантиметра": "cm", "сантиметров": "cm",
    "сантиметры": "cm", "centimeter": "cm", "centimeters": "cm",
    "centimetre": "cm", "cm": "cm",
    "миля": "mi", "миль": "mi", "мили": "mi", "mile": "mi", "miles": "mi",
    "ми": "mi", "mi": "mi",
    "ярд": "yd", "ярда": "yd", "ярдов": "yd", "ярды": "yd",
    "yard": "yd", "yards": "yd", "yd": "yd",
    "фут": "ft", "фута": "ft", "футов": "ft", "футы": "ft",
    "foot": "ft", "feet": "ft", "ft": "ft", "фт": "ft",
    "дюйм": "in", "дюйма": "in", "дюймов": "in", "дюймы": "in",
    "инч": "in", "инча": "in", "инчей": "in", "инчи": "in",
    "inch": "in", "inches": "in", "in": "in", "\"": "in",
    # ── ВЕС
    "кг": "kg", "кило": "kg", "килограмм": "kg", "килограмма": "kg",
    "килограммов": "kg", "килограммы": "kg",
    "kilogram": "kg", "kilograms": "kg", "kilo": "kg", "kg": "kg",
    "г": "g", "гр": "g", "грамм": "g", "грамма": "g", "граммов": "g",
    "граммы": "g", "gram": "g", "grams": "g", "gramme": "g", "g": "g",
    "тонна": "t", "тонн": "t", "тонны": "t",
    "tonne": "t", "tonnes": "t", "ton": "t", "tons": "t",
    "metric ton": "t", "т": "t",
    "фунт": "lb", "фунта": "lb", "фунтов": "lb", "фунты": "lb",
    "pound": "lb", "pounds": "lb", "lb": "lb", "lbs": "lb",
    "либра": "lb", "либр": "lb",
    "унция": "oz", "унции": "oz", "унций": "oz",
    "ounce": "oz", "ounces": "oz", "oz": "oz",
    "стоун": "st", "стоуна": "st", "стоунов": "st",
    "stone": "st", "stones": "st", "st": "st",
    # ── ТЕМПЕРАТУРА
    "°c": "C", "цельсий": "C", "целси": "C", "цельс": "C",
    "цельсия": "C", "celsius": "C", "cel": "C", "цел": "C",
    "градус": "C", "градусы": "C", "градусов": "C", "целсий": "C",
    "°f": "F", "фаренгейт": "F", "fahrenheit": "F",
    "форингейт": "F", "фаренгит": "F", "фаренгейта": "F",
    "фаренгейтов": "F", "фарингейт": "F", "фаренгет": "F",
    "фарингет": "F", "форенгейт": "F",
    "fahr": "F", "фар": "F", "фарен": "F",
    "fahrengeyt": "F", "farenheit": "F",
    "°k": "K", "кельвин": "K", "кельвина": "K", "кельвинов": "K",
    "kelvin": "K", "kelvins": "K", "кел": "K",
    # ── ОБЪЁМ
    "л": "l", "литр": "l", "литра": "l", "литров": "l", "литры": "l",
    "liter": "l", "liters": "l", "litre": "l", "litres": "l", "l": "l",
    "мл": "ml", "миллилитр": "ml", "миллилитра": "ml", "миллилитров": "ml",
    "milliliter": "ml", "milliliters": "ml", "millilitre": "ml", "ml": "ml",
    "галлон": "gal", "галлона": "gal", "галлонов": "gal", "галлоны": "gal",
    "галон": "gal", "галона": "gal",
    "gallon": "gal", "gallons": "gal", "gal": "gal",
    "пинта": "pt", "пинты": "pt", "пинт": "pt",
    "pint": "pt", "pints": "pt", "pt": "pt",
    "fl oz": "floz", "fl. oz": "floz", "fl.oz": "floz",
    "жидкая унция": "floz", "жидких унций": "floz",
    "fluid ounce": "floz", "fluid ounces": "floz",
    "флоз": "floz",
    "кварта": "qt", "кварты": "qt", "кварт": "qt",
    "quart": "qt", "quarts": "qt", "qt": "qt",
    "куб. см": "cm3", "куб.см": "cm3", "см³": "cm3", "cc": "cm3",
    "кубический сантиметр": "cm3", "cubic centimeter": "cm3", "cm3": "cm3",
}

_SINGLE_CHAR: dict[str, str] = {
    "c": "C", "f": "F", "k": "K",
    "g": "g", "m": "m", "l": "l", "t": "t",
}
ALIASES.update(_SINGLE_CHAR)

_FUZZY_KEYS = [k for k in ALIASES if len(k) > 1]


def detect_unit(raw: str) -> Optional[str]:
    if not raw:
        return None
    s = raw.strip().lower().rstrip(".")
    s = _TRANSLIT_TABLE.get(s, s)
    s = s.strip().lower()
    if s in ALIASES:
        return ALIASES[s]
    if len(s) > 1:
        matches = get_close_matches(s, _FUZZY_KEYS, n=1, cutoff=0.72)
        if matches:
            return ALIASES[matches[0]]
    return None
