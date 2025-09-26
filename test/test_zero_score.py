"""
Test GameEndManager with 0 score (immediate loss)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from systems.game_end_manager import GameEndManager, GTGISSScores

def test_zero_score():
    """Test the game end manager with 0 score"""
    print("Testing GameEndManager with 0 score (immediate loss)...")
    print("="*60)

    # Create initial scores
    initial_scores = GTGISSScores(
        gameplay=5,
        technical=3,
        graphics=4,
        innovation=2,
        sound=2,
        story=3
    )

    print("Initial GTGISS Scores:")
    print(f"  Gameplay:   {initial_scores.gameplay}")
    print(f"  Technical:  {initial_scores.technical}")
    print(f"  Graphics:   {initial_scores.graphics}")
    print(f"  Innovation: {initial_scores.innovation}")
    print(f"  Sound:      {initial_scores.sound}")
    print(f"  Story:      {initial_scores.story}")
    print(f"  Total:      {initial_scores.total}")
    print()

    # Test with 0 score
    manager = GameEndManager()
    manager.set_game_info(
        game_name="Test Game - Lost Immediately",
        game_type="Arcade",
        game_topic="Bugs",
        current_scores=initial_scores
    )

    # Simulate losing immediately (0 score)
    minigame_score = 0
    print(f"Minigame Score: {minigame_score} (Lost immediately!)")
    print()

    # Distribute score (should handle 0 gracefully)
    manager.distribute_score(minigame_score)

    print("\nFinal GTGISS Scores:")
    print(f"  Gameplay:   {manager.after_scores.gameplay}")
    print(f"  Technical:  {manager.after_scores.technical}")
    print(f"  Graphics:   {manager.after_scores.graphics}")
    print(f"  Innovation: {manager.after_scores.innovation}")
    print(f"  Sound:      {manager.after_scores.sound}")
    print(f"  Story:      {manager.after_scores.story}")
    print(f"  Total:      {manager.after_scores.total}")
    print()

    # Verify no change with 0 score
    if manager.after_scores.total == initial_scores.total:
        print("[PASS] Scores unchanged with 0 minigame score")
    else:
        print("[FAIL] Scores changed unexpectedly")

    print("\nTest complete!")
    print("="*60)
    print("\nThe UI will show:")
    print("- 'Minigame Score: 0 points - Try harder next time!' in red")
    print("- 'No Points Gained' in gray")
    print("- A 'Next' button to continue")

if __name__ == "__main__":
    test_zero_score()