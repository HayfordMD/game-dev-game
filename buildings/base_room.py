"""
Base room class for all game rooms
Provides common functionality including debug menu support
"""

import tkinter as tk
from tkinter import ttk
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tech.run_platforms import RunPlatforms


class BaseRoom:
    """Base class for all room screens"""

    def __init__(self, root, game_data, on_back=None):
        self.root = root
        self.game_data = game_data
        self.on_back = on_back

        # Initialize run platforms (load existing or create new)
        self.run_platforms = RunPlatforms()
        if not self.run_platforms.load_run():
            # New run - randomize platforms
            self.run_platforms.randomize_run()
            self.run_platforms.save_run()

        # Bind Alt+Q for debug menu globally
        self.root.bind('<Alt-q>', lambda e: self.show_debug_menu())

    def show_debug_menu(self):
        """Show debug menu with Run Consoles and Run Companies lists (Alt+Q)"""
        debug_window = tk.Toplevel(self.root)
        debug_window.title("Debug Menu - Run Configuration")
        debug_window.geometry("800x600")
        debug_window.transient(self.root)
        debug_window.grab_set()

        # Center the window
        debug_window.update_idletasks()
        x = (debug_window.winfo_screenwidth() // 2) - 400
        y = (debug_window.winfo_screenheight() // 2) - 300
        debug_window.geometry(f"800x600+{x}+{y}")

        # Title
        title_label = tk.Label(debug_window, text="Run Configuration (Alt+Q)",
                              font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)

        # Create notebook for tabs
        notebook = ttk.Notebook(debug_window)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Run Consoles Tab
        consoles_frame = ttk.Frame(notebook)
        notebook.add(consoles_frame, text="Run Consoles")
        self.create_consoles_tab(consoles_frame)

        # Run Companies Tab
        companies_frame = ttk.Frame(notebook)
        notebook.add(companies_frame, text="Run Companies")
        self.create_companies_tab(companies_frame)

        # Close button
        close_button = ttk.Button(debug_window, text="Close", command=debug_window.destroy)
        close_button.pack(pady=10)

    def create_consoles_tab(self, parent):
        """Create the Run Consoles tab content"""
        # Title
        title_label = tk.Label(parent, text="Platforms Selected for This Run",
                              font=('Arial', 14, 'bold'))
        title_label.pack(pady=10)

        # Create scrollable frame
        canvas = tk.Canvas(parent, bg='white')
        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Display run platforms by generation
        generation_names = [
            ("early_80s", "Early 80s (1978-1983)"),
            ("late_80s", "Late 80s (1984-1989)"),
            ("early_90s", "Early 90s (1990-1994)"),
            ("late_90s", "Late 90s (1995-1999)"),
            ("early_2000s", "Early 2000s (2000-2005)"),
            ("late_2000s", "Late 2000s (2006-2009)"),
            ("early_2010s", "Early 2010s (2010-2017)"),
            ("late_2010s", "Late 2010s (2018-2024)"),
            ("future_2025", "Future (2025-2030)")
        ]

        for gen_key, gen_name in generation_names:
            # Generation frame
            gen_frame = ttk.LabelFrame(scrollable_frame, text=gen_name)
            gen_frame.pack(fill='x', padx=10, pady=5)

            # Consoles
            consoles_label = tk.Label(gen_frame, text="CONSOLES:", font=('Arial', 10, 'bold'))
            consoles_label.pack(anchor='w', padx=10, pady=(5, 0))

            consoles = self.run_platforms.run_consoles.get(gen_key, [])
            if consoles:
                for i, console in enumerate(consoles, 1):
                    console_text = f"  {i}. {console['name']}"
                    tk.Label(gen_frame, text=console_text, font=('Arial', 9)).pack(anchor='w', padx=20)
            else:
                tk.Label(gen_frame, text="  None", font=('Arial', 9, 'italic')).pack(anchor='w', padx=20)

            # Handhelds
            handhelds_label = tk.Label(gen_frame, text="HANDHELDS:", font=('Arial', 10, 'bold'))
            handhelds_label.pack(anchor='w', padx=10, pady=(5, 0))

            handhelds = self.run_platforms.run_handhelds.get(gen_key, [])
            if handhelds:
                for i, handheld in enumerate(handhelds, 1):
                    handheld_text = f"  {i}. {handheld['name']}"
                    tk.Label(gen_frame, text=handheld_text, font=('Arial', 9)).pack(anchor='w', padx=20)
            else:
                tk.Label(gen_frame, text="  None", font=('Arial', 9, 'italic')).pack(anchor='w', padx=20)

            # Computers (always available)
            computers_label = tk.Label(gen_frame, text="COMPUTERS:", font=('Arial', 10, 'bold'))
            computers_label.pack(anchor='w', padx=10, pady=(5, 0))
            tk.Label(gen_frame, text="  • PC (Always Available)", font=('Arial', 9)).pack(anchor='w', padx=20)
            tk.Label(gen_frame, text="  • MAC (Always Available)", font=('Arial', 9)).pack(anchor='w', padx=20, pady=(0, 5))

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def create_companies_tab(self, parent):
        """Create the Run Companies tab content"""
        # Title
        title_label = tk.Label(parent, text=f"Competitor Companies for This Run ({len(self.run_platforms.run_companies)} companies)",
                              font=('Arial', 14, 'bold'))
        title_label.pack(pady=10)

        # Create scrollable frame
        canvas = tk.Canvas(parent, bg='white')
        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Display companies in columns
        columns_frame = ttk.Frame(scrollable_frame)
        columns_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Create 3 columns for companies
        num_columns = 3
        companies_per_column = (len(self.run_platforms.run_companies) + num_columns - 1) // num_columns

        for col in range(num_columns):
            column_frame = ttk.Frame(columns_frame)
            column_frame.pack(side='left', fill='both', expand=True, padx=10, anchor='n')

            start_idx = col * companies_per_column
            end_idx = min(start_idx + companies_per_column, len(self.run_platforms.run_companies))

            for i in range(start_idx, end_idx):
                company_text = f"{i + 1:2}. {self.run_platforms.run_companies[i]}"
                tk.Label(column_frame, text=company_text, font=('Arial', 10), anchor='w').pack(fill='x', pady=2)

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def back_to_menu(self):
        """Go back to previous screen"""
        if self.on_back:
            self.on_back()