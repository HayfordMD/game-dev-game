"""
Test sample game generation for DeepAdventure
"""

import sys
import os
import json

# Add paths for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'DevelopmentGames'))

# Create a mock DeepAdventure to test sample generation
class MockDeepAdventure:
    def __init__(self, topic="AI Uprising"):
        self.topic = topic
        self.topic_configs = {
            "AI Uprising": {
                "setting": "server farm where rogue AI has taken control",
                "boon_examples": ["Core of the Singularity", "Master Control Protocol", "Quantum Consciousness Key"],
                "hazards": ["security drones", "data corruption", "neural overload"],
                "atmosphere": "humming servers and cascading code"
            }
        }

    def create_sample_game(self):
        """Create a sample game structure for testing"""
        import random

        config = self.topic_configs.get(self.topic, self.topic_configs["AI Uprising"])
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
        import random

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
        import random

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

# Test the sample generation
def test_sample():
    print("Testing sample game generation for AI Uprising...")
    print("-" * 50)

    mock = MockDeepAdventure("AI Uprising")
    game_data = mock.create_sample_game()

    print(f"Game Title: {game_data['game_title']}")
    print(f"\nWelcome Message:")
    print(game_data['welcome_message'])
    print(f"\nBoon Description:")
    print(game_data['boon_description'])
    print(f"\nNumber of rooms: {len(game_data['rooms'])}")

    # Validate room structure
    print("\nRoom validation:")
    valid = True
    for i in range(1, 11):
        room_key = str(i)
        if room_key in game_data['rooms']:
            room = game_data['rooms'][room_key]
            choices = room.get('choices', {})
            outcomes = [c.get('outcome') for c in choices.values()]

            has_death = 'DEATH' in outcomes
            has_retreat = 'RETREAT' in outcomes
            advance_count = outcomes.count('ADVANCE')

            status = "[OK]" if has_death and has_retreat else "[ERROR]"
            print(f"  Room {i:2}: {len(choices)} choices - DEATH:{has_death}, RETREAT:{has_retreat}, ADVANCE:{advance_count} {status}")

            if not (has_death and has_retreat):
                valid = False
        else:
            print(f"  Room {i:2}: MISSING")
            valid = False

    print("\n" + "=" * 50)
    if valid:
        print("[SUCCESS] Sample game generation works correctly!")
        print("\nThe game will use this fallback when the API is unavailable.")
        print("You can run: python DevelopmentGames/DeepAdventure.py \"AI Uprising\"")
    else:
        print("[ERROR] Sample generation has issues")

if __name__ == "__main__":
    test_sample()