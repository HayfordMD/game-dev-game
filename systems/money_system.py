"""
Money System for Game Dev Tycoon
Handles cash, bank balance, transactions, and financial history
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

class MoneySystem:
    """Manages player's money including cash and bank accounts"""

    def __init__(self, game_data):
        self.game_data = game_data
        self.initialize_money_data()

    def initialize_money_data(self):
        """Initialize money data if not present"""
        if 'money' not in self.game_data.data:
            self.game_data.data['money'] = {
                'cash_on_hand': 30,
                'bank_balance': 1500,
                'monthly_rent': 150,
                'transaction_history': [],
                'recurring_expenses': [
                    {'name': 'Apartment Rent', 'amount': 150, 'day_of_month': 1}
                ],
                'last_rent_paid': None
            }
            # GameData doesn't have save_game method, data is saved elsewhere

    def get_cash(self):
        """Get current cash on hand"""
        return self.game_data.data['money']['cash_on_hand']

    def get_bank_balance(self):
        """Get current bank balance"""
        return self.game_data.data['money']['bank_balance']

    def get_total_money(self):
        """Get total money (cash + bank)"""
        return self.get_cash() + self.get_bank_balance()

    def withdraw_cash(self, amount):
        """Withdraw money from bank to cash"""
        if amount <= 0:
            return False, "Invalid amount"

        if amount > self.get_bank_balance():
            return False, "Insufficient funds in bank"

        self.game_data.data['money']['bank_balance'] -= amount
        self.game_data.data['money']['cash_on_hand'] += amount

        # Record transaction
        self.add_transaction('Withdrawal', -amount, 'bank')
        self.add_transaction('Withdrawal', amount, 'cash')

        # Data is saved elsewhere, not here
        return True, f"Withdrew ${amount}"

    def deposit_cash(self, amount):
        """Deposit cash into bank"""
        if amount <= 0:
            return False, "Invalid amount"

        if amount > self.get_cash():
            return False, "Insufficient cash on hand"

        self.game_data.data['money']['cash_on_hand'] -= amount
        self.game_data.data['money']['bank_balance'] += amount

        # Record transaction
        self.add_transaction('Deposit', -amount, 'cash')
        self.add_transaction('Deposit', amount, 'bank')

        # Data is saved elsewhere, not here
        return True, f"Deposited ${amount}"

    def spend_money(self, amount, description, from_cash=True):
        """Spend money (from cash or bank)"""
        if amount <= 0:
            return False, "Invalid amount"

        if from_cash:
            if amount > self.get_cash():
                return False, "Insufficient cash on hand"
            self.game_data.data['money']['cash_on_hand'] -= amount
            self.add_transaction(description, -amount, 'cash')
        else:
            if amount > self.get_bank_balance():
                return False, "Insufficient funds in bank"
            self.game_data.data['money']['bank_balance'] -= amount
            self.add_transaction(description, -amount, 'bank')

        # Data is saved elsewhere, not here
        return True, f"Spent ${amount} on {description}"

    def earn_money(self, amount, description, to_bank=True):
        """Earn money (to bank or cash)"""
        if amount <= 0:
            return False, "Invalid amount"

        if to_bank:
            self.game_data.data['money']['bank_balance'] += amount
            self.add_transaction(description, amount, 'bank')
        else:
            self.game_data.data['money']['cash_on_hand'] += amount
            self.add_transaction(description, amount, 'cash')

        # Data is saved elsewhere, not here
        return True, f"Earned ${amount} from {description}"

    def add_transaction(self, description, amount, account_type):
        """Add a transaction to history"""
        from systems.game_systems import TimeSystem

        # Get current game date
        if 'game_time' in self.game_data.data:
            current_date = self.game_data.data['game_time'].get('current_date', '1984-01-01')
        else:
            current_date = '1984-01-01'

        transaction = {
            'date': current_date,
            'description': description,
            'amount': amount,
            'account': account_type,
            'balance_after': self.get_bank_balance() if account_type == 'bank' else self.get_cash()
        }

        if 'transaction_history' not in self.game_data.data['money']:
            self.game_data.data['money']['transaction_history'] = []

        self.game_data.data['money']['transaction_history'].append(transaction)

        # Keep only last 90 days of transactions
        self.cleanup_old_transactions()

    def cleanup_old_transactions(self):
        """Remove transactions older than 3 months"""
        if 'transaction_history' not in self.game_data.data['money']:
            return

        # Get current game date
        if 'game_time' in self.game_data.data:
            current_date = self.game_data.data['game_time'].get('current_date', '1984-01-01')
        else:
            current_date = '1984-01-01'

        # Convert to datetime
        current = datetime.strptime(current_date, '%Y-%m-%d')
        cutoff = current - timedelta(days=90)

        # Filter transactions
        self.game_data.data['money']['transaction_history'] = [
            t for t in self.game_data.data['money']['transaction_history']
            if datetime.strptime(t['date'], '%Y-%m-%d') > cutoff
        ]

    def get_transaction_history(self, days=90):
        """Get transaction history for last N days"""
        if 'transaction_history' not in self.game_data.data['money']:
            return []

        # Get current game date
        if 'game_time' in self.game_data.data:
            current_date = self.game_data.data['game_time'].get('current_date', '1984-01-01')
        else:
            current_date = '1984-01-01'

        current = datetime.strptime(current_date, '%Y-%m-%d')
        cutoff = current - timedelta(days=days)

        # Filter and return transactions
        return [
            t for t in self.game_data.data['money']['transaction_history']
            if datetime.strptime(t['date'], '%Y-%m-%d') > cutoff
        ]

    def get_monthly_summary(self):
        """Get income and expenses summary for last 3 months"""
        transactions = self.get_transaction_history(90)

        # Group by month
        monthly_data = {}
        for trans in transactions:
            date = datetime.strptime(trans['date'], '%Y-%m-%d')
            month_key = date.strftime('%Y-%m')

            if month_key not in monthly_data:
                monthly_data[month_key] = {
                    'income': 0,
                    'expenses': 0,
                    'transactions': []
                }

            if trans['amount'] > 0:
                monthly_data[month_key]['income'] += trans['amount']
            else:
                monthly_data[month_key]['expenses'] += abs(trans['amount'])

            monthly_data[month_key]['transactions'].append(trans)

        return monthly_data

    def process_monthly_expenses(self, current_date):
        """Process recurring monthly expenses like rent"""
        if 'last_rent_paid' not in self.game_data.data['money']:
            self.game_data.data['money']['last_rent_paid'] = None

        # Parse current date
        date = datetime.strptime(current_date, '%Y-%m-%d')
        current_month = date.strftime('%Y-%m')

        # Check if rent needs to be paid
        last_rent = self.game_data.data['money']['last_rent_paid']
        if last_rent != current_month and date.day >= 1:
            # Pay rent
            rent_amount = self.game_data.data['money']['monthly_rent']

            # Try to pay from bank first
            if self.get_bank_balance() >= rent_amount:
                self.spend_money(rent_amount, 'Apartment Rent', from_cash=False)
                self.game_data.data['money']['last_rent_paid'] = current_month
                return True, f"Rent of ${rent_amount} paid from bank account"
            elif self.get_total_money() >= rent_amount:
                # Try to use cash + bank
                return False, f"Rent due: ${rent_amount}. Please ensure funds are in your bank account"
            else:
                # Can't afford rent
                return False, f"OVERDUE: Rent of ${rent_amount} - Insufficient funds!"

        return None, None

    def can_use_online_banking(self, current_year):
        """Check if online banking is available (after 2004)"""
        return current_year >= 2004