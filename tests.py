"""
tests.py — Юнит-тесты
Запуск: python tests.py
"""

import sys
from fuzzy import detect_unit
from converter import convert_message, _parse_value_and_unit, is_bare_number

PASS = 0
FAIL = 0

def check(label, got, expected):
    global PASS, FAIL
    ok = got == expected
    print(f"  {'✅' if ok else '❌'}  {label}")
    if not ok:
        print(f"       got:      {got!r}")
        print(f"       expected: {expected!r}")
        FAIL += 1
    else:
        PASS += 1

# ── detect_unit ───────────────────────────────────────────────────────────────
print("\n── detect_unit ──────────────────────────────────────────────────")

# Расстояние
check("km",          detect_unit("km"),          "km")
check("км",          detect_unit("км"),          "km")
check("ft",          detect_unit("ft"),          "ft")
check("фут",         detect_unit("фут"),         "ft")
check("инч",         detect_unit("инч"),         "in")   # транслит ← новое
check("инчи",        detect_unit("инчи"),        "in")   # транслит ← новое
check("дюйм",        detect_unit("дюйм"),        "in")

# Вес
check("lb",          detect_unit("lb"),          "lb")
check("lbs",         detect_unit("lbs"),         "lb")
check("фунтов",      detect_unit("фунтов"),      "lb")
check("кило",        detect_unit("кило"),        "kg")
check("унций",       detect_unit("унций"),       "oz")

# Температура — опечатки
check("форингейт",   detect_unit("форингейт"),   "F")
check("фаренгит",    detect_unit("фаренгит"),    "F")
check("фарингейт",   detect_unit("фарингейт"),   "F")
check("фаренгет",    detect_unit("фаренгет"),    "F")
check("форенгейт",   detect_unit("форенгейт"),   "F")
check("цельсий",     detect_unit("цельсий"),     "C")
check("целсий",      detect_unit("целсий"),      "C")
check("кельвин",     detect_unit("кельвин"),     "K")
check("°F",          detect_unit("°F"),          "F")
check("°C",          detect_unit("°C"),          "C")

# Объём ← новое
check("л",           detect_unit("л"),           "l")
check("литр",        detect_unit("литр"),        "l")
check("литров",      detect_unit("литров"),      "l")
check("liter",       detect_unit("liter"),       "l")
check("мл",          detect_unit("мл"),          "ml")
check("галлон",      detect_unit("галлон"),      "gal")
check("галон",       detect_unit("галон"),       "gal")   # опечатка
check("gallon",      detect_unit("gallon"),      "gal")
check("пинта",       detect_unit("пинта"),       "pt")
check("pint",        detect_unit("pint"),        "pt")
check("fl oz",       detect_unit("fl oz"),       "floz")
check("кварта",      detect_unit("кварта"),      "qt")
check("quart",       detect_unit("quart"),       "qt")

# Транслит ← новое
check("fut (транслит)",      detect_unit("fut"),      "ft")
check("metr (транслит)",     detect_unit("metr"),     "m")
check("funt (транслит)",     detect_unit("funt"),     "lb")
check("litr (транслит)",     detect_unit("litr"),     "l")
check("galon (транслит)",    detect_unit("galon"),    "gal")

# None
check("xyz → None",  detect_unit("xyz"),  None)
check("'' → None",   detect_unit(""),     None)

# ── is_bare_number ────────────────────────────────────────────────────────────
print("\n── is_bare_number ───────────────────────────────────────────────")
check("'42'",       is_bare_number("42"),        True)
check("'3.14'",     is_bare_number("3.14"),      True)
check("'-40'",      is_bare_number("-40"),       True)
check("'100 км'",   is_bare_number("100 км"),    False)
check("'привет'",   is_bare_number("привет"),    False)

# ── _parse_value_and_unit ────────────────────────────────────────────────────
print("\n── _parse_value_and_unit ────────────────────────────────────────")
check("'100 км'",        _parse_value_and_unit("100 км"),         (100.0, "km"))
check("'5.5 miles'",     _parse_value_and_unit("5.5 miles"),      (5.5,   "mi"))
check("'-40 F'",         _parse_value_and_unit("-40 F"),          (-40.0, "F"))
check("'36,6 цельсий'",  _parse_value_and_unit("36,6 цельсий"),  (36.6,  "C"))
check("'70 кило'",       _parse_value_and_unit("70 кило"),       (70.0,  "kg"))
check("'212 форингейт'", _parse_value_and_unit("212 форингейт"), (212.0, "F"))
check("'2 литра'",       _parse_value_and_unit("2 литра"),       (2.0,   "l"))
check("'1 gallon'",      _parse_value_and_unit("1 gallon"),      (1.0,  "gal"))
check("'500 мл'",        _parse_value_and_unit("500 мл"),        (500.0, "ml"))
check("'10 инч'",        _parse_value_and_unit("10 инч"),        (10.0,  "in"))

# ── convert_message ───────────────────────────────────────────────────────────
print("\n── convert_message ──────────────────────────────────────────────")

def has(text): return convert_message(text) is not None

check("100 км",        has("100 км"),          True)
check("32 форингейт",  has("32 форингейт"),    True)
check("150 lbs",       has("150 lbs"),         True)
check("6 feet",        has("6 feet"),          True)
check("10 инч",        has("10 инч"),          True)   # транслит дюймов
check("2 литра",       has("2 литра"),         True)   # объём
check("1 gallon",      has("1 gallon"),        True)
check("500 мл",        has("500 мл"),          True)
check("16 fl oz",      has("16 fl oz"),        True)
check("1 пинта",       has("1 пинта"),         True)
check("мусор → None",  convert_message("привет как дела"), None)

# Числовая точность
r0c = convert_message("0 C")
check("0°C → 32",  r0c is not None and "32" in r0c, True)
rm40 = convert_message("-40 F")
check("-40°F → -40", rm40 is not None and "-40" in rm40, True)

# Объём: 1 литр ≈ 0.264 галлона
r1l = convert_message("1 литр")
check("1 л содержит 'гал'", r1l is not None and "гал" in r1l, True)

# ── Итог ─────────────────────────────────────────────────────────────────────
print(f"\n{'─'*55}")
print(f"  Итог: {PASS} прошло, {FAIL} упало")
if FAIL:
    print("  Есть ошибки — проверь вывод выше.")
    sys.exit(1)
else:
    print("  Все тесты прошли 🎉")
