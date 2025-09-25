"""
Game Type and Topic Combination Ratings System
Rates how well certain game types work with specific topics
Rating Scale: 1-5 (1=Terrible, 2=Poor, 3=Average, 4=Good, 5=Perfect)
Score Modifiers: 5/5 = +2, 4/5 = +1, 3/5 = 0, 2/5 = -1, 1/5 = -2
"""

from typing import Tuple, Dict

# Combination ratings: (game_type, topic) -> rating (1-5)
COMBINATION_RATINGS: Dict[Tuple[str, str], int] = {
    # ============= ARCADE COMBINATIONS =============
    # Perfect Arcade Combos (5/5)
    ('Arcade', 'Table Tennis'): 5,  # Classic arcade game
    ('Arcade', 'Space'): 5,  # Space invaders, Galaga, etc.
    ('Arcade', 'Martial Arts'): 5,  # Street Fighter, Mortal Kombat
    ('Arcade', 'Skateboarding'): 5,  # Tony Hawk style

    # Good Arcade Combos (4/5)
    ('Arcade', 'Boxing'): 4,
    ('Arcade', 'Basketball'): 4,  # NBA Jam style
    ('Arcade', 'Soccer'): 4,
    ('Arcade', 'Tennis'): 4,
    ('Arcade', 'Golf'): 4,  # Mini golf
    ('Arcade', 'Surfing'): 4,
    ('Arcade', 'Zombies'): 4,
    ('Arcade', 'Robots'): 4,
    ('Arcade', 'Dinosaurs'): 4,
    ('Arcade', 'Ninjas'): 4,

    # Average Arcade Combos (3/5)
    ('Arcade', 'Fantasy'): 3,
    ('Arcade', 'Pirates'): 3,
    ('Arcade', 'War'): 3,
    ('Arcade', 'Temple'): 3,

    # Poor Arcade Combos (2/5)
    ('Arcade', 'City Building'): 2,
    ('Arcade', 'Dating Sim'): 2,
    ('Arcade', 'Farming'): 2,

    # Terrible Arcade Combos (1/5)
    ('Arcade', 'Poetry'): 1,
    ('Arcade', 'Office'): 1,
    ('Arcade', 'Journalism'): 1,

    # ============= ACTION COMBINATIONS =============
    # Perfect Action Combos (5/5)
    ('Action', 'War'): 5,
    ('Action', 'Zombies'): 5,
    ('Action', 'Ninjas'): 5,
    ('Action', 'Space'): 5,
    ('Action', 'Martial Arts'): 5,
    ('Action', 'Monster Hunting'): 5,

    # Good Action Combos (4/5)
    ('Action', 'Pirates'): 4,
    ('Action', 'Wild West'): 4,
    ('Action', 'Cyberpunk'): 4,
    ('Action', 'Dragons'): 4,
    ('Action', 'Robots'): 4,
    ('Action', 'Gladiator Arenas'): 4,

    # Average Action Combos (3/5)
    ('Action', 'Fantasy'): 3,
    ('Action', 'Egypt'): 3,
    ('Action', 'Viking'): 3,

    # Poor Action Combos (2/5)
    ('Action', 'Farming'): 2,
    ('Action', 'Office'): 2,
    ('Action', 'Dating Sim'): 2,

    # Terrible Action Combos (1/5)
    ('Action', 'Poetry'): 1,
    ('Action', 'Gardening'): 1,

    # ============= RPG COMBINATIONS =============
    # Perfect RPG Combos (5/5)
    ('RPG', 'Fantasy'): 5,
    ('RPG', 'Dragons'): 5,
    ('RPG', 'Magic Schools'): 5,
    ('RPG', 'Kingdoms & Castles'): 5,
    ('RPG', 'Elves & Dwarves'): 5,

    # Good RPG Combos (4/5)
    ('RPG', 'Space'): 4,
    ('RPG', 'Cyberpunk'): 4,
    ('RPG', 'Post-Apocalyptic'): 4,
    ('RPG', 'Pirates'): 4,
    ('RPG', 'Vikings'): 4,
    ('RPG', 'Ancient Ruins'): 4,

    # Average RPG Combos (3/5)
    ('RPG', 'Wild West'): 3,
    ('RPG', 'Ninjas'): 3,
    ('RPG', 'Zombies'): 3,

    # Poor RPG Combos (2/5)
    ('RPG', 'Table Tennis'): 2,
    ('RPG', 'Golf'): 2,
    ('RPG', 'Basketball'): 2,

    # Terrible RPG Combos (1/5)
    ('RPG', 'Office'): 1,
    ('RPG', 'Trucking'): 1,

    # ============= SIMULATION COMBINATIONS =============
    # Perfect Simulation Combos (5/5)
    ('Simulation', 'City Building'): 5,
    ('Simulation', 'Farming'): 5,
    ('Simulation', 'Trucking'): 5,
    ('Simulation', 'Restaurant Management'): 5,
    ('Simulation', 'Wildlife Rescue'): 5,
    # All sports simulations are perfect matches (realistic sports sims)
    ('Simulation', 'Football'): 5,
    ('Simulation', 'Basketball'): 5,
    ('Simulation', 'Soccer'): 5,
    ('Simulation', 'Baseball'): 5,
    ('Simulation', 'Golf'): 5,
    ('Simulation', 'Tennis'): 5,
    ('Simulation', 'Boxing'): 5,
    ('Simulation', 'Skateboarding'): 5,
    ('Simulation', 'Surfing'): 5,
    ('Simulation', 'Olympics'): 5,
    ('Simulation', 'Volleyball'): 5,
    ('Simulation', 'Swimming'): 5,
    ('Simulation', 'Track & Field'): 5,

    # Good Simulation Combos (4/5)
    ('Simulation', 'Table Tennis'): 4,  # Slightly less popular as a full sim
    ('Simulation', 'Mining'): 4,
    ('Simulation', 'Factory Work'): 4,
    ('Simulation', 'Emergency Response'): 4,
    ('Simulation', 'Ocean Exploration'): 4,
    ('Simulation', 'Space Exploration'): 4,

    # Average Simulation Combos (3/5)
    ('Simulation', 'Office'): 3,
    ('Simulation', 'Fishing'): 3,
    ('Simulation', 'Gardening'): 3,

    # Poor Simulation Combos (2/5)
    ('Simulation', 'Ninjas'): 2,
    ('Simulation', 'Zombies'): 2,
    ('Simulation', 'Dragons'): 2,

    # Terrible Simulation Combos (1/5)
    ('Simulation', 'Poetry'): 1,

    # ============= STRATEGY COMBINATIONS =============
    # Perfect Strategy Combos (5/5)
    ('Strategy', 'War'): 5,
    ('Strategy', 'City Building'): 5,
    ('Strategy', 'Kingdoms & Castles'): 5,
    ('Strategy', 'Roman Empire'): 5,
    ('Strategy', 'World War II'): 5,

    # Good Strategy Combos (4/5)
    ('Strategy', 'Space'): 4,
    ('Strategy', 'Medieval Europe'): 4,
    ('Strategy', 'Vikings'): 4,
    ('Strategy', 'Egypt'): 4,
    ('Strategy', 'Tactical Infiltration'): 4,

    # Average Strategy Combos (3/5)
    ('Strategy', 'Pirates'): 3,
    ('Strategy', 'Fantasy'): 3,
    ('Strategy', 'Robots'): 3,

    # Poor Strategy Combos (2/5)
    ('Strategy', 'Dating Sim'): 2,
    ('Strategy', 'Poetry'): 2,
    ('Strategy', 'Dance'): 2,

    # Terrible Strategy Combos (1/5)
    ('Strategy', 'Table Tennis'): 1,
    ('Strategy', 'Skateboarding'): 1,

    # ============= PUZZLE COMBINATIONS =============
    # Perfect Puzzle Combos (5/5)
    ('Puzzle', 'Temple'): 5,
    ('Puzzle', 'Ancient Ruins'): 5,
    ('Puzzle', 'Magic Schools'): 5,

    # Good Puzzle Combos (4/5)
    ('Puzzle', 'Space'): 4,
    ('Puzzle', 'Egypt'): 4,
    ('Puzzle', 'Robots'): 4,
    ('Puzzle', 'Cave Diving'): 4,

    # Average Puzzle Combos (3/5)
    ('Puzzle', 'Fantasy'): 3,
    ('Puzzle', 'Pirates'): 3,
    ('Puzzle', 'Office'): 3,

    # Poor Puzzle Combos (2/5)
    ('Puzzle', 'War'): 2,
    ('Puzzle', 'Zombies'): 2,
    ('Puzzle', 'Boxing'): 2,

    # Terrible Puzzle Combos (1/5)
    ('Puzzle', 'Martial Arts'): 1,
    ('Puzzle', 'Basketball'): 1,

    # ============= SPORTS COMBINATIONS =============
    # Perfect Sports Combos (5/5)
    ('Sports', 'Football'): 5,
    ('Sports', 'Basketball'): 5,
    ('Sports', 'Soccer'): 5,
    ('Sports', 'Baseball'): 5,
    ('Sports', 'Golf'): 5,
    ('Sports', 'Tennis'): 5,
    ('Sports', 'Olympics'): 5,

    # Good Sports Combos (4/5)
    ('Sports', 'Boxing'): 4,
    ('Sports', 'Skateboarding'): 4,
    ('Sports', 'Surfing'): 4,
    ('Sports', 'Swimming'): 4,

    # Average Sports Combos (3/5)
    ('Sports', 'Table Tennis'): 3,  # Real sim vs arcade

    # Poor Sports Combos (2/5)
    ('Sports', 'Fantasy'): 2,
    ('Sports', 'Space'): 2,
    ('Sports', 'Zombies'): 2,

    # Terrible Sports Combos (1/5)
    ('Sports', 'Poetry'): 1,
    ('Sports', 'Dragons'): 1,

    # ============= ADVENTURE COMBINATIONS =============
    # Perfect Adventure Combos (5/5)
    ('Adventure', 'Temple'): 5,
    ('Adventure', 'Pirates'): 5,
    ('Adventure', 'Ancient Ruins'): 5,
    ('Adventure', 'Space Exploration'): 5,

    # Good Adventure Combos (4/5)
    ('Adventure', 'Fantasy'): 4,
    ('Adventure', 'Egypt'): 4,
    ('Adventure', 'Cave Diving'): 4,
    ('Adventure', 'Ocean Exploration'): 4,
    ('Adventure', 'Wild West'): 4,

    # Average Adventure Combos (3/5)
    ('Adventure', 'Dragons'): 3,
    ('Adventure', 'Zombies'): 3,
    ('Adventure', 'Ninjas'): 3,

    # Poor Adventure Combos (2/5)
    ('Adventure', 'Office'): 2,
    ('Adventure', 'Farming'): 2,
    ('Adventure', 'City Building'): 2,

    # Terrible Adventure Combos (1/5)
    ('Adventure', 'Table Tennis'): 1,
    ('Adventure', 'Golf'): 1,

    # ============= HORROR COMBINATIONS =============
    # Perfect Horror Combos (5/5)
    ('Horror', 'Zombies'): 5,
    ('Horror', 'Vampires'): 5,
    ('Horror', 'Ghosts'): 5,
    ('Horror', 'Haunted Houses'): 5,
    ('Horror', 'Psychological Horror'): 5,

    # Good Horror Combos (4/5)
    ('Horror', 'Post-Apocalyptic'): 4,
    ('Horror', 'Ancient Ruins'): 4,
    ('Horror', 'Cave Diving'): 4,

    # Average Horror Combos (3/5)
    ('Horror', 'Space'): 3,
    ('Horror', 'Ocean Exploration'): 3,

    # Poor Horror Combos (2/5)
    ('Horror', 'Fantasy'): 2,
    ('Horror', 'Pirates'): 2,

    # Terrible Horror Combos (1/5)
    ('Horror', 'Table Tennis'): 1,
    ('Horror', 'Golf'): 1,
    ('Horror', 'Office'): 1,
}


class CombinationRatingSystem:
    """System for rating game type and topic combinations"""

    @staticmethod
    def get_combination_rating(game_type: str, topic: str) -> int:
        """
        Get the rating for a game type and topic combination

        Args:
            game_type: The game type (e.g., 'Arcade', 'RPG')
            topic: The topic (e.g., 'Table Tennis', 'Fantasy')

        Returns:
            Rating from 1-5, defaults to 3 if not specified
        """
        return COMBINATION_RATINGS.get((game_type, topic), 3)

    @staticmethod
    def get_score_modifier(game_type: str, topic: str) -> int:
        """
        Convert combination rating to score modifier

        Rating Scale:
        5/5 = +2 bonus
        4/5 = +1 bonus
        3/5 = 0 (neutral)
        2/5 = -1 penalty
        1/5 = -2 penalty

        Args:
            game_type: The game type
            topic: The topic

        Returns:
            Score modifier from -2 to +2
        """
        rating = CombinationRatingSystem.get_combination_rating(game_type, topic)
        return rating - 3  # Convert 1-5 scale to -2 to +2

    @staticmethod
    def get_rating_description(rating: int) -> str:
        """Get a text description for a rating"""
        descriptions = {
            5: "Perfect Match!",
            4: "Good Combination",
            3: "Average Fit",
            2: "Poor Match",
            1: "Terrible Combination"
        }
        return descriptions.get(rating, "Unknown")

    @staticmethod
    def get_all_combinations_for_type(game_type: str) -> Dict[str, int]:
        """Get all rated combinations for a specific game type"""
        results = {}
        for (g_type, topic), rating in COMBINATION_RATINGS.items():
            if g_type == game_type:
                results[topic] = rating
        return results

    @staticmethod
    def get_all_combinations_for_topic(topic: str) -> Dict[str, int]:
        """Get all rated combinations for a specific topic"""
        results = {}
        for (game_type, t), rating in COMBINATION_RATINGS.items():
            if t == topic:
                results[game_type] = rating
        return results


# Example usage:
if __name__ == "__main__":
    # Test the system
    print("Testing Combination Rating System")
    print("-" * 40)

    test_combos = [
        ('Arcade', 'Table Tennis'),
        ('RPG', 'Fantasy'),
        ('Horror', 'Zombies'),
        ('Sports', 'Poetry'),
        ('Strategy', 'War'),
    ]

    for game_type, topic in test_combos:
        rating = CombinationRatingSystem.get_combination_rating(game_type, topic)
        modifier = CombinationRatingSystem.get_score_modifier(game_type, topic)
        description = CombinationRatingSystem.get_rating_description(rating)

        print(f"{game_type} + {topic}:")
        print(f"  Rating: {rating}/5 - {description}")
        print(f"  Score Modifier: {modifier:+d}")
        print()