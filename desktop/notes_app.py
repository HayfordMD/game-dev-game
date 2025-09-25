"""
Notes App for saving game ideas and names
"""

import tkinter as tk
from tkinter import ttk, messagebox


class NotesApp:
    """Simple notes application for saving game names and ideas"""

    def __init__(self, parent, game_data):
        self.parent = parent
        self.game_data = game_data

        # Create notes window
        self.notes_window = tk.Toplevel(parent)
        self.notes_window.title("Notes")
        self.notes_window.geometry("800x600")
        self.notes_window.configure(bg='#2b2b3c')

        # Make it modal
        self.notes_window.transient(parent)
        self.notes_window.grab_set()

        # Center the window
        self.notes_window.update_idletasks()
        x = (self.notes_window.winfo_screenwidth() // 2) - 400
        y = (self.notes_window.winfo_screenheight() // 2) - 300
        self.notes_window.geometry(f"800x600+{x}+{y}")

        # Initialize saved names list if not exists
        if 'saved_game_names' not in self.game_data.data:
            self.game_data.data['saved_game_names'] = []

        self.setup_ui()

    def setup_ui(self):
        """Setup the notes interface"""
        # Title bar
        title_frame = tk.Frame(self.notes_window, bg='#1e1e2e', height=40)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)

        tk.Label(title_frame, text="Notes", font=('Arial', 14, 'bold'),
                bg='#1e1e2e', fg='#00ff00').pack(side='left', padx=15, pady=8)

        # Close button
        close_btn = tk.Button(title_frame, text="X", command=self.notes_window.destroy,
                            bg='#ff4444', fg='white', font=('Arial', 10, 'bold'),
                            padx=10, cursor='hand2')
        close_btn.pack(side='right', padx=5, pady=5)

        # Create notebook for tabs
        notebook = ttk.Notebook(self.notes_window)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Style the notebook
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background='#2b2b3c', borderwidth=0)
        style.configure('TNotebook.Tab', background='#3c3c4c', foreground='white',
                       padding=[20, 10], font=('Arial', 10))
        style.map('TNotebook.Tab', background=[('selected', '#4a4a5a')])

        # Saved Names tab
        saved_names_frame = tk.Frame(notebook, bg='#1e1e2e')
        notebook.add(saved_names_frame, text='Saved Game Names')
        self.setup_saved_names_tab(saved_names_frame)

        # General Notes tab
        general_notes_frame = tk.Frame(notebook, bg='#1e1e2e')
        notebook.add(general_notes_frame, text='General Notes')
        self.setup_general_notes_tab(general_notes_frame)

    def setup_saved_names_tab(self, parent_frame):
        """Setup the saved game names tab"""
        # Header
        header_frame = tk.Frame(parent_frame, bg='#1e1e2e')
        header_frame.pack(fill='x', padx=20, pady=(20, 10))

        tk.Label(header_frame, text="Saved Game Names", font=('Arial', 12, 'bold'),
                bg='#1e1e2e', fg='#00ff00').pack(side='left')

        # Count label
        count = len(self.game_data.data.get('saved_game_names', []))
        self.count_label = tk.Label(header_frame, text=f"({count} names saved)",
                                   font=('Arial', 10), bg='#1e1e2e', fg='#888888')
        self.count_label.pack(side='left', padx=10)

        # Clear all button
        if count > 0:
            clear_btn = tk.Button(header_frame, text="Clear All", command=self.clear_all_names,
                                bg='#ff4444', fg='white', font=('Arial', 9),
                                padx=10, pady=3, cursor='hand2')
            clear_btn.pack(side='right')

        # Listbox frame
        list_frame = tk.Frame(parent_frame, bg='#1e1e2e')
        list_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')

        # Listbox for saved names
        self.names_listbox = tk.Listbox(list_frame, bg='#0a0a0f', fg='white',
                                       font=('Courier', 11), selectmode='single',
                                       yscrollcommand=scrollbar.set,
                                       selectbackground='#4a4a5a',
                                       selectforeground='#00ff00')
        self.names_listbox.pack(fill='both', expand=True)
        scrollbar.config(command=self.names_listbox.yview)

        # Load saved names
        saved_names = self.game_data.data.get('saved_game_names', [])
        for i, name in enumerate(saved_names, 1):
            self.names_listbox.insert('end', f"{i:3d}. {name}")

        # Buttons frame
        if count > 0:
            buttons_frame = tk.Frame(parent_frame, bg='#1e1e2e')
            buttons_frame.pack(fill='x', padx=20, pady=(0, 20))

            # Copy selected button
            copy_btn = tk.Button(buttons_frame, text="Copy Selected", command=self.copy_selected,
                               bg='#4a9eff', fg='white', font=('Arial', 10),
                               padx=15, pady=5, cursor='hand2')
            copy_btn.pack(side='left', padx=5)

            # Delete selected button
            delete_btn = tk.Button(buttons_frame, text="Delete Selected", command=self.delete_selected,
                                 bg='#ff6644', fg='white', font=('Arial', 10),
                                 padx=15, pady=5, cursor='hand2')
            delete_btn.pack(side='left', padx=5)

        # Empty state message
        if count == 0:
            empty_label = tk.Label(parent_frame,
                                 text="No saved game names yet.\n\nUse the 'Save name for later' button\nin the game engine to save names here.",
                                 font=('Arial', 11), bg='#1e1e2e', fg='#666666',
                                 justify='center')
            empty_label.pack(expand=True)

    def setup_general_notes_tab(self, parent_frame):
        """Setup the general notes tab"""
        # Header
        header_frame = tk.Frame(parent_frame, bg='#1e1e2e')
        header_frame.pack(fill='x', padx=20, pady=(20, 10))

        tk.Label(header_frame, text="General Notes", font=('Arial', 12, 'bold'),
                bg='#1e1e2e', fg='#00ff00').pack(side='left')

        # Text widget frame
        text_frame = tk.Frame(parent_frame, bg='#1e1e2e')
        text_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        # Scrollbar
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side='right', fill='y')

        # Text widget for general notes
        self.notes_text = tk.Text(text_frame, bg='#0a0a0f', fg='white',
                                font=('Courier', 11), wrap='word',
                                yscrollcommand=scrollbar.set,
                                insertbackground='#00ff00')
        self.notes_text.pack(fill='both', expand=True)
        scrollbar.config(command=self.notes_text.yview)

        # Load existing notes if any
        if 'general_notes' in self.game_data.data:
            self.notes_text.insert('1.0', self.game_data.data['general_notes'])

        # Save button
        save_btn = tk.Button(parent_frame, text="Save Notes", command=self.save_general_notes,
                           bg='#00aa00', fg='white', font=('Arial', 10, 'bold'),
                           padx=20, pady=5, cursor='hand2')
        save_btn.pack(pady=(0, 20))

    def copy_selected(self):
        """Copy selected name to clipboard"""
        selection = self.names_listbox.curselection()
        if selection:
            name = self.names_listbox.get(selection[0])
            # Remove the number prefix
            name = name.split('. ', 1)[1] if '. ' in name else name

            # Copy to clipboard
            self.notes_window.clipboard_clear()
            self.notes_window.clipboard_append(name)

            messagebox.showinfo("Copied", f"'{name}' copied to clipboard!")

    def delete_selected(self):
        """Delete selected name"""
        selection = self.names_listbox.curselection()
        if selection:
            index = selection[0]
            name = self.names_listbox.get(index)
            # Remove the number prefix
            name = name.split('. ', 1)[1] if '. ' in name else name

            # Confirm deletion
            if messagebox.askyesno("Delete", f"Delete '{name}'?"):
                # Remove from data
                self.game_data.data['saved_game_names'].remove(name)
                self.game_data.save_game()

                # Update UI
                self.names_listbox.delete(index)

                # Update count
                count = len(self.game_data.data['saved_game_names'])
                self.count_label.config(text=f"({count} names saved)")

                # Renumber remaining items
                for i in range(self.names_listbox.size()):
                    old_text = self.names_listbox.get(i)
                    name_part = old_text.split('. ', 1)[1] if '. ' in old_text else old_text
                    self.names_listbox.delete(i)
                    self.names_listbox.insert(i, f"{i+1:3d}. {name_part}")

    def clear_all_names(self):
        """Clear all saved names"""
        if messagebox.askyesno("Clear All", "Delete all saved game names?"):
            self.game_data.data['saved_game_names'] = []
            self.game_data.save_game()

            # Clear listbox
            self.names_listbox.delete(0, 'end')

            # Update count
            self.count_label.config(text="(0 names saved)")

    def save_general_notes(self):
        """Save general notes to game data"""
        notes_content = self.notes_text.get('1.0', 'end-1c')
        self.game_data.data['general_notes'] = notes_content
        self.game_data.save_game()

        messagebox.showinfo("Saved", "Notes saved successfully!")