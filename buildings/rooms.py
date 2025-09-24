"""
Placeholder rooms for the game
All rooms inherit from BaseRoom to get the Alt+Q debug menu functionality
"""

import tkinter as tk
from tkinter import Canvas, ttk
from buildings.base_room import BaseRoom


class ApartmentRoom(BaseRoom):
    """Player's apartment room"""

    def __init__(self, root, game_data, on_back=None):
        super().__init__(root, game_data, on_back)
        self.setup_ui()

    def setup_ui(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main frame
        self.main_frame = tk.Frame(self.root, bg='#2a2a2a')
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        tk.Label(self.main_frame, text="APARTMENT",
                font=('Arial', 24, 'bold'), bg='#2a2a2a', fg='white').pack(pady=50)

        tk.Label(self.main_frame, text="Your personal apartment",
                font=('Arial', 12), bg='#2a2a2a', fg='#888').pack()

        tk.Label(self.main_frame, text="[Under Construction]",
                font=('Arial', 10, 'italic'), bg='#2a2a2a', fg='#666').pack(pady=20)

        # Back button
        tk.Button(self.main_frame, text="Back", command=self.back_to_menu,
                 font=('Arial', 12), bg='#555', fg='white', padx=20, pady=5).pack(pady=20)

        # Instructions
        tk.Label(self.main_frame, text="Press Alt+Q for Debug Menu",
                font=('Arial', 10), bg='#2a2a2a', fg='yellow').pack(pady=10)


class Office1Room(BaseRoom):
    """First office room"""

    def __init__(self, root, game_data, on_back=None):
        super().__init__(root, game_data, on_back)
        self.setup_ui()

    def setup_ui(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main frame
        self.main_frame = tk.Frame(self.root, bg='#3a3a3a')
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        tk.Label(self.main_frame, text="OFFICE 1",
                font=('Arial', 24, 'bold'), bg='#3a3a3a', fg='white').pack(pady=50)

        tk.Label(self.main_frame, text="Small starter office",
                font=('Arial', 12), bg='#3a3a3a', fg='#888').pack()

        tk.Label(self.main_frame, text="[Under Construction]",
                font=('Arial', 10, 'italic'), bg='#3a3a3a', fg='#666').pack(pady=20)

        # Back button
        tk.Button(self.main_frame, text="Back", command=self.back_to_menu,
                 font=('Arial', 12), bg='#555', fg='white', padx=20, pady=5).pack(pady=20)

        # Instructions
        tk.Label(self.main_frame, text="Press Alt+Q for Debug Menu",
                font=('Arial', 10), bg='#3a3a3a', fg='yellow').pack(pady=10)


class Office2Room(BaseRoom):
    """Second office room"""

    def __init__(self, root, game_data, on_back=None):
        super().__init__(root, game_data, on_back)
        self.setup_ui()

    def setup_ui(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main frame
        self.main_frame = tk.Frame(self.root, bg='#3a3a4a')
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        tk.Label(self.main_frame, text="OFFICE 2",
                font=('Arial', 24, 'bold'), bg='#3a3a4a', fg='white').pack(pady=50)

        tk.Label(self.main_frame, text="Medium-sized office",
                font=('Arial', 12), bg='#3a3a4a', fg='#888').pack()

        tk.Label(self.main_frame, text="[Under Construction]",
                font=('Arial', 10, 'italic'), bg='#3a3a4a', fg='#666').pack(pady=20)

        # Back button
        tk.Button(self.main_frame, text="Back", command=self.back_to_menu,
                 font=('Arial', 12), bg='#555', fg='white', padx=20, pady=5).pack(pady=20)

        # Instructions
        tk.Label(self.main_frame, text="Press Alt+Q for Debug Menu",
                font=('Arial', 10), bg='#3a3a4a', fg='yellow').pack(pady=10)


class Office3Room(BaseRoom):
    """Third office room"""

    def __init__(self, root, game_data, on_back=None):
        super().__init__(root, game_data, on_back)
        self.setup_ui()

    def setup_ui(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main frame
        self.main_frame = tk.Frame(self.root, bg='#4a3a4a')
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        tk.Label(self.main_frame, text="OFFICE 3",
                font=('Arial', 24, 'bold'), bg='#4a3a4a', fg='white').pack(pady=50)

        tk.Label(self.main_frame, text="Large corporate office",
                font=('Arial', 12), bg='#4a3a4a', fg='#888').pack()

        tk.Label(self.main_frame, text="[Under Construction]",
                font=('Arial', 10, 'italic'), bg='#4a3a4a', fg='#666').pack(pady=20)

        # Back button
        tk.Button(self.main_frame, text="Back", command=self.back_to_menu,
                 font=('Arial', 12), bg='#555', fg='white', padx=20, pady=5).pack(pady=20)

        # Instructions
        tk.Label(self.main_frame, text="Press Alt+Q for Debug Menu",
                font=('Arial', 10), bg='#4a3a4a', fg='yellow').pack(pady=10)


class HomeRoom(BaseRoom):
    """Player's home room"""

    def __init__(self, root, game_data, on_back=None):
        super().__init__(root, game_data, on_back)
        self.setup_ui()

    def setup_ui(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main frame
        self.main_frame = tk.Frame(self.root, bg='#2a3a2a')
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        tk.Label(self.main_frame, text="HOME",
                font=('Arial', 24, 'bold'), bg='#2a3a2a', fg='white').pack(pady=50)

        tk.Label(self.main_frame, text="Your family home",
                font=('Arial', 12), bg='#2a3a2a', fg='#888').pack()

        tk.Label(self.main_frame, text="[Under Construction]",
                font=('Arial', 10, 'italic'), bg='#2a3a2a', fg='#666').pack(pady=20)

        # Back button
        tk.Button(self.main_frame, text="Back", command=self.back_to_menu,
                 font=('Arial', 12), bg='#555', fg='white', padx=20, pady=5).pack(pady=20)

        # Instructions
        tk.Label(self.main_frame, text="Press Alt+Q for Debug Menu",
                font=('Arial', 10), bg='#2a3a2a', fg='yellow').pack(pady=10)


class Building1Room(BaseRoom):
    """First building room"""

    def __init__(self, root, game_data, on_back=None):
        super().__init__(root, game_data, on_back)
        self.setup_ui()

    def setup_ui(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main frame
        self.main_frame = tk.Frame(self.root, bg='#5a4a3a')
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        tk.Label(self.main_frame, text="BUILDING 1",
                font=('Arial', 24, 'bold'), bg='#5a4a3a', fg='white').pack(pady=50)

        tk.Label(self.main_frame, text="Company headquarters",
                font=('Arial', 12), bg='#5a4a3a', fg='#888').pack()

        tk.Label(self.main_frame, text="[Under Construction]",
                font=('Arial', 10, 'italic'), bg='#5a4a3a', fg='#666').pack(pady=20)

        # Back button
        tk.Button(self.main_frame, text="Back", command=self.back_to_menu,
                 font=('Arial', 12), bg='#555', fg='white', padx=20, pady=5).pack(pady=20)

        # Instructions
        tk.Label(self.main_frame, text="Press Alt+Q for Debug Menu",
                font=('Arial', 10), bg='#5a4a3a', fg='yellow').pack(pady=10)


class BarRoom(BaseRoom):
    """Bar room for socializing"""

    def __init__(self, root, game_data, on_back=None):
        super().__init__(root, game_data, on_back)
        self.setup_ui()

    def setup_ui(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main frame
        self.main_frame = tk.Frame(self.root, bg='#4a2a2a')
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        tk.Label(self.main_frame, text="BAR",
                font=('Arial', 24, 'bold'), bg='#4a2a2a', fg='white').pack(pady=50)

        tk.Label(self.main_frame, text="Local watering hole",
                font=('Arial', 12), bg='#4a2a2a', fg='#888').pack()

        tk.Label(self.main_frame, text="[Under Construction]",
                font=('Arial', 10, 'italic'), bg='#4a2a2a', fg='#666').pack(pady=20)

        # Back button
        tk.Button(self.main_frame, text="Back", command=self.back_to_menu,
                 font=('Arial', 12), bg='#555', fg='white', padx=20, pady=5).pack(pady=20)

        # Instructions
        tk.Label(self.main_frame, text="Press Alt+Q for Debug Menu",
                font=('Arial', 10), bg='#4a2a2a', fg='yellow').pack(pady=10)


class LibraryRoom(BaseRoom):
    """Library room for research"""

    def __init__(self, root, game_data, on_back=None):
        super().__init__(root, game_data, on_back)
        self.setup_ui()

    def setup_ui(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main frame
        self.main_frame = tk.Frame(self.root, bg='#3a3a5a')
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        tk.Label(self.main_frame, text="LIBRARY",
                font=('Arial', 24, 'bold'), bg='#3a3a5a', fg='white').pack(pady=50)

        tk.Label(self.main_frame, text="Research and learning center",
                font=('Arial', 12), bg='#3a3a5a', fg='#888').pack()

        tk.Label(self.main_frame, text="[Under Construction]",
                font=('Arial', 10, 'italic'), bg='#3a3a5a', fg='#666').pack(pady=20)

        # Back button
        tk.Button(self.main_frame, text="Back", command=self.back_to_menu,
                 font=('Arial', 12), bg='#555', fg='white', padx=20, pady=5).pack(pady=20)

        # Instructions
        tk.Label(self.main_frame, text="Press Alt+Q for Debug Menu",
                font=('Arial', 10), bg='#3a3a5a', fg='yellow').pack(pady=10)