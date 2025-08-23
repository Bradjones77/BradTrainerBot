# Crypto Signal Bot (CoinMarketCap Only, Full Coin List)

## Overview
This bot monitors your selected coins using CoinMarketCap only, calculates technical indicators, and sends buy/sell/HOLD signals to your Telegram bot with probability and stop-loss.

## Setup
1. Install Python 3.13.3
2. Install dependencies:
```
pip install -r requirements.txt
```
3. Configure `config.py` with your CoinMarketCap API key and Telegram chat/channel ID.

## Run
```
python main.py
```
The bot runs continuously, updating signals every minute.