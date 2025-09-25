"""
Test script for DeepSeek API integration
"""

import sys
import os
import json

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from deepseek.deepseek_client import DeepSeekClient

def test_api_connection():
    """Test the DeepSeek API connection and game generation"""
    print("Testing DeepSeek API connection...")
    print("-" * 50)

    try:
        # Create client
        client = DeepSeekClient()
        print("[OK] API key loaded successfully")

        # Test with AI Uprising topic
        topic = "AI Uprising"
        print(f"\nGenerating adventure game for topic: {topic}")
        print("This may take 10-30 seconds...")
        print("(If this takes more than 60 seconds, the API may be unavailable)")

        # Generate game
        game_data = client.generate_adventure_game(topic)

        if game_data:
            print("\n[SUCCESS] Game generated successfully!")
            print("\nGame structure:")
            print(f"  - Title: {game_data.get('game_title', 'N/A')}")
            print(f"  - Rooms: {len(game_data.get('rooms', {}))}")
            print(f"  - Has welcome message: {'welcome_message' in game_data}")
            print(f"  - Has victory message: {'victory_message' in game_data}")
            print(f"  - Has boon description: {'boon_description' in game_data}")

            # Save the generated game for inspection
            save_path = os.path.join("DevelopmentGames", "generated_ai_uprising.json")
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(game_data, f, indent=2, ensure_ascii=False)
            print(f"\n[SAVED] Game saved to: {save_path}")

            # Check room structure
            if 'rooms' in game_data:
                print("\nRoom validation:")
                for room_num in range(1, 11):
                    room_key = str(room_num)
                    if room_key in game_data['rooms']:
                        room = game_data['rooms'][room_key]
                        choice_count = len(room.get('choices', {}))
                        print(f"  Room {room_num}: {choice_count} choices", end="")

                        # Check outcomes
                        choices = room.get('choices', {})
                        outcomes = [c.get('outcome') for c in choices.values()]
                        has_death = 'DEATH' in outcomes
                        has_retreat = 'RETREAT' in outcomes
                        advance_count = outcomes.count('ADVANCE')

                        print(f" (DEATH: {has_death}, RETREAT: {has_retreat}, ADVANCE: {advance_count})")
                    else:
                        print(f"  Room {room_num}: MISSING")

            return True
        else:
            print("\n[ERROR] Failed to generate game")
            return False

    except ValueError as e:
        print(f"\n[ERROR] Configuration error: {e}")
        print("Make sure DEEPSEEK_API_KEY is set in your .env file")
        return False
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_api_connection()
    print("\n" + "=" * 50)
    if success:
        print("API test completed successfully!")
        print("You can now run: python DevelopmentGames/DeepAdventure.py \"AI Uprising\"")
    else:
        print("API test failed. Please check your configuration.")
    print("=" * 50)