"""
Grocery Store UI
Interface for browsing and purchasing items
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Callable, Optional
from systems.grocery_items import GroceryStore, ItemCategory, GROCERY_ITEMS

class GroceryStoreWindow:
    """UI for the grocery store"""

    def __init__(self, game_data: Dict, on_close: Optional[Callable] = None):
        self.game_data = game_data
        self.on_close = on_close
        self.store = GroceryStore(game_data)

        # Create window
        self.window = tk.Toplevel()
        self.window.title("DevMart - 24/7 Developer Essentials")
        self.window.geometry("900x600")
        self.window.configure(bg='#2b2b2b')

        # Prevent closing without proper cleanup
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)

        self.setup_ui()
        self.refresh_display()

    def setup_ui(self):
        """Setup the store interface"""
        # Header
        header_frame = tk.Frame(self.window, bg='#1a1a1a', height=60)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="🛒 DevMart",
            font=('Arial', 20, 'bold'),
            fg='#4CAF50',
            bg='#1a1a1a'
        ).pack(side='left', padx=20, pady=15)

        # Money display
        self.money_label = tk.Label(
            header_frame,
            text=f"Balance: ${self.game_data.get('money', 0):,.0f}",
            font=('Arial', 14, 'bold'),
            fg='#FFD700',
            bg='#1a1a1a'
        )
        self.money_label.pack(side='right', padx=20, pady=15)

        # Main container
        main_container = tk.Frame(self.window, bg='#2b2b2b')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)

        # Left panel - Categories
        left_panel = tk.Frame(main_container, bg='#1a1a1a', width=200)
        left_panel.pack(side='left', fill='y', padx=(0, 10))
        left_panel.pack_propagate(False)

        tk.Label(
            left_panel,
            text="Categories",
            font=('Arial', 14, 'bold'),
            fg='white',
            bg='#1a1a1a'
        ).pack(pady=10)

        # Category buttons
        self.category_buttons = {}
        for category in ItemCategory:
            btn = tk.Button(
                left_panel,
                text=category.value,
                font=('Arial', 11),
                bg='#3a3a3a',
                fg='white',
                activebackground='#4a4a4a',
                relief='flat',
                command=lambda c=category: self.filter_by_category(c),
                width=20
            )
            btn.pack(pady=2, padx=10)
            self.category_buttons[category] = btn

        # Show all button
        tk.Button(
            left_panel,
            text="Show All",
            font=('Arial', 11, 'bold'),
            bg='#4CAF50',
            fg='white',
            activebackground='#5CBF60',
            relief='flat',
            command=self.show_all_items,
            width=20
        ).pack(pady=10, padx=10)

        # Right panel - Items
        right_panel = tk.Frame(main_container, bg='#2b2b2b')
        right_panel.pack(side='left', fill='both', expand=True)

        # Search bar
        search_frame = tk.Frame(right_panel, bg='#2b2b2b')
        search_frame.pack(fill='x', pady=(0, 10))

        tk.Label(
            search_frame,
            text="Search:",
            font=('Arial', 11),
            fg='white',
            bg='#2b2b2b'
        ).pack(side='left', padx=5)

        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.search_items())

        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=('Arial', 11),
            bg='#3a3a3a',
            fg='white',
            insertbackground='white'
        )
        search_entry.pack(side='left', fill='x', expand=True, padx=5)

        # Items display area with scrollbar
        items_frame = tk.Frame(right_panel, bg='#2b2b2b')
        items_frame.pack(fill='both', expand=True)

        # Canvas and scrollbar for items
        self.canvas = tk.Canvas(items_frame, bg='#2b2b2b', highlightthickness=0)
        scrollbar = ttk.Scrollbar(items_frame, orient='vertical', command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='#2b2b2b')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Bottom panel - Inventory preview
        bottom_panel = tk.Frame(self.window, bg='#1a1a1a', height=100)
        bottom_panel.pack(fill='x', side='bottom', padx=0, pady=0)
        bottom_panel.pack_propagate(False)

        tk.Label(
            bottom_panel,
            text="Your Inventory:",
            font=('Arial', 12, 'bold'),
            fg='white',
            bg='#1a1a1a'
        ).pack(anchor='w', padx=20, pady=(10, 5))

        self.inventory_label = tk.Label(
            bottom_panel,
            text="Empty",
            font=('Arial', 10),
            fg='#888888',
            bg='#1a1a1a',
            justify='left',
            anchor='w'
        )
        self.inventory_label.pack(anchor='w', padx=20)

        # Close button
        tk.Button(
            bottom_panel,
            text="Close Store",
            font=('Arial', 12, 'bold'),
            bg='#F44336',
            fg='white',
            activebackground='#D32F2F',
            command=self.close_window,
            width=15
        ).pack(side='right', padx=20, pady=10)

        self.current_category = None
        self.item_widgets = []

    def create_item_card(self, item_id: str, row: int, col: int):
        """Create a card for an item"""
        item = GROCERY_ITEMS[item_id]

        # Item frame
        item_frame = tk.Frame(
            self.scrollable_frame,
            bg='#3a3a3a',
            relief='raised',
            bd=1
        )
        item_frame.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')

        # Configure grid weights
        self.scrollable_frame.grid_columnconfigure(col, weight=1)

        # Item name
        tk.Label(
            item_frame,
            text=item.name,
            font=('Arial', 12, 'bold'),
            fg='white',
            bg='#3a3a3a'
        ).pack(padx=10, pady=(10, 5))

        # Category
        tk.Label(
            item_frame,
            text=item.category.value,
            font=('Arial', 9),
            fg='#888888',
            bg='#3a3a3a'
        ).pack()

        # Price
        tk.Label(
            item_frame,
            text=f"${item.price}",
            font=('Arial', 14, 'bold'),
            fg='#4CAF50',
            bg='#3a3a3a'
        ).pack(pady=5)

        # Description
        tk.Label(
            item_frame,
            text=item.description,
            font=('Arial', 9),
            fg='#cccccc',
            bg='#3a3a3a',
            wraplength=200
        ).pack(padx=10, pady=5)

        # Effect
        tk.Label(
            item_frame,
            text=item.effect_description,
            font=('Arial', 9, 'italic'),
            fg='#FFD700',
            bg='#3a3a3a',
            wraplength=200
        ).pack(padx=10, pady=5)

        # Quantity info
        if item.quantity > 1:
            tk.Label(
                item_frame,
                text=f"Qty: {item.quantity} per purchase",
                font=('Arial', 9),
                fg='#888888',
                bg='#3a3a3a'
            ).pack()

        # Stack info
        current_owned = self.game_data.get("inventory", {}).get(item_id, 0)
        tk.Label(
            item_frame,
            text=f"Owned: {current_owned}/{item.max_stack}",
            font=('Arial', 9),
            fg='#00BCD4',
            bg='#3a3a3a'
        ).pack(pady=2)

        # Buy button
        can_buy, reason = self.store.can_purchase(item_id)

        buy_btn = tk.Button(
            item_frame,
            text="BUY" if can_buy else reason,
            font=('Arial', 11, 'bold'),
            bg='#4CAF50' if can_buy else '#666666',
            fg='white',
            activebackground='#5CBF60' if can_buy else '#666666',
            state='normal' if can_buy else 'disabled',
            command=lambda: self.purchase_item(item_id),
            width=15
        )
        buy_btn.pack(pady=10)

        self.item_widgets.append(item_frame)

    def filter_by_category(self, category: ItemCategory):
        """Filter items by category"""
        self.current_category = category
        self.refresh_display()

        # Highlight selected category
        for cat, btn in self.category_buttons.items():
            if cat == category:
                btn.config(bg='#4CAF50')
            else:
                btn.config(bg='#3a3a3a')

    def show_all_items(self):
        """Show all items"""
        self.current_category = None
        self.refresh_display()

        # Reset category buttons
        for btn in self.category_buttons.values():
            btn.config(bg='#3a3a3a')

    def search_items(self):
        """Search items by name"""
        self.refresh_display()

    def refresh_display(self):
        """Refresh the items display"""
        # Clear existing items
        for widget in self.item_widgets:
            widget.destroy()
        self.item_widgets.clear()

        # Get items to display
        items_to_show = []
        search_term = self.search_var.get().lower()

        for item_id, item in GROCERY_ITEMS.items():
            # Filter by category
            if self.current_category and item.category != self.current_category:
                continue

            # Filter by search
            if search_term and search_term not in item.name.lower() and search_term not in item.description.lower():
                continue

            items_to_show.append(item_id)

        # Display items in grid
        row = 0
        col = 0
        for item_id in items_to_show:
            self.create_item_card(item_id, row, col)
            col += 1
            if col >= 3:  # 3 items per row
                col = 0
                row += 1

        # Update money display
        self.money_label.config(text=f"Balance: ${self.game_data.get('money', 0):,.0f}")

        # Update inventory display
        self.update_inventory_display()

    def purchase_item(self, item_id: str):
        """Purchase an item"""
        if self.store.purchase_item(item_id):
            item = GROCERY_ITEMS[item_id]
            messagebox.showinfo(
                "Purchase Successful",
                f"You bought {item.name} for ${item.price}!"
            )
            self.refresh_display()
        else:
            messagebox.showerror(
                "Purchase Failed",
                "Could not complete purchase."
            )

    def update_inventory_display(self):
        """Update the inventory display at the bottom"""
        inventory = self.store.get_inventory_display()

        if not inventory:
            self.inventory_label.config(text="Empty")
        else:
            inv_text = ""
            for item_id, info in inventory.items():
                inv_text += f"{info['name']} x{info['quantity']}  |  "

            self.inventory_label.config(text=inv_text.rstrip("  |  "))

    def close_window(self):
        """Close the store window"""
        self.window.destroy()
        if self.on_close:
            self.on_close()