import tkinter as tk
from tkinter import ttk

class DesktopToolStrongside:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Desktop Tool Strongside")
        self.root.geometry("1920x1080")
        self.root.resizable(False, False)

        self.video_expanded = False

        # Main container
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Top section - Video and 2D Draw areas (80% of height)
        self.top_frame = tk.Frame(main_frame, bg="#ffffff", relief=tk.RAISED, bd=2, height=864)  # 80% of 1080
        self.top_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.top_frame.pack_propagate(False)

        # Video section (left side of top)
        self.video_frame = tk.Frame(self.top_frame, bg="#2c3e50", relief=tk.SUNKEN, bd=3)
        self.video_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        video_header = tk.Frame(self.video_frame, bg="#2c3e50")
        video_header.pack(fill=tk.X, pady=10)

        video_label = tk.Label(video_header, text="VIDEO", fg="#ecf0f1", bg="#2c3e50",
                              font=("Arial", 24, "bold"))
        video_label.pack(side=tk.LEFT, padx=20)

        # Expand/Collapse button
        self.expand_btn = tk.Button(video_header, text="⛶ Expand", bg="#3498db", fg="white",
                                   font=("Arial", 12, "bold"), padx=15, pady=5,
                                   command=self.toggle_video_expand)
        self.expand_btn.pack(side=tk.RIGHT, padx=20)

        video_content = tk.Label(self.video_frame, text="Video playback area\n\n[Video controls would go here]\n\nPlay | Pause | Stop",
                                fg="#bdc3c7", bg="#2c3e50", font=("Arial", 12))
        video_content.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # 2D Draw section (right side of top)
        self.draw_frame = tk.Frame(self.top_frame, bg="#ecf0f1", relief=tk.SUNKEN, bd=3)
        self.draw_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        draw_label = tk.Label(self.draw_frame, text="2D DRAW", fg="#2c3e50", bg="#ecf0f1",
                             font=("Arial", 24, "bold"))
        draw_label.pack(pady=20)

        # Canvas for drawing
        self.canvas = tk.Canvas(self.draw_frame, bg="white", highlightthickness=1, highlightbackground="#34495e")
        self.canvas.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Draw some example shapes
        self.canvas.create_rectangle(50, 50, 200, 150, outline="#3498db", width=2)
        self.canvas.create_oval(250, 50, 400, 150, outline="#e74c3c", width=2)
        self.canvas.create_line(50, 200, 400, 200, fill="#2ecc71", width=3)
        self.canvas.create_text(225, 250, text="Drawing Canvas", font=("Arial", 16), fill="#34495e")

        # Bottom section - Text Form (20% of height)
        bottom_frame = tk.Frame(main_frame, bg="#ffffff", relief=tk.RAISED, bd=2, height=216)  # 20% of 1080
        bottom_frame.pack(fill=tk.BOTH, padx=10, pady=(0, 10))
        bottom_frame.pack_propagate(False)

        form_label = tk.Label(bottom_frame, text="TEXT FORM EXAMPLE", fg="#2c3e50", bg="#ffffff",
                             font=("Arial", 18, "bold"))
        form_label.pack(pady=5)

        # Form container
        form_container = tk.Frame(bottom_frame, bg="#ffffff")
        form_container.pack(expand=False, padx=50, pady=5)

        # Form fields - reduced to fit in 20% height
        fields = [
            ("Name:", "Enter your name"),
            ("Project:", "Enter project name"),
        ]

        self.entries = {}
        for i, (label_text, placeholder) in enumerate(fields):
            # Label
            label = tk.Label(form_container, text=label_text, bg="#ffffff", font=("Arial", 12))
            label.grid(row=0, column=i*2, sticky="e", padx=(0, 5), pady=5)

            # Entry
            entry = tk.Entry(form_container, width=30, font=("Arial", 11))
            entry.insert(0, placeholder)
            entry.bind("<FocusIn>", lambda e, ent=entry, ph=placeholder:
                      ent.delete(0, tk.END) if ent.get() == ph else None)

            entry.grid(row=0, column=i*2+1, padx=(0, 20), pady=5)
            self.entries[label_text] = entry

        # Submit button
        submit_btn = tk.Button(form_container, text="Submit", bg="#3498db", fg="white",
                              font=("Arial", 12, "bold"), padx=20, pady=5,
                              command=self.submit_form)
        submit_btn.grid(row=0, column=4, pady=5)

        # Status bar
        status_bar = tk.Label(self.root, text="Ready", bg="#34495e", fg="#ecf0f1",
                             font=("Arial", 10), anchor="w", padx=10)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def toggle_video_expand(self):
        if self.video_expanded:
            # Collapse video back to normal
            self.draw_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
            self.expand_btn.config(text="⛶ Expand")
            self.video_expanded = False
        else:
            # Expand video to full width
            self.draw_frame.pack_forget()
            self.expand_btn.config(text="◱ Collapse")
            self.video_expanded = True

    def submit_form(self):
        print("Form submitted!")
        for label, entry in self.entries.items():
            value = entry.get()
            print(f"{label} {value}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = DesktopToolStrongside()
    app.run()