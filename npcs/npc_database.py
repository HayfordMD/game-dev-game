"""
NPC Database and Generator
Contains name lists and NPC generation logic
"""

import random
import yaml
import os
from pathlib import Path

# Company names for game industry
COMPANY_NAMES = [
    "Vertex Studios", "Pixel Forge", "Binary Dreams", "Quantum Games", "Atlas Interactive",
    "Nebula Software", "Crimson Byte", "Echo Entertainment", "Helix Productions", "Nexus Games",
    "Prism Studios", "Cipher Works", "Dynamo Games", "Horizon Interactive", "Titan Soft",
    "Phoenix Digital", "Omega Studios", "Cascade Games", "Aurora Entertainment", "Zenith Games",
    "Apex Software", "Fusion Studios", "Infinity Games", "Stellar Productions", "Neon Interactive",
    "Vector Games", "Matrix Studios", "Chronos Software", "Eclipse Entertainment", "Nova Games",
    "Raven Studios", "Dragon Byte", "Tempest Games", "Onyx Interactive", "Lightning Software",
    "Crystal Studios", "Phantom Games", "Vertex Entertainment", "Pulse Interactive", "Cosmic Games",
    "Thunder Studios", "Blaze Software", "Frost Games", "Shadow Productions", "Mirror Interactive",
    "Spark Studios", "Vortex Games", "Element Software", "Circuit Entertainment", "Flux Games"
]

# First names for NPC generation
FIRST_NAMES = {
    "male": [
        "Christopher", "James", "Richard", "Michael", "Robert", "Thomas", "David", "John",
        "Kenneth", "Steven", "William", "Mark", "Gary", "Brian", "Jason", "Jeff", "Ryan",
        "Joshua", "Brandon", "Daniel", "Andrew", "Matthew", "Justin", "Jonathan", "Eric",
        "Kevin", "Austin", "Nathan", "Dylan", "Tyler", "Kyle", "Zachary", "Jordan", "Jacob",
        "Logan", "Lucas", "Noah", "Mason", "Alexander", "Ethan", "Aiden", "Liam", "Jayden",
        "Oliver", "Elijah", "Benjamin", "Rowan", "Atlas", "Ezra", "Phoenix", "Mateo", "River",
        "Kai", "Neo", "Orion", "Zion", "Zen", "Quantum", "Zephyr", "Luca", "Victor", "Marcus",
        "Raymond", "Derek", "Seth", "Trevor", "Blake", "Colin", "Lance", "Shane", "Dean",
        "Adrian", "Preston", "Graham", "Felix", "Oscar", "Dominic", "Ivan", "Russell", "Wesley",
        "Byron", "Calvin", "Grant", "Edgar", "Jared", "Vincent", "Theodore", "Malcolm", "Tristan",
        "Curtis", "Damian", "Perry", "Hugh", "Cyrus", "Levi", "Gavin", "Pierce", "Drake",
        "Xavier", "Mitchell", "Tobias", "Roland", "Jasper", "Caleb", "Nolan", "Ross", "Alvin",
        "Eugene", "Chester", "Leonard"
    ],
    "female": [
        "Carol", "Jennifer", "Barbara", "Patricia", "Mary", "Linda", "Susan", "Nancy", "Amy",
        "Dorothy", "Lisa", "Michelle", "Karen", "Betty", "Amanda", "Ashley", "Nicole", "Jessica",
        "Heather", "Stephanie", "Emily", "Samantha", "Brittany", "Megan", "Rachel", "Sarah",
        "Laura", "Kayla", "Hannah", "Madison", "Morgan", "Taylor", "Alexis", "Sophia", "Isabella",
        "Emma", "Ava", "Mia", "Charlotte", "Olivia", "Abigail", "Amelia", "Willow", "Aurora",
        "Hazel", "Nova", "Ivy", "Sage", "Luna", "Aria", "Echo", "Stella", "Claire", "Diana",
        "Vanessa", "Monica", "Jasmine", "Chloe", "Grace", "Paige", "Ruby", "Brooke", "Natalie",
        "Maya", "Violet", "Naomi", "Iris", "Zoe", "Piper", "Molly", "Aubrey", "Tessa", "Kelsey",
        "Layla", "Sienna", "Holly", "Fiona", "Scarlett", "Penelope", "Gabrielle", "Elena",
        "Lillian", "Audrey", "Juliana", "Daisy", "Nora", "Bethany", "Ariana", "Lydia", "Camila",
        "Vera", "Clara", "Faith", "Destiny", "Cecilia", "Mariana", "Bianca", "Josephine", "Sylvia",
        "Genevieve", "Priscilla", "Bonnie"
    ]
}

# Last names for NPC generation
LAST_NAMES = [
    "Adams", "Martinez", "Thompson", "Miller", "Anderson", "Smith", "Wilson", "Davis",
    "Johnson", "Brown", "White", "Garcia", "Rodriguez", "Lopez", "Jackson", "Harris",
    "Taylor", "Moore", "Walker", "Lee", "Hall", "Allen", "Young", "King", "Wright",
    "Scott", "Martin", "Williams", "Baker", "Nelson", "Carter", "Phillips", "Evans",
    "Turner", "Parker", "Collins", "Edwards", "Stewart", "Sanchez", "Morris", "Rogers",
    "Reed", "Cook", "Morgan", "Bell", "Murphy", "Bailey", "Rivera", "Cooper", "Richardson",
    "Cox", "Howard", "Ward", "Torres", "Peterson", "Gray", "Ramirez", "James", "Watson",
    "Brooks", "Kelly", "Sanders", "Price", "Bennett", "Wood", "Barnes", "Ross", "Henderson",
    "Coleman", "Jenkins", "Perry", "Powell", "Long", "Patterson", "Hughes", "Flores",
    "Washington", "Butler", "Simmons", "Foster", "Gonzalez", "Bryant", "Russell", "Griffin",
    "Hayes", "Myers", "Ford", "Hamilton", "Graham", "Sullivan", "Wallace", "Woods", "Cole",
    "West", "Jordan", "Owens", "Reynolds", "Fisher", "Ellis", "Harrison", "Gibson", "McDonald",
    "Cruz", "Marshall", "Ortiz", "Gomez", "Murray", "Freeman", "Wells", "Webb", "Chen",
    "Singh", "Patel", "Kim", "Zhang", "Wong", "Liu", "Dawson", "Hoffman", "Fleming", "Pierce",
    "Knox", "Chambers", "Vaughn", "Reeves", "Lambert", "Bishop", "Nash", "Carpenter", "Sherman",
    "Mendoza", "Webster", "Nichols", "Stevenson", "Pearson", "Caldwell", "Quinn", "Holt",
    "Garrett", "Bowman", "Ramsey", "Barker", "Curtis", "Bowers", "Barton", "Cunningham",
    "Frost", "Meadows", "Fletcher", "Carr", "Sims", "Marsh", "Larson", "Yates", "Stone",
    "Hunter", "Winters", "Bates", "Osborne", "Montgomery", "Buchanan", "Sampson", "Wagner",
    "Malone", "Douglas", "Drake", "Manning", "Doyle", "French", "Stanton", "Ingram", "Hyde",
    "Pratt", "Holloway", "Merrill", "Whitman", "Norris", "Garza", "Atkins", "Chandler",
    "Sutton", "Bridges", "Warren", "Austin", "Walters", "Combs", "Dalton", "Hutchinson",
    "Wolfe", "Jensen", "Hayden", "Valentine", "Donovan", "Blackburn", "Steele", "Sloan",
    "Everett", "Sheppard", "Mullins", "Hobbs", "Roberson", "Dickson", "Conway", "Stafford",
    "McConnell", "Hendricks", "Brady", "Brennan", "Floyd", "Mathis", "Hammond", "Avery",
    "Richmond", "Mckay", "Marks"
]

class NPCGenerator:
    """Generator for creating random NPCs"""

    def __init__(self):
        self.used_names = set()
        self.npc_data_path = Path("npcs/npcslist")

    def generate_npc(self, npc_id):
        """Generate a random NPC with unique name"""
        gender = random.choice(["male", "female"])

        # Keep trying until we get a unique name
        while True:
            first_name = random.choice(FIRST_NAMES[gender])
            last_name = random.choice(LAST_NAMES)
            full_name = f"{first_name} {last_name}"

            if full_name not in self.used_names:
                self.used_names.add(full_name)
                break

        # Assign random job from the jobs file
        jobs = self.load_jobs()
        job = random.choice(jobs) if jobs else "Game Developer"

        return {
            "id": npc_id,
            "name": full_name,
            "gender": gender,
            "job": job
        }

    def load_jobs(self):
        """Load jobs from the jobs file"""
        jobs_file = Path("npcs/jobs")
        if jobs_file.exists():
            with open(jobs_file, 'r') as f:
                return [line.strip() for line in f.readlines() if line.strip()]
        return []

    def load_existing_npcs(self):
        """Load NPCs from yaml files in npcslist directory"""
        npcs = []
        if self.npc_data_path.exists():
            for yaml_file in self.npc_data_path.glob("*.yml"):
                try:
                    with open(yaml_file, 'r') as f:
                        data = yaml.safe_load(f)
                        if data and 'character' in data:
                            char = data['character']
                            npcs.append({
                                "id": char.get('id'),
                                "name": char.get('name'),
                                "gender": char.get('gender'),
                                "job": char.get('job')
                            })
                except Exception as e:
                    print(f"Error loading {yaml_file}: {e}")
        return npcs

def generate_all_npcs(count=200):
    """Generate a list of NPCs"""
    generator = NPCGenerator()

    # First try to load existing NPCs
    existing_npcs = generator.load_existing_npcs()
    if existing_npcs:
        return existing_npcs[:count]

    # Otherwise generate new ones
    npcs = []
    for i in range(1, count + 1):
        npcs.append(generator.generate_npc(i))
    return npcs