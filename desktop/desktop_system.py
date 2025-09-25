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

        # Notes icon
        notes_frame = tk.Frame(icons_frame, bg='#0a0a0f')
        notes_frame.place(x=250, y=50)

        notes_btn = tk.Button(notes_frame, text="📝", font=('Arial', 32),
                            bg='#0a0a0f', fg='#ffcc00', bd=0,
                            cursor='hand2', command=self.open_notes)
        notes_btn.pack()

        tk.Label(notes_frame, text="Notes", font=('Arial', 10),
                bg='#0a0a0f', fg='white').pack()

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

        # Contacts icon
        contacts_frame = tk.Frame(icons_frame, bg='#0a0a0f')
        contacts_frame.place(x=250, y=150)

        contacts_btn = tk.Button(contacts_frame, text="📖", font=('Arial', 32),
                                bg='#0a0a0f', fg='#00ddff', bd=0,
                                cursor='hand2', command=self.open_contacts)
        contacts_btn.pack()

        tk.Label(contacts_frame, text="Contacts", font=('Arial', 10),
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

    def open_topics_unlocks(self):
        """Open the topics unlock page"""
        UnlockViewer(self.desktop_window, self.game_data, view_type="topics")

    def open_types_unlocks(self):
        """Open the game types unlock page"""
        UnlockViewer(self.desktop_window, self.game_data, view_type="types")

    def open_notes(self):
        """Open the notes app"""
        from desktop.notes_app import NotesApp
        NotesApp(self.desktop_window, self.game_data)

    def open_contacts(self):
        """Open the contacts viewer"""
        # For now, show a placeholder message
        import tkinter.messagebox as messagebox
        messagebox.showinfo("Contacts", "Contacts viewer coming soon!\n\nThis will show all NPCs you've met and those you haven't.")

    def close_desktop(self):
        """Close the desktop and return to room"""
        self.desktop_window.destroy()
        if self.on_close:
            self.on_close()