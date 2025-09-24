"""
NPC Database for Game Developers and Company Names
Contains 1000+ developer names (born up to 2005) and period-appropriate company names
"""

import random
from typing import List, Tuple, Dict

# First names by era (for developers born 1950-2005)
FIRST_NAMES = {
    "male_classic": [  # Popular 1950-1980
        "John", "James", "Robert", "Michael", "David", "William", "Richard", "Thomas",
        "Charles", "Joseph", "Christopher", "Daniel", "Paul", "Mark", "Donald", "George",
        "Kenneth", "Steven", "Edward", "Brian", "Ronald", "Anthony", "Kevin", "Larry",
        "Jeffrey", "Frank", "Scott", "Eric", "Stephen", "Andrew", "Gary", "Joshua",
        "Dennis", "Jerry", "Gregory", "Samuel", "Benjamin", "Ralph", "Carl", "Arthur",
        "Peter", "Henry", "Jack", "Wayne", "Roger", "Keith", "Gerald", "Albert"
    ],
    "female_classic": [  # Popular 1950-1980
        "Mary", "Patricia", "Linda", "Barbara", "Elizabeth", "Jennifer", "Maria", "Susan",
        "Margaret", "Dorothy", "Lisa", "Nancy", "Karen", "Betty", "Helen", "Sandra",
        "Donna", "Carol", "Ruth", "Sharon", "Michelle", "Laura", "Sarah", "Kimberly",
        "Deborah", "Jessica", "Shirley", "Cynthia", "Angela", "Melissa", "Brenda", "Amy",
        "Anna", "Rebecca", "Kathleen", "Amanda", "Stephanie", "Carolyn", "Christine", "Marie",
        "Janet", "Catherine", "Frances", "Christina", "Debra", "Martha", "Joyce", "Diane"
    ],
    "male_modern": [  # Popular 1980-2005
        "Matthew", "Jason", "Justin", "Ryan", "Nathan", "Tyler", "Brandon", "Austin",
        "Jordan", "Zachary", "Dylan", "Hunter", "Logan", "Jacob", "Ethan", "Mason",
        "Noah", "Alexander", "Liam", "Connor", "Cameron", "Trevor", "Blake", "Chase",
        "Cody", "Kyle", "Shane", "Travis", "Derek", "Corey", "Jesse", "Aaron",
        "Adam", "Brett", "Chad", "Dustin", "Evan", "Ian", "Jeremy", "Marcus",
        "Nicholas", "Patrick", "Sean", "Wesley", "Adrian", "Alex", "Christian", "Gabriel"
    ],
    "female_modern": [  # Popular 1980-2005
        "Ashley", "Brittany", "Samantha", "Taylor", "Megan", "Hannah", "Kayla", "Rachel",
        "Emily", "Madison", "Emma", "Olivia", "Abigail", "Isabella", "Sophia", "Charlotte",
        "Alexis", "Alyssa", "Brianna", "Chelsea", "Courtney", "Danielle", "Haley", "Jasmine",
        "Jordan", "Kelsey", "Lauren", "Miranda", "Morgan", "Nicole", "Paige", "Savannah",
        "Sydney", "Victoria", "Allison", "Andrea", "Brooke", "Chloe", "Destiny", "Erica",
        "Faith", "Grace", "Jenna", "Katie", "Kristen", "Lindsey", "Natalie", "Vanessa"
    ],
    "unisex": [  # Gender-neutral names
        "Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Cameron", "Quinn",
        "Avery", "Blake", "Drew", "Jamie", "Leslie", "Reese", "Robin", "Sage",
        "Shannon", "Skyler", "Terry", "Tracy", "Bailey", "Dakota", "Hayden", "Parker"
    ]
}

# Last names (common American surnames)
LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas",
    "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White",
    "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young",
    "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
    "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker",
    "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris", "Morales", "Murphy",
    "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper", "Peterson", "Bailey",
    "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson",
    "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett", "Gray", "Mendoza",
    "Ruiz", "Hughes", "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers",
    "Long", "Ross", "Foster", "Jimenez", "Powell", "Jenkins", "Perry", "Russell",
    "Sullivan", "Bell", "Coleman", "Butler", "Henderson", "Barnes", "Gonzales", "Fisher",
    "Vasquez", "Simmons", "Romero", "Jordan", "Patterson", "Alexander", "Hamilton", "Graham",
    "Reynolds", "Griffin", "Wallace", "Moreno", "West", "Cole", "Hayes", "Bryant",
    "Herrera", "Gibson", "Ellis", "Tran", "Medina", "Aguilar", "Stevens", "Murray",
    "Ford", "Castro", "Marshall", "Owens", "Harrison", "Fernandez", "McDonald", "Woods",
    "Washington", "Kennedy", "Wells", "Vargas", "Henry", "Freeman", "Webb", "Tucker",
    "Guzman", "Burns", "Crawford", "Olson", "Simpson", "Porter", "Hunter", "Gordon",
    "Mendez", "Silva", "Shaw", "Snyder", "Mason", "Dixon", "Munoz", "Hunt",
    "Hicks", "Holmes", "Palmer", "Wagner", "Black", "Robertson", "Boyd", "Rose",
    "Stone", "Salazar", "Fox", "Warren", "Mills", "Meyer", "Rice", "Schmidt",
    "Garza", "Daniels", "Ferguson", "Nichols", "Stephens", "Soto", "Weaver", "Ryan",
    "Gardner", "Payne", "Grant", "Dunn", "Kelley", "Spencer", "Hawkins", "Arnold",
    "Pierce", "Vazquez", "Hansen", "Peters", "Santos", "Hart", "Bradley", "Knight",
    "Elliott", "Cunningham", "Duncan", "Armstrong", "Hudson", "Carroll", "Lane", "Riley",
    "Andrews", "Alvarado", "Ray", "Delgado", "Berry", "Perkins", "Hoffman", "Johnston",
    "Matthews", "Pena", "Richards", "Contreras", "Willis", "Carpenter", "Lawrence", "Sandoval"
]

# Tech-related middle initials/nicknames for flavor
NICKNAMES = [
    "Dev", "Code", "Byte", "Bit", "Tech", "Hack", "Pixel", "Data", "Logic", "Debug",
    "Script", "Stack", "Buffer", "Cache", "Kernel", "Root", "Admin", "User", "Shell", "Core"
]

# Company names by era
COMPANY_NAMES = {
    "1970-1974": [
        # Early computing era
        "Mainframe Systems Inc", "Digital Computing Corp", "Binary Logic Ltd", "Data Systems International",
        "Electronic Machines Corp", "Computer Sciences Inc", "Automated Systems", "Information Processing Corp",
        "Magnetic Storage Systems", "Punch Card Technologies", "Terminal Systems Ltd", "Circuit Board Inc",
        "Transistor Technologies", "Microprocessor Corp", "Silicon Systems", "Memory Core Inc",
        "Tape Drive Technologies", "Computing Laboratories", "Electronic Data Corp", "Business Machines Inc",
        "Scientific Computing", "Research Systems Corp", "Mathematical Machines", "Logic Gate Inc",
        "Semiconductor Corp", "Integrated Circuits Ltd", "Assembly Systems", "Compiler Technologies",
        "Operating Systems Inc", "Database Machines Corp", "Network Computing", "Time-Share Systems",
        "Batch Processing Inc", "Terminal Connect Corp", "Data Entry Systems", "Card Reader Technologies",
        "Magnetic Drum Corp", "Core Memory Inc", "Vacuum Tube Systems", "Relay Computing Ltd",
        "Binary Systems", "Octal Technologies", "Hexadecimal Corp", "ASCII Systems Inc",
        "FORTRAN Technologies", "COBOL Systems Corp", "BASIC Computing", "Assembly Language Inc",
        "Machine Code Corp", "Bit Byte Technologies", "Register Systems Ltd"
    ],

    "1975-1979": [
        # Personal computer revolution begins
        "Micro Computer Corp", "Personal Systems Inc", "Home Computing Ltd", "Desktop Technologies",
        "8-Bit Systems", "Microprocessor Magic", "RAM Technologies Corp", "ROM Systems Inc",
        "Floppy Disk Corp", "Cassette Storage Ltd", "Video Display Inc", "Keyboard Interface Corp",
        "BASIC Software", "CP/M Systems", "Altair Compatible Inc", "Apple Grove Computing",
        "Commodore Systems", "Radio Electronics Corp", "Tandy Technologies", "Sinclair Research",
        "Atari Computing", "Texas Digital", "Intel Compatible Corp", "Zilog Systems",
        "MOS Technology Inc", "6502 Systems", "Z80 Computing", "8080 Technologies",
        "S-100 Bus Corp", "Parallel Port Inc", "Serial Systems Ltd", "ASCII Terminal Corp",
        "Green Screen Technologies", "Dot Matrix Inc", "Daisy Wheel Corp", "Acoustic Coupler Ltd",
        "300 Baud Systems", "Bulletin Board Inc", "User Group Technologies", "Hobbyist Computing",
        "Kit Computer Corp", "Solder Systems Inc", "Wire Wrap Technologies", "Breadboard Computing",
        "LED Display Corp", "Seven Segment Inc", "Calculator Chip Ltd", "Watch Computer Systems"
    ],

    "1980-1984": [
        # PC era, arcade games boom
        "IBM Compatible Corp", "Clone Systems Inc", "MS-DOS Technologies", "Lotus Software",
        "WordPerfect Corp", "dBase Systems", "Arcade Games Inc", "Coin-Op Technologies",
        "Vector Graphics Corp", "Sprite Systems", "Joystick Interface Inc", "Game Cartridge Corp",
        "16-Bit Computing", "GUI Systems Ltd", "Mouse Interface Corp", "Hard Drive Technologies",
        "Winchester Disk Inc", "EGA Graphics Corp", "Sound Blaster Inc", "MIDI Systems Ltd",
        "Pac-Man Technologies", "Space Invader Corp", "Donkey Kong Inc", "Frogger Systems",
        "Centipede Computing", "Defender Technologies", "Galaga Games", "Q*bert Corp",
        "Zaxxon Systems", "Robotron Inc", "Tempest Technologies", "Missile Command Corp",
        "Asteroids Inc", "Breakout Systems", "Pong Evolution Ltd", "Tennis for Two Corp",
        "Adventure Games Inc", "Text Parser Systems", "Sierra Compatible", "LucasArts Style Corp",
        "Point Click Inc", "Parser Technologies", "8088 Systems", "80286 Computing Corp"
    ],

    "1985-1989": [
        # GUI era, Nintendo dominance
        "Windows Systems Corp", "Macintosh Software", "Desktop Publishing Inc", "LaserJet Corp",
        "PostScript Technologies", "Vector Font Systems", "TrueType Inc", "PageMaker Corp",
        "Nintendo Compatible", "Super Mario Systems", "Zelda Technologies", "Metroid Corp",
        "Sega Systems Inc", "Sonic Speed Corp", "16-Bit Console Ltd", "Blast Processing Inc",
        "VGA Graphics Corp", "256 Color Systems", "Sound Card Inc", "AdLib Technologies",
        "Roland MIDI Corp", "Yamaha Sound Inc", "Creative Audio Ltd", "3D Graphics Systems",
        "Polygon Rendering Inc", "Texture Mapping Corp", "Ray Casting Technologies", "Wolf3D Systems",
        "Commander Keen Corp", "Duke Nukem Inc", "Prince of Persia Ltd", "SimCity Systems",
        "Tetris Technologies", "Game Boy Compatible", "Portable Gaming Inc", "Link Cable Corp",
        "Turbo Graphics", "Neo Geo Systems", "Arcade Perfect Inc", "Fighting Game Corp",
        "Beat Em Up Ltd", "Shoot Em Up Inc", "Platform Game Systems", "RPG Technologies"
    ],

    "1990-1994": [
        # Internet emerges, 3D gaming
        "World Wide Web Corp", "Mosaic Browser Inc", "Netscape Compatible", "HTML Systems Ltd",
        "HTTP Technologies", "TCP/IP Corp", "Ethernet Systems", "Token Ring Inc",
        "Doom Engine Corp", "Quake Technologies", "Build Engine Inc", "3D Realms Systems",
        "Polygon Graphics Ltd", "Texture Cache Corp", "Z-Buffer Inc", "Gouraud Shading Systems",
        "CD-ROM Technologies", "Multimedia Corp", "FMV Games Inc", "Interactive Movie Ltd",
        "Virtual Reality Systems", "VR Headset Corp", "Motion Control Inc", "Force Feedback Ltd",
        "Super Nintendo Compatible", "Genesis Does Corp", "32-Bit Systems", "64-Bit Technologies",
        "PlayStation Inc", "Saturn Systems", "3DO Interactive", "Jaguar Technologies",
        "Fighting Game Corp", "Street Fighter Systems", "Mortal Kombat Inc", "Tekken Technologies",
        "Final Fantasy Corp", "Dragon Quest Inc", "Chrono Systems", "Secret of Mana Ltd",
        "LAN Party Corp", "IPX Gaming Inc", "Null Modem Systems", "BBS Door Games Ltd"
    ],

    "1995-1999": [
        # Dot-com boom, online gaming
        "Yahoo Compatible Corp", "Amazon Systems Inc", "eBay Technologies", "PayPal Processing",
        "Dot Com Ventures", "E-Commerce Systems", "SSL Secure Corp", "HTTPS Technologies",
        "Java Applet Inc", "Flash Animation Corp", "Shockwave Games", "RealPlayer Systems",
        "MP3 Technologies", "Napster Compatible", "Winamp Skins Inc", "ICQ Messaging Corp",
        "AOL Instant Systems", "GeoCities Hosting", "Angelfire Pages", "Tripod Sites Inc",
        "Counter-Strike Servers", "Quake Arena Corp", "Unreal Tournament", "Half-Life Mods Inc",
        "StarCraft Strategies", "Warcraft Online", "Diablo Dungeons Corp", "EverQuest Worlds",
        "Ultima Online Systems", "MMO Technologies", "MUD Games Inc", "MMORPG Corp",
        "Nintendo 64 Dev", "PlayStation One Games", "Dreamcast Studios", "DVD Game Corp",
        "USB Technologies", "FireWire Systems", "Pentium Optimized", "3dfx Voodoo Inc",
        "GeForce Graphics", "ATI Radeon Corp", "DirectX Games", "OpenGL Systems Ltd"
    ],

    "2000-2004": [
        # Social media dawn, mobile gaming starts
        "Friendster Networks", "MySpace Pages Inc", "LinkedIn Professional", "Orkut Social Corp",
        "Blog Platform Systems", "RSS Feed Technologies", "Podcast Network Inc", "Wiki Collaborative",
        "BitTorrent Games", "Kazaa Share Corp", "LimeWire Downloads", "eMule Networks Inc",
        "Steam Platform Corp", "Xbox Live Systems", "PlayStation Network", "GameCube Connect",
        "Halo Multiplayer Inc", "GTA Open World Corp", "Sims Life Systems", "World of Warcraft",
        "Second Life Virtual", "Flash Games Portal", "Newgrounds Compatible", "Miniclip Games",
        "PopCap Casual Corp", "Big Fish Games", "Yahoo Games Inc", "MSN Gaming Zone",
        "Java Mobile Games", "J2ME Technologies", "Palm Pilot Apps", "Pocket PC Games",
        "Nokia N-Gage Dev", "Game Boy Advance", "Nintendo DS Touch", "PSP Portable Corp",
        "Wi-Fi Gaming Inc", "Bluetooth Multiplayer", "Browser Games Ltd", "AJAX Interactive"
    ],

    "2005-2009": [
        # Facebook era, iPhone revolution
        "Facebook Apps Inc", "Twitter Games Corp", "YouTube Gaming", "Gmail Platform Systems",
        "iPhone App Store", "Android Market Dev", "Mobile Gaming Corp", "Touch Screen Games",
        "Accelerometer Control", "GPS Gaming Inc", "Augmented Reality App", "QR Code Games",
        "Wii Motion Gaming", "Xbox 360 Live", "PlayStation 3 Network", "Achievement Systems",
        "Trophy Hunter Corp", "Gamerscore Inc", "DLC Content Corp", "Season Pass Games",
        "Free to Play Inc", "Microtransaction Corp", "Virtual Currency", "Loot Box Systems",
        "Unity Engine Games", "Unreal Engine 3", "Source Engine Mods", "CryEngine Studios",
        "Physics Gaming Corp", "Havok Ragdoll Inc", "Motion Capture Studio", "Facial Animation",
        "HD Graphics Corp", "1080p Gaming Inc", "Blu-ray Games", "Digital Download Only",
        "Steam Workshop Mods", "User Generated Content", "Minecraft Clones Inc", "Indie Bundle Games"
    ],

    "2010-2014": [
        # Mobile dominance, indie boom
        "Instagram Filters Inc", "Snapchat Games", "WhatsApp Connect", "Vine Loop Games",
        "Kickstarter Funded", "Indiegogo Games", "Early Access Corp", "Greenlight Games",
        "Humble Bundle Dev", "itch.io Indie", "Game Jolt Upload", "Desura Platform Inc",
        "Twitch Streaming", "Let's Play Games", "YouTube Gaming Corp", "Patreon Supported",
        "Unity 3D Mobile", "Unreal Engine 4", "GameMaker Studio", "Construct Games Inc",
        "Flappy Bird Clones", "Angry Birds Style", "Candy Crush Match", "Clash of Clans",
        "Minecraft Inspired", "Terraria Like Games", "Rogue-like Revival", "Souls-like Difficulty",
        "Battle Royale Proto", "MOBA Mobile Corp", "Tower Defense Plus", "Idle Clicker Games",
        "Freemium Model Inc", "Pay to Win Corp", "Cosmetic Only Store", "Battle Pass System",
        "Cloud Gaming Beta", "Cross Platform Play", "4K Gaming Ready", "VR Revival Corp"
    ],

    "2015-2019": [
        # Streaming era, battle royale boom
        "Discord Gaming Inc", "Slack Integrated", "Microsoft Teams App", "Zoom Games Corp",
        "Fortnite Inspired", "PUBG Style Games", "Apex Legends Like", "Overwatch Heroes",
        "Hero Shooter Corp", "Battle Royale Inc", "Auto Chess Games", "Card Battler Digital",
        "Nintendo Switch Dev", "PlayStation 4 Pro", "Xbox One X Enhanced", "Ray Tracing Demo",
        "DLSS Technology", "AMD FidelityFX", "Vulkan API Games", "Metal Graphics Corp",
        "React Native Apps", "Flutter Games Inc", "Progressive Web App", "WebAssembly Games",
        "Blockchain Gaming", "NFT Marketplace", "Crypto Rewards Corp", "Play to Earn Inc",
        "Game Pass Studios", "PlayStation Now", "Stadia Cloud Gaming", "GeForce NOW Stream",
        "Epic Games Store", "Discord Store Games", "Riot Games Client", "Battle.net 2.0",
        "Auto Battler Genre", "Roguelike Deckbuilder", "Metroidvania Plus", "Soulsborne Style"
    ],

    "2020-2024": [
        # Pandemic era, AI emergence
        "Zoom Gaming Social", "Remote Play Together", "Parsec Streaming", "Steam Remote Play",
        "Among Us Inspired", "Fall Guys Style", "Valorant Tactical", "Genshin Impact Like",
        "COVID Game Jams", "Quarantine Indies", "Work From Home Dev", "Discord Activities",
        "Wordle Clone Games", "Netflix Gaming Div", "Apple Arcade Plus", "Xbox Cloud Gaming",
        "PlayStation 5 Exclusive", "Xbox Series X|S", "Steam Deck Verified", "ROG Ally Ready",
        "Unreal Engine 5", "Unity 2022 LTS", "Godot 4 Engine", "ChatGPT Integrated",
        "Stable Diffusion Art", "Midjourney Assets", "DALL-E Graphics", "AI Dungeon Style",
        "GPT-4 NPCs Inc", "Procedural Dialog AI", "Machine Learning Boss", "Neural Network Games",
        "Metaverse Platform", "Virtual Worlds Inc", "Social VR Gaming", "AR Glasses Ready",
        "8K Gaming Future", "120 FPS Target", "Variable Rate Shade", "Mesh Shaders Inc",
        "WebGPU Games", "WebXR Experiences", "Cloud Native Gaming", "5G Streaming Ready"
    ],

    "2025-2030": [
        # Future projection
        "Quantum Gaming Corp", "Neural Interface Games", "Brain Computer Play", "Holographic Display",
        "AR Contact Lens Dev", "Tactile Suit Gaming", "Smell-O-Vision Games", "Taste Simulation Inc",
        "AI Director Studios", "Procedural Everything", "Infinite World Gen", "Dynamic Story AI",
        "Photorealistic NPCs", "Emotion Recognition", "Biometric Gaming", "DNA Customized Play",
        "Mars Colony Sims", "Space Tourism Games", "Climate Crisis Gaming", "Sustainability Sim",
        "Post-Singularity Dev", "AGI Game Masters", "Consciousness Upload", "Digital Twin Gaming",
        "Nano-tech Interface", "Molecular Display", "Quantum Entangle Play", "Time Dilated Gaming",
        "Parallel Universe Co", "Multiverse Gaming Inc", "Reality Synthesis Corp", "Dream Recording",
        "Memory Implant Games", "Synthetic Reality Inc", "Bio-Digital Fusion", "Cyber-Organic Play",
        "Zero Latency Global", "Instant Anywhere Game", "Universal Translator", "Mind Meld Multi",
        "Perpetual Energy Game", "Self-Evolving AI", "Emergent Gameplay Inc", "Living World Systems",
        "Sentient NPC Corp", "Ethical AI Gaming", "Sustainable Compute", "Carbon Negative Dev"
    ]
}


class NPCGenerator:
    """Generate NPC developers and companies for the game"""

    def __init__(self):
        self.used_names = set()
        self.used_companies = set()

    def generate_developer(self, birth_year: int = None) -> Dict[str, any]:
        """
        Generate a random developer NPC

        Args:
            birth_year: Optional birth year (1950-2005), random if not specified

        Returns:
            Dictionary with developer details
        """
        if birth_year is None:
            birth_year = random.randint(1950, 2005)

        # Determine name pool based on birth year
        if birth_year < 1965:
            male_pool = FIRST_NAMES["male_classic"]
            female_pool = FIRST_NAMES["female_classic"]
        elif birth_year < 1985:
            male_pool = FIRST_NAMES["male_classic"] + FIRST_NAMES["male_modern"][:20]
            female_pool = FIRST_NAMES["female_classic"] + FIRST_NAMES["female_modern"][:20]
        else:
            male_pool = FIRST_NAMES["male_modern"]
            female_pool = FIRST_NAMES["female_modern"]

        # Add unisex names
        male_pool = male_pool + FIRST_NAMES["unisex"]
        female_pool = female_pool + FIRST_NAMES["unisex"]

        # Determine gender (60% male, 40% female for historical accuracy in tech)
        is_male = random.random() < 0.6

        # Generate unique name
        attempts = 0
        while attempts < 100:
            if is_male:
                first_name = random.choice(male_pool)
            else:
                first_name = random.choice(female_pool)

            last_name = random.choice(LAST_NAMES)
            full_name = f"{first_name} {last_name}"

            if full_name not in self.used_names:
                self.used_names.add(full_name)
                break
            attempts += 1

        # Generate developer attributes
        specialties = ["Programming", "Art", "Design", "Audio", "Writing", "Production", "QA", "Marketing"]
        languages = ["C++", "C#", "Java", "Python", "JavaScript", "Ruby", "Go", "Rust", "Swift", "Kotlin"]

        # Skills based on experience
        current_year = 2024
        experience = current_year - (birth_year + random.randint(18, 25))  # Start career at 18-25
        experience = max(0, min(experience, 40))  # Cap at 40 years

        skill_level = min(100, 30 + experience * 2 + random.randint(-10, 20))

        return {
            "name": full_name,
            "first_name": first_name,
            "last_name": last_name,
            "birth_year": birth_year,
            "gender": "male" if is_male else "female",
            "experience_years": experience,
            "specialty": random.choice(specialties),
            "skill_level": skill_level,
            "primary_language": random.choice(languages),
            "salary_expectation": 30000 + (experience * 2000) + (skill_level * 200),
            "personality": random.choice(["Creative", "Analytical", "Leader", "Team Player", "Perfectionist", "Fast Worker"]),
            "nickname": random.choice(NICKNAMES) if random.random() < 0.1 else None
        }

    def generate_developers_batch(self, count: int = 100, birth_year_range: Tuple[int, int] = (1950, 2005)) -> List[Dict]:
        """
        Generate a batch of developers

        Args:
            count: Number of developers to generate
            birth_year_range: Tuple of (min_year, max_year) for birth years

        Returns:
            List of developer dictionaries
        """
        developers = []
        for _ in range(count):
            birth_year = random.randint(birth_year_range[0], birth_year_range[1])
            developers.append(self.generate_developer(birth_year))
        return developers

    def get_company_for_year(self, year: int) -> str:
        """
        Get a period-appropriate company name for a given year

        Args:
            year: The year to get a company name for

        Returns:
            A period-appropriate company name
        """
        # Find the appropriate period
        period = None
        for period_key in COMPANY_NAMES.keys():
            start_year, end_year = map(int, period_key.split('-'))
            if start_year <= year <= end_year:
                period = period_key
                break

        if not period:
            if year < 1970:
                period = "1970-1974"
            elif year > 2030:
                period = "2025-2030"
            else:
                period = "1995-1999"  # Default fallback

        return random.choice(COMPANY_NAMES[period])

    def generate_company_history(self, company_name: str, founded_year: int) -> Dict:
        """
        Generate a company with history

        Args:
            company_name: Name of the company
            founded_year: Year the company was founded

        Returns:
            Dictionary with company details
        """
        company_types = ["Publisher", "Developer", "Publisher/Developer", "Indie", "AAA Studio", "Mobile Studio"]

        # Companies get bigger over time
        age = 2024 - founded_year
        size_categories = ["Tiny", "Small", "Medium", "Large", "Massive"]
        size_index = min(4, age // 10)

        employees = [1, 5, 20, 100, 500][size_index] + random.randint(-20, 50)
        employees = max(1, employees)

        return {
            "name": company_name,
            "founded": founded_year,
            "type": random.choice(company_types),
            "size": size_categories[size_index],
            "employees": employees,
            "revenue": employees * random.randint(50000, 200000),
            "reputation": random.randint(1, 100),
            "specialties": random.sample(["Action", "RPG", "Strategy", "Puzzle", "Simulation", "Sports", "Racing"], k=random.randint(1, 3)),
            "notable_games": []
        }


def generate_all_npcs(count: int = 1000) -> Dict:
    """
    Generate a complete NPC database

    Args:
        count: Number of NPCs to generate

    Returns:
        Dictionary with developers and companies
    """
    generator = NPCGenerator()

    # Generate developers with realistic distribution
    developers = []

    # Distribution by birth year
    birth_distributions = [
        (1950, 1960, int(count * 0.05)),  # 5% - Older veterans
        (1960, 1970, int(count * 0.10)),  # 10% - Senior developers
        (1970, 1980, int(count * 0.20)),  # 20% - Experienced
        (1980, 1990, int(count * 0.30)),  # 30% - Mid-career
        (1990, 2000, int(count * 0.25)),  # 25% - Junior/Mid
        (2000, 2005, int(count * 0.10)),  # 10% - Junior
    ]

    for min_year, max_year, dev_count in birth_distributions:
        batch = generator.generate_developers_batch(dev_count, (min_year, max_year))
        developers.extend(batch)

    # Generate companies for each era
    companies = []
    for period in COMPANY_NAMES.keys():
        start_year = int(period.split('-')[0])
        for company_name in random.sample(COMPANY_NAMES[period], min(20, len(COMPANY_NAMES[period]))):
            founded_year = start_year + random.randint(0, 4)
            companies.append(generator.generate_company_history(company_name, founded_year))

    return {
        "developers": developers,
        "companies": companies,
        "total_developers": len(developers),
        "total_companies": len(companies)
    }


# Test the system
if __name__ == "__main__":
    print("Generating NPC Database...")
    print("=" * 60)

    # Generate NPCs
    npc_data = generate_all_npcs(1000)

    print(f"Generated {npc_data['total_developers']} developers")
    print(f"Generated {npc_data['total_companies']} companies")

    print("\nSample Developers:")
    for dev in npc_data['developers'][:5]:
        print(f"  {dev['name']} ({dev['birth_year']}) - {dev['specialty']}, {dev['experience_years']} years exp")

    print("\nSample Companies:")
    for company in npc_data['companies'][:5]:
        print(f"  {company['name']} ({company['founded']}) - {company['size']}, {company['employees']} employees")

    # Test name uniqueness
    names = [dev['name'] for dev in npc_data['developers']]
    print(f"\nUnique names: {len(set(names))} / {len(names)}")

    # Show distribution by birth decade
    print("\nDevelopers by birth decade:")
    decades = {}
    for dev in npc_data['developers']:
        decade = (dev['birth_year'] // 10) * 10
        decades[decade] = decades.get(decade, 0) + 1

    for decade in sorted(decades.keys()):
        print(f"  {decade}s: {decades[decade]} developers")