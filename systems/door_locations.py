import random
from datetime import datetime, time, timedelta
from enum import Enum
from typing import Dict, List, Optional, Tuple

class DayOfWeek(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

class Location:
    """Base class for all door locations"""
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.npc_pool = []  # List of NPC IDs that can be found here

    def is_available(self, game_date: datetime) -> Tuple[bool, str]:
        """Check if location is available at given date/time
        Returns (is_available, reason_if_not)"""
        return False, "Location not configured"

    def visit(self, game_state: Dict) -> Dict:
        """Execute the visit action and return results"""
        return {"success": False, "message": "Not implemented"}

class ConferenceLocation(Location):
    """GDC, E3, local gamedev meetups - Last weekend of each quarter"""
    def __init__(self):
        super().__init__(
            "Conference",
            "Industry conferences and gamedev meetups - Last weekend of March, June, September, December"
        )
        self.npc_pool = list(range(1, 21))  # Can meet any NPC at conferences

    def is_available(self, game_date: datetime) -> Tuple[bool, str]:
        month = game_date.month
        day = game_date.day

        # Check if it's a quarter-end month
        if month not in [3, 6, 9, 12]:
            return False, "Conferences only happen in March, June, September, and December"

        # Find last weekend of the month
        # Get last day of month
        if month == 12:
            next_month = game_date.replace(year=game_date.year + 1, month=1, day=1)
        else:
            next_month = game_date.replace(month=month + 1, day=1)
        last_day = next_month - timedelta(days=1)

        # Find last Sunday
        days_until_sunday = (last_day.weekday() + 1) % 7
        last_sunday = last_day - timedelta(days=days_until_sunday)
        last_saturday = last_sunday - timedelta(days=1)
        last_friday = last_sunday - timedelta(days=2)

        # Check if current date is in the last weekend
        if game_date.date() in [last_friday.date(), last_saturday.date(), last_sunday.date()]:
            return True, ""

        return False, f"Conference weekend is {last_friday.strftime('%b %d')}-{last_sunday.strftime('%d')}"

class ArcadeLocation(Location):
    """Local arcade, retro gaming store - Friday morning through Sunday afternoon"""
    def __init__(self):
        super().__init__(
            "Arcade",
            "Local arcade and retro gaming store - Open Friday morning through Sunday afternoon"
        )
        self.npc_pool = [1, 3, 4, 7, 11, 17]  # Game designers, artists, gameplay programmers

    def is_available(self, game_date: datetime) -> Tuple[bool, str]:
        weekday = game_date.weekday()
        hour = game_date.hour

        # Friday (4) from 8am onwards
        if weekday == DayOfWeek.FRIDAY.value and hour >= 8:
            return True, ""
        # Saturday (5) all day
        elif weekday == DayOfWeek.SATURDAY.value:
            return True, ""
        # Sunday (6) until 6pm
        elif weekday == DayOfWeek.SUNDAY.value and hour < 18:
            return True, ""

        return False, "Arcade is open Friday 8am through Sunday 6pm"

class UniversityLocation(Location):
    """University for training - Tuesday and Thursday nights"""
    def __init__(self):
        super().__init__(
            "University",
            "Campus for guest lectures and training - Tuesday and Thursday nights (6pm-10pm)"
        )
        self.npc_pool = [2, 5, 8, 9, 13, 20]  # Engineers, researchers, architects

    def is_available(self, game_date: datetime) -> Tuple[bool, str]:
        weekday = game_date.weekday()
        hour = game_date.hour

        if weekday in [DayOfWeek.TUESDAY.value, DayOfWeek.THURSDAY.value]:
            if 18 <= hour <= 22:
                return True, ""
            return False, "University training is 6pm-10pm"

        return False, "University training only on Tuesday and Thursday nights"

    def visit(self, game_state: Dict) -> Dict:
        """Training increases a random skill for the player"""
        skills = ["engineering", "marketing", "leadership", "design", "research", "communication"]
        skill_to_train = random.choice(skills)

        # Advance time by 4 hours
        game_state["current_time"] += timedelta(hours=4)

        return {
            "success": True,
            "message": f"Attended training session. Improved {skill_to_train} knowledge!",
            "skill_trained": skill_to_train,
            "time_spent": 4
        }

class RealtorOfficeLocation(Location):
    """Realtor office to see properties - Weekday mornings"""
    def __init__(self):
        super().__init__(
            "Realtor Office",
            "Browse available office spaces - Weekday mornings (8am-12pm)"
        )
        self.npc_pool = []  # No NPCs here, just property viewing

    def is_available(self, game_date: datetime) -> Tuple[bool, str]:
        weekday = game_date.weekday()
        hour = game_date.hour

        if weekday < DayOfWeek.FRIDAY.value:  # Monday-Thursday
            if 8 <= hour < 12:
                return True, ""
            return False, "Realtor office is open 8am-12pm"

        return False, "Realtor office only open weekday mornings"

class ElectronicsStoreLocation(Location):
    """Electronics store for office upgrades - Saturdays only"""
    def __init__(self):
        super().__init__(
            "Electronics Store",
            "Buy office equipment upgrades - Saturdays only"
        )
        self.npc_pool = [12, 14, 15]  # Hardware engineers, firmware devs

    def is_available(self, game_date: datetime) -> Tuple[bool, str]:
        weekday = game_date.weekday()

        if weekday == DayOfWeek.SATURDAY.value:
            return True, ""

        return False, "Electronics store only open on Saturdays"

class GymLocation(Location):
    """Gym for hygiene boost - Monday mornings only"""
    def __init__(self):
        super().__init__(
            "Gym",
            "Work out to maximize hygiene for one week - Monday mornings (8am-10am)"
        )
        self.npc_pool = [18]  # Project managers who value discipline

    def is_available(self, game_date: datetime) -> Tuple[bool, str]:
        weekday = game_date.weekday()
        hour = game_date.hour

        if weekday == DayOfWeek.MONDAY.value:
            if 8 <= hour <= 10:
                return True, ""
            return False, "Gym sessions are 8am-10am"

        return False, "Gym only available Monday mornings"

    def visit(self, game_state: Dict) -> Dict:
        """Gym visit maxes hygiene for a week and advances time 4 hours"""
        game_state["hygiene"] = 100
        game_state["hygiene_boost_until"] = game_state["current_time"] + timedelta(days=7)
        game_state["current_time"] += timedelta(hours=4)

        return {
            "success": True,
            "message": "Great workout! Hygiene maximized for one week.",
            "time_spent": 4,
            "effect_duration": 7
        }

class LibraryLocation(Location):
    """Library for finding talent - Tuesday mornings"""
    def __init__(self):
        super().__init__(
            "Library",
            "Quiet place to find studious talent - Tuesday mornings"
        )
        self.npc_pool = [2, 5, 8, 9, 10, 13, 19, 20]  # Researchers, analysts, engineers

    def is_available(self, game_date: datetime) -> Tuple[bool, str]:
        weekday = game_date.weekday()
        hour = game_date.hour

        if weekday == DayOfWeek.TUESDAY.value:
            if 8 <= hour < 12:
                return True, ""
            return False, "Library talent scouting is morning only"

        return False, "Library talent scouting only on Tuesday mornings"

class HackerMeetupLocation(Location):
    """Hacker meetup for finding talent - Friday nights"""
    def __init__(self):
        super().__init__(
            "Hacker Meetup",
            "Underground coding meetup - Friday nights (8pm-2am)"
        )
        self.npc_pool = [2, 5, 6, 8, 12, 14, 20]  # Programmers, hardware folks, tools devs

    def is_available(self, game_date: datetime) -> Tuple[bool, str]:
        weekday = game_date.weekday()
        hour = game_date.hour

        if weekday == DayOfWeek.FRIDAY.value:
            if hour >= 20:  # 8pm onwards
                return True, ""
        elif weekday == DayOfWeek.SATURDAY.value:
            if hour <= 2:  # Until 2am Saturday morning
                return True, ""

        return False, "Hacker meetup only Friday nights (8pm-2am)"

class BankLocation(Location):
    """Bank for loans - chance to meet NPCs when taking loans"""
    def __init__(self):
        super().__init__(
            "Bank",
            "Financial services and loans - Weekdays 9am-5pm"
        )
        self.npc_pool = [10, 16, 18]  # Business-minded NPCs

    def is_available(self, game_date: datetime) -> Tuple[bool, str]:
        weekday = game_date.weekday()
        hour = game_date.hour

        if weekday < DayOfWeek.FRIDAY.value:  # Monday-Thursday
            if 9 <= hour < 17:
                return True, ""
            return False, "Bank hours are 9am-5pm"

        return False, "Bank only open on weekdays"

    def visit(self, game_state: Dict) -> Dict:
        """Bank visit for loans, with chance to meet NPCs"""
        result = {
            "success": True,
            "message": "Visited the bank.",
            "action_available": "loan"
        }

        # If taking a loan, chance to meet an NPC
        if game_state.get("taking_loan", False):
            if random.random() < 0.3:  # 30% chance when taking loan
                result["npc_encounter"] = random.choice(self.npc_pool)

        return result

class BarLocation(Location):
    """Bar for casual encounters - Evenings and weekends"""
    def __init__(self):
        super().__init__(
            "Bar",
            "Local developer hangout - Evenings after 5pm and weekends"
        )
        self.npc_pool = list(range(1, 21))  # Anyone could be at the bar

    def is_available(self, game_date: datetime) -> Tuple[bool, str]:
        weekday = game_date.weekday()
        hour = game_date.hour

        # Weekends - all day
        if weekday in [DayOfWeek.FRIDAY.value, DayOfWeek.SATURDAY.value, DayOfWeek.SUNDAY.value]:
            if weekday == DayOfWeek.FRIDAY.value and hour < 17:
                return False, "Bar opens at 5pm on Fridays"
            return True, ""

        # Weekdays - after 5pm
        if hour >= 17:
            return True, ""

        return False, "Bar opens at 5pm on weekdays"

class SpecialEncounterLocation(Location):
    """Special encounter types that can happen under certain conditions"""
    pass

class FriendReferralLocation(SpecialEncounterLocation):
    """Friend of a current employee refers someone"""
    def __init__(self):
        super().__init__(
            "Friend Referral",
            "A team member recommends a friend"
        )
        self.npc_pool = list(range(1, 21))

    def is_available(self, game_date: datetime) -> Tuple[bool, str]:
        # This is triggered by having employees with high morale
        return False, "Triggered by employee referrals"

class HeadhunterLocation(SpecialEncounterLocation):
    """Recruitment agency contact"""
    def __init__(self):
        super().__init__(
            "Headhunter",
            "Professional recruitment agency"
        )
        self.npc_pool = list(range(1, 21))

    def is_available(self, game_date: datetime) -> Tuple[bool, str]:
        # Available when you have budget for hiring
        return True, ""

class BankruptcyAuctionLocation(SpecialEncounterLocation):
    """Failed studio's talent available"""
    def __init__(self):
        super().__init__(
            "Bankruptcy Auction",
            "Talent from failed studios"
        )
        self.npc_pool = list(range(1, 21))

    def is_available(self, game_date: datetime) -> Tuple[bool, str]:
        # Random event when other studios fail
        return False, "Triggered by studio failures in the industry"

class NewspaperAdLocation(SpecialEncounterLocation):
    """Help wanted ads"""
    def __init__(self):
        super().__init__(
            "Newspaper Ad",
            "Classified ads for talent"
        )
        self.npc_pool = list(range(1, 21))

    def is_available(self, game_date: datetime) -> Tuple[bool, str]:
        # Available any time for a cost
        return True, ""

class DreamLocation(SpecialEncounterLocation):
    """Dream sequences for special encounters"""
    def __init__(self):
        super().__init__(
            "Dream",
            "Strange dreams reveal hidden talent"
        )
        self.npc_pool = [1, 3, 7, 11]  # Creative types appear in dreams

    def is_available(self, game_date: datetime) -> Tuple[bool, str]:
        # Random chance when sleeping/resting
        return False, "Happens randomly during rest"

class OnlineLocation(SpecialEncounterLocation):
    """Online forums and BBS for finding talent"""
    def __init__(self):
        super().__init__(
            "Online",
            "BBS and early internet forums"
        )
        self.npc_pool = list(range(1, 21))  # Anyone can be found online

    def is_available(self, game_date: datetime) -> Tuple[bool, str]:
        # Available after certain year (1985+)
        if game_date.year >= 1985:
            return True, ""
        return False, "Online connections not available before 1985"

class MakingGameLocation(SpecialEncounterLocation):
    """Meet NPCs while making a game together"""
    def __init__(self):
        super().__init__(
            "Making a Game",
            "Collaborate and meet talent during development"
        )
        self.npc_pool = list(range(1, 21))

    def is_available(self, game_date: datetime) -> Tuple[bool, str]:
        # Available when actively developing a game
        return False, "Triggered during game development"

class DoorSystem:
    """Manages all door locations and NPC encounters"""

    def __init__(self, game_state: Dict):
        self.game_state = game_state
        self.locations = {
            "conference": ConferenceLocation(),
            "arcade": ArcadeLocation(),
            "university": UniversityLocation(),
            "realtor": RealtorOfficeLocation(),
            "electronics": ElectronicsStoreLocation(),
            "gym": GymLocation(),
            "library": LibraryLocation(),
            "hacker": HackerMeetupLocation(),
            "bank": BankLocation(),
            "bar": BarLocation(),
            "friend_referral": FriendReferralLocation(),
            "headhunter": HeadhunterLocation(),
            "bankruptcy": BankruptcyAuctionLocation(),
            "newspaper": NewspaperAdLocation(),
            "dream": DreamLocation(),
            "online": OnlineLocation(),
            "making_game": MakingGameLocation()
        }

        # Track unlocked NPCs across all playthroughs
        if "permanent_unlocked_npcs" not in game_state:
            game_state["permanent_unlocked_npcs"] = []

    def get_available_locations(self, current_date: datetime) -> List[Dict]:
        """Get list of currently available locations"""
        available = []

        for key, location in self.locations.items():
            is_available, reason = location.is_available(current_date)
            if is_available:
                available.append({
                    "key": key,
                    "name": location.name,
                    "description": location.description
                })

        return available

    def visit_location(self, location_key: str) -> Dict:
        """Visit a location and potentially meet an NPC"""
        if location_key not in self.locations:
            return {"success": False, "message": "Invalid location"}

        location = self.locations[location_key]
        current_date = self.game_state.get("current_time", datetime.now())

        is_available, reason = location.is_available(current_date)
        if not is_available:
            return {"success": False, "message": reason}

        # Base visit result
        result = location.visit(self.game_state)

        # Check for NPC encounter
        if location.npc_pool:
            encounter_roll = random.random()

            # Different encounter rates for different locations
            encounter_rates = {
                "conference": 0.8,  # Very likely at conferences
                "arcade": 0.4,
                "university": 0.5,
                "library": 0.3,
                "hacker": 0.6,
                "bar": 0.3,
                "bank": 0.2,
                "electronics": 0.2,
                "gym": 0.1,
                "online": 0.4,
                "making_game": 0.7,
                "friend_referral": 0.9,
                "headhunter": 0.95,
                "bankruptcy": 0.85,
                "newspaper": 0.5,
                "dream": 0.5
            }

            encounter_chance = encounter_rates.get(location_key, 0.3)

            if encounter_roll < encounter_chance:
                npc_id = random.choice(location.npc_pool)
                result["npc_encountered"] = npc_id

                # 5% chance to permanently unlock this NPC
                if random.random() < 0.05:
                    if npc_id not in self.game_state["permanent_unlocked_npcs"]:
                        self.game_state["permanent_unlocked_npcs"].append(npc_id)
                        result["npc_permanently_unlocked"] = True
                        result["message"] += f" You've formed a lasting connection!"

        return result

    def get_location_schedule(self) -> Dict:
        """Get a weekly schedule of when locations are available"""
        schedule = {
            "Monday": {
                "morning": ["realtor", "gym", "bank"],
                "afternoon": ["bank"],
                "evening": ["bar"],
                "night": []
            },
            "Tuesday": {
                "morning": ["realtor", "library", "bank"],
                "afternoon": ["bank"],
                "evening": ["bar"],
                "night": ["university"]
            },
            "Wednesday": {
                "morning": ["realtor", "bank"],
                "afternoon": ["bank"],
                "evening": ["bar"],
                "night": []
            },
            "Thursday": {
                "morning": ["realtor", "bank"],
                "afternoon": ["bank"],
                "evening": ["bar"],
                "night": ["university"]
            },
            "Friday": {
                "morning": ["arcade", "bank"],
                "afternoon": ["arcade", "bank"],
                "evening": ["arcade", "bar"],
                "night": ["arcade", "bar", "hacker"]
            },
            "Saturday": {
                "morning": ["arcade", "electronics"],
                "afternoon": ["arcade", "electronics"],
                "evening": ["arcade", "bar", "electronics"],
                "night": ["arcade", "bar"]
            },
            "Sunday": {
                "morning": ["arcade"],
                "afternoon": ["arcade"],
                "evening": ["bar"],
                "night": ["bar"]
            }
        }

        # Add special quarterly conference weekends
        schedule["special"] = {
            "conference": "Last weekend of March, June, September, December",
            "online": "Available after 1985",
            "dream": "Random during rest",
            "making_game": "During active development",
            "friend_referral": "When employees have high morale",
            "bankruptcy": "When studios fail",
            "headhunter": "When you have hiring budget",
            "newspaper": "Anytime for a fee"
        }

        return schedule