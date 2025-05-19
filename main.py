import pandas as pd
import ta
import time
from datetime import datetime

def load_price_data():
    # Load price data from a local CSV file or an API later
    try:
        df = pd.read_csv("EURUSD_M5.csv")  # 5-minute candlesticks
        df = df[['close']]  # Make sure 'close' column exists
        return df
    except Exception as e:
        print("Error loading data:", e)
        return None

def generate_signal(df):
    # Calculate indicators
    df['ema8'] = ta.trend.ema_indicator(df['close'], window=8)
    df['ema21'] = ta.trend.ema_indicator(df['close'], window=21)
    df['rsi'] = ta.momentum.rsi(df['close'], window=14)
    df['macd'] = ta.trend.macd_diff(df['close'])

    latest = df.iloc[-1]
    signal = "NO SIGNAL"

    if latest['ema8'] > latest['ema21'] and latest['rsi'] < 30 and latest['macd'] > 0:
        signal = "BUY"
    elif latest['ema8'] < latest['ema21'] and latest['rsi'] > 70 and latest['macd'] < 0:
        signal = "SELL"

    return signal

def main():
    while True:
        df = load_price_data()
        if df is not None:
            signal = generate_signal(df)
            print(f"[{datetime.now()}] Signal: {signal}")

            # Save signal to file
            with open("signal.txt", "w") as f:
                f.write(f"{signal} @ {datetime.now()}")
        
        time.sleep(60)  # Wait 1 minute before next analysis

if __name__ == "__main__":
    main()