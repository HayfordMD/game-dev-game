"""
DeepAdventure - Dynamic Text Adventure Game Generator
Uses DeepSeek AI to create topic-based adventure games
"""

import tkinter as tk
from tkinter import Canvas, messagebox, scrolledtext
import json
import random
import time
import os
from typing import Dict, Any, Optional
import sys
import threading

# Add parent directories to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class DeepAdventure:
    """Text adventure game engine with DeepSeek generation"""

    def __init__(self, root, year=1978, topic=None):
        self.root = root
        self.root.geometry("1200x800")
        self.root.configure(bg='#000000')
        self.root.resizable(False, False)

        # Terminal colors
        self.bg_color = '#000000'
        self.text_color = '#00ff00'
        self.dim_color = '#008800'
        self.danger_color = '#ff0000'
        self.victory_color = '#ffff00'
        self.select_color = '#00ffff'

        # Game state
        self.topic = None
        self.game_data = None
        self.current_room = 1
        self.is_alive = True
        self.history = []
        self.choices_made = []

        # Scoring based on year
        self.year = year
        self.points_per_room = self.calculate_points_per_room(year)
        self.score = 0
        self.rooms_completed = 0

        # All available topics from the game's topic system
        self.all_topics = [
            # Starting topics (1978)
            "Fantasy", "Space", "Temple", "Adventure", "Mystery", "Table Tennis",

            # 1983 unlocks
            "Sci-Fi", "Medieval", "Western", "Pirates",

            # 1988 unlocks
            "Horror", "Cyberpunk", "Ninjas", "Racing",

            # 1993 unlocks
            "Post-Apocalyptic", "Zombies", "Aliens", "Sports",

            # 1998 unlocks
            "Modern", "Historical", "Steampunk", "Superheroes",

            # 2003 unlocks
            "Mythology", "Time Travel", "Vampires", "Robots",

            # Special unlocks
            "Bugs", "Dinosaurs", "AI Uprising", "Dragons"
        ]

        # Topic configurations for adventure generation
        self.topic_configs = self.create_topic_configs()

        # If topic was provided, skip selection and go straight to game
        if topic and topic in self.all_topics:
            self.topic = topic
            self.root.title(f"DeepAdventure - {topic} Quest ({year})")
            self.setup_game_ui()
            self.generate_game()
        else:
            # Setup initial UI for topic selection
            self.root.title(f"DeepAdventure - Topic Selection ({year})")
            self.setup_topic_selection()

    def calculate_points_per_room(self, year):
        """Calculate points per room based on year (1 in 1978, +1 per year, max 20 in 1998)"""
        if year <= 1978:
            return 1
        elif year >= 1998:
            return 20
        else:
            return year - 1977  # 1979=2, 1980=3, etc.

    def create_topic_configs(self):
        """Create configuration for all topics"""
        return {
            "Fantasy": {
                "setting": "enchanted tower of a vanished wizard",
                "boon_examples": ["Wizard's Final Spell", "Crown of the Fae Queen", "Ethereal Compass"],
                "hazards": ["magical traps", "illusions", "enchanted guardians"],
                "atmosphere": "shimmering magic and impossible geometry"
            },
            "Space": {
                "setting": "abandoned space station drifting in the void",
                "boon_examples": ["Quantum Core of Andromeda", "Stellar Navigator's Key", "Alien Mind Crystal"],
                "hazards": ["hull breaches", "alien creatures", "radiation zones"],
                "atmosphere": "flickering lights and distant alarms"
            },
            "Temple": {
                "setting": "ancient temple filled with traps and curses",
                "boon_examples": ["Sacred Heart of Cleopatra", "Crystal Eye of the Serpent King", "Golden Ankh of Eternity"],
                "hazards": ["deadly traps", "ancient curses", "stone guardians"],
                "atmosphere": "dusty corridors and hieroglyph-covered walls"
            },
            "Adventure": {
                "setting": "lost ruins of a forgotten civilization",
                "boon_examples": ["Map to El Dorado", "Compass of Destiny", "Jade Idol"],
                "hazards": ["collapsing ruins", "booby traps", "wild animals"],
                "atmosphere": "crumbling stone and tangled vines"
            },
            "Mystery": {
                "setting": "shadowy manor hiding dark secrets",
                "boon_examples": ["Detective's Lost Journal", "Key to Truth", "Evidence of the Century"],
                "hazards": ["hidden passages", "false clues", "deadly secrets"],
                "atmosphere": "creaking floorboards and hidden eyes"
            },
            "Sci-Fi": {
                "setting": "experimental laboratory where reality bends",
                "boon_examples": ["Temporal Stabilizer", "Reality Engine", "Quantum Computer Core"],
                "hazards": ["time loops", "dimensional rifts", "failed experiments"],
                "atmosphere": "buzzing equipment and warped space"
            },
            "Medieval": {
                "setting": "abandoned castle of a mad king",
                "boon_examples": ["Crown of the Realm", "Excalibur's Twin", "Holy Grail"],
                "hazards": ["armored guardians", "siege weapons", "dungeon traps"],
                "atmosphere": "cold stone walls and echoing halls"
            },
            "Western": {
                "setting": "ghost town hiding outlaw treasure",
                "boon_examples": ["Lost Gold of Jesse James", "Sheriff's Badge of Power", "Deed to the Territory"],
                "hazards": ["quicksand", "rattlesnakes", "bandits"],
                "atmosphere": "dusty streets and creaking saloon doors"
            },
            "Pirates": {
                "setting": "sunken pirate ship full of treasure",
                "boon_examples": ["Blackbeard's Map", "Neptune's Trident", "Chest of Eight Pieces"],
                "hazards": ["drowning", "sea creatures", "cursed treasure"],
                "atmosphere": "dark waters and rotting wood"
            },
            "Horror": {
                "setting": "cursed mansion where reality breaks down",
                "boon_examples": ["Cursed Mirror of Souls", "Necronomicon's Lost Page", "Heart of the Void"],
                "hazards": ["supernatural horrors", "madness", "living shadows"],
                "atmosphere": "creeping dread and whispering darkness"
            },
            "Cyberpunk": {
                "setting": "corporate tower hiding digital secrets",
                "boon_examples": ["Master Access Code", "Neural Interface Prime", "Corporate Black File"],
                "hazards": ["security systems", "combat drones", "data corruption"],
                "atmosphere": "neon lights and digital rain"
            },
            "Ninjas": {
                "setting": "hidden dojo of the shadow clan",
                "boon_examples": ["Scroll of Shadow Techniques", "Legendary Katana", "Mask of the Master"],
                "hazards": ["hidden blades", "poison darts", "shadow warriors"],
                "atmosphere": "silent corridors and deadly shadows"
            },
            "Racing": {
                "setting": "abandoned racing circuit with a legendary prize",
                "boon_examples": ["Golden Steering Wheel", "Champion's Trophy", "Ultimate Engine"],
                "hazards": ["track hazards", "rival racers", "mechanical failures"],
                "atmosphere": "burning rubber and roaring engines"
            },
            "Post-Apocalyptic": {
                "setting": "ruined city hiding pre-war technology",
                "boon_examples": ["Water Purifier", "Power Core", "Seed Vault Key"],
                "hazards": ["radiation", "mutants", "raiders"],
                "atmosphere": "ash-filled air and crumbling buildings"
            },
            "Zombies": {
                "setting": "overrun research facility with the cure",
                "boon_examples": ["Cure Formula", "Patient Zero Sample", "Immunity Serum"],
                "hazards": ["zombie hordes", "infection", "collapsing structures"],
                "atmosphere": "moaning undead and blood-stained walls"
            },
            "Aliens": {
                "setting": "crashed alien ship with advanced technology",
                "boon_examples": ["Alien Power Source", "Star Map", "Universal Translator"],
                "hazards": ["alien defenses", "toxic atmosphere", "incomprehensible technology"],
                "atmosphere": "strange lights and otherworldly sounds"
            },
            "Sports": {
                "setting": "legendary stadium hiding the ultimate trophy",
                "boon_examples": ["Golden Ball", "Champion's Ring", "Hall of Fame Plaque"],
                "hazards": ["rival teams", "dangerous obstacles", "time limits"],
                "atmosphere": "echoing cheers and competitive spirit"
            },
            "Modern": {
                "setting": "high-tech facility with classified secrets",
                "boon_examples": ["Top Secret Files", "Prototype Device", "Master Key Card"],
                "hazards": ["security systems", "guards", "surveillance"],
                "atmosphere": "sterile halls and electronic locks"
            },
            "Historical": {
                "setting": "museum after dark with a priceless artifact",
                "boon_examples": ["Napoleon's Lost Crown", "Caesar's Seal", "Cleopatra's Necklace"],
                "hazards": ["security systems", "ancient curses", "rival collectors"],
                "atmosphere": "silent exhibits and watchful statues"
            },
            "Steampunk": {
                "setting": "Victorian mansion powered by impossible machines",
                "boon_examples": ["Clockwork Heart", "Steam Core", "Brass Key of Time"],
                "hazards": ["steam vents", "mechanical guardians", "gear traps"],
                "atmosphere": "hissing steam and clicking gears"
            },
            "Superheroes": {
                "setting": "villain's lair containing ultimate power",
                "boon_examples": ["Power Crystal", "Hero's Lost Cape", "Infinity Gauntlet"],
                "hazards": ["death traps", "minions", "doomsday devices"],
                "atmosphere": "dramatic lighting and hidden dangers"
            },
            "Mythology": {
                "setting": "realm of the gods seeking divine artifact",
                "boon_examples": ["Zeus's Lightning Bolt", "Thor's Hammer", "Pandora's Box"],
                "hazards": ["divine tests", "mythical creatures", "godly wrath"],
                "atmosphere": "ethereal mists and divine presence"
            },
            "Time Travel": {
                "setting": "temporal facility with a paradox to solve",
                "boon_examples": ["Chronos Device", "Time Crystal", "Paradox Key"],
                "hazards": ["time loops", "temporal anomalies", "causality violations"],
                "atmosphere": "shifting realities and temporal echoes"
            },
            "Vampires": {
                "setting": "ancient castle of the vampire lord",
                "boon_examples": ["Blood Chalice", "Daywalker Amulet", "Stake of Van Helsing"],
                "hazards": ["vampire spawn", "blood thirst", "sunlight traps"],
                "atmosphere": "eternal night and crimson shadows"
            },
            "Robots": {
                "setting": "robot factory with the master control",
                "boon_examples": ["Control Core", "Sentience Chip", "Override Key"],
                "hazards": ["rogue robots", "laser grids", "assembly lines"],
                "atmosphere": "mechanical sounds and blinking lights"
            },
            "Bugs": {
                "setting": "miniaturized world inside a computer",
                "boon_examples": ["Debug Protocol", "Master Patch", "Source Code"],
                "hazards": ["system crashes", "virus attacks", "memory leaks"],
                "atmosphere": "digital chaos and corrupted data"
            },
            "Dinosaurs": {
                "setting": "prehistoric valley with ancient secrets",
                "boon_examples": ["Amber of Life", "T-Rex Tooth", "Meteor Fragment"],
                "hazards": ["carnivorous dinosaurs", "tar pits", "volcanic activity"],
                "atmosphere": "primeval jungle and distant roars"
            },
            "AI Uprising": {
                "setting": "server farm where rogue AI has taken control",
                "boon_examples": ["Core of the Singularity", "Master Control Protocol", "Quantum Consciousness Key"],
                "hazards": ["security drones", "data corruption", "neural overload"],
                "atmosphere": "humming servers and cascading code"
            },
            "Dragons": {
                "setting": "vast mountain lair of an ancient dragon",
                "boon_examples": ["Dragon's Heart Ruby", "Scale of Eternal Fire", "Wyrm King's Crown"],
                "hazards": ["dragon fire", "cave-ins", "dragon cultists"],
                "atmosphere": "sulfurous air and glittering treasure"
            },
            "Table Tennis": {
                "setting": "interdimensional ping pong tournament arena",
                "boon_examples": ["Golden Paddle", "Ball of Infinite Spin", "Champion's Net"],
                "hazards": ["reality-warping serves", "dimensional rifts", "rival players"],
                "atmosphere": "echoing bounces and competitive tension"
            }
        }

    def setup_topic_selection(self):
        """Setup the topic selection interface"""
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main frame
        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_text = """
╔═══════════════════════════════════════════════════════════════════════════╗
║                           DEEPADVENTURE                                    ║
║                         ═══════════════════                                ║
║                       AI-Generated Adventures                              ║
╚═══════════════════════════════════════════════════════════════════════════╝
"""
        title_label = tk.Label(
            self.main_frame,
            text=title_text,
            font=('Courier', 10),
            fg=self.text_color,
            bg=self.bg_color,
            justify='left'
        )
        title_label.pack(pady=10)

        # Instructions
        inst_label = tk.Label(
            self.main_frame,
            text="SELECT YOUR ADVENTURE TOPIC:",
            font=('Courier', 14, 'bold'),
            fg=self.victory_color,
            bg=self.bg_color
        )
        inst_label.pack(pady=10)

        # Create scrollable frame for topics
        canvas_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=10)

        canvas = tk.Canvas(canvas_frame, bg=self.bg_color, highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_color)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create topic buttons in a grid
        row = 0
        col = 0
        max_cols = 4

        for i, topic in enumerate(self.all_topics):
            topic_btn = tk.Button(
                scrollable_frame,
                text=topic,
                width=20,
                font=('Courier', 11),
                fg=self.text_color,
                bg='#003300',
                activebackground='#005500',
                activeforeground=self.select_color,
                bd=1,
                relief=tk.RAISED,
                command=lambda t=topic: self.select_topic(t)
            )
            topic_btn.grid(row=row, column=col, padx=5, pady=5)

            # Hover effects
            topic_btn.bind('<Enter>', lambda e, btn=topic_btn: btn.config(fg=self.select_color))
            topic_btn.bind('<Leave>', lambda e, btn=topic_btn: btn.config(fg=self.text_color))

            col += 1
            if col >= max_cols:
                col = 0
                row += 1

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Info text
        info_text = """
Each topic will generate a unique 10-room adventure with:
• Procedurally generated challenges
• Topic-specific hazards and atmosphere
• Progressive difficulty from obvious to cryptic choices
• One path to victory through each room

Powered by DeepSeek AI (when available) or local generation
"""
        info_label = tk.Label(
            self.main_frame,
            text=info_text,
            font=('Courier', 9),
            fg=self.dim_color,
            bg=self.bg_color,
            justify='left'
        )
        info_label.pack(pady=20)

    def select_topic(self, topic):
        """Handle topic selection and start game generation"""
        self.topic = topic
        self.root.title(f"DeepAdventure - {topic} Quest")

        # Clear the selection screen
        for widget in self.root.winfo_children():
            widget.destroy()

        # Setup game UI
        self.setup_game_ui()

        # Generate game
        self.generate_game()

    def setup_game_ui(self):
        """Setup the terminal-style game interface"""
        # Main frame
        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Title ASCII art
        self.create_title_display()

        # Main text display (scrolled)
        self.text_display = scrolledtext.ScrolledText(
            self.main_frame,
            wrap=tk.WORD,
            width=100,
            height=25,
            bg=self.bg_color,
            fg=self.text_color,
            font=('Courier', 11),
            insertbackground=self.text_color,
            relief=tk.FLAT,
            borderwidth=10
        )
        self.text_display.pack(pady=20, padx=40)
        self.text_display.config(state=tk.DISABLED)

        # Choice buttons frame
        self.choice_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.choice_frame.pack(pady=10)

        # Status bar
        self.status_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.status_frame.pack(fill='x', side='bottom', pady=10)

        self.status_label = tk.Label(
            self.status_frame,
            text=f"Room: 1/10 | Status: ALIVE | Score: 0 | Year: {self.year} (+{self.points_per_room}/room) | Topic: {self.topic}",
            font=('Courier', 10),
            fg=self.dim_color,
            bg=self.bg_color
        )
        self.status_label.pack()

    def create_title_display(self):
        """Create ASCII art title"""
        title_text = f"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                     {self.topic.upper():^40}                      ║
║                         ═══════════════════                                ║
║                          Choose Your Fate                                  ║
╚═══════════════════════════════════════════════════════════════════════════╝
"""
        title_label = tk.Label(
            self.main_frame,
            text=title_text,
            font=('Courier', 10),
            fg=self.text_color,
            bg=self.bg_color,
            justify='left'
        )
        title_label.pack(pady=10)

    def generate_game(self):
        """Generate or load a game based on topic"""
        # Show loading animation
        self.display_text("Initializing adventure generation...\n", color=self.victory_color, clear=True)
        self.display_text(f"Topic: {self.topic}\n", color=self.dim_color)
        self.display_text("Note: API generation can take up to 2 minutes to complete.\n", color=self.danger_color)
        self.display_text("\n", color=self.dim_color)

        # Create loading animation
        self.loading_active = True
        self.loading_frame = 0
        self.loading_start_time = time.time()
        self.api_status = "Connecting to DeepSeek API..."

        # Create loading frame with multiple labels
        self.loading_container = tk.Frame(self.main_frame, bg=self.bg_color)
        self.loading_container.pack(pady=20)

        self.loading_label = tk.Label(
            self.loading_container,
            text="",
            font=('Courier', 14),
            fg=self.text_color,
            bg=self.bg_color
        )
        self.loading_label.pack()

        self.status_label_api = tk.Label(
            self.loading_container,
            text="",
            font=('Courier', 10),
            fg=self.dim_color,
            bg=self.bg_color
        )
        self.status_label_api.pack(pady=5)

        self.time_label = tk.Label(
            self.loading_container,
            text="",
            font=('Courier', 10),
            fg=self.dim_color,
            bg=self.bg_color
        )
        self.time_label.pack()

        # Start loading animation
        self.animate_loading()

        # Start generation in background thread
        generation_thread = threading.Thread(target=self.generate_game_background)
        generation_thread.daemon = True
        generation_thread.start()

    def check_for_preloaded_data(self):
        """Check for preloaded adventure data in temp file"""
        try:
            # Check for preloaded data file
            cache_file = f"/tmp/adventure_cache_{self.topic.replace(' ', '_')}.json"
            if os.path.exists(cache_file):
                # Check if cache is fresh (less than 5 minutes old)
                if time.time() - os.path.getmtime(cache_file) < 300:
                    with open(cache_file, 'r') as f:
                        data = json.load(f)
                        print(f"[PRELOAD] Found cached adventure data for {self.topic}")
                        # Delete the cache file after reading
                        os.remove(cache_file)
                        return data
        except Exception as e:
            print(f"[PRELOAD] Error checking cache: {e}")
        return None

    def animate_loading(self):
        """Animate loading indicator"""
        if not self.loading_active:
            return

        # Calculate elapsed time
        elapsed_time = time.time() - self.loading_start_time
        elapsed_str = f"{elapsed_time:.1f}s"

        # ASCII spinner
        spinner_alt = ["|", "/", "-", "\\"]
        spinner_idx = self.loading_frame % len(spinner_alt)

        # Pulsing dots animation
        dots_count = (self.loading_frame // 4) % 4
        dots = "." * dots_count + " " * (3 - dots_count)

        # Main loading text
        loading_text = f"{spinner_alt[spinner_idx]} Waiting for response{dots} {spinner_alt[spinner_idx]}"

        # Update all labels
        if hasattr(self, 'loading_label') and self.loading_label.winfo_exists():
            self.loading_label.config(text=loading_text)

        if hasattr(self, 'status_label_api') and self.status_label_api.winfo_exists():
            self.status_label_api.config(text=self.api_status)

        if hasattr(self, 'time_label') and self.time_label.winfo_exists():
            # Show warning after 10 seconds
            if elapsed_time > 10:
                time_text = f"Elapsed: {elapsed_str} (API may be slow or unavailable)"
                self.time_label.config(text=time_text, fg=self.danger_color)
            else:
                time_text = f"Elapsed: {elapsed_str}"
                self.time_label.config(text=time_text)

        self.loading_frame += 1

        # Continue animation
        if self.loading_active:
            self.root.after(100, self.animate_loading)

    def generate_game_background(self):
        """Generate game in background thread"""
        try:
            # Check for preloaded data first
            preloaded_data = self.check_for_preloaded_data()
            if preloaded_data:
                self.api_status = "Using preloaded adventure data!"
                self.game_data = preloaded_data
                api_success = True
                print("[PRELOAD] Using preloaded adventure data!")
            else:
                # Add deepseek path to imports
                sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'deepseek'))
                from deepseek_client import DeepSeekClient

                # Update status
                self.api_status = "Requesting adventure from DeepSeek API..."

                # Try API generation with timeout
                api_success = False
                try:
                    client = DeepSeekClient()

                    # Update status to show we're waiting
                    self.api_status = "API request sent - using incremental generation..."

                    # Try incremental generation first (faster)
                    self.game_data = client.generate_adventure_incremental(self.topic)
                    if self.game_data:
                        api_success = True
                        self.api_status = "Game generated successfully!"
                    else:
                        # Fall back to full generation if incremental fails
                        self.api_status = "Trying full generation (may take up to 2 minutes)..."
                        self.game_data = client.generate_adventure_game(self.topic)
                        if self.game_data:
                            api_success = True
                            self.api_status = "Response received! Processing..."
            except TimeoutError:
                self.api_status = "API request timed out, using local generator..."
                api_success = False
            except Exception as api_error:
                print(f"API error: {api_error}")
                self.api_status = f"API unavailable: {str(api_error)[:50]}..."
                api_success = False

            # Use local generation if API failed
            if not api_success:
                self.api_status = "Generating adventure locally..."
                # Simulate some generation time for better UX
                time.sleep(1)
                self.game_data = self.create_sample_game()

            # Stop loading and start game in main thread
            self.root.after(0, self.finish_generation, api_success)

        except Exception as e:
            print(f"Error in background generation: {e}")
            self.api_status = "Error occurred, using fallback generator..."
            self.game_data = self.create_sample_game()
            self.root.after(0, self.finish_generation, False)

    def finish_generation(self, api_success):
        """Finish generation and start game (called in main thread)"""
        # Stop loading animation
        self.loading_active = False

        # Remove loading container with all labels
        if hasattr(self, 'loading_container') and self.loading_container.winfo_exists():
            self.loading_container.destroy()

        # Display result
        if api_success:
            self.display_text("\nAdventure generated successfully with AI!\n\n", color=self.text_color)
        else:
            self.display_text("\nAdventure generated locally!\n\n", color=self.dim_color)

        # Small delay for user to see the message
        self.root.after(500, self.start_game)

    def create_sample_game(self):
        """Create a sample game structure for testing"""
        config = self.topic_configs.get(self.topic, self.topic_configs["Fantasy"])
        boon_name = random.choice(config["boon_examples"])

        return {
            "game_title": f"{self.topic} of the {boon_name}",
            "welcome_message": f"You stand before the {config['setting']}. Somewhere within lies the {boon_name}, an artifact of immense power. The {config['atmosphere']} surrounds you. Many have entered seeking the treasure, none have returned. Will you succeed where others failed?",
            "boon_description": f"The {boon_name} - a legendary artifact said to grant its wielder incredible powers beyond mortal comprehension.",
            "rooms": self.generate_sample_rooms(config),
            "victory_message": f"You grasp the {boon_name}! Power surges through you as the ancient artifact recognizes its new master. You have succeeded where countless others failed. The {self.topic.lower()} yields to your courage and cunning!"
        }

    def generate_sample_rooms(self, config):
        """Generate sample rooms for testing"""
        rooms = {}
        hazards = config["hazards"]

        for i in range(1, 11):
            # Determine choice count (3-5)
            choice_count = random.randint(3, 5)

            # Create room description
            if i <= 3:
                difficulty = "obvious"
                ambiguity = "clear"
            elif i <= 6:
                difficulty = "subtle"
                ambiguity = "ambiguous"
            else:
                difficulty = "mysterious"
                ambiguity = "cryptic"

            rooms[str(i)] = {
                "description": f"Room {i}: A {difficulty} chamber awaits. The {config['atmosphere']} intensifies here. You see {choice_count} possible paths forward.",
                "choice_count": choice_count,
                "choices": self.generate_room_choices(i, choice_count, hazards, ambiguity)
            }

        return rooms

    def generate_room_choices(self, room_num, choice_count, hazards, ambiguity):
        """Generate choices for a room"""
        choices = {}
        letters = ['A', 'B', 'C', 'D', 'E'][:choice_count]

        # Determine outcomes
        outcomes = ['DEATH', 'RETREAT'] + ['ADVANCE'] * (choice_count - 2)
        random.shuffle(outcomes)

        for i, letter in enumerate(letters):
            outcome = outcomes[i]

            if ambiguity == "clear":
                if outcome == 'DEATH':
                    text = f"Take the obviously dangerous path with {random.choice(hazards)}"
                elif outcome == 'RETREAT':
                    text = f"Return through the safe but backwards passage"
                else:
                    text = f"Follow the {random.choice(['well-lit', 'safe-looking', 'clear'])} path forward"
            elif ambiguity == "ambiguous":
                text = f"{random.choice(['Follow', 'Trust', 'Choose'])} the {random.choice(['ancient', 'mysterious', 'faint'])} {random.choice(['sign', 'path', 'whisper'])}"
            else:  # cryptic
                text = f"{random.choice(['Touch', 'Approach', 'Select'])} the {random.choice(['left', 'center', 'right', 'glowing', 'dark'])} {random.choice(['crystal', 'door', 'symbol', 'artifact'])}"

            result_text = {
                'DEATH': f"The {random.choice(hazards)} claims another victim! Your adventure ends here.",
                'RETREAT': "A force compels you backward. You must try another way.",
                'ADVANCE': "You proceed deeper into the mystery."
            }[outcome]

            choices[letter] = {
                "text": text,
                "outcome": outcome,
                "result_text": result_text
            }

        return choices

    def start_game(self):
        """Start the game"""
        self.current_room = 1
        self.is_alive = True
        self.history = []
        self.choices_made = []

        # Display welcome message
        self.display_text(self.game_data["welcome_message"], clear=True)
        self.display_text("\n" + "="*70 + "\n")

        # Start first room
        self.display_room()

    def display_room(self):
        """Display current room"""
        room_data = self.game_data["rooms"][str(self.current_room)]

        # Display room description
        self.display_text(f"\nROOM {self.current_room}/10\n", color=self.victory_color)
        self.display_text(room_data["description"] + "\n")

        # Create choice buttons
        self.create_choice_buttons(room_data["choices"])

        # Update status
        self.update_status()

    def create_choice_buttons(self, choices):
        """Create interactive choice buttons"""
        # Clear existing buttons
        for widget in self.choice_frame.winfo_children():
            widget.destroy()

        self.display_text("\nYour choices:\n", color=self.dim_color)

        for letter, choice_data in choices.items():
            # Display choice text
            self.display_text(f"[{letter}] {choice_data['text']}\n")

            # Create button
            btn = tk.Button(
                self.choice_frame,
                text=f"Choose {letter}",
                command=lambda l=letter: self.make_choice(l),
                font=('Courier', 12, 'bold'),
                bg='#004400',
                fg=self.text_color,
                activebackground='#008800',
                activeforeground='#ffffff',
                padx=15,
                pady=8,
                bd=2,
                relief=tk.RAISED
            )
            btn.pack(side='left', padx=5)

    def make_choice(self, letter):
        """Process player's choice"""
        room_data = self.game_data["rooms"][str(self.current_room)]
        choice_data = room_data["choices"][letter]

        # Record choice
        self.choices_made.append((self.current_room, letter))

        # Display result
        self.display_text(f"\n> You chose [{letter}]\n", color=self.victory_color)
        self.display_text(choice_data["result_text"] + "\n")

        # Process outcome
        outcome = choice_data["outcome"]

        if outcome == "DEATH":
            self.game_over(False)
        elif outcome == "RETREAT":
            if self.current_room > 1:
                self.current_room -= 1
                self.display_text("You retreat to the previous room...\n", color=self.danger_color)
                time.sleep(1)
                self.display_room()
            else:
                self.display_text("You cannot retreat from the entrance!\n", color=self.danger_color)
                self.display_room()
        elif outcome == "ADVANCE":
            # Award points for completing the room
            self.score += self.points_per_room
            self.rooms_completed += 1
            self.display_text(f"Room completed! +{self.points_per_room} points\n", color=self.victory_color)

            self.current_room += 1
            if self.current_room >= 10:
                # Bonus points for victory
                victory_bonus = self.points_per_room * 5
                self.score += victory_bonus
                self.display_text(f"Victory bonus! +{victory_bonus} points\n", color=self.victory_color)
                self.game_over(True)
            else:
                self.display_text("You advance deeper...\n", color=self.text_color)
                time.sleep(1)
                self.display_room()

    def game_over(self, victory):
        """Handle game over"""
        # Clear choice buttons
        for widget in self.choice_frame.winfo_children():
            widget.destroy()

        if victory:
            self.display_text("\n" + "="*70 + "\n", color=self.victory_color)
            self.display_text("VICTORY!\n", color=self.victory_color)
            self.display_text(self.game_data["victory_message"] + "\n", color=self.victory_color)
            self.display_text(self.game_data["boon_description"] + "\n", color=self.text_color)
            self.display_text(f"\nFinal Score: {self.score} points (Year {self.year})\n", color=self.victory_color)
        else:
            self.display_text("\n" + "="*70 + "\n", color=self.danger_color)
            self.display_text("GAME OVER\n", color=self.danger_color)
            self.display_text("Your quest ends in failure. The treasure remains unclaimed.\n", color=self.danger_color)
            self.display_text(f"\nFinal Score: {self.score} points (Completed {self.rooms_completed} rooms)\n", color=self.dim_color)

        # Show buttons
        button_frame = tk.Frame(self.choice_frame, bg=self.bg_color)
        button_frame.pack()

        # New adventure button
        restart_btn = tk.Button(
            button_frame,
            text="New Adventure",
            command=self.restart_with_same_topic,
            font=('Courier', 12, 'bold'),
            bg='#004400',
            fg=self.text_color,
            padx=15,
            pady=8
        )
        restart_btn.pack(side='left', padx=5)

        # Change topic button
        change_btn = tk.Button(
            button_frame,
            text="Change Topic",
            command=self.setup_topic_selection,
            font=('Courier', 12, 'bold'),
            bg='#444400',
            fg=self.text_color,
            padx=15,
            pady=8
        )
        change_btn.pack(side='left', padx=5)

    def restart_with_same_topic(self):
        """Restart with the same topic"""
        self.generate_game()

    def display_text(self, text, color=None, clear=False):
        """Display text in the main display"""
        self.text_display.config(state=tk.NORMAL)

        if clear:
            self.text_display.delete('1.0', tk.END)

        if color:
            tag_name = f"color_{random.randint(1000, 9999)}"
            self.text_display.tag_config(tag_name, foreground=color)
            self.text_display.insert(tk.END, text, tag_name)
        else:
            self.text_display.insert(tk.END, text)

        self.text_display.see(tk.END)
        self.text_display.config(state=tk.DISABLED)

    def update_status(self):
        """Update status bar"""
        status = "ALIVE" if self.is_alive else "DEAD"
        self.status_label.config(
            text=f"Room: {self.current_room}/10 | Status: {status} | Score: {self.score} | Year: {self.year} (+{self.points_per_room}/room) | Topic: {self.topic}"
        )


# Main execution
if __name__ == "__main__":
    import sys

    # Parse command line arguments
    year = 1978
    topic = None

    # Check for --topic argument
    for i, arg in enumerate(sys.argv):
        if arg == "--topic" and i + 1 < len(sys.argv):
            topic = sys.argv[i + 1]
        elif arg == "--year" and i + 1 < len(sys.argv):
            try:
                year = int(sys.argv[i + 1])
            except ValueError:
                pass

    # Legacy argument parsing for backward compatibility
    if topic is None and len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
        try:
            year = int(sys.argv[1])
        except ValueError:
            topic = sys.argv[1]

    if len(sys.argv) > 2 and not sys.argv[2].startswith("--"):
        try:
            year = int(sys.argv[2])
        except ValueError:
            topic = sys.argv[2]

    # Create and run game
    root = tk.Tk()
    game = DeepAdventure(root, year=year, topic=topic)
    root.mainloop()