import yfinance as yf
import pandas as pd
from telegram import Bot
import logging
import asyncio
from aiogram import Bot as AiogramBot
from dotenv import load_dotenv
load_dotenv()
import os


# Enable logging to help debug issues
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Telegram bot settings
bot_token = os.environ.get('bot_token')
chat_id = int(os.environ.get('chat_id'))
# Telegram bot function
async def send_telegram_message(text):
    try:
        bot = AiogramBot(token=bot_token)
        await bot.send_message(chat_id=chat_id, text=text)
        logging.info("Message sent successfully to Telegram.")
    except Exception as e:
        logging.error(f"Failed to send message: {e}")

# Function to fetch stock data
def get_stock_data(symbol, period='5y', interval='1wk'):
    try:
        data = yf.download(symbol + '.IS', period=period, interval=interval)
        if data.empty:
            logging.warning(f"No data found for {symbol}")
        else:
            logging.info(f"Data fetched successfully for {symbol}")
        return data
    except Exception as e:
        logging.error(f"Error fetching data for {symbol}: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error

# Function to calculate moving averages
def calculate_moving_averages(data, windows=[50, 100, 144]):
    averages = {}
    try:
        for window in windows:
            averages[f"SMA_{window}"] = data['Close'].rolling(window=window).mean()
        logging.info("Moving averages calculated successfully.")
    except Exception as e:
        logging.error(f"Error calculating moving averages: {e}")
    return averages

# Function to check if the close price is close to any moving average
def is_close_to_average(data, averages, tolerance=0.02):  # 2% tolerance
    try:
        close_price = data['Close'].iloc[-1]  # Latest close price
        for key, avg_series in averages.items():
            if not avg_series.empty:
                last_avg_value = avg_series.iloc[-1]
                if (abs(close_price - last_avg_value) / last_avg_value <= tolerance).all():
                    return f"{key}: Close price is near the {key}"
        return None
    except Exception as e:
        logging.error(f"Error checking close price against averages: {e}")
        return None

# Main function to fetch data, calculate averages, and send a message
async def main():
    symbols = [
    "AKBNK", "ARCLK", "ASELS", "BIMAS", "DOHOL", "ECILC", "EGEEN", "ENJSA",
    "EREGL", "FROTO", "GARAN", "GUBRF", "HEKTS", "ISCTR", "KARSN", "KCHOL",
    "KRDMD", "LOGO", "MGROS", "ODAS", "PETKM", "PGSUS", "SAHOL", "SASA",
    "SISE", "SODA", "TAVHL", "TCELL", "THYAO", "TOASO", "TSKB", "TTKOM",
    "TUPRS", "VAKBN", "VESTL", "YKBNK", "ZOREN", "KOZAL", "KOZAA", "HALKB",
    "ISFIN", "CIMSA", "OTKAR", "ALARK", "AYGAZ", "ENKAI", "IPEKE", "KORDS",
    "SOKM", "TTRAK", "VESBE", "ULKER", "GOZDE", "KLKIM", "HUBVC", "AKSEN",
    "ANHYT", "BAGFS", "BERA", "BRSAN", "DOAS", "KATMR", "NTHOL", "OTOKC",
    "OYAKC", "PRKAB", "PSGYO", "SELEC", "SOKM", "TATGD", "TMSN", "TRCAS",
    "ULUUN", "VERUS", "YATAS", "ZRGYO", "AKFGY", "AKSUE", "AKSGY", "AKGUV",
    "ALBRK", "ALMAD", "AVGYO", "BRYAT", "BTTAS", "CLEBI", "COSMO", "CUPON",
    "DAGI", "DARDL", "DERIM", "DYOBY", "DZYAD", "EGCYO", "ESCOM", "FINTR",
    "FRIGO", "GENTS", "GEREL", "GLBMD", "HATEK", "IEYHO", "ISBIR", "KERVN",
    "KRONT", "LKMNH", "MZHLD", "MNDRS", "NETAS", "ORGE", "OSTIM", "QNBFB"
];

    for symbol in symbols:
        data = get_stock_data(symbol)
        if data.empty:
            continue  # Skip if no data

        averages = calculate_moving_averages(data)
        message = is_close_to_average(data, averages)

        if message:
            await send_telegram_message(f"{symbol}: {message}")
        else:
            logging.info(f"{symbol}: No significant movement detected.")

if __name__ == "__main__":
    asyncio.run(main())
