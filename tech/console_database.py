"""
Console and Platform Database
Contains all gaming platforms, computers, and handhelds from 1978-2030
Uses randomized company names from our NPC database
"""

import random
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from npcs.npc_database import COMPANY_NAMES

class ConsoleDatabase:
    def __init__(self):
        # Define console lineages - these will evolve across generations
        self.console_lineages = {
            # Long-running lineages (span 5+ generations)
            "Phoenix": ["Phoenix", "Phoenix II", "Phoenix Super", "Phoenix Pro", "Phoenix Next", "Phoenix Elite", "Phoenix Revolution", "Phoenix Eternal", "Phoenix Ascension"],
            "Dragon": ["Dragon", "Dragon Plus", "Dragon 64", "Dragon 2000", "Dragon X", "Dragon Supreme", "Dragon Master", "Dragon Legacy", None],
            "Sphinx": ["Sphinx", "Sphinx 2", "Sphinx III", "Pyramid", "Pyramid 1000", "Pyramid Pro", "Pyramid X", "Pyramid Elite", None],
            "Titan": ["Titan", "Titan 100", "Titan 2000", "Titan Pro", "Titan X", "Titan Elite", "Titan Omega", None, None],

            # Medium lineages (3-4 generations then die)
            "Griffin": ["Griffin", "Griffin II", "Griffin Super", "Griffin Max"],
            "Hydra": ["Hydra", "Hydra Plus", "Hydra 3000", None],
            "Valkyrie": ["Valkyrie", "Valkyrie II", "Valkyrie Next", None],

            # Early lineages (die after 2-3 generations)
            "Odyssey": ["Odyssey", "Odyssey II", None],
            "Dynasty": ["Dynasty", "Dynasty Plus", None],
            "Empire": ["Empire", None, None],

            # Late starters (begin in generation 3-4)
            "Quantum": [None, None, None, "Quantum", "Quantum 2", "Quantum Pro", "Quantum X", "Quantum Sequence", "Quantum Beyond"],
            "Aurora": [None, None, None, None, "Aurora", "Aurora 3200", "Aurora Pro", "Aurora X", "Aurora Radiant"],

            # Very late starters (begin in generation 6+)
            "Neural": [None, None, None, None, None, None, "Neural", "Neural Link", "Neural Connect"],
            "Cosmos": [None, None, None, None, None, None, "Cosmos", "Cosmos 5000", "Cosmos Universal"],
        }

        # Standalone consoles by generation (unique per generation to avoid duplicates)
        self.standalone_consoles_by_gen = {
            0: ["Lightning Box", "Storm Machine"],  # Early 80s (only need 2 to reach 10 total)
            1: ["Thunder Station", "Nova Core"],  # Late 80s
            2: ["Eclipse Drive", "Zenith Engine"],  # Early 90s
            3: ["Harmony Console", "Serenity Station", "Eternity Box"],  # Late 90s (only 3 needed)
            4: ["Legacy System", "Oracle Engine", "Mystic Core"],  # Early 2000s
            5: ["Arcane Station", "Ethereal Console", "Celestial Box"],  # Late 2000s
            6: ["Astral Machine"],  # Early 2010s (only 1 needed)
            7: ["Nebula System"],  # Late 2010s (only 1 needed)
            8: [  # Future 2025 (market explosion - 25 additional consoles)
                "Void Station", "Plasma Core", "Fusion Drive", "Reality Engine", "Dream Console",
                "Mind Box", "Soul Machine", "Spirit System", "Phantom Platform", "Ghost Drive",
                "Cyber Matrix", "Digital Realm", "Virtual Throne", "Meta Station", "Holo Core",
                "Nano System", "Micro Universe", "Macro Engine", "Terra Console", "Luna Box",
                "Solar Drive", "Stellar Platform", "Galactic Station", "Universal Core", "Infinite Loop"
            ]
        }

        self.handheld_lineages = {
            "PocketBuddy": ["PocketBuddy", "PocketBuddy Color", "PocketBuddy Advance", "PocketBuddy Touch", "PocketBuddy 3D"],
            "MicroPlay": ["MicroPlay", "MicroPlay Plus", "MicroPlay Pro", "MicroPlay Vision", "MicroPlay HD"],
            "GoGamer": ["GoGamer", "GoGamer 2000", "GoGamer Pro", "GoGamer Touch", "GoGamer Ultra"],
            "HandyMax": ["HandyMax", "HandyMax Color", "HandyMax XL", "HandyMax Touch", "HandyMax Cloud"]
        }

        # Console generations with lineage system
        self.console_generations = self.generate_all_console_generations()

    def get_random_company(self, year):
        """Get a random company name for the given year"""
        # COMPANY_NAMES is a list, just pick a random one
        return random.choice(COMPANY_NAMES)


    def generate_all_console_generations(self):
        """Generate all console generations using lineage system"""
        generations = {}

        generation_names = [
            "early_80s", "late_80s", "early_90s", "late_90s",
            "early_2000s", "late_2000s", "early_2010s", "late_2010s", "future_2025"
        ]

        year_ranges = [
            (1978, 1983), (1984, 1989), (1990, 1994), (1995, 1999),
            (2000, 2005), (2006, 2009), (2010, 2017), (2018, 2024), (2025, 2030)
        ]

        for gen_index, (gen_name, year_range) in enumerate(zip(generation_names, year_ranges)):
            consoles = []

            # Add lineage consoles for this generation
            for lineage_name, lineage_consoles in self.console_lineages.items():
                if gen_index < len(lineage_consoles) and lineage_consoles[gen_index] is not None:
                    consoles.append({
                        "name": lineage_consoles[gen_index],
                        "company": self.get_random_company(year_range[0])
                    })

            # Fill remaining slots with standalone consoles
            max_consoles = 30 if gen_index == 8 else 10  # 30 for future, 10 for others
            if gen_index in self.standalone_consoles_by_gen:
                for console_name in self.standalone_consoles_by_gen[gen_index]:
                    if len(consoles) < max_consoles:
                        consoles.append({
                            "name": console_name,
                            "company": self.get_random_company(year_range[0])
                        })

            # Generate exactly 3 handhelds per generation
            handhelds = []

            # Regular handhelds for early generations
            if gen_index < 5:  # Up to early 2000s
                handheld_idx = 0
                for hh_lineage_name, hh_lineage in self.handheld_lineages.items():
                    if handheld_idx >= 3:
                        break
                    if gen_index < len(hh_lineage):
                        handhelds.append({
                            "name": hh_lineage[gen_index],
                            "company": self.get_random_company(year_range[0])
                        })
                        handheld_idx += 1
            elif gen_index == 5:  # Late 2000s
                handhelds = [
                    {"name": "PocketBuddy Ultra", "company": self.get_random_company(year_range[0])},
                    {"name": "MicroPlay Touch", "company": self.get_random_company(year_range[0])},
                    {"name": "Mobile Phone Gaming", "company": "Various Manufacturers"}
                ]
            elif gen_index == 6:  # 2010s
                handhelds = [
                    {"name": "GoGamer Cloud", "company": self.get_random_company(year_range[0])},
                    {"name": "Tablet Gaming", "company": "Various Manufacturers"},
                    {"name": "Smartphone Gaming", "company": "Various Manufacturers"}
                ]
            elif gen_index == 7:  # Late 2010s
                handhelds = [
                    {"name": "HandyMax Neural", "company": self.get_random_company(year_range[0])},
                    {"name": "Portable PC Gaming", "company": "Various Manufacturers"},
                    {"name": "Cloud Gaming Device", "company": "Various Manufacturers"}
                ]
            elif gen_index == 8:  # Future
                handhelds = [
                    {"name": "Neural Portable", "company": self.get_random_company(year_range[0])},
                    {"name": "Holographic Mobile", "company": self.get_random_company(year_range[0])},
                    {"name": "Brain Interface Gaming", "company": self.get_random_company(year_range[0])}
                ]

            generations[gen_name] = {
                "year_range": year_range,
                "consoles": consoles,
                "computers": [
                    {"name": "PC", "company": "Various Manufacturers"},
                    {"name": "MAC", "company": "Various Manufacturers"}
                ],
                "handhelds": handhelds
            }

        return generations

    def get_platforms_for_year(self, year):
        """Get available platforms for a specific year with randomized companies"""
        # Regenerate companies each time for variety
        available = {
            "consoles": [],
            "computers": [],
            "handhelds": []
        }

        # Find the right generation
        for gen_name, gen_data in self.console_generations.items():
            if gen_data["year_range"][0] <= year <= gen_data["year_range"][1]:
                # Regenerate companies for this session
                for console in gen_data["consoles"]:
                    available["consoles"].append({
                        "name": console["name"],
                        "company": self.get_random_company(year)
                    })
                for computer in gen_data["computers"]:
                    if "Various" in computer["company"]:
                        available["computers"].append(computer)
                    else:
                        available["computers"].append({
                            "name": computer["name"],
                            "company": self.get_random_company(year)
                        })
                for handheld in gen_data["handhelds"]:
                    if "Various" in handheld.get("company", ""):
                        available["handhelds"].append(handheld)
                    else:
                        available["handhelds"].append({
                            "name": handheld["name"],
                            "company": self.get_random_company(year)
                        })
                break

        return available

    def print_full_database(self):
        """Print the complete console database"""
        print("=" * 80)
        print("COMPLETE CONSOLE DATABASE")
        print("=" * 80)
        print("\nNOTE: Console names are fixed, but manufacturers randomize each game session")
        print("=" * 80)

        # First print the lineage overview
        print("\n" + "=" * 80)
        print("CONSOLE LINEAGES OVERVIEW")
        print("=" * 80)

        gen_labels = ["1978-83", "1984-89", "1990-94", "1995-99", "2000-05", "2006-09", "2010-17", "2018-24", "2025-30"]

        for lineage_name, lineage_consoles in self.console_lineages.items():
            print(f"\n{lineage_name}:")
            for gen_idx, console_name in enumerate(lineage_consoles[:9]):  # Only show first 9 generations
                if console_name:
                    print(f"  {gen_labels[gen_idx]}: {console_name}")
                else:
                    print(f"  {gen_labels[gen_idx]}: ---")

        print("\n" + "=" * 80)
        print("DETAILED GENERATION BREAKDOWN")
        print("=" * 80)

        for gen_idx, (gen_name, gen_data) in enumerate(self.console_generations.items()):
            year_start, year_end = gen_data["year_range"]
            print(f"\n{gen_name.upper().replace('_', ' ')} ({year_start}-{year_end})")
            print("-" * 60)

            # Separate lineage consoles from standalone
            lineage_consoles = []
            standalone_consoles = []

            for console in gen_data["consoles"]:
                # Check if this console is part of a lineage
                is_lineage = False
                for lineage_name, lineage_list in self.console_lineages.items():
                    if gen_idx < len(lineage_list) and lineage_list[gen_idx] == console["name"]:
                        is_lineage = True
                        break

                if is_lineage:
                    lineage_consoles.append(console["name"])
                else:
                    standalone_consoles.append(console["name"])

            print("\nLINEAGE CONSOLES:")
            for i, console_name in enumerate(lineage_consoles, 1):
                print(f"  {i:2}. {console_name:30}")

            print("\nSTANDALONE CONSOLES:")
            for i, console_name in enumerate(standalone_consoles, 1):
                print(f"  {i:2}. {console_name:30}")

            print("\nCOMPUTERS:")
            for computer in gen_data["computers"]:
                print(f"  - {computer['name']:30}")

            print("\nHANDHELDS:")
            for handheld in gen_data["handhelds"]:
                print(f"  - {handheld['name']:30}")

# Test and print the database
if __name__ == "__main__":
    db = ConsoleDatabase()
    db.print_full_database()

    # Test year-specific retrieval
    print("\n" + "=" * 80)
    print("PLATFORMS AVAILABLE IN 1985 (Example):")
    print("-" * 60)
    platforms_1985 = db.get_platforms_for_year(1985)
    print("Consoles:", len(platforms_1985["consoles"]))
    for console in platforms_1985["consoles"][:5]:
        print(f"  - {console['name']}")
    print("\nComputers:", len(platforms_1985["computers"]))
    for computer in platforms_1985["computers"]:
        print(f"  - {computer['name']}")
    print("\nHandhelds:", len(platforms_1985["handhelds"]))
    for handheld in platforms_1985["handhelds"]:
        print(f"  - {handheld['name']}")