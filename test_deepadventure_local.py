"""
Test DeepAdventure with local sample game generation
"""

import tkinter as tk
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import DeepAdventure
from DevelopmentGames.DeepAdventure import DeepAdventure

def test_local_game():
    """Test DeepAdventure with AI Uprising topic using sample generator"""
    print("Testing DeepAdventure with AI Uprising topic...")
    print("Using local sample game generator (API appears unavailable)")
    print("-" * 50)

    # Create window and run game
    root = tk.Tk()

    # Test with AI Uprising topic
    game = DeepAdventure(root, topic="AI Uprising")

    # The game will try the API first, then fall back to sample generation
    print("\nDeepAdventure window should be open.")
    print("The game will use the sample generator if API is unavailable.")

    # Start the game
    root.mainloop()

if __name__ == "__main__":
    test_local_game()