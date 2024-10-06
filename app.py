from flask import Flask, render_template_string
import yfinance as yf

app = Flask(__name__)

# Hardcoded watchlist of stock tickers
watchlist = ['AAPL', 'CRM', 'MSFT', 'TSLA', 'SPYG', 'SCHD', 'NVDA', 'META', 'BND', 'MA', 'VOO', 'VIG', 'VIGI','SPGI', 'BTC', 'ETH', 'QQQ', 'O', 'KO']

# Create a dictionary to store the stock data
stock_data = {}

# Loop through each stock in the watchlist
for stock in watchlist:
    try:
        print(f"Processing {stock}...")  # Log the ticker being processed
        # Get the stock data from Yahoo Finance
        ticker = yf.Ticker(stock)
        data = ticker.history(period='1y')

        # Check if the stock data is available
        if data.empty:
            print(f"Error: No data available for {stock}.")
            continue

        # Calculate the 52-week high and low
        high_52_week = data['High'].max()
        low_52_week = data['Low'].min()

        # Calculate the current price
        current_price = data['Close'][-1]

        # Determine the buy, hold, or sell signal
        if current_price <= low_52_week * 1.1:
            signal = 'Buy'
        elif current_price >= high_52_week * 0.9:
            signal = 'Sell'
        else:
            signal = 'Hold'

        # Store the stock data in the dictionary
        stock_data[stock] = {
            '52-week high': high_52_week,
            '52-week low': low_52_week,
            'current price': current_price,
            'signal': signal
        }
    except Exception as e:
        print(f"Error processing {stock}: {e}")

# Define the HTML template
template = """
<!DOCTYPE html>
<html>
<head>
    <title>Stock Watchlist</title>
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        table {
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 10px;
        }
        .buy {
            color: green;
        }
        .sell {
            color: red;
        }
        .hold {
            color: yellow;
        }
    </style>
</head>
<body>
    <h1>Stock Watchlist</h1>
    <table>
        <tr>
            <th>Stock</th>
            <th>52-week High</th>
            <th>52-week Low</th>
            <th>Current Price</th>
            <th>Signal</th>
        </tr>
        {% for stock, data in stock_data.items() %}
        <tr>
            <td>{{ stock }}</td>
            <td>{{ data['52-week high'] }}</td>
            <td>{{ data['52-week low'] }}</td>
            <td>{{ data['current price'] }}</td>
            <td class="{{ data['signal'].lower() }}">{{ data['signal'] }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

# Define the route for the homepage
@app.route("/")
def index():
    return render_template_string(template, stock_data=stock_data)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)