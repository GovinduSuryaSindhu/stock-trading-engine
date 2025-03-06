#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  6 17:02:20 2025

@author: suryasindhugovindu
"""

import heapq
import random
import threading
import time

class StockTradingEngine:
    def __init__(self):
        # Dictionary to store order books for each ticker
        self.order_books = {}
        self.lock = threading.Lock()  # Ensure thread safety

    def add_order(self, order_type, ticker, quantity, price):
        with self.lock:
            if ticker not in self.order_books:
                self.order_books[ticker] = {"buy": [], "sell": []}  

            if order_type == "Buy":
                # Max-Heap for Buy Orders (Highest price prioritized)
                heapq.heappush(self.order_books[ticker]["buy"], (-price, quantity))
            else:
                # Min-Heap for Sell Orders (Lowest price prioritized)
                heapq.heappush(self.order_books[ticker]["sell"], (price, quantity))

            self.match_orders(ticker)

    def match_orders(self, ticker):
        buy_orders = self.order_books[ticker]["buy"]
        sell_orders = self.order_books[ticker]["sell"]

        while buy_orders and sell_orders:
            buy_price, buy_quantity = -buy_orders[0][0], buy_orders[0][1]
            sell_price, sell_quantity = sell_orders[0]

            if buy_price >= sell_price:  # Match found
                trade_quantity = min(buy_quantity, sell_quantity)
                print(f"Trade executed: {trade_quantity} shares of {ticker} at ${sell_price}")

                # Update orders
                if buy_quantity > trade_quantity:
                    buy_orders[0] = (-buy_price, buy_quantity - trade_quantity)
                else:
                    heapq.heappop(buy_orders)

                if sell_quantity > trade_quantity:
                    sell_orders[0] = (sell_price, sell_quantity - trade_quantity)
                else:
                    heapq.heappop(sell_orders)
            else:
                break

# Simulating real-time trading activity
def simulate_trading(engine, tickers):
    while True:
        order_type = random.choice(["Buy", "Sell"])
        ticker = random.choice(tickers)
        quantity = random.randint(1, 100)
        price = round(random.uniform(10, 500), 2)

        engine.add_order(order_type, ticker, quantity, price)
        time.sleep(random.uniform(0.5, 2))  # Random delay to mimic real trading

# Initialize the trading engine
tickers = [f"STOCK{i}" for i in range(1, 1025)]  # 1,024 stocks
trading_engine = StockTradingEngine()

# Start the simulation in a separate thread
thread = threading.Thread(target=simulate_trading, args=(trading_engine, tickers))
thread.daemon = True
thread.start()

# Keep the main thread alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Simulation stopped.")
