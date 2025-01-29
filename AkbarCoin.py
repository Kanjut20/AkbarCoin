import hashlib
import time
import json
import random
from datetime import datetime
from colorama import init, Fore, Back, Style
from tabulate import tabulate
import os
import sys
from time import sleep
from tqdm import tqdm
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress
import threading

# Inisialisasi
init()
console = Console()

class Market:
    def __init__(self):
        self.price = 1.0  # Initial price in USDT
        self.volume_24h = 0
        self.high_24h = 1.0
        self.low_24h = 1.0
        self.price_history = []
        self.orders = {'buy': [], 'sell': []}
        self.trades = []
        self.volatility = 0.02  # 2% volatility

    def update_price(self):
        # Simulasi pergerakan harga
        change = random.uniform(-self.volatility, self.volatility)
        self.price *= (1 + change)
        self.price = round(self.price, 6)
        self.high_24h = max(self.high_24h, self.price)
        self.low_24h = min(self.low_24h, self.price)
        self.price_history.append((time.time(), self.price))

        # Hapus data harga lebih dari 24 jam
        current_time = time.time()
        self.price_history = [(t, p) for t, p in self.price_history 
                             if current_time - t <= 86400]

class AkbarCoin:
    def __init__(self):
        self.chain = []
        self.difficulty = 4
        self.pending_transactions = []
        self.wallets = {}
        self.mining_reward = 50
        self.airdrop_amount = 100
        self.market = Market()
        self.total_supply = 1000000  # 1 million AKB
        self.circulating_supply = 0
        self.create_genesis_block()
        
        # Start market simulation thread
        self.market_thread = threading.Thread(target=self.simulate_market, daemon=True)
        self.market_thread.start()

    def create_genesis_block(self):
        genesis_block = {
            'index': 0,
            'timestamp': time.time(),
            'transactions': [],
            'previous_hash': '0',
            'nonce': 0,
            'hash': self.calculate_hash(0, time.time(), [], '0', 0)
        }
        self.chain.append(genesis_block)

    def simulate_market(self):
        while True:
            self.market.update_price()
            sleep(5)  # Update every 5 seconds

    def calculate_hash(self, index, timestamp, transactions, previous_hash, nonce):
        block_string = f"{index}{timestamp}{transactions}{previous_hash}{nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class Wallet:
    def __init__(self, address=None):
        self.address = address or self.generate_address()
        self.balance = 0
        self.usdt_balance = 1000  # Starting with 1000 USDT
        self.transactions = []
        self.mining_rewards = 0
        self.airdrop_rewards = 0
        self.trading_profits = 0

    def generate_address(self):
        random_string = str(random.random())
        return "AKB_" + hashlib.sha256(random_string.encode()).hexdigest()[:8]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = f"""
    ╔══════════════════════════════════════════════════════╗
    ║                   🌟 AKBARCOIN 🌟                    ║
    ║              The Future of Digital Asset             ║
    ║                                                      ║
    ║  Mining • Trading • Airdrop • Blockchain Explorer   ║
    ╚══════════════════════════════════════════════════════╝
    """
    console.print(Panel(banner, style="cyan"))

def show_market_status(akbar):
    market = akbar.market
    
    table = Table(title="Market Status")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Current Price", f"${market.price:.6f}")
    table.add_row("24h High", f"${market.high_24h:.6f}")
    table.add_row("24h Low", f"${market.low_24h:.6f}")
    table.add_row("24h Volume", f"${market.volume_24h:.2f}")
    table.add_row("Market Cap", f"${akbar.circulating_supply * market.price:.2f}")
    table.add_row("Circulating Supply", f"{akbar.circulating_supply:,} AKB")
    table.add_row("Total Supply", f"{akbar.total_supply:,} AKB")
    
    console.print(table)

def trade_menu(akbar, wallet_address):
    while True:
        clear_screen()
        print_banner()
        show_market_status(akbar)
        
        wallet = akbar.wallets[wallet_address]
        
        console.print(Panel.fit(
            f"Your Balance: {wallet.balance:.6f} AKB (${wallet.balance * akbar.market.price:.2f})\n"
            f"USDT Balance: ${wallet.usdt_balance:.2f}",
            title="Wallet Status"
        ))
        
        console.print(Panel.fit("""
            1. Buy AKB
            2. Sell AKB
            3. View Order Book
            4. View Trade History
            5. Cancel Order
            6. Back to Main Menu
        """, title="Trading Menu"))
        
        choice = input("\nEnter your choice: ")
        
        if choice == "1":
            try:
                amount = float(input("Enter USDT amount to spend: "))
                if amount > wallet.usdt_balance:
                    console.print("[red]Insufficient USDT balance!")
                    continue
                
                akb_amount = amount / akbar.market.price
                wallet.usdt_balance -= amount
                wallet.balance += akb_amount
                akbar.market.volume_24h += amount
                
                trade = {
                    'type': 'buy',
                    'price': akbar.market.price,
                    'amount': akb_amount,
                    'total': amount,
                    'timestamp': time.time()
                }
                akbar.market.trades.append(trade)
                
                console.print(f"[green]Successfully bought {akb_amount:.6f} AKB!")
            
            except ValueError:
                console.print("[red]Invalid input!")
        
        elif choice == "2":
            try:
                amount = float(input("Enter AKB amount to sell: "))
                if amount > wallet.balance:
                    console.print("[red]Insufficient AKB balance!")
                    continue
                
                usdt_amount = amount * akbar.market.price
                wallet.balance -= amount
                wallet.usdt_balance += usdt_amount
                akbar.market.volume_24h += usdt_amount
                
                trade = {
                    'type': 'sell',
                    'price': akbar.market.price,
                    'amount': amount,
                    'total': usdt_amount,
                    'timestamp': time.time()
                }
                akbar.market.trades.append(trade)
                
                console.print(f"[green]Successfully sold {amount:.6f} AKB for ${usdt_amount:.2f}!")
            
            except ValueError:
                console.print("[red]Invalid input!")
        
        elif choice == "3":
            show_order_book(akbar)
        
        elif choice == "4":
            show_trade_history(akbar)
        
        elif choice == "5":
            # Implement order cancellation
            pass
        
        elif choice == "6":
            break
        
        input("\nPress Enter to continue...")

def show_order_book(akbar):
    buy_orders = sorted(akbar.market.orders['buy'], 
                       key=lambda x: x['price'], 
                       reverse=True)[:10]
    sell_orders = sorted(akbar.market.orders['sell'], 
                        key=lambda x: x['price'])[:10]
    
    table = Table(title="Order Book")
    table.add_column("Buy Orders", style="green")
    table.add_column("Price", style="cyan")
    table.add_column("Sell Orders", style="red")
    
    for i in range(max(len(buy_orders), len(sell_orders))):
        buy = f"{buy_orders[i]['amount']:.6f} AKB" if i < len(buy_orders) else ""
        price = f"${akbar.market.price:.6f}"
        sell = f"{sell_orders[i]['amount']:.6f} AKB" if i < len(sell_orders) else ""
        table.add_row(buy, price, sell)
    
    console.print(table)

def show_trade_history(akbar):
    table = Table(title="Recent Trades")
    table.add_column("Time", style="cyan")
    table.add_column("Type", style="green")
    table.add_column("Price", style="yellow")
    table.add_column("Amount", style="magenta")
    table.add_column("Total", style="blue")
    
    for trade in reversed(akbar.market.trades[-10:]):
        table.add_row(
            datetime.fromtimestamp(trade['timestamp']).strftime('%H:%M:%S'),
            trade['type'].upper(),
            f"${trade['price']:.6f}",
            f"{trade['amount']:.6f} AKB",
            f"${trade['total']:.2f}"
        )
    
    console.print(table)

def mining_menu(akbar, wallet_address):
    while True:
        clear_screen()
        print_banner()
        
        wallet = akbar.wallets[wallet_address]
        console.print(Panel.fit(
            f"Current Mining Reward: {akbar.mining_reward} AKB\n"
            f"Mining Difficulty: {akbar.difficulty}\n"
            f"Total Mined: {wallet.mining_rewards} AKB",
            title="Mining Status"
        ))
        
        console.print(Panel.fit("""
            1. Start Mining
            2. View Mining History
            3. Back to Main Menu
        """, title="Mining Menu"))
        
        choice = input("\nEnter your choice: ")
        
        if choice == "1":
            with Progress() as progress:
                task = progress.add_task("[cyan]Mining...", total=100)
                
                while not progress.finished:
                    progress.update(task, advance=random.uniform(0.1, 1.0))
                    sleep(0.1)
            
            reward = random.uniform(0.1, akbar.mining_reward)
            wallet.balance += reward
            wallet.mining_rewards += reward
            akbar.circulating_supply += reward
            
            console.print(f"[green]Successfully mined {reward:.6f} AKB!")
        
        elif choice == "2":
            # Implement mining history view
            pass
        
        elif choice == "3":
            break
        
        input("\nPress Enter to continue...")

def main():
    akbar = AkbarCoin()
    
    while True:
        clear_screen()
        print_banner()
        show_market_status(akbar)
        
        console.print(Panel.fit("""
            1. Create New Wallet
            2. Access Wallet
            3. Mining Center
            4. Trading Platform
            5. Claim Airdrop
            6. Blockchain Explorer
            7. Exit
        """, title="Main Menu"))
        
        choice = input("\nEnter your choice: ")
        
        if choice == "1":
            wallet = Wallet()
            akbar.wallets[wallet.address] = wallet
            console.print(f"[green]New wallet created!")
            console.print(f"Address: {wallet.address}")
            console.print(f"Initial USDT balance: ${wallet.usdt_balance}")
        
        elif choice == "2":
            address = input("Enter wallet address: ")
            if address in akbar.wallets:
                wallet = akbar.wallets[address]
                console.print(f"\nBalance: {wallet.balance:.6f} AKB")
                console.print(f"USDT Balance: ${wallet.usdt_balance:.2f}")
            else:
                console.print("[red]Wallet not found!")
        
        elif choice == "3":
            address = input("Enter wallet address: ")
            if address in akbar.wallets:
                mining_menu(akbar, address)
            else:
                console.print("[red]Wallet not found!")
        
        elif choice == "4":
            address = input("Enter wallet address: ")
            if address in akbar.wallets:
                trade_menu(akbar, address)
            else:
                console.print("[red]Wallet not found!")
        
        elif choice == "5":
            address = input("Enter wallet address: ")
            if address in akbar.wallets:
                wallet = akbar.wallets[address]
                wallet.balance += akbar.airdrop_amount
                wallet.airdrop_rewards += akbar.airdrop_amount
                akbar.circulating_supply += akbar.airdrop_amount
                console.print(f"[green]Successfully claimed {akbar.airdrop_amount} AKB!")
            else:
                console.print("[red]Wallet not found!")
        
        elif choice == "6":
            # Implement blockchain explorer
            pass
        
        elif choice == "7":
            console.print("\n[cyan]Thank you for using AkbarCoin![/cyan]")
            break
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[red]Program terminated by user.[/red]")
