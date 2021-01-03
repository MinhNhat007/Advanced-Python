from datetime import date, timedelta

import pandas as pd
from flask import Flask, render_template, request, redirect, url_for

import gatherer
import logica

app = Flask(__name__)

symbol = ""
start = ""
end = ""
data = pd.DataFrame()
comp_name = ""
today = date.today()
one_month_ago = today - timedelta(1 * 30)


@app.route('/')
def index():
    global today
    global one_month_ago

    return render_template('main.html', today=today, one_month_ago=one_month_ago)


@app.route('/data', methods=["POST", 'GET'])
def data():
    global symbol
    global start
    global end
    global data
    global comp_name
    global today
    global one_month_ago

    if request.method == 'POST':
        symbol = request.form['search']
        source = request.form['sourcery']
        start = request.form['trip-start']
        end = request.form['trip-end']

        data = gatherer.data(symbol, source, start, end)
        comp_name = gatherer.get_symbol(symbol)
        return redirect(url_for("chart1"))


@app.route('/chart1')
def chart1():
    global start
    global end
    global data
    global comp_name
    global today
    global one_month_ago

    dt, dd, rets = logica.data_retrieve(data)
    print(type(dd))
    return render_template('chart1.html', stock_date=dt, stock_data=dd, company=comp_name, start=start,
                           end=end, today=today, one_month_ago=one_month_ago)


@app.route('/chart2')
def chart2():
    global start
    global end
    global data
    global comp_name
    global today
    global one_month_ago

    dt, dd, rets = logica.data_retrieve(data)
    return render_template('chart2.html', stock_date=dt, rets=rets, company=comp_name, start=start, end=end,
                           today=today, one_month_ago=one_month_ago)


@app.route('/chart3')
def chart3():
    global start
    global end
    global data
    global comp_name
    global today
    global one_month_ago

    predicted_value = logica.data_prediction(data)
    return render_template('chart3.html', predicted_value=predicted_value, company=comp_name, start=start, end=end,
                           today=today, one_month_ago=one_month_ago)


if __name__ == '__main__':
    app.run(debug=1)
