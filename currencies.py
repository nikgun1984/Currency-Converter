from forex_python.converter import CurrencyRates, CurrencyCodes
from numbers import Number
from flask import flash, session

def check_value(val):
    """Checking for value validity"""
    if not val:
        raise ValueError("Amount cannot be empty...")
    if not val.isnumeric():
        raise ValueError("Value must be a valid number...")
    if float(val) < 0:
        raise ValueError("Value must be greater than zero...")
    return val

def check_currency(curr):
    """Checking for currency validity"""
    currencies = {i for i in CurrencyRates().get_rates('USD').keys()}
    if not curr:
        raise ValueError("Currency cannot be empty...")
    if curr not in currencies:
        raise ValueError("Not valid code "+curr)
    return curr

def calculate_total(val, curr_1, curr_2):
    """convert and calculate totals of currency conversion"""
    conversion = CurrencyRates().get_rate(curr_1, curr_2)
    total = conversion*float(val)
    return f"The result is {CurrencyCodes().get_symbol(curr_2)} {total}"

def handle_errors(val,checker,key):
    try:
        checked = checker(val)
        return checked
    except ValueError as err:
        session[key]["valid"] = "border border-danger"
        flash(str(err),"error")
        return None

def set_cookies():
    defaults = {
        "val": " ",
        "valid": ""
    }
    session.setdefault("curr_1",defaults)
    session.setdefault("curr_2",defaults)
    session.setdefault("amount",defaults)

def get_cookies(from_curr,to_curr,amount):
    session["curr_1"]["val"] = from_curr
    session["curr_2"]["val"] = to_curr
    session["amount"]["val"] = amount

def clear_styles():
    session["curr_1"]["valid"] = ""
    session["curr_2"]["valid"] = ""
    session["amount"]["valid"] = ""

def handle_all(from_curr,to_curr,amount):
    amount = handle_errors(amount,check_value,"amount")
    from_currency = handle_errors(from_curr,check_currency,"curr_1")
    to_currency = handle_errors(to_curr,check_currency,"curr_2")
    return from_currency, to_currency, amount










