"""
Hardcoded period-appropriate names database for the game
Contains ~900 names across different time periods from 1970 to 2030
Names are period-appropriate and reflect naming trends of each era
"""

import random
from typing import List

PERIOD_NAMES = {
    "1970-1974": [
        # Traditional 70s names
        "David Johnson", "Susan Miller", "Michael Thompson", "Linda Williams", "John Davis",
        "Patricia Brown", "Robert Wilson", "Barbara Anderson", "James Garcia", "Mary Martinez",
        "Richard Taylor", "Jennifer Thomas", "Thomas Moore", "Carol Jackson", "Christopher White",
        "Nancy Harris", "William Martin", "Betty Clark", "Kenneth Lewis", "Dorothy Walker",
        "Donald Hall", "Karen Allen", "Gary Young", "Helen King", "Steven Wright",
        "Deborah Lopez", "Paul Hill", "Sandra Scott", "Mark Green", "Donna Adams",
        "Charles Baker", "Lisa Nelson", "Daniel Carter", "Margaret Mitchell", "Kevin Roberts",
        "Brenda Turner", "Larry Phillips", "Cynthia Campbell", "Jeffrey Parker", "Diane Evans",
        "Ronald Edwards", "Sharon Collins", "Brian Stewart", "Kathy Morris", "Dennis Murphy",
        "Pamela Cook", "Timothy Rogers", "Rebecca Morgan", "Gerald Peterson", "Janet Cooper",
        "George Bailey", "Ruth Reed", "Jerry Bell", "Laura Ward", "Gregory Torres",
        "Gloria Powell", "Roger Russell", "Carolyn Foster", "Frank Henderson", "Marie Perry",
        "Raymond Butler", "Frances Washington", "Stephen Price", "Teresa Bennett", "Peter Wood",
        "Martha Barnes", "Harold Ross", "Joyce Long", "Arthur Hughes", "Shirley Watson",
        "Wayne Coleman", "Judy Jenkins", "Philip Ramirez", "Alice Patterson", "Eugene Gray"
    ],

    "1975-1979": [
        # Late 70s names with disco era influence
        "Jason Williams", "Amy Johnson", "Jeffrey Brown", "Michelle Davis", "Brian Miller",
        "Lisa Anderson", "Mark Wilson", "Karen Martinez", "Steven Garcia", "Nancy Rodriguez",
        "Gary Thompson", "Betty Lewis", "Kenneth Hall", "Dorothy Clark", "Matthew Walker",
        "Jennifer Young", "David King", "Sarah Wright", "Michael Scott", "Laura Hill",
        "Christopher Green", "Melissa Adams", "Robert Baker", "Kimberly Nelson", "James Carter",
        "Angela Mitchell", "John Roberts", "Stephanie Turner", "Richard Phillips", "Jessica Campbell",
        "William Parker", "Deborah Evans", "Thomas Edwards", "Cynthia Collins", "Daniel Stewart",
        "Patricia Morris", "Charles Murphy", "Rebecca Cook", "Joseph Rogers", "Susan Morgan",
        "Kevin Peterson", "Donna Cooper", "Timothy Bailey", "Sandra Reed", "Gregory Bell",
        "Brenda Ward", "Eric Torres", "Janet Powell", "Scott Russell", "Nancy Foster",
        "Donald Henderson", "Carol Perry", "Larry Butler", "Barbara Washington", "Jeffrey Price",
        "Diana Bennett", "Paul Wood", "Sharon Barnes", "Dennis Ross", "Linda Watson",
        "Ronald Gray", "Teresa Coleman", "Gerald Jenkins", "Joyce Patterson", "Frank Ramirez",
        "Marie Hughes", "Raymond Long", "Frances Rivera", "Stephen Alexander", "Gloria Gonzalez",
        "Roger Simmons", "Carolyn Murphy", "Arthur Kelly", "Diane Sanders", "Philip Morris"
    ],

    "1980-1984": [
        # Early 80s - Jennifer/Jason era
        "Jennifer Smith", "Jason Anderson", "Jessica Brown", "Matthew Johnson", "Ashley Davis",
        "Christopher Miller", "Amanda Wilson", "Michael Moore", "Stephanie Taylor", "Joshua Martinez",
        "Nicole Garcia", "Andrew Thomas", "Heather Jackson", "Daniel White", "Melissa Harris",
        "David Martin", "Sarah Thompson", "Robert Clark", "Amy Rodriguez", "James Lewis",
        "Michelle Walker", "John Hall", "Kimberly Allen", "Brian Young", "Lisa King",
        "Kevin Wright", "Angela Lopez", "Timothy Hill", "Crystal Scott", "Eric Green",
        "Rebecca Adams", "Scott Baker", "Laura Nelson", "Joseph Carter", "Tiffany Mitchell",
        "Jeffrey Roberts", "Christina Turner", "Mark Phillips", "Kelly Campbell", "William Parker",
        "Rachel Evans", "Thomas Edwards", "Brittany Collins", "Richard Stewart", "Samantha Morris",
        "Charles Murphy", "Danielle Cook", "Steven Rogers", "Monica Morgan", "Kenneth Peterson",
        "Andrea Cooper", "Paul Bailey", "Maria Reed", "Donald Bell", "Julie Ward",
        "Gary Torres", "Shannon Powell", "Raymond Russell", "Erin Foster", "Frank Henderson",
        "April Perry", "Ronald Butler", "Tammy Washington", "Larry Price", "Dawn Bennett",
        "Jerry Wood", "Tracy Barnes", "Dennis Ross", "Karen Long", "Gerald Watson",
        "Cynthia Gray", "Arthur Coleman", "Denise Jenkins", "Philip Patterson", "Cheryl Ramirez"
    ],

    "1985-1989": [
        # Late 80s names
        "Michael Johnson", "Ashley Williams", "David Brown", "Jessica Davis", "Robert Miller",
        "Sarah Anderson", "James Wilson", "Brittany Martinez", "John Garcia", "Samantha Rodriguez",
        "Christopher Thompson", "Megan Lewis", "Matthew Clark", "Rachel Walker", "Joshua Hall",
        "Emily Allen", "Andrew Young", "Lauren King", "Daniel Wright", "Kayla Lopez",
        "Joseph Hill", "Amanda Scott", "Ryan Green", "Stephanie Adams", "Justin Baker",
        "Nicole Nelson", "Brandon Carter", "Heather Mitchell", "Kevin Roberts", "Christina Turner",
        "Eric Phillips", "Michelle Campbell", "Jonathan Parker", "Amber Evans", "Tyler Edwards",
        "Danielle Collins", "Nicholas Stewart", "Courtney Morris", "Steven Murphy", "Tiffany Cook",
        "Adam Rogers", "Jennifer Morgan", "Kyle Peterson", "Elizabeth Cooper", "Nathan Bailey",
        "Rebecca Reed", "Jason Bell", "Melissa Ward", "Jeremy Torres", "Crystal Powell",
        "Aaron Russell", "Kimberly Foster", "Sean Henderson", "Angela Perry", "Patrick Butler",
        "Laura Washington", "Zachary Price", "Kelly Bennett", "Benjamin Wood", "Amy Barnes",
        "Timothy Ross", "Shannon Long", "Derek Watson", "Monica Gray", "Shane Coleman",
        "Maria Jenkins", "Chad Patterson", "April Ramirez", "Travis Hughes", "Julie Alexander",
        "Dustin Gonzalez", "Erin Simmons", "Cody Murphy", "Andrea Kelly", "Brett Sanders"
    ],

    "1990-1994": [
        # Early 90s - Grunge era names
        "Tyler Smith", "Taylor Johnson", "Brandon Brown", "Brittany Williams", "Austin Davis",
        "Kayla Miller", "Kyle Anderson", "Alexis Wilson", "Jordan Martinez", "Morgan Garcia",
        "Dylan Rodriguez", "Hannah Thompson", "Zachary Lewis", "Madison Clark", "Nathan Walker",
        "Samantha Hall", "Hunter Allen", "Destiny Young", "Cody King", "Sierra Wright",
        "Cameron Lopez", "Jasmine Hill", "Logan Scott", "Haley Green", "Trevor Adams",
        "Alyssa Baker", "Blake Nelson", "Sydney Carter", "Chase Mitchell", "Savannah Roberts",
        "Dakota Turner", "Paige Phillips", "Tanner Campbell", "Rachel Parker", "Spencer Evans",
        "Brooke Edwards", "Garrett Collins", "Miranda Stewart", "Shane Morris", "Courtney Murphy",
        "Devin Cook", "Chelsea Rogers", "Connor Morgan", "Shelby Peterson", "Mason Cooper",
        "Victoria Bailey", "Evan Reed", "Danielle Bell", "Jesse Ward", "Marissa Torres",
        "Colton Powell", "Amber Russell", "Brady Foster", "Vanessa Henderson", "Seth Perry",
        "Jenna Butler", "Ian Washington", "Cassandra Price", "Dalton Bennett", "Monica Wood",
        "Wesley Barnes", "Kaitlyn Ross", "Caleb Long", "Erica Watson", "Jared Gray",
        "Lindsey Coleman", "Mitchell Jenkins", "Sabrina Patterson", "Wyatt Ramirez", "Tara Hughes"
    ],

    "1995-1999": [
        # Late 90s - Dot-com era names
        "Jacob Anderson", "Emma Thompson", "Ethan Martinez", "Olivia Johnson", "Noah Brown",
        "Isabella Davis", "Mason Miller", "Sophia Wilson", "Logan Garcia", "Ava Rodriguez",
        "Alexander Lewis", "Mia Clark", "Lucas Walker", "Charlotte Hall", "Michael Allen",
        "Abigail Young", "William King", "Emily Wright", "Joshua Lopez", "Madison Hill",
        "Matthew Scott", "Elizabeth Green", "Ryan Adams", "Chloe Baker", "Tyler Nelson",
        "Ella Carter", "Daniel Mitchell", "Grace Roberts", "Andrew Turner", "Lily Phillips",
        "Nathan Campbell", "Zoe Parker", "Christopher Evans", "Natalie Edwards", "Joseph Collins",
        "Victoria Stewart", "David Morris", "Samantha Murphy", "James Cook", "Hannah Rogers",
        "Benjamin Morgan", "Addison Peterson", "Samuel Cooper", "Avery Bailey", "John Reed",
        "Sofia Bell", "Dylan Ward", "Riley Torres", "Jonathan Powell", "Alexis Russell",
        "Christian Foster", "Leah Henderson", "Hunter Perry", "Audrey Butler", "Jordan Washington",
        "Brooklyn Price", "Austin Bennett", "Allison Wood", "Kevin Barnes", "Anna Ross",
        "Zachary Long", "Sarah Watson", "Brandon Gray", "Kaylee Coleman", "Justin Jenkins",
        "Maya Patterson", "Blake Ramirez", "Gabriella Hughes", "Connor Alexander", "Mackenzie Gonzalez"
    ],

    "2000-2004": [
        # Early 2000s - Reality TV era names
        "Aiden Smith", "Madison Johnson", "Jayden Brown", "Emma Williams", "Ethan Davis",
        "Abigail Miller", "Mason Anderson", "Olivia Wilson", "Noah Martinez", "Isabella Garcia",
        "Liam Rodriguez", "Sophia Thompson", "Jackson Lewis", "Ava Clark", "Lucas Walker",
        "Mia Hall", "Oliver Allen", "Charlotte Young", "Carter King", "Amelia Wright",
        "Grayson Lopez", "Harper Hill", "Hudson Scott", "Evelyn Green", "Landon Adams",
        "Addison Baker", "Wyatt Nelson", "Aubrey Carter", "Sebastian Mitchell", "Scarlett Roberts",
        "Owen Turner", "Chloe Phillips", "Eli Campbell", "Grace Parker", "Cameron Evans",
        "Lily Edwards", "Nolan Collins", "Zoe Stewart", "Colton Morris", "Hannah Murphy",
        "Hunter Cook", "Ella Rogers", "Parker Morgan", "Avery Peterson", "Carson Cooper",
        "Riley Bailey", "Bentley Reed", "Layla Bell", "Brody Ward", "Aria Torres",
        "Easton Powell", "Paisley Russell", "Ryder Foster", "Savannah Henderson", "Cooper Perry",
        "Brooklyn Butler", "Jaxon Washington", "Bella Price", "Lincoln Bennett", "Maya Wood",
        "Asher Barnes", "Kinsley Ross", "Sawyer Long", "Kaylee Watson", "Gavin Gray",
        "Madelyn Coleman", "Dominic Jenkins", "Aaliyah Patterson", "Austin Ramirez", "Ellie Hughes"
    ],

    "2005-2009": [
        # Late 2000s - Social media era names
        "Mason Taylor", "Emma Johnson", "Liam Brown", "Olivia Smith", "Noah Davis",
        "Sophia Miller", "Ethan Anderson", "Isabella Wilson", "Aiden Martinez", "Mia Garcia",
        "Jackson Rodriguez", "Charlotte Thompson", "Lucas Lewis", "Amelia Clark", "Oliver Walker",
        "Ava Hall", "Elijah Allen", "Harper Young", "Logan King", "Evelyn Wright",
        "Carter Lopez", "Abigail Hill", "Jayden Scott", "Emily Green", "Wyatt Adams",
        "Madison Baker", "Owen Nelson", "Ella Carter", "Gabriel Mitchell", "Scarlett Roberts",
        "Matthew Turner", "Grace Phillips", "Jaxon Campbell", "Chloe Parker", "Ryan Evans",
        "Lily Edwards", "Nathan Collins", "Zoe Stewart", "Isaac Morris", "Layla Murphy",
        "Hunter Cook", "Aubrey Rogers", "Christian Morgan", "Addison Peterson", "Landon Cooper",
        "Brooklyn Bailey", "Jonathan Reed", "Bella Bell", "Dylan Ward", "Hannah Torres",
        "Caleb Powell", "Avery Russell", "Austin Foster", "Leah Henderson", "Connor Perry",
        "Savannah Butler", "Jeremiah Washington", "Aria Price", "Cameron Bennett", "Riley Wood",
        "Julian Barnes", "Paisley Ross", "Aaron Long", "Nora Watson", "Tyler Gray",
        "Madelyn Coleman", "Luke Jenkins", "Aaliyah Patterson", "Colton Ramirez", "Ellie Hughes"
    ],

    "2010-2014": [
        # Early 2010s - Instagram era names
        "Liam Smith", "Emma Johnson", "Noah Brown", "Olivia Williams", "Oliver Davis",
        "Ava Miller", "Elijah Anderson", "Sophia Wilson", "William Martinez", "Isabella Garcia",
        "James Rodriguez", "Mia Thompson", "Benjamin Lewis", "Charlotte Clark", "Lucas Walker",
        "Amelia Hall", "Mason Allen", "Harper Young", "Ethan King", "Evelyn Wright",
        "Alexander Lopez", "Abigail Hill", "Michael Scott", "Emily Green", "Daniel Adams",
        "Madison Baker", "Henry Nelson", "Ella Carter", "Jackson Mitchell", "Scarlett Roberts",
        "Sebastian Turner", "Grace Phillips", "David Campbell", "Chloe Parker", "Joseph Evans",
        "Lily Edwards", "Owen Collins", "Zoe Stewart", "Samuel Morris", "Layla Murphy",
        "Matthew Cook", "Aubrey Rogers", "Wyatt Morgan", "Hannah Peterson", "Jayden Cooper",
        "Addison Bailey", "John Reed", "Bella Bell", "Carter Ward", "Aria Torres",
        "Luke Powell", "Leah Russell", "Gabriel Foster", "Savannah Henderson", "Anthony Perry",
        "Brooklyn Butler", "Dylan Washington", "Nora Price", "Isaac Bennett", "Riley Wood",
        "Christopher Barnes", "Paisley Ross", "Joshua Long", "Aaliyah Watson", "Andrew Gray",
        "Madelyn Coleman", "Nathan Jenkins", "Kinsley Patterson", "Ryan Ramirez", "Ellie Hughes"
    ],

    "2015-2019": [
        # Late 2010s - Unique names era
        "Oliver Chen", "Luna Martinez", "Mateo Rodriguez", "Aurora Smith", "Kai Johnson",
        "Nova Brown", "Ezra Williams", "Willow Davis", "River Miller", "Hazel Anderson",
        "Atlas Wilson", "Ivy Garcia", "Phoenix Thompson", "Sage Lewis", "Rowan Clark",
        "Juniper Walker", "Felix Hall", "Iris Allen", "Jasper Young", "Violet King",
        "Arlo Wright", "Poppy Lopez", "Milo Hill", "Daisy Scott", "Finn Green",
        "Rose Adams", "Leo Baker", "Flora Nelson", "Silas Carter", "Ruby Mitchell",
        "Oscar Roberts", "Pearl Turner", "Hugo Phillips", "Opal Campbell", "Atticus Parker",
        "Jade Evans", "Theodore Edwards", "Coral Collins", "August Stewart", "Maple Morris",
        "Bodhi Murphy", "Clover Cook", "Cassius Rogers", "Meadow Morgan", "Orion Peterson",
        "Rain Cooper", "Zephyr Bailey", "Sky Reed", "Arrow Bell", "Storm Ward",
        "Forest Torres", "Ocean Powell", "Fox Russell", "River Foster", "Wolf Henderson",
        "Moon Perry", "Bear Butler", "Star Washington", "Hawk Price", "Snow Bennett",
        "Eagle Wood", "Dawn Barnes", "Blaze Ross", "Winter Long", "Stone Watson",
        "Summer Gray", "Ridge Coleman", "Autumn Jenkins", "Canyon Patterson", "Spring Ramirez"
    ],

    "2020-2024": [
        # Early 2020s - Pandemic era names
        "Luca Martin", "Luna Patel", "Kai Chen", "Nova Kim", "Zion Singh",
        "Aurora Lee", "River Wong", "Aria Zhang", "Phoenix Liu", "Ivy Park",
        "Atlas Nguyen", "Sage Sharma", "Orion Das", "Willow Kumar", "Neo Gupta",
        "Stella Moon", "Axel Storm", "Maya Ray", "Jax Fox", "Ava Sky",
        "Ezra Cloud", "Nora Sun", "Leo Star", "Zara Dawn", "Max Light",
        "Cora Blaze", "Rex Knight", "Eva Rose", "Zane Wolf", "Mia Dream",
        "Cruz Phoenix", "Ella Hope", "Knox Brave", "Ada Grace", "Onyx Strong",
        "Ruby Faith", "Ace Power", "Pearl Joy", "Blaze Wild", "Jade Peace",
        "Hawk Freedom", "Rose Love", "Wolf Spirit", "Lily Truth", "Bear Heart",
        "Iris Soul", "Fox Mind", "Violet Zen", "Stone River", "Daisy Wave",
        "Ridge Mountain", "Poppy Field", "Canyon Desert", "Flora Garden", "Storm Ocean",
        "Winter Snow", "Summer Rain", "Spring Bloom", "Autumn Leaf", "Dawn Light",
        "Dusk Shadow", "Echo Sound", "Zen Calm", "Cosmo Space", "Tesla Spark"
    ],

    "2025-2030": [
        # Late 2020s - Future/AI era names
        "Zephyr Nova", "Aria Quantum", "Orion Nexus", "Luna Ray", "Phoenix Blaze",
        "Stella Mars", "Neo Vector", "Aurora Sky", "Atlas Storm", "Sage Cosmos",
        "River Cloud", "Nova Star", "Echo Prime", "Zen Matrix", "Kai Fusion",
        "Iris Pixel", "Leo Cipher", "Maya Code", "Rex Binary", "Eva Neural",
        "Jax Cyber", "Nora Digital", "Max Quantum", "Zara Photon", "Axel Sonic",
        "Cora Laser", "Cruz Neon", "Ada Virtual", "Knox Techno", "Ruby Crystal",
        "Onyx Carbon", "Pearl Silicon", "Ace Titanium", "Jade Chrome", "Blaze Plasma",
        "Hawk Electron", "Rose Proton", "Wolf Neutron", "Lily Atom", "Bear Molecule",
        "Fox Element", "Violet Spectrum", "Stone Terra", "Daisy Flora", "Ridge Geo",
        "Canyon Solar", "Storm Thunder", "Winter Frost", "Summer Heat", "Spring Growth",
        "Autumn Change", "Dawn Future", "Dusk Past", "Echo Memory", "Zen Balance",
        "Cosmo Universe", "Tesla Energy", "Darwin Evolution", "Vega Star", "Apollo Mission",
        "Artemis Moon", "Mars Red", "Venus Green", "Jupiter Giant", "Saturn Ring"
    ]
}


def get_names_for_year(year: int, count: int = 10) -> List[str]:
    """
    Get appropriate names for a specific year

    Args:
        year: The year to get names for
        count: Number of names to return

    Returns:
        List of period-appropriate names
    """
    # Find the appropriate period for the year
    period = None
    for period_key in PERIOD_NAMES.keys():
        start_year, end_year = map(int, period_key.split('-'))
        if start_year <= year <= end_year:
            period = period_key
            break

    if not period:
        # Default to 1990s if year is out of range
        if year < 1970:
            period = "1970-1974"
        elif year > 2030:
            period = "2025-2030"
        else:
            period = "1990-1994"

    names = PERIOD_NAMES[period]

    # Return random selection of names
    if len(names) >= count:
        return random.sample(names, count)
    else:
        # If we need more names than available, repeat some
        result = names.copy()
        while len(result) < count:
            result.append(random.choice(names))
        return result[:count]


def get_all_period_names() -> dict:
    """
    Get all period names

    Returns:
        Dictionary of all period names
    """
    return PERIOD_NAMES


def get_total_names() -> int:
    """
    Get total number of names in database

    Returns:
        Total count of all names
    """
    return sum(len(names) for names in PERIOD_NAMES.values())


# Test function
if __name__ == "__main__":
    print("Game Names Database")
    print("=" * 60)

    total = get_total_names()
    print(f"Total names in database: {total}")
    print()

    # Show summary by period
    for period, names in PERIOD_NAMES.items():
        print(f"{period}: {len(names)} names")
        print(f"  Examples: {', '.join(names[:5])}")

    print("\n" + "=" * 60)
    print("Testing year-based retrieval:")
    print("=" * 60)

    test_years = [1972, 1978, 1985, 1992, 1999, 2005, 2015, 2025]
    for year in test_years:
        names = get_names_for_year(year, 5)
        print(f"{year}: {', '.join(names)}")