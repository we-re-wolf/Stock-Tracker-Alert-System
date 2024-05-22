import yfinance as yf 
import smtplib  
from datetime import datetime  
from email.mime.text import MIMEText 
import time


EMAIL_ADDRESS = ""
EMAIL_PASSWORD = ""


def get_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        current_price = stock.info["currentPrice"]
        return current_price
    except (yf.DownloadError, KeyError):
        print(f"Error fetching data for {symbol}. Skipping...")
        return None 


def send_email_alert(stock_name, symbol, target_price, current_price, alert_time):
    message = MIMEText(f"""
    <html>
      <body>
        <h1>{stock_name} Alert: Price Hit!</h1>
        <p>Target price: ${target_price}</p>
        <p>Current price: ${current_price} (as of {alert_time})</p>
      </body>
    </html>
    """, "html")

    message["Subject"] = f"{stock_name} alert price hit"
    message["From"] = EMAIL_ADDRESS
    message["To"] = EMAIL_ADDRESS

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message.as_string())
        print(f"Email alert sent for {symbol} at {alert_time}")


if __name__ == "__main__":

    stock_symbols = []
    target_prices = {}

    while True:
        symbol = input("Enter stock symbol (or 'q' to quit): ")
        if symbol.lower() == "q":
            break

        target_price = float(input(f"Enter target price for {symbol}: "))
        stock_symbols.append(symbol.upper())
        target_prices[symbol.upper()] = target_price


    while True:
        for symbol in stock_symbols:
            current_price = get_stock_data(symbol)
            if current_price is not None and current_price >= target_prices[symbol]:
                alert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                send_email_alert(symbol, symbol, target_prices[symbol], current_price, alert_time)
                target_prices.pop(symbol)


        time.sleep(60)


