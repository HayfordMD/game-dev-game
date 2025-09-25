"""
Run-specific Platform Selection System
Randomly selects 5 consoles and 2 handhelds per generation for each game run
Also selects competitor companies for the run
"""

import random
import pickle
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tech.console_database import ConsoleDatabase
from npcs.npc_database import COMPANY_NAMES, NPCGenerator

class RunPlatforms:
    """Manages platform selection for a specific game run"""

    def __init__(self):
        self.console_db = ConsoleDatabase()
        self.npc_gen = NPCGenerator()

        # Selected platforms for this run
        self.run_consoles = {}  # {generation_name: [5 selected consoles]}
        self.run_handhelds = {}  # {generation_name: [2 selected handhelds]}

        # Selected competitor companies for this run (10-20 companies)
        self.run_companies = []

        # Initialize the run
        self.randomize_run()

    def randomize_run(self):
        """Randomize platforms and companies for this run"""
        self.select_run_platforms()
        self.select_run_companies()

    def select_run_platforms(self):
        """Select 5 consoles and 2 handhelds per generation"""
        generation_names = [
            "early_80s", "late_80s", "early_90s", "late_90s",
            "early_2000s", "late_2000s", "early_2010s", "late_2010s", "future_2025"
        ]

        for gen_name in generation_names:
            if gen_name in self.console_db.console_generations:
                gen_data = self.console_db.console_generations[gen_name]

                # Select 5 random consoles (or all if less than 5)
                all_consoles = gen_data["consoles"]
                if gen_name == "future_2025":
                    # For future, select 10 instead of 5 (more variety)
                    num_consoles = min(10, len(all_consoles))
                else:
                    num_consoles = min(5, len(all_consoles))

                selected_consoles = random.sample(all_consoles, num_consoles)
                self.run_consoles[gen_name] = selected_consoles

                # Select 2 random handhelds (or all if less than 2)
                all_handhelds = gen_data["handhelds"]
                num_handhelds = min(2, len(all_handhelds))
                selected_handhelds = random.sample(all_handhelds, num_handhelds) if all_handhelds else []
                self.run_handhelds[gen_name] = selected_handhelds

    def select_run_companies(self):
        """Select 10-20 competitor companies for this run"""
        num_companies = random.randint(10, 20)

        # COMPANY_NAMES is a list of company names
        # Select random companies from the list
        self.run_companies = random.sample(COMPANY_NAMES, min(num_companies, len(COMPANY_NAMES)))

        # Sort alphabetically for easier viewing
        self.run_companies.sort()

    def get_platforms_for_year(self, year):
        """Get available platforms for a specific year (only from selected run platforms)"""
        # Find the right generation
        generation_map = {
            "early_80s": (1978, 1983),
            "late_80s": (1984, 1989),
            "early_90s": (1990, 1994),
            "late_90s": (1995, 1999),
            "early_2000s": (2000, 2005),
            "late_2000s": (2006, 2009),
            "early_2010s": (2010, 2017),
            "late_2010s": (2018, 2024),
            "future_2025": (2025, 2030)
        }

        for gen_name, (start_year, end_year) in generation_map.items():
            if start_year <= year <= end_year:
                return {
                    "consoles": self.run_consoles.get(gen_name, []),
                    "computers": [
                        {"name": "PC", "company": "Various Manufacturers"},
                        {"name": "MAC", "company": "Various Manufacturers"}
                    ],
                    "handhelds": self.run_handhelds.get(gen_name, [])
                }

        return {"consoles": [], "computers": [], "handhelds": []}

    def save_run(self, filename="current_run.pkl"):
        """Save the current run configuration"""
        save_path = os.path.join("saves", filename)
        os.makedirs("saves", exist_ok=True)

        save_data = {
            "run_consoles": self.run_consoles,
            "run_handhelds": self.run_handhelds,
            "run_companies": self.run_companies
        }

        with open(save_path, 'wb') as f:
            pickle.dump(save_data, f)

    def load_run(self, filename="current_run.pkl"):
        """Load a saved run configuration"""
        save_path = os.path.join("saves", filename)

        if os.path.exists(save_path):
            with open(save_path, 'rb') as f:
                save_data = pickle.load(f)
                self.run_consoles = save_data["run_consoles"]
                self.run_handhelds = save_data["run_handhelds"]
                self.run_companies = save_data["run_companies"]
                return True
        return False

    def print_run_platforms(self):
        """Print the selected platforms for this run"""
        print("=" * 80)
        print("PLATFORMS SELECTED FOR THIS RUN")
        print("=" * 80)

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
            print(f"\n{gen_name}")
            print("-" * 40)

            print("CONSOLES:")
            for i, console in enumerate(self.run_consoles.get(gen_key, []), 1):
                print(f"  {i}. {console['name']}")

            print("HANDHELDS:")
            for i, handheld in enumerate(self.run_handhelds.get(gen_key, []), 1):
                print(f"  {i}. {handheld['name']}")

            print("COMPUTERS:")
            print("  - PC (Always Available)")
            print("  - MAC (Always Available)")

    def print_run_companies(self):
        """Print the selected companies for this run"""
        print("=" * 80)
        print(f"COMPETITOR COMPANIES FOR THIS RUN ({len(self.run_companies)} companies)")
        print("=" * 80)

        for i, company in enumerate(self.run_companies, 1):
            print(f"{i:2}. {company}")


# Test the system
if __name__ == "__main__":
    run = RunPlatforms()
    run.print_run_platforms()
    print()
    run.print_run_companies()

    # Save the run
    run.save_run()
    print("\n\nRun configuration saved to saves/current_run.pkl")