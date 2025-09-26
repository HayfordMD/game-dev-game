"""
Test the GameEndManager functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from systems.game_end_manager import GameEndManager, GTGISSScores
import tkinter as tk

def test_game_end_manager():
    """Test the game end manager with sample data"""
    print("Testing GameEndManager...")

    # Create initial scores
    initial_scores = GTGISSScores(
        gameplay=10,
        technical=5,
        graphics=8,
        innovation=3,
        sound=4,
        story=6
    )

    print(f"\nInitial GTGISS Scores:")
    print(f"  Gameplay: {initial_scores.gameplay}")
    print(f"  Technical: {initial_scores.technical}")
    print(f"  Graphics: {initial_scores.graphics}")
    print(f"  Innovation: {initial_scores.innovation}")
    print(f"  Sound: {initial_scores.sound}")
    print(f"  Story: {initial_scores.story}")
    print(f"  Total: {initial_scores.total}")

    # Create manager and set game info
    manager = GameEndManager()
    manager.set_game_info(
        game_name="Space Adventure Test",
        game_type="Arcade",
        game_topic="Space",
        current_scores=initial_scores
    )

    # Simulate minigame score
    minigame_score = 25
    print(f"\nMinigame Score: {minigame_score}")

    # Create root window
    root = tk.Tk()
    root.withdraw()  # Hide main window

    def on_continue(updated_scores):
        """Callback when continuing from results"""
        print(f"\nFinal GTGISS Scores:")
        print(f"  Gameplay: {updated_scores.gameplay}")
        print(f"  Technical: {updated_scores.technical}")
        print(f"  Graphics: {updated_scores.graphics}")
        print(f"  Innovation: {updated_scores.innovation}")
        print(f"  Sound: {updated_scores.sound}")
        print(f"  Story: {updated_scores.story}")
        print(f"  Total: {updated_scores.total}")
        print(f"\nPoints gained: {updated_scores.total - initial_scores.total}")
        root.quit()

    # Handle game end
    manager.handle_game_end(minigame_score, root, on_continue)

    # Run main loop
    root.mainloop()

    print("\nTest complete!")

if __name__ == "__main__":
    test_game_end_manager()