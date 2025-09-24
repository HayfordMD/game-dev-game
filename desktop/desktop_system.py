"""
Desktop PC Interface System
Provides the computer interface for game development
"""

import tkinter as tk
from tkinter import ttk, messagebox
from systems.unlock_system import UnlockSystem
from desktop.unlock_viewer import UnlockViewer
from desktop.game_engine import GameEngineWindow


class DesktopScreen:
    """PC Desktop interface that appears when using the desk"""

    def __init__(self, parent, game_data, on_close):
        self.parent = parent
        self.game_data = game_data
        self.on_close = on_close

        # Create desktop window - fullscreen
        self.desktop_window = tk.Toplevel(parent)
        self.desktop_window.title("Desktop - Game Development PC")
        self.desktop_window.geometry("1920x1080")
        self.desktop_window.configure(bg='#1e1e2e')

        # Make it modal and center it
        self.desktop_window.transient(parent)
        self.desktop_window.grab_set()

        # Center the window
        self.desktop_window.update_idletasks()
        x = (self.desktop_window.winfo_screenwidth() // 2) - 960
        y = (self.desktop_window.winfo_screenheight() // 2) - 540
        self.desktop_window.geometry(f"1920x1080+{x}+{y}")

        # Bind close event
        self.desktop_window.protocol("WM_DELETE_WINDOW", self.close_desktop)

        # Track if OpenEngine is open
        self.openengine_active = False

        # Initialize unlock system
        self.unlock_system = UnlockSystem(game_data)

        # Update last desktop use time
        time_data = self.game_data.data.get('time', {})
        self.game_data.data['last_desktop_use'] = {
            'year': time_data.get('year', 1978),
            'month': time_data.get('month', 1),
            'day': time_data.get('day', 1)
        }

        self.setup_desktop()

    def setup_desktop(self):
        """Setup the desktop interface"""
        # Title bar
        title_frame = tk.Frame(self.desktop_window, bg='#2b2b3c', height=30)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)

        tk.Label(title_frame, text="GameDev OS - 1978 Edition",
                font=('Courier', 12, 'bold'), bg='#2b2b3c', fg='#00ff00').pack(side='left', padx=10, pady=5)

        # Close button
        close_btn = tk.Button(title_frame, text="X", command=self.close_desktop,
                            bg='#ff4444', fg='white', font=('Arial', 10, 'bold'),
                            padx=10, cursor='hand2')
        close_btn.pack(side='right', padx=5, pady=2)

        # Desktop area
        self.desktop_frame = tk.Frame(self.desktop_window, bg='#0a0a0f')
        self.desktop_frame.pack(fill='both', expand=True)

        # Show initial desktop with OpenEngine icon
        self.show_desktop_icons()

    def show_desktop_icons(self):
        """Show desktop with application icons"""
        # Clear desktop
        for widget in self.desktop_frame.winfo_children():
            widget.destroy()

        # Desktop icons frame
        icons_frame = tk.Frame(self.desktop_frame, bg='#0a0a0f')
        icons_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # OpenEngine icon
        openengine_frame = tk.Frame(icons_frame, bg='#0a0a0f')
        openengine_frame.place(x=50, y=50)

        # Icon button
        icon_btn = tk.Button(openengine_frame, text="📦", font=('Arial', 32),
                           bg='#0a0a0f', fg='#4a9eff', bd=0,
                           cursor='hand2', command=self.open_openengine)
        icon_btn.pack()

        tk.Label(openengine_frame, text="OpenEngine", font=('Arial', 10),
                bg='#0a0a0f', fg='white').pack()

        # Future app placeholders
        # Browser icon (placeholder)
        browser_frame = tk.Frame(icons_frame, bg='#0a0a0f')
        browser_frame.place(x=150, y=50)

        browser_btn = tk.Button(browser_frame, text="🌐", font=('Arial', 32),
                              bg='#0a0a0f', fg='#666666', bd=0,
                              state='disabled')
        browser_btn.pack()

        tk.Label(browser_frame, text="Browser\n(Coming Soon)", font=('Arial', 8),
                bg='#0a0a0f', fg='#666666').pack()

        # Notes icon (placeholder)
        notes_frame = tk.Frame(icons_frame, bg='#0a0a0f')
        notes_frame.place(x=250, y=50)

        notes_btn = tk.Button(notes_frame, text="📝", font=('Arial', 32),
                            bg='#0a0a0f', fg='#666666', bd=0,
                            state='disabled')
        notes_btn.pack()

        tk.Label(notes_frame, text="Notes\n(Coming Soon)", font=('Arial', 8),
                bg='#0a0a0f', fg='#666666').pack()

        # Topics Unlock icon
        topics_frame = tk.Frame(icons_frame, bg='#0a0a0f')
        topics_frame.place(x=50, y=150)

        topics_btn = tk.Button(topics_frame, text="📚", font=('Arial', 32),
                              bg='#0a0a0f', fg='#ffaa00', bd=0,
                              cursor='hand2', command=self.open_topics_unlocks)
        topics_btn.pack()

        tk.Label(topics_frame, text="Topics", font=('Arial', 10),
                bg='#0a0a0f', fg='white').pack()

        # Types Unlock icon
        types_frame = tk.Frame(icons_frame, bg='#0a0a0f')
        types_frame.place(x=150, y=150)

        types_btn = tk.Button(types_frame, text="🎮", font=('Arial', 32),
                              bg='#0a0a0f', fg='#ffaa00', bd=0,
                              cursor='hand2', command=self.open_types_unlocks)
        types_btn.pack()

        tk.Label(types_frame, text="Types", font=('Arial', 10),
                bg='#0a0a0f', fg='white').pack()

        # Status bar
        status_frame = tk.Frame(self.desktop_frame, bg='#1a1a2e', height=25)
        status_frame.pack(side='bottom', fill='x')
        status_frame.pack_propagate(False)

        tk.Label(status_frame, text="Ready", font=('Courier', 9),
                bg='#1a1a2e', fg='#00ff00').pack(side='left', padx=10)

        # Time display
        time_data = self.game_data.data.get('time', {})
        year = time_data.get('year', 1978)
        month = time_data.get('month', 1)
        day = time_data.get('day', 1)

        tk.Label(status_frame, text=f"{year}/{month:02d}/{day:02d}", font=('Courier', 9),
                bg='#1a1a2e', fg='#00ff00').pack(side='right', padx=10)

    def open_openengine(self):
        """Open the OpenEngine game development application"""
        # Open the new game engine window with list-based selection
        GameEngineWindow(self.desktop_window, self.game_data)
        return

        # Old code below (not used anymore)
        if self.openengine_active:
            return

        self.openengine_active = True

        # Clear desktop
        for widget in self.desktop_frame.winfo_children():
            widget.destroy()

        # OpenEngine window
        app_frame = tk.Frame(self.desktop_frame, bg='#1a1a2e')
        app_frame.pack(fill='both', expand=True)

        # Title bar
        titlebar = tk.Frame(app_frame, bg='#2b2b3c', height=30)
        titlebar.pack(fill='x')
        titlebar.pack_propagate(False)

        tk.Label(titlebar, text="OpenEngine - Game Development Suite",
                font=('Courier', 11, 'bold'), bg='#2b2b3c', fg='#4a9eff').pack(side='left', padx=10, pady=5)

        # Minimize button (returns to desktop)
        min_btn = tk.Button(titlebar, text="_", command=self.minimize_openengine,
                          bg='#444455', fg='white', font=('Arial', 10, 'bold'),
                          padx=10, cursor='hand2')
        min_btn.pack(side='right', padx=2, pady=2)

        # Main content area
        content_frame = tk.Frame(app_frame, bg='#0f0f1e')
        content_frame.pack(fill='both', expand=True, padx=5, pady=5)

        # Create the layout as specified
        # Top row: Topic and Game Type
        top_frame = tk.Frame(content_frame, bg='#0f0f1e')
        top_frame.pack(fill='x', padx=10, pady=10)

        # Topic button
        topic_frame = tk.Frame(top_frame, bg='#2a2a3e', relief='ridge', bd=2)
        topic_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))

        topic_btn = tk.Button(topic_frame, text="📚 TOPIC", font=('Arial', 14, 'bold'),
                            bg='#3a3a4e', fg='white', height=3,
                            cursor='hand2', command=self.select_topic)
        topic_btn.pack(fill='both', expand=True, padx=2, pady=2)

        tk.Label(topic_frame, text="Select Game Topic", font=('Arial', 9),
                bg='#2a2a3e', fg='#888888').pack()

        # Game Type button
        game_frame = tk.Frame(top_frame, bg='#2a2a3e', relief='ridge', bd=2)
        game_frame.pack(side='left', fill='both', expand=True, padx=(5, 0))

        game_btn = tk.Button(game_frame, text="🎮 GAME TYPE", font=('Arial', 14, 'bold'),
                           bg='#3a3a4e', fg='white', height=3,
                           cursor='hand2', command=self.select_game_type)
        game_btn.pack(fill='both', expand=True, padx=2, pady=2)

        tk.Label(game_frame, text="Choose Game Genre", font=('Arial', 9),
                bg='#2a2a3e', fg='#888888').pack()

        # Bottom row: IDE and empty space for future buttons
        bottom_frame = tk.Frame(content_frame, bg='#0f0f1e')
        bottom_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # IDE button (left half)
        ide_frame = tk.Frame(bottom_frame, bg='#2a2a3e', relief='ridge', bd=2)
        ide_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))

        ide_btn = tk.Button(ide_frame, text="💻 IDE", font=('Arial', 14, 'bold'),
                          bg='#3a3a4e', fg='white', height=3,
                          cursor='hand2', command=self.open_ide)
        ide_btn.pack(fill='both', expand=True, padx=2, pady=2)

        tk.Label(ide_frame, text="Development Environment", font=('Arial', 9),
                bg='#2a2a3e', fg='#888888').pack()

        # Empty space for future buttons (right half)
        future_frame = tk.Frame(bottom_frame, bg='#1a1a2e', relief='ridge', bd=1)
        future_frame.pack(side='left', fill='both', expand=True, padx=(5, 0))

        tk.Label(future_frame, text="More Options\nComing Soon", font=('Arial', 11),
                bg='#1a1a2e', fg='#555555').pack(expand=True)

        # Additional space for future expansion
        expand_frame = tk.Frame(content_frame, bg='#0f0f1e', height=100)
        expand_frame.pack(fill='x', padx=10, pady=10)
        expand_frame.pack_propagate(False)

        tk.Label(expand_frame, text="[ Space Reserved for Future Features ]", font=('Courier', 10),
                bg='#0f0f1e', fg='#444444').pack(expand=True)

        # Status bar
        status_frame = tk.Frame(app_frame, bg='#1a1a2e', height=25)
        status_frame.pack(side='bottom', fill='x')
        status_frame.pack_propagate(False)

        tk.Label(status_frame, text="OpenEngine Ready", font=('Courier', 9),
                bg='#1a1a2e', fg='#00ff00').pack(side='left', padx=10)

    def minimize_openengine(self):
        """Minimize OpenEngine back to desktop"""
        self.openengine_active = False
        self.show_desktop_icons()

    def select_topic(self):
        """Open topic selection dialog"""
        # Check for new unlocks
        new_unlocks = self.unlock_system.check_special_requirements()
        for unlock_type, name, reason in new_unlocks:
            if unlock_type == 'topic':
                messagebox.showinfo("New Topic Unlocked!", f"Unlocked: {name}\nReason: {reason}")

        # Get all unlocked topics
        topics = self.unlock_system.get_all_unlocked_topics()

        dialog = tk.Toplevel(self.desktop_window)
        dialog.title("Select Game Topic")
        dialog.geometry("400x500")
        dialog.transient(self.desktop_window)
        dialog.grab_set()

        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - 200
        y = (dialog.winfo_screenheight() // 2) - 250
        dialog.geometry(f"400x500+{x}+{y}")

        tk.Label(dialog, text="Choose a Topic", font=('Arial', 14, 'bold')).pack(pady=10)

        # Topic list
        listbox = tk.Listbox(dialog, font=('Arial', 12), height=15)
        listbox.pack(fill='both', expand=True, padx=20, pady=10)

        for topic in topics:
            listbox.insert(tk.END, topic)

        def select():
            if listbox.curselection():
                selected = listbox.get(listbox.curselection())
                self.game_data.data['current_project'] = {'topic': selected}
                messagebox.showinfo("Topic Selected", f"Selected topic: {selected}")
                dialog.destroy()

        tk.Button(dialog, text="Select", command=select,
                 bg='#4a9eff', fg='white', font=('Arial', 12, 'bold'),
                 padx=20, pady=5).pack(pady=10)

    def select_game_type(self):
        """Open game type selection dialog"""
        # Check for new unlocks
        new_unlocks = self.unlock_system.check_special_requirements()
        for unlock_type, name, reason in new_unlocks:
            if unlock_type == 'game_type':
                messagebox.showinfo("New Game Type Unlocked!", f"Unlocked: {name}\nReason: {reason}")

        # Get all unlocked game types
        unlocked = self.unlock_system.get_all_unlocked_game_types()

        # All possible game types for display
        all_game_types = [
            "Text Adventure", "Arcade", "Platformer", "Puzzle", "Shooter",
            "Beat em Up", "RPG", "Racing", "Fighting", "Action-Adventure",
            "FPS", "TPS", "Sports", "Simulation", "Survival",
            "Strategy", "MMORPG", "Rhythm", "Visual Novel", "Horror",
            "Sandbox", "Open World", "Battle Royale", "MOBA", "Idle",
            "Office", "Retro", "Educational"
        ]

        dialog = tk.Toplevel(self.desktop_window)
        dialog.title("Select Game Type")
        dialog.geometry("400x500")
        dialog.transient(self.desktop_window)
        dialog.grab_set()

        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - 200
        y = (dialog.winfo_screenheight() // 2) - 250
        dialog.geometry(f"400x500+{x}+{y}")

        tk.Label(dialog, text="Choose Game Type", font=('Arial', 14, 'bold')).pack(pady=10)

        # Game type list
        listbox = tk.Listbox(dialog, font=('Arial', 12), height=15)
        listbox.pack(fill='both', expand=True, padx=20, pady=10)

        for game_type in all_game_types:
            if game_type in unlocked:
                listbox.insert(tk.END, game_type)
            else:
                listbox.insert(tk.END, f"{game_type} [LOCKED]")

        def select():
            if listbox.curselection():
                selected = listbox.get(listbox.curselection())
                if "[LOCKED]" not in selected:
                    if 'current_project' not in self.game_data.data:
                        self.game_data.data['current_project'] = {}
                    self.game_data.data['current_project']['type'] = selected
                    messagebox.showinfo("Type Selected", f"Selected type: {selected}")
                    dialog.destroy()
                else:
                    messagebox.showwarning("Locked", "This game type is locked. Continue developing to unlock it!")

        tk.Button(dialog, text="Select", command=select,
                 bg='#4a9eff', fg='white', font=('Arial', 12, 'bold'),
                 padx=20, pady=5).pack(pady=10)

    def open_ide(self):
        """Open the IDE for game development"""
        messagebox.showinfo("IDE", "IDE opening... Development environment will be implemented soon!")
        # TODO: Implement full IDE interface

    def open_topics_unlocks(self):
        """Open the topics unlock page"""
        UnlockViewer(self.desktop_window, self.game_data, view_type="topics")

    def open_types_unlocks(self):
        """Open the game types unlock page"""
        UnlockViewer(self.desktop_window, self.game_data, view_type="types")

    def close_desktop(self):
        """Close the desktop and return to room"""
        self.desktop_window.destroy()
        if self.on_close:
            self.on_close()