"""
Game Development System
Handles game development phases, scoring, and rating
"""

import random
import csv
import os
from enum import Enum
from dataclasses import dataclass
from typing import Dict, Tuple, Optional, List
from .game_combinations import CombinationRatingSystem

class GameRating(Enum):
    """Game rating tiers based on total score"""
    MASTERPIECE = "Masterpiece"
    LEGENDARY = "Legendary"
    OUTSTANDING = "Outstanding"
    EXCELLENT = "Excellent"
    NOTABLE = "Notable"
    GOOD = "Good"
    FUN = "Fun"
    DECENT = "Decent"
    MEH = "Meh..."
    POOR = "Poor"

@dataclass
class GameScore:
    """Represents the scores for a game in development"""
    gameplay: int = 0
    technical: int = 0
    graphics: int = 0
    innovation: int = 0
    sound_audio: int = 0
    story: int = 0

    @property
    def total(self) -> int:
        """Calculate total score"""
        return (self.gameplay + self.technical + self.graphics +
                self.innovation + self.sound_audio + self.story)

    @property
    def average(self) -> float:
        """Calculate average score across all categories"""
        return self.total / 6

    def to_dict(self) -> Dict[str, int]:
        """Convert to dictionary"""
        return {
            'gameplay': self.gameplay,
            'technical': self.technical,
            'graphics': self.graphics,
            'innovation': self.innovation,
            'sound_audio': self.sound_audio,
            'story': self.story,
            'total': self.total
        }


class GameDevelopment:
    """Handles game development mechanics and scoring"""

    def __init__(self, game_data):
        self.game_data = game_data

        # Load rating thresholds from CSV
        self.rating_thresholds_by_year = self._load_rating_thresholds()

        # Default rating thresholds (year 1984) as fallback
        self.default_rating_thresholds = {
            GameRating.MASTERPIECE: {'min_total': 180, 'min_avg': 30},  # 30+ in all categories
            GameRating.LEGENDARY: {'min_total': 165, 'min_avg': 27.5},
            GameRating.OUTSTANDING: {'min_total': 150, 'min_avg': 25},
            GameRating.EXCELLENT: {'min_total': 135, 'min_avg': 22.5},
            GameRating.NOTABLE: {'min_total': 120, 'min_avg': 20},
            GameRating.GOOD: {'min_total': 105, 'min_avg': 17.5},
            GameRating.FUN: {'min_total': 90, 'min_avg': 15},
            GameRating.DECENT: {'min_total': 75, 'min_avg': 12.5},
            GameRating.MEH: {'min_total': 60, 'min_avg': 10},
            GameRating.POOR: {'min_total': 0, 'min_avg': 0}
        }

    def _load_rating_thresholds(self) -> Dict[int, Dict[GameRating, Dict[str, float]]]:
        """Load rating thresholds from CSV file"""
        thresholds_by_year = {}
        csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'rating_thresholds.csv')

        if not os.path.exists(csv_path):
            return thresholds_by_year

        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    year = int(row['year'])
                    rating_name = row['rating'].upper()

                    # Find matching GameRating enum
                    rating_enum = None
                    for rating in GameRating:
                        if rating.value.upper() == rating_name or rating.name == rating_name:
                            rating_enum = rating
                            break

                    if rating_enum:
                        if year not in thresholds_by_year:
                            thresholds_by_year[year] = {}

                        thresholds_by_year[year][rating_enum] = {
                            'min_total': float(row['min_total_score']),
                            'min_avg': float(row['min_avg_score']),
                            'description': row.get('description', '')
                        }
        except Exception as e:
            print(f"Error loading rating thresholds from CSV: {e}")

        return thresholds_by_year

    def develop_game(self, game_name: str, game_type: str, game_topic: str,
                     lead_developer: str, engine: str = "OpenEngine") -> GameScore:
        """
        Develop a game and generate scores for each category

        Returns:
            GameScore object with points for each category
        """
        # Base range for random points (will be modified by various factors)
        base_min = 5
        base_max = 15

        # Get current year to adjust expectations
        current_year = self._get_current_year()

        # Adjust based on year (games get harder to impress as time goes on)
        year_modifier = self._get_year_modifier(current_year)

        # Developer skill modifier (for now, just player gets a small bonus)
        dev_modifier = 5 if lead_developer == "You (Player)" else 0

        # Game type modifiers for different categories
        type_modifiers = self._get_type_modifiers(game_type)

        # Topic modifiers
        topic_modifiers = self._get_topic_modifiers(game_topic)

        # Get combination rating modifier
        combo_modifier = CombinationRatingSystem.get_score_modifier(game_type, game_topic)
        combo_rating = CombinationRatingSystem.get_combination_rating(game_type, game_topic)
        combo_description = CombinationRatingSystem.get_rating_description(combo_rating)

        # Log the combination rating
        print(f"\n[COMBINATION] {game_type} + {game_topic}: {combo_rating}/5 - {combo_description}")
        print(f"[COMBINATION] Score modifier: {combo_modifier:+d}")

        # Generate scores for each category
        score = GameScore()

        # Calculate each category with modifiers and randomness
        # Apply combination modifier to all categories
        score.gameplay = self._generate_category_score(
            base_min + dev_modifier + type_modifiers.get('gameplay', 0) + topic_modifiers.get('gameplay', 0) + combo_modifier,
            base_max + dev_modifier + type_modifiers.get('gameplay', 0) + topic_modifiers.get('gameplay', 0) + combo_modifier
        )

        score.technical = self._generate_category_score(
            base_min + dev_modifier + type_modifiers.get('technical', 0) + combo_modifier,
            base_max + dev_modifier + type_modifiers.get('technical', 0) + combo_modifier
        )

        score.graphics = self._generate_category_score(
            base_min + dev_modifier + type_modifiers.get('graphics', 0) + topic_modifiers.get('graphics', 0) + combo_modifier,
            base_max + dev_modifier + type_modifiers.get('graphics', 0) + topic_modifiers.get('graphics', 0) + combo_modifier
        )

        score.innovation = self._generate_category_score(
            base_min + type_modifiers.get('innovation', 0) + topic_modifiers.get('innovation', 0) + combo_modifier,
            base_max + type_modifiers.get('innovation', 0) + topic_modifiers.get('innovation', 0) + combo_modifier
        )

        score.sound_audio = self._generate_category_score(
            base_min + type_modifiers.get('sound_audio', 0) + topic_modifiers.get('sound_audio', 0) + combo_modifier,
            base_max + type_modifiers.get('sound_audio', 0) + topic_modifiers.get('sound_audio', 0) + combo_modifier
        )

        score.story = self._generate_category_score(
            base_min + type_modifiers.get('story', 0) + topic_modifiers.get('story', 0) + combo_modifier,
            base_max + type_modifiers.get('story', 0) + topic_modifiers.get('story', 0) + combo_modifier
        )

        # Apply year modifier to all scores
        score = self._apply_year_modifier(score, year_modifier)

        return score

    def _generate_category_score(self, min_val: int, max_val: int) -> int:
        """Generate a random score for a category with some variance"""
        # Ensure min and max are valid
        min_val = max(1, min_val)
        max_val = max(min_val + 1, max_val)

        # Generate base score
        base_score = random.randint(min_val, max_val)

        # Add some variance for excitement (small chance of critical success/failure)
        crit_roll = random.random()
        if crit_roll < 0.05:  # 5% chance of critical failure
            base_score = max(1, base_score - random.randint(5, 10))
        elif crit_roll > 0.95:  # 5% chance of critical success
            base_score = min(50, base_score + random.randint(5, 10))

        # Cap at reasonable limits for early game
        return min(40, max(1, base_score))

    def _get_type_modifiers(self, game_type: str) -> Dict[str, int]:
        """Get score modifiers based on game type"""
        modifiers = {
            'Text Adventure': {'story': 15, 'innovation': 5, 'graphics': -10},
            'Arcade': {'gameplay': 12, 'sound_audio': 5, 'technical': -3},
            'Platformer': {'gameplay': 10, 'technical': 3, 'sound_audio': 3},
            'Puzzle': {'gameplay': 10, 'innovation': 5, 'technical': -2},
            'Shooter': {'gameplay': 8, 'technical': 5, 'sound_audio': 5},
            'RPG': {'gameplay': 5, 'story': 10, 'innovation': 3},
            'Simulation': {'technical': 8, 'innovation': 5, 'gameplay': 3},
            # Commented out - not in active game types
            # 'Racing': {'technical': 8, 'graphics': 5, 'sound_audio': 5},
            # 'Fighting': {'gameplay': 8, 'technical': 5, 'graphics': 5},
            # 'Adventure': {'story': 8, 'gameplay': 5, 'graphics': 3},
            # 'Action': {'gameplay': 8, 'technical': 5, 'graphics': 5},
            # 'Strategy': {'gameplay': 7, 'technical': 5, 'innovation': 3},
            # 'Online': {'technical': -5, 'gameplay': -5, 'innovation': 8},  # negative due to connection issues
            # 'Visual Novel': {'story': 12, 'graphics': 5, 'gameplay': 2},
            # 'Educational': {'innovation': 10, 'gameplay': 5, 'story': 3}
        }
        return modifiers.get(game_type, {})

    def _get_topic_modifiers(self, game_topic: str) -> Dict[str, int]:
        """Get score modifiers based on game topic"""
        modifiers = {
            # Active Topics
            'Table Tennis': {'gameplay': 8, 'technical': 2},
            'Fantasy': {'story': 5, 'graphics': 3, 'innovation': 2},
            'Space': {'innovation': 5, 'graphics': 5},
            'Temple': {'story': 3, 'graphics': 4, 'gameplay': 3},
            'Zombies': {'sound_audio': 5, 'graphics': 3},
            'Postal Work': {'gameplay': 4, 'story': 2},
            'Questing Heroes': {'story': 6, 'gameplay': 5, 'graphics': 4},  # New topic
            'World War II': {'sound_audio': 5, 'technical': 4},
            'City Building': {'technical': 5, 'gameplay': 6},
            'Ocean Exploration': {'graphics': 6, 'sound_audio': 4},
            'Golf': {'gameplay': 5, 'technical': 3},
            'Painting': {'graphics': 8, 'innovation': 3},
            'Bugs': {'innovation': 4, 'graphics': 3},
            # Commented out - not in active topics list
            # 'Vampires': {'story': 5, 'sound_audio': 4, 'graphics': 3},
            # 'Ghosts': {'sound_audio': 6, 'story': 4},
            # 'Haunted Houses': {'sound_audio': 7, 'graphics': 4},
            # 'Psychological Horror': {'sound_audio': 8, 'story': 6},
            # 'Post-Apocalyptic': {'story': 5, 'graphics': 4},
            # 'Space Exploration': {'innovation': 6, 'graphics': 5},
            # 'Alien Invasion': {'sound_audio': 4, 'graphics': 5},
            # 'Cyberpunk': {'innovation': 8, 'graphics': 5, 'technical': 5},
            # 'AI Uprising': {'innovation': 7, 'technical': 5},
            # 'Mechs': {'graphics': 6, 'technical': 5},
            # 'Terraforming': {'innovation': 5, 'technical': 4},
            # 'Galactic Warfare': {'graphics': 5, 'sound_audio': 5},
            # 'Interdimensional Travel': {'innovation': 8, 'story': 4},
            # 'Trucking': {'technical': 4, 'gameplay': 3},
            # 'Farming': {'gameplay': 5, 'graphics': 3},
            # 'Mining': {'technical': 3, 'gameplay': 4},
            # 'Fishing': {'graphics': 4, 'gameplay': 5},
            # 'Logging': {'technical': 3, 'sound_audio': 3},
            # 'Factory Work': {'technical': 4, 'gameplay': 3},
            # 'Emergency Response': {'gameplay': 6, 'sound_audio': 5},
            # 'Oil Drilling': {'technical': 5, 'graphics': 3},
            # 'Dragons': {'graphics': 6, 'story': 5},
            # 'Elves & Dwarves': {'story': 5, 'graphics': 4},
            # 'Magic Schools': {'story': 6, 'innovation': 4},
            # 'Kingdoms & Castles': {'story': 5, 'graphics': 5},
            # 'Gods & Titans': {'graphics': 7, 'story': 6},
            # 'Mythical Creatures': {'graphics': 5, 'story': 4},
            # 'Ancient Ruins': {'story': 5, 'graphics': 4},
            # 'Fairy Tales': {'story': 7, 'graphics': 3},
            # 'Magical Artifacts': {'story': 5, 'innovation': 4},
            # 'Prophecies': {'story': 6, 'gameplay': 3},
            # 'War': {'sound_audio': 5, 'technical': 3, 'graphics': 3},
            # 'Martial Arts': {'gameplay': 6, 'technical': 3},
            # 'Gladiator Arenas': {'gameplay': 5, 'graphics': 4},
            # 'Monster Hunting': {'gameplay': 6, 'graphics': 5},
            # 'Mercenary Missions': {'gameplay': 5, 'story': 3},
            # 'Tactical Infiltration': {'gameplay': 5, 'technical': 5},
            # 'Egypt': {'story': 5, 'graphics': 4},
            # 'Viking': {'story': 4, 'sound_audio': 4},
            # 'Roman Empire': {'story': 5, 'graphics': 4},
            # 'Wild West': {'story': 5, 'sound_audio': 5},
            # 'World War I': {'sound_audio': 5, 'technical': 3},
            # 'Cold War': {'story': 5, 'technical': 3},
            # 'Medieval Europe': {'story': 5, 'graphics': 3},
            # 'Colonial Exploration': {'story': 4, 'gameplay': 4},
            # 'Tribal Societies': {'story': 4, 'sound_audio': 3},
            # 'Dating Sim': {'story': 7, 'graphics': 3},
            # 'High School Drama': {'story': 6, 'gameplay': 3},
            # 'Office': {'gameplay': 4, 'technical': 3},
            # 'Social Media Fame': {'innovation': 5, 'gameplay': 4},
            # 'Fashion Design': {'graphics': 6, 'innovation': 3},
            # 'Restaurant Management': {'gameplay': 5, 'technical': 3},
            # 'Journalism': {'story': 6, 'gameplay': 3},
            # 'Wildlife Rescue': {'graphics': 5, 'gameplay': 4},
            # 'Gardening': {'graphics': 5, 'gameplay': 4},
            # 'Animal': {'graphics': 5, 'gameplay': 4},
            # 'Weather Control': {'innovation': 6, 'graphics': 5},
            # 'Arctic Expeditions': {'graphics': 5, 'sound_audio': 3},
            # 'Cave Diving': {'sound_audio': 5, 'graphics': 4},
            # 'Music Creation': {'sound_audio': 10, 'innovation': 5},
            # 'Dance': {'sound_audio': 6, 'gameplay': 5},
            # 'Poetry': {'story': 8, 'sound_audio': 3},
            # 'Film Production': {'story': 6, 'graphics': 5},
            # 'Photography': {'graphics': 7, 'innovation': 3},
            # 'Fashion': {'graphics': 6, 'innovation': 3},
            # 'Toy Making': {'innovation': 5, 'gameplay': 4},
            # 'Basketball': {'gameplay': 6, 'technical': 4},
            # 'Football': {'gameplay': 6, 'technical': 4},
            # 'Soccer': {'gameplay': 6, 'technical': 3},
            # 'Baseball': {'gameplay': 5, 'technical': 3},
            # 'Tennis': {'gameplay': 6, 'technical': 3},
            # 'Boxing': {'gameplay': 5, 'sound_audio': 4},
            # 'Skateboarding': {'gameplay': 6, 'sound_audio': 5},
            # 'Surfing': {'gameplay': 5, 'graphics': 5},
            # 'Olympics': {'gameplay': 5, 'graphics': 4},
            # 'Volleyball': {'gameplay': 5, 'technical': 3},
            # 'Swimming': {'gameplay': 5, 'graphics': 4},
            # 'Track & Field': {'gameplay': 5, 'technical': 3},
            # 'Ninjas': {'gameplay': 6, 'technical': 3},
            # 'Pirates': {'story': 5, 'sound_audio': 3, 'graphics': 3},
            # 'Dinosaurs': {'graphics': 6, 'sound_audio': 5},
            # 'Robots': {'technical': 6, 'innovation': 5}
        }
        return modifiers.get(game_topic, {})

    def _get_year_modifier(self, year: int) -> float:
        """Get a modifier based on the current year (games get harder to impress over time)"""
        if year <= 1984:
            return 1.0  # Base year, no modifier
        elif year <= 1990:
            return 0.95
        elif year <= 1995:
            return 0.90
        elif year <= 2000:
            return 0.85
        elif year <= 2005:
            return 0.80
        elif year <= 2010:
            return 0.75
        elif year <= 2015:
            return 0.70
        elif year <= 2020:
            return 0.65
        else:
            return 0.60

    def _apply_year_modifier(self, score: GameScore, modifier: float) -> GameScore:
        """Apply year modifier to all score categories"""
        score.gameplay = int(score.gameplay * modifier)
        score.technical = int(score.technical * modifier)
        score.graphics = int(score.graphics * modifier)
        score.innovation = int(score.innovation * modifier)
        score.sound_audio = int(score.sound_audio * modifier)
        score.story = int(score.story * modifier)
        return score

    def _get_current_year(self) -> int:
        """Get the current game year"""
        if 'game_time' in self.game_data.data:
            date_str = self.game_data.data['game_time'].get('current_date', '1984-01-01')
            return int(date_str.split('-')[0])
        return 1984

    def get_game_rating(self, score: GameScore, year: Optional[int] = None) -> GameRating:
        """
        Determine the game's rating based on its scores

        Args:
            score: GameScore object
            year: Optional year for period-specific ratings

        Returns:
            GameRating enum value
        """
        if year is None:
            year = self._get_current_year()

        # Adjust thresholds based on year (will be loaded from CSV later)
        adjusted_thresholds = self._adjust_thresholds_for_year(year)

        # Check each rating tier from best to worst
        for rating in GameRating:
            threshold = adjusted_thresholds.get(rating)
            if threshold:
                if score.total >= threshold['min_total'] and score.average >= threshold['min_avg']:
                    return rating

        return GameRating.POOR

    def _adjust_thresholds_for_year(self, year: int) -> Dict[GameRating, Dict[str, float]]:
        """Get rating thresholds for a specific year from loaded CSV data"""
        # If we have thresholds for this exact year, use them
        if year in self.rating_thresholds_by_year:
            return self.rating_thresholds_by_year[year]

        # Otherwise, find the closest year
        if self.rating_thresholds_by_year:
            available_years = sorted(self.rating_thresholds_by_year.keys())

            # Find the closest year that's not in the future
            closest_year = None
            for available_year in available_years:
                if available_year <= year:
                    closest_year = available_year
                else:
                    break

            # If we found a suitable year, use it
            if closest_year:
                return self.rating_thresholds_by_year[closest_year]

            # If the requested year is before all available years, use the earliest
            if year < available_years[0]:
                return self.rating_thresholds_by_year[available_years[0]]

        # Fallback to default thresholds
        return self.default_rating_thresholds

    def get_rating_description(self, rating: GameRating) -> str:
        """Get a random description for the rating"""
        descriptions = {
            GameRating.MASTERPIECE: [
                "An absolute masterpiece! This game will be remembered for decades!",
                "Gaming perfection! A title that defines the generation!",
                "Breathtaking! This is why we make games!",
                "A monumental achievement that pushes every boundary!",
                "Instant classic! This game will inspire developers for years!",
                "Flawless execution! A new benchmark for the industry!",
                "Revolutionary! This changes everything we know about gaming!",
                "Pure genius! A once-in-a-lifetime gaming experience!",
                "Phenomenal! Critics are calling it the game of the decade!"
            ],
            GameRating.LEGENDARY: [
                "A legendary achievement in game development!",
                "Incredible work! This will be talked about for years!",
                "Extraordinary! A true testament to gaming excellence!",
                "Remarkable achievement! Setting new industry standards!",
                "Absolutely brilliant! A defining moment in gaming history!",
                "Stunning success! This is how games should be made!",
                "Magnificent! A legendary title is born!",
                "Exceptional quality! This game will stand the test of time!",
                "Truly special! A legendary entry in gaming's hall of fame!"
            ],
            GameRating.OUTSTANDING: [
                "Outstanding work! This game sets new standards!",
                "Superb quality! Players will love every moment!",
                "Impressive achievement! Well above the competition!",
                "Excellent craftsmanship! A standout title this year!",
                "Fantastic work! This game really shines!",
                "Top-tier quality! Outstanding in every aspect!",
                "Brilliant execution! Rising above expectations!",
                "Superior design! An outstanding addition to any library!",
                "Exceptional game! Critics and players are raving!"
            ],
            GameRating.EXCELLENT: [
                "Excellent game that will be highly praised!",
                "Great success! Players will thoroughly enjoy this!",
                "Very impressive! A strong contender this year!",
                "High quality work! Definitely worth playing!",
                "Wonderful game! Exceeding most expectations!",
                "Really well done! An excellent gaming experience!",
                "Strong showing! This game delivers on its promises!",
                "Quality title! Excellence in game design!",
                "Highly polished! An excellent addition to the genre!"
            ],
            GameRating.NOTABLE: [
                "A notable release that will get attention!",
                "Good work! This game stands out from the crowd!",
                "Solid title! Players will take notice!",
                "Noteworthy effort! Has some really great moments!",
                "Respectable showing! Worth checking out!",
                "Interesting game! Notable for its unique approach!",
                "Decent success! Getting positive attention!",
                "Worth playing! A notable entry in the genre!",
                "Pretty good! Has enough to make it memorable!"
            ],
            GameRating.GOOD: [
                "A good, solid game that players will enjoy!",
                "Nice work! A reliable and enjoyable experience!",
                "Solid effort! Does what it sets out to do!",
                "Good game! Players will have fun with this one!",
                "Well made! A good addition to any collection!",
                "Competent work! Delivers solid entertainment!",
                "Enjoyable! A good way to spend some time!",
                "Satisfying! Does the job and does it well!",
                "Pleasant surprise! Better than expected!"
            ],
            GameRating.FUN: [
                "A fun game that will find its audience!",
                "Entertaining enough! Has its moments of joy!",
                "Quirky fun! Not for everyone but has charm!",
                "Casual fun! Perfect for its target audience!",
                "Light entertainment! Fun in small doses!",
                "Has potential! Fun despite some rough edges!",
                "Modest success! Those who get it will love it!",
                "Simple fun! Does what it says on the tin!",
                "Niche appeal! The right players will enjoy this!"
            ],
            GameRating.DECENT: [
                "A decent effort with some good moments.",
                "Okay game. Has both highs and lows.",
                "Mixed results. Some parts work, others don't.",
                "Average. Neither great nor terrible.",
                "Serviceable. Gets the basics right at least.",
                "Passable. Worth a look on sale maybe.",
                "Fair attempt. Shows promise but needs work.",
                "Middling. Some will like it, many won't.",
                "Adequate. Does the minimum required."
            ],
            GameRating.MEH: [
                "Meh... It's playable but forgettable.",
                "Mediocre. Nothing really stands out here.",
                "Uninspiring. Goes through the motions.",
                "Bland. Lacks any real personality.",
                "Forgettable. Won't leave much impression.",
                "Weak showing. Needed more development time.",
                "Disappointing. Falls short of expectations.",
                "Lackluster. Missing that special something.",
                "Below average. Too many better options exist."
            ],
            GameRating.POOR: [
                "Poor execution. Back to the drawing board.",
                "Failed attempt. Numerous issues throughout.",
                "Not ready. Should have stayed in development.",
                "Rough. Too many problems to recommend.",
                "Unfortunate. Good ideas, terrible execution.",
                "Needs work. Not worth it in current state.",
                "Miss. Completely misses the mark.",
                "Flawed. Fundamental problems at its core.",
                "Avoid. Save your money for something better."
            ]
        }

        # Get the list of descriptions for this rating
        rating_descriptions = descriptions.get(rating, ["No description available."])

        # Return a random description from the list
        return random.choice(rating_descriptions)