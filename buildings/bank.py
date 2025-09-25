"""
Bank Interface for Game Dev Tycoon
Handles banking transactions, withdrawals, deposits, and transaction history
"""

import tkinter as tk
from tkinter import ttk, messagebox
from systems.money_system import MoneySystem
from datetime import datetime

class BankInterface:
    """Bank interface for managing money"""

    def __init__(self, root, game_data, on_back=None):
        self.root = root
        self.game_data = game_data
        self.on_back = on_back
        self.money_system = MoneySystem(game_data)

        # Check if online banking is available
        current_year = self.get_current_year()
        self.online_banking = self.money_system.can_use_online_banking(current_year)

        self.setup_ui()

    def get_current_year(self):
        """Get current game year"""
        if 'game_time' in self.game_data.data:
            date_str = self.game_data.data['game_time'].get('current_date', '1984-01-01')
            return int(date_str.split('-')[0])
        return 1984

    def setup_ui(self):
        """Setup bank interface UI"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main frame
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_text = "Online Banking" if self.online_banking else "First National Bank"
        title_label = tk.Label(main_frame, text=title_text,
                              font=('Arial', 24, 'bold'), bg='#1a1a1a', fg='white')
        title_label.pack(pady=20)

        # Account Summary Frame
        summary_frame = tk.LabelFrame(main_frame, text="Account Summary",
                                     font=('Arial', 14, 'bold'), bg='#2a2a2a', fg='white')
        summary_frame.pack(pady=10, padx=20, fill='x')

        # Cash on hand
        cash_frame = tk.Frame(summary_frame, bg='#2a2a2a')
        cash_frame.pack(pady=10, padx=20, fill='x')
        tk.Label(cash_frame, text="Cash on Hand:", font=('Arial', 12),
                bg='#2a2a2a', fg='#cccccc').pack(side='left')
        self.cash_label = tk.Label(cash_frame, text=f"${self.money_system.get_cash():,.2f}",
                                  font=('Arial', 12, 'bold'), bg='#2a2a2a', fg='#90EE90')
        self.cash_label.pack(side='right')

        # Bank balance
        bank_frame = tk.Frame(summary_frame, bg='#2a2a2a')
        bank_frame.pack(pady=10, padx=20, fill='x')
        tk.Label(bank_frame, text="Bank Balance:", font=('Arial', 12),
                bg='#2a2a2a', fg='#cccccc').pack(side='left')
        self.bank_label = tk.Label(bank_frame, text=f"${self.money_system.get_bank_balance():,.2f}",
                                  font=('Arial', 12, 'bold'), bg='#2a2a2a', fg='#90EE90')
        self.bank_label.pack(side='right')

        # Total
        total_frame = tk.Frame(summary_frame, bg='#2a2a2a')
        total_frame.pack(pady=10, padx=20, fill='x')
        tk.Label(total_frame, text="Total Assets:", font=('Arial', 12, 'bold'),
                bg='#2a2a2a', fg='white').pack(side='left')
        self.total_label = tk.Label(total_frame, text=f"${self.money_system.get_total_money():,.2f}",
                                   font=('Arial', 12, 'bold'), bg='#2a2a2a', fg='#FFD700')
        self.total_label.pack(side='right')

        # Transaction Buttons Frame
        button_frame = tk.LabelFrame(main_frame, text="Transactions",
                                    font=('Arial', 14, 'bold'), bg='#2a2a2a', fg='white')
        button_frame.pack(pady=10, padx=20, fill='x')

        trans_buttons = tk.Frame(button_frame, bg='#2a2a2a')
        trans_buttons.pack(pady=20)

        # Withdraw button
        tk.Button(trans_buttons, text="Withdraw Cash", command=self.show_withdraw_dialog,
                 font=('Arial', 12), bg='#4a4a4a', fg='white', width=15,
                 padx=10, pady=10).pack(side='left', padx=10)

        # Deposit button
        tk.Button(trans_buttons, text="Deposit Cash", command=self.show_deposit_dialog,
                 font=('Arial', 12), bg='#4a4a4a', fg='white', width=15,
                 padx=10, pady=10).pack(side='left', padx=10)

        # Transaction History Frame
        history_frame = tk.LabelFrame(main_frame, text="Transaction History (Last 3 Months)",
                                     font=('Arial', 14, 'bold'), bg='#2a2a2a', fg='white')
        history_frame.pack(pady=10, padx=20, fill='both', expand=True)

        # Create Treeview for transactions
        columns = ('Date', 'Description', 'Amount', 'Account', 'Balance')
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show='headings', height=10)

        # Configure columns
        self.history_tree.heading('Date', text='Date')
        self.history_tree.heading('Description', text='Description')
        self.history_tree.heading('Amount', text='Amount')
        self.history_tree.heading('Account', text='Account')
        self.history_tree.heading('Balance', text='Balance After')

        self.history_tree.column('Date', width=100)
        self.history_tree.column('Description', width=200)
        self.history_tree.column('Amount', width=100)
        self.history_tree.column('Account', width=80)
        self.history_tree.column('Balance', width=100)

        # Style for treeview
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Treeview', background='#3a3a3a', foreground='white', fieldbackground='#3a3a3a')
        style.configure('Treeview.Heading', background='#4a4a4a', foreground='white')

        self.history_tree.pack(pady=10, padx=10, fill='both', expand=True)

        # Load transaction history
        self.load_transaction_history()

        # Monthly Summary Frame
        summary_monthly_frame = tk.LabelFrame(main_frame, text="Monthly Summary",
                                             font=('Arial', 14, 'bold'), bg='#2a2a2a', fg='white')
        summary_monthly_frame.pack(pady=10, padx=20, fill='x')

        self.monthly_summary_text = tk.Text(summary_monthly_frame, height=4, bg='#3a3a3a', fg='white',
                                           font=('Courier', 10))
        self.monthly_summary_text.pack(pady=10, padx=10, fill='x')
        self.load_monthly_summary()

        # Back button
        tk.Button(main_frame, text="Back", command=self.go_back,
                 font=('Arial', 12), bg='#555', fg='white', padx=20, pady=5).pack(pady=20)

    def show_withdraw_dialog(self):
        """Show withdrawal dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Withdraw Cash")
        dialog.geometry("400x200")
        dialog.transient(self.root)
        dialog.grab_set()

        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - 200
        y = (dialog.winfo_screenheight() // 2) - 100
        dialog.geometry(f"400x200+{x}+{y}")

        # Content
        tk.Label(dialog, text="Withdraw from Bank", font=('Arial', 14, 'bold')).pack(pady=10)

        tk.Label(dialog, text=f"Available: ${self.money_system.get_bank_balance():,.2f}",
                font=('Arial', 12)).pack(pady=5)

        # Amount entry
        entry_frame = tk.Frame(dialog)
        entry_frame.pack(pady=10)
        tk.Label(entry_frame, text="Amount: $", font=('Arial', 12)).pack(side='left')
        amount_entry = tk.Entry(entry_frame, font=('Arial', 12), width=10)
        amount_entry.pack(side='left')
        amount_entry.focus()

        # Quick amount buttons
        quick_frame = tk.Frame(dialog)
        quick_frame.pack(pady=5)
        for amount in [20, 50, 100, 200]:
            tk.Button(quick_frame, text=f"${amount}", command=lambda a=amount: amount_entry.insert(0, str(a)),
                     font=('Arial', 10), width=6).pack(side='left', padx=2)

        # Buttons
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=10)

        def withdraw():
            try:
                amount = float(amount_entry.get())
                success, message = self.money_system.withdraw_cash(amount)
                if success:
                    messagebox.showinfo("Success", message)
                    self.refresh_display()
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", message)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount")

        tk.Button(button_frame, text="Withdraw", command=withdraw,
                 font=('Arial', 12), bg='#4a7a4a', fg='white', padx=20).pack(side='left', padx=5)
        tk.Button(button_frame, text="Cancel", command=dialog.destroy,
                 font=('Arial', 12), bg='#7a4a4a', fg='white', padx=20).pack(side='left', padx=5)

    def show_deposit_dialog(self):
        """Show deposit dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Deposit Cash")
        dialog.geometry("400x200")
        dialog.transient(self.root)
        dialog.grab_set()

        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - 200
        y = (dialog.winfo_screenheight() // 2) - 100
        dialog.geometry(f"400x200+{x}+{y}")

        # Content
        tk.Label(dialog, text="Deposit to Bank", font=('Arial', 14, 'bold')).pack(pady=10)

        tk.Label(dialog, text=f"Cash on Hand: ${self.money_system.get_cash():,.2f}",
                font=('Arial', 12)).pack(pady=5)

        # Amount entry
        entry_frame = tk.Frame(dialog)
        entry_frame.pack(pady=10)
        tk.Label(entry_frame, text="Amount: $", font=('Arial', 12)).pack(side='left')
        amount_entry = tk.Entry(entry_frame, font=('Arial', 12), width=10)
        amount_entry.pack(side='left')
        amount_entry.focus()

        # Deposit all button
        tk.Button(dialog, text="Deposit All", command=lambda: amount_entry.insert(0, str(self.money_system.get_cash())),
                 font=('Arial', 10)).pack(pady=5)

        # Buttons
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=10)

        def deposit():
            try:
                amount = float(amount_entry.get())
                success, message = self.money_system.deposit_cash(amount)
                if success:
                    messagebox.showinfo("Success", message)
                    self.refresh_display()
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", message)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount")

        tk.Button(button_frame, text="Deposit", command=deposit,
                 font=('Arial', 12), bg='#4a7a4a', fg='white', padx=20).pack(side='left', padx=5)
        tk.Button(button_frame, text="Cancel", command=dialog.destroy,
                 font=('Arial', 12), bg='#7a4a4a', fg='white', padx=20).pack(side='left', padx=5)

    def load_transaction_history(self):
        """Load transaction history into treeview"""
        # Clear existing items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        # Get transactions
        transactions = self.money_system.get_transaction_history()

        # Add transactions to tree (newest first)
        for trans in reversed(transactions):
            amount_str = f"${abs(trans['amount']):,.2f}"
            if trans['amount'] < 0:
                amount_str = f"-{amount_str}"
            else:
                amount_str = f"+{amount_str}"

            values = (
                trans['date'],
                trans['description'],
                amount_str,
                trans['account'].capitalize(),
                f"${trans['balance_after']:,.2f}"
            )

            # Color coding
            tag = 'income' if trans['amount'] > 0 else 'expense'
            self.history_tree.insert('', 0, values=values, tags=(tag,))

        # Configure tags
        self.history_tree.tag_configure('income', foreground='#90EE90')
        self.history_tree.tag_configure('expense', foreground='#FF6B6B')

    def load_monthly_summary(self):
        """Load monthly summary"""
        self.monthly_summary_text.delete('1.0', tk.END)

        monthly_data = self.money_system.get_monthly_summary()

        if not monthly_data:
            self.monthly_summary_text.insert('1.0', "No transaction data available")
            return

        # Sort by month
        sorted_months = sorted(monthly_data.keys(), reverse=True)[:3]

        summary_lines = []
        for month in sorted_months:
            data = monthly_data[month]
            # Format month for display
            year, month_num = month.split('-')
            month_name = datetime(int(year), int(month_num), 1).strftime('%B %Y')

            net = data['income'] - data['expenses']
            summary_lines.append(f"{month_name}: Income: ${data['income']:,.0f} | "
                                f"Expenses: ${data['expenses']:,.0f} | Net: ${net:+,.0f}")

        self.monthly_summary_text.insert('1.0', '\n'.join(summary_lines))

    def refresh_display(self):
        """Refresh all displayed values"""
        self.cash_label.config(text=f"${self.money_system.get_cash():,.2f}")
        self.bank_label.config(text=f"${self.money_system.get_bank_balance():,.2f}")
        self.total_label.config(text=f"${self.money_system.get_total_money():,.2f}")
        self.load_transaction_history()
        self.load_monthly_summary()

    def go_back(self):
        """Return to previous screen"""
        if self.on_back:
            self.on_back()