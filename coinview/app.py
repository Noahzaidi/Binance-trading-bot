# import asyncio
from flask import Flask, render_template, request, flash, redirect, jsonify
import config, csv, datetime
from binance.client import Client
from binance.enums import *
import time 


app = Flask(__name__)
app.secret_key = None
app.debug = True  # Force debug mode                                                                                                                                                                                            


client =Client(config.API_KEY,config.API_SECRET )

# Fetch system status to check for a connection
system_status = client.get_system_status()
print(system_status)

# Adjust time offset
client.get_server_time()
time_res = client.get_server_time()
server_time = time_res['serverTime']
time_offset = server_time - int(time.time() * 1000)

# Now, set this offset
client.time_offset = time_offset


@app.route('/')
def index():
    title = 'CoinView'

    account = client.get_account()
    # Extract balances from the account
    all_balances = account['balances']

    # Filter balances where 'free' amount is greater than 0
    non_zero_balances = [balance for balance in all_balances if float(balance['free']) > 0]

    exchange_info = client.get_exchange_info()
    symbols = exchange_info['symbols']

    # Pass non-zero balances to your template
    return render_template('index.html', title=title, my_balances=non_zero_balances, symbols=symbols)




# @app.route('/buy', methods=['POST'])
# def buy():
#     print(request.form)
#     try:
#         order = client.create_order(symbol=request.form['symbol'], 
#             side=SIDE_BUY,
#             type=ORDER_TYPE_MARKET,
#             quantity=request.form['quantity'])
#     except Exception as e:
#         flash(e.message, "error")

#     return redirect('/')


@app.route('/sell')
def sell():
    return 'sell'


@app.route('/settings')
def settings():
    return 'settings'

from datetime import datetime

@app.route('/history')
def history():
    # Format today's date as '1 Jan, 2024' for Binance API call
    end_date = datetime.now().strftime("%d %b, %Y")

    candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_15MINUTE, "1 Jul, 2023", end_date)

    processed_candlesticks = []

    for data in candlesticks:
        candlestick = {
            "time": data[0] / 1000,
            "open": data[1],
            "high": data[2],
            "low": data[3],
            "close": data[4]
        }

        processed_candlesticks.append(candlestick)

    return jsonify(processed_candlesticks)


if __name__ == '__main__':
    app.run()

