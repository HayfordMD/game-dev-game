"""
Bills and Financial Obligations System
Handles monthly bills, tracks missed payments, and manages game over conditions
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from enum import Enum

class BillType(Enum):
    """Types of bills"""
    OFFICE_RENT = "Office Rent"
    APARTMENT_RENT = "Apartment Rent"
    EMPLOYEE_SALARY = "Employee Salary"
    UTILITIES = "Utilities"
    LOAN_PAYMENT = "Loan Payment"

class BillStatus(Enum):
    """Status of bill payments"""
    PAID = "Paid"
    DUE = "Due"
    OVERDUE = "Overdue"
    MISSED = "Missed"

class BillsSystem:
    """Manages all bills and financial obligations"""

    def __init__(self, game_data, money_system=None):
        self.game_data = game_data
        self.money_system = money_system
        self.initialize_bills_data()

    def initialize_bills_data(self):
        """Initialize bills tracking data"""
        if 'bills' not in self.game_data.data:
            self.game_data.data['bills'] = {
                'monthly_bills': [],
                'payment_history': [],
                'missed_payments': 0,
                'consecutive_missed': 0,
                'last_payment_month': None,
                'warnings_given': [],
                'game_over': False,
                'bankruptcy_date': None
            }

    def calculate_monthly_bills(self) -> List[Dict]:
        """Calculate all bills due for the current month"""
        bills = []

        # Apartment rent (always present)
        apartment_rent = self.game_data.data.get('money', {}).get('monthly_rent', 150)
        bills.append({
            'type': BillType.APARTMENT_RENT.value,
            'amount': apartment_rent,
            'description': 'Monthly apartment rent',
            'mandatory': True
        })

        # Office rent (if player has an office)
        if self.has_office():
            office_rent = self.get_office_rent()
            bills.append({
                'type': BillType.OFFICE_RENT.value,
                'amount': office_rent,
                'description': f'Office space rental',
                'mandatory': True
            })

        # Employee salaries
        employees = self.game_data.data.get('employees', [])
        for employee in employees:
            if employee.get('active', True):
                salary = employee.get('salary', 500)
                bills.append({
                    'type': BillType.EMPLOYEE_SALARY.value,
                    'amount': salary,
                    'description': f"Salary for {employee.get('name', 'Employee')}",
                    'mandatory': True,
                    'employee_id': employee.get('id')
                })

        # Utilities (scales with office size)
        if self.has_office():
            utilities = self.calculate_utilities()
            bills.append({
                'type': BillType.UTILITIES.value,
                'amount': utilities,
                'description': 'Electricity, internet, phone',
                'mandatory': False  # Can be skipped but with consequences
            })

        # Loan payments (if any)
        loans = self.game_data.data.get('loans', [])
        for loan in loans:
            if loan.get('active', False):
                payment = loan.get('monthly_payment', 0)
                bills.append({
                    'type': BillType.LOAN_PAYMENT.value,
                    'amount': payment,
                    'description': f"Loan payment to {loan.get('lender', 'Bank')}",
                    'mandatory': True,
                    'loan_id': loan.get('id')
                })

        return bills

    def get_total_monthly_bills(self) -> int:
        """Get total amount of all monthly bills"""
        bills = self.calculate_monthly_bills()
        return sum(bill['amount'] for bill in bills)

    def get_mandatory_bills_total(self) -> int:
        """Get total of mandatory bills only"""
        bills = self.calculate_monthly_bills()
        return sum(bill['amount'] for bill in bills if bill.get('mandatory', True))

    def process_monthly_bills(self, current_date: str) -> Tuple[bool, List[str]]:
        """
        Process all monthly bills
        Returns: (success, list of messages)
        """
        messages = []
        all_paid = True
        bills = self.calculate_monthly_bills()

        # Parse date
        date = datetime.strptime(current_date, '%Y-%m-%d')
        current_month = date.strftime('%Y-%m')

        # Check if bills already processed this month
        if self.game_data.data['bills']['last_payment_month'] == current_month:
            return True, ["Bills already processed for this month"]

        # Get available funds
        if self.money_system:
            total_funds = self.money_system.get_total_money()
            bank_funds = self.money_system.get_bank_balance()
        else:
            total_funds = self.game_data.data.get('money', {}).get('bank_balance', 0)
            bank_funds = total_funds

        total_bills = sum(bill['amount'] for bill in bills)
        mandatory_total = sum(bill['amount'] for bill in bills if bill.get('mandatory', True))

        # Check if player can afford bills
        if total_funds < mandatory_total:
            # Can't pay mandatory bills - this is serious!
            all_paid = False
            self.game_data.data['bills']['consecutive_missed'] += 1
            self.game_data.data['bills']['missed_payments'] += 1

            messages.append(f"CRITICAL: Unable to pay mandatory bills (${mandatory_total})!")
            messages.append(f"You only have ${total_funds} available.")

            # Record missed bills
            for bill in bills:
                if bill.get('mandatory', True):
                    self.record_payment(current_date, bill, BillStatus.MISSED)

            # Check for game over
            if self.check_game_over():
                messages.append("GAME OVER: Failed to pay bills for 3 consecutive months!")
                messages.append("Your studio has gone bankrupt.")

        elif bank_funds < total_bills:
            # Can pay mandatory but not all bills
            messages.append(f"Warning: Insufficient bank funds for all bills.")

            # Pay mandatory bills first
            for bill in bills:
                if bill.get('mandatory', True):
                    if self.pay_bill(bill, current_date):
                        messages.append(f"Paid: {bill['description']} - ${bill['amount']}")
                    else:
                        all_paid = False
                        messages.append(f"FAILED: {bill['description']} - ${bill['amount']}")
                        self.record_payment(current_date, bill, BillStatus.MISSED)

        else:
            # Can pay all bills
            for bill in bills:
                if self.pay_bill(bill, current_date):
                    messages.append(f"Paid: {bill['description']} - ${bill['amount']}")
                else:
                    all_paid = False
                    messages.append(f"Failed to pay: {bill['description']}")
                    self.record_payment(current_date, bill, BillStatus.OVERDUE)

            if all_paid:
                # Reset missed payment counter
                self.game_data.data['bills']['consecutive_missed'] = 0

        # Update last payment month
        self.game_data.data['bills']['last_payment_month'] = current_month

        # Generate warnings if needed
        warning_messages = self.generate_warnings(total_funds, mandatory_total)
        messages.extend(warning_messages)

        return all_paid, messages

    def pay_bill(self, bill: Dict, current_date: str) -> bool:
        """
        Pay a single bill
        Returns: True if successful
        """
        if not self.money_system:
            return False

        amount = bill['amount']
        description = bill['description']

        # Try to pay from bank first
        success, msg = self.money_system.spend_money(
            amount,
            description,
            from_cash=False
        )

        if success:
            self.record_payment(current_date, bill, BillStatus.PAID)
            return True

        # Try cash if bank failed
        success, msg = self.money_system.spend_money(
            amount,
            description,
            from_cash=True
        )

        if success:
            self.record_payment(current_date, bill, BillStatus.PAID)
            return True

        return False

    def record_payment(self, date: str, bill: Dict, status: BillStatus):
        """Record a bill payment or failure"""
        record = {
            'date': date,
            'type': bill['type'],
            'amount': bill['amount'],
            'status': status.value,
            'description': bill['description']
        }

        if 'payment_history' not in self.game_data.data['bills']:
            self.game_data.data['bills']['payment_history'] = []

        self.game_data.data['bills']['payment_history'].append(record)

        # Keep only last 6 months of history
        self.cleanup_old_history()

    def cleanup_old_history(self):
        """Remove payment history older than 6 months"""
        if 'game_time' not in self.game_data.data:
            return

        current_date = self.game_data.data['game_time'].get('current_date', '1984-01-01')
        current = datetime.strptime(current_date, '%Y-%m-%d')
        cutoff = current - timedelta(days=180)

        self.game_data.data['bills']['payment_history'] = [
            record for record in self.game_data.data['bills']['payment_history']
            if datetime.strptime(record['date'], '%Y-%m-%d') > cutoff
        ]

    def generate_warnings(self, available_funds: int, required_funds: int) -> List[str]:
        """Generate warning messages based on financial situation"""
        messages = []
        consecutive_missed = self.game_data.data['bills']['consecutive_missed']

        if consecutive_missed == 0:
            # Check if next month will be problematic
            if available_funds < required_funds * 2:
                messages.append("WARNING: Low funds - may struggle with next month's bills!")

        elif consecutive_missed == 1:
            messages.append("WARNING: 1 month of missed payments - 2 more leads to BANKRUPTCY!")
            messages.append("Consider: Taking a loan, selling assets, or reducing expenses")

        elif consecutive_missed == 2:
            messages.append("CRITICAL WARNING: 2 months of missed payments!")
            messages.append("NEXT MISSED PAYMENT = GAME OVER!")
            messages.append("URGENT: Get funds immediately or face bankruptcy!")

        # Check specific situations
        if self.has_employees() and available_funds < self.get_total_salaries():
            messages.append("Warning: May not be able to pay employee salaries!")

        return messages

    def check_game_over(self) -> bool:
        """
        Check if game over conditions are met
        Returns: True if game is over
        """
        consecutive_missed = self.game_data.data['bills']['consecutive_missed']

        if consecutive_missed >= 3:
            self.game_data.data['bills']['game_over'] = True
            self.game_data.data['bills']['bankruptcy_date'] = \
                self.game_data.data.get('game_time', {}).get('current_date', '1984-01-01')
            return True

        return False

    def get_financial_status(self) -> Dict:
        """Get comprehensive financial status"""
        if self.money_system:
            total_funds = self.money_system.get_total_money()
            bank_balance = self.money_system.get_bank_balance()
            cash = self.money_system.get_cash()
        else:
            money_data = self.game_data.data.get('money', {})
            bank_balance = money_data.get('bank_balance', 0)
            cash = money_data.get('cash_on_hand', 0)
            total_funds = bank_balance + cash

        monthly_bills = self.get_total_monthly_bills()
        mandatory_bills = self.get_mandatory_bills_total()
        consecutive_missed = self.game_data.data['bills']['consecutive_missed']

        # Calculate runway (months until bankruptcy)
        if mandatory_bills > 0:
            runway = total_funds // mandatory_bills
        else:
            runway = 999

        # Determine status level
        if consecutive_missed >= 2:
            status = "CRITICAL"
            status_color = "red"
        elif consecutive_missed == 1:
            status = "WARNING"
            status_color = "yellow"
        elif runway < 2:
            status = "CAUTION"
            status_color = "orange"
        elif runway < 6:
            status = "STABLE"
            status_color = "white"
        else:
            status = "HEALTHY"
            status_color = "green"

        return {
            'total_funds': total_funds,
            'bank_balance': bank_balance,
            'cash': cash,
            'monthly_bills': monthly_bills,
            'mandatory_bills': mandatory_bills,
            'runway_months': runway,
            'consecutive_missed': consecutive_missed,
            'status': status,
            'status_color': status_color,
            'game_over': self.game_data.data['bills']['game_over'],
            'can_afford_bills': total_funds >= mandatory_bills
        }

    # Helper methods
    def has_office(self) -> bool:
        """Check if player has an office"""
        return self.game_data.data.get('office', {}).get('has_office', False)

    def get_office_rent(self) -> int:
        """Get office rent amount"""
        office = self.game_data.data.get('office', {})
        size = office.get('size', 'small')

        rent_rates = {
            'small': 500,
            'medium': 1200,
            'large': 2500,
            'corporate': 5000
        }

        return rent_rates.get(size, 500)

    def calculate_utilities(self) -> int:
        """Calculate utility costs based on office size"""
        if not self.has_office():
            return 0

        office = self.game_data.data.get('office', {})
        size = office.get('size', 'small')

        utility_rates = {
            'small': 50,
            'medium': 120,
            'large': 250,
            'corporate': 500
        }

        base = utility_rates.get(size, 50)

        # Add for employees
        employee_count = len(self.game_data.data.get('employees', []))
        base += employee_count * 10

        return base

    def has_employees(self) -> bool:
        """Check if player has any employees"""
        employees = self.game_data.data.get('employees', [])
        return any(emp.get('active', True) for emp in employees)

    def get_total_salaries(self) -> int:
        """Get total monthly salary expenses"""
        total = 0
        for emp in self.game_data.data.get('employees', []):
            if emp.get('active', True):
                total += emp.get('salary', 500)
        return total

    def get_payment_history(self, months: int = 3) -> List[Dict]:
        """Get payment history for last N months"""
        history = self.game_data.data['bills'].get('payment_history', [])

        if not history:
            return []

        # Get current date
        if 'game_time' in self.game_data.data:
            current_date = self.game_data.data['game_time'].get('current_date', '1984-01-01')
        else:
            current_date = '1984-01-01'

        current = datetime.strptime(current_date, '%Y-%m-%d')
        cutoff = current - timedelta(days=months * 30)

        return [
            record for record in history
            if datetime.strptime(record['date'], '%Y-%m-%d') > cutoff
        ]

    def can_take_loan(self) -> bool:
        """Check if player is eligible for a loan"""
        # Can't take loan if already in critical state
        if self.game_data.data['bills']['consecutive_missed'] >= 2:
            return False

        # Check if already has active loans
        active_loans = sum(1 for loan in self.game_data.data.get('loans', [])
                          if loan.get('active', False))

        # Max 2 active loans
        return active_loans < 2


# Emergency loan system for desperate situations
class EmergencyLoan:
    """Handle emergency loans when facing bankruptcy"""

    @staticmethod
    def offer_emergency_loan(bills_system, money_system) -> Dict:
        """
        Offer emergency loan when player is about to go bankrupt
        Returns loan details
        """
        status = bills_system.get_financial_status()

        if status['consecutive_missed'] < 2:
            return None

        # Calculate loan amount (3 months of bills + buffer)
        monthly_bills = status['mandatory_bills']
        loan_amount = monthly_bills * 3 + 500

        # High interest due to desperation
        interest_rate = 0.25  # 25% interest
        total_repayment = int(loan_amount * (1 + interest_rate))
        monthly_payment = total_repayment // 12  # 12 month term

        return {
            'type': 'emergency',
            'amount': loan_amount,
            'interest_rate': interest_rate,
            'total_repayment': total_repayment,
            'monthly_payment': monthly_payment,
            'term_months': 12,
            'lender': 'Loan Shark Larry',
            'description': 'High-interest emergency loan to avoid bankruptcy'
        }