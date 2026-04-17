import pandas as pd


def safe_value(value, default=0):
    if value is None or pd.isna(value):
        return default
    return value


def format_brl(value):
    value = safe_value(value, 0)
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def format_m2(value):
    value = safe_value(value, 0)
    return f"{value:,.2f} m²".replace(",", "X").replace(".", ",").replace("X", ".")


def format_int(value):
    value = safe_value(value, 0)
    return f"{int(value):,}".replace(",", ".")


def format_pct(value):
    value = safe_value(value, 0)
    return f"{value * 100:,.2f}%".replace(",", "X").replace(".", ",").replace("X", ".")