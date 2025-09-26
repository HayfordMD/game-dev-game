"""
Simple test of GameEndManager score distribution
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from systems.game_end_manager import GameEndManager, GTGISSScores

def test_score_distribution():
    """Test score distribution logic"""
    print("Testing GameEndManager Score Distribution...")

    # Create initial scores
    initial_scores = GTGISSScores(
        gameplay=10,
        technical=5,
        graphics=8,
        innovation=3,
        sound=4,
        story=6
    )

    print(f"\n{'='*50}")
    print("INITIAL GTGISS SCORES")
    print(f"{'='*50}")
    for key, value in initial_scores.to_dict().items():
        if key != 'total':
            print(f"  {key.capitalize():12} {value:3}")
    print(f"  {'-'*20}")
    print(f"  {'Total':12} {initial_scores.total:3}")

    # Test different game types
    game_types = ["Arcade", "Text Adventure", "RPG", "Puzzle"]
    minigame_score = 30

    for game_type in game_types:
        print(f"\n{'='*50}")
        print(f"TESTING: {game_type} Game")
        print(f"{'='*50}")

        # Reset manager
        GameEndManager.reset()
        manager = GameEndManager()

        # Set game info
        manager.set_game_info(
            game_name=f"Test {game_type} Game",
            game_type=game_type,
            game_topic="Test Topic",
            current_scores=initial_scores.copy()
        )

        # Get weights for this game type
        weights = manager.get_category_weights()
        print("\nCategory Weights:")
        for category, weight in weights.items():
            print(f"  {category:12} {weight:2}")

        # Distribute score
        manager.distribute_score(minigame_score)

        # Show results
        print(f"\nScore Distribution ({minigame_score} points):")
        changes = {}
        for key in ['gameplay', 'technical', 'graphics', 'innovation', 'sound', 'story']:
            before = getattr(manager.before_scores, key)
            after = getattr(manager.after_scores, key)
            change = after - before
            changes[key] = change
            if change > 0:
                print(f"  {key:12} +{change:2} ({before} -> {after})")

        total_distributed = sum(changes.values())
        print(f"  {'-'*20}")
        print(f"  Total distributed: {total_distributed}")

    print(f"\n{'='*50}")
    print("TEST COMPLETE")
    print(f"{'='*50}")

if __name__ == "__main__":
    test_score_distribution()