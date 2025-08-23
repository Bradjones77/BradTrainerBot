import pandas as pd
import ta

def compute_indicators(df):
    df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
    macd = ta.trend.MACD(df['close'])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    df['ema10'] = ta.trend.EMAIndicator(df['close'], window=10).ema_indicator()
    df['ema50'] = ta.trend.EMAIndicator(df['close'], window=50).ema_indicator()
    return df

def generate_signal(df, cmc_data):
    last = df.iloc[-1]
    signal = 'HOLD'
    prob = 50
    stop_loss = last['close'] * 0.95

    if last['rsi'] < 30 and last['close'] > last['ema10'] and cmc_data['price'] >= last['close']:
        signal = 'BUY'
        prob = 70 + int((30 - last['rsi'])/2)
        stop_loss = last['close'] * 0.95
    elif last['rsi'] > 70 or last['macd'] < last['macd_signal'] or cmc_data['price'] < last['close']:
        signal = 'SELL'
        prob = 65 + int((last['rsi'] - 70)/2)
        stop_loss = last['close'] * 1.05

    return {
        'signal': signal,
        'probability': prob,
        'stop_loss': stop_loss,
        'current_price': last['close']
    }