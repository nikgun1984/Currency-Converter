from flask import Flask, render_template, redirect, flash, request, url_for, session
from flask_debugtoolbar import DebugToolbarExtension
from forex_python.converter import CurrencyCodes
from currencies import handle_all, set_cookies, get_cookies, calculate_total, clear_styles
app = Flask(__name__)

app.config["SECRET_KEY"] = "pass1237654"
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["TESTING"] = True
app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]

# debug  = DebugToolbarExtension(app)

@app.route("/")
def get_form():
    set_cookies()
    return render_template("index.html")

@app.route("/res")
def get_result():
    clear_styles()
    amount = request.args["amount"]
    from_curr = request.args["from"]
    to_curr = request.args["to"]
    get_cookies(from_curr,to_curr,amount)
    from_currency,to_currency,amount = handle_all(from_curr,to_curr,amount)

    if amount and from_currency and to_currency:
        total = calculate_total(amount, from_currency,to_currency)
        session.clear()
        return render_template("result.html",total=total)
    else:
        return redirect("/")



