import requests
import json
import os
import logging
from typing import List, Optional
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

class DeepSeekNamingService:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize DeepSeek naming service

        Args:
            api_key: DeepSeek API key. If None, will try to get from environment variable DEEPSEEK_API_KEY
        """
        # Always try to load the API key - fallback to hardcoded for testing
        self.api_key = api_key or os.getenv('DEEPSEEK_API_KEY') or "sk-e4c9755d6cbc43979d8eee3f7e251c22"
        self.base_url = "https://api.deepseek.com/v1/chat/completions"

        # Only warn if truly no key (shouldn't happen now)
        if not self.api_key:
            print("Warning: No DeepSeek API key found. Using creative fallback names.")

    def generate_studio_names(self) -> List[str]:
        """
        Generate 3 game studio names using DeepSeek API

        Returns:
            List of 3 studio names:
            [descriptive_name, fierce_elemental_name, simple_brandable_name]
        """
        if not self.api_key:
            logger.info("No API key available, using fallback studio names")
            return self._get_fallback_names()

        logger.info("Calling DeepSeek API to generate studio names...")

        prompt = """Give me 5 game studio names. I need:

1. One descriptive/technical name like "Sun Systems Development" or "ID Software"
2. One fierce/elemental name like "Shark Systems", "Shadow Games", "Light House Studios", or "Fast Games"
3. One simple/brandable name like "Bungie", "Blizzard", "FOREDATING", "AXEL", or "QUBIT"
4. One creative/artistic name like "Pixel Dreams", "Neon Canvas", "Digital Muse"
5. One tech/modern name like "ByteForge", "CodeCraft", "DataFlow Studios"

Return only the five names, one per line, no explanations."""

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            data = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 100,
                "temperature": 0.8
            }

            response = requests.post(self.base_url, headers=headers, json=data, timeout=10)
            logger.info(f"DeepSeek API response status: {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content'].strip()
                names = [name.strip() for name in content.split('\n') if name.strip()]

                # Ensure we have exactly 5 names
                if len(names) >= 5:
                    logger.info(f"Successfully generated {len(names)} studio names")
                    return names[:5]
                else:
                    # If we got fewer than 5, pad with fallback names
                    logger.warning(f"Only got {len(names)} names, padding with fallbacks")
                    fallback = self._get_fallback_names()
                    while len(names) < 5:
                        names.append(fallback[len(names) % 5])
                    return names[:5]
            else:
                logger.error(f"DeepSeek API error: {response.status_code} - {response.text}")
                return self._get_fallback_names()

        except requests.exceptions.RequestException as e:
            logger.error(f"Network error calling DeepSeek API: {e}")
            return self._get_fallback_names()
        except Exception as e:
            logger.error(f"Error calling DeepSeek API: {e}")
            return self._get_fallback_names()

    def _get_fallback_names(self) -> List[str]:
        """
        Fallback names when API is not available

        Returns:
            List of 5 predetermined studio names
        """
        import random

        all_names = [
            "Digital Systems Development", "Code Forge Studios", "Pixel Engine Works", "Interactive Media Labs", "Game Logic Studios",
            "Storm Games", "Iron Wolf Studios", "Lightning Studios", "Fire Mountain Games", "Thunder Bay Studios",
            "Zenith", "Apex", "Nexus", "Prism", "Flux",
            "Pixel Dreams", "Neon Canvas", "Digital Muse", "Creative Labs", "Art Engine",
            "ByteForge", "CodeCraft", "DataFlow Studios", "TechCore", "Binary Studios"
        ]

        # Shuffle and return 5 names
        random.shuffle(all_names)
        return all_names[:5]

    def generate_player_names(self) -> List[str]:
        """
        Generate 10 random American player names using DeepSeek API

        Returns:
            List of 10 player names
        """
        if not self.api_key:
            logger.info("No API key available, using fallback player names")
            return self._get_fallback_player_names()

        logger.info("Calling DeepSeek API to generate player names...")

        prompt = """Give me 10 random American names. These are for game characters/players.

Return only the names, one per line, no explanations. Mix of first names only and full names (first + last). Examples: John, Sarah Martinez, Mike, Jennifer Chen, etc."""

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            data = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 150,
                "temperature": 0.8
            }

            response = requests.post(self.base_url, headers=headers, json=data, timeout=10)
            logger.info(f"DeepSeek API response status: {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content'].strip()
                names = [name.strip() for name in content.split('\n') if name.strip()]

                # Ensure we have exactly 10 names
                if len(names) >= 10:
                    return names[:10]
                else:
                    # If we got fewer than 10, pad with fallback names
                    fallback = self._get_fallback_player_names()
                    while len(names) < 10:
                        names.append(fallback[len(names) % 10])
                    return names[:10]
            else:
                logger.error(f"DeepSeek API error: {response.status_code} - {response.text}")
                return self._get_fallback_player_names()

        except requests.exceptions.RequestException as e:
            logger.error(f"Network error calling DeepSeek API: {e}")
            return self._get_fallback_player_names()
        except Exception as e:
            logger.error(f"Error calling DeepSeek API: {e}")
            return self._get_fallback_player_names()

    def generate_competitor_companies(self) -> List[str]:
        """
        Generate 20 competitor game company names using DeepSeek API for 1978 era

        Returns:
            List of 20 competitor company names
        """
        if not self.api_key:
            logger.info("No API key available, using fallback competitor names")
            return self._get_fallback_competitor_names()

        logger.info("Calling DeepSeek API to generate competitor companies...")

        prompt = """Give me 20 game company names that would exist in 1978. These are competitors in the early computer/arcade game era.

Mix of:
- Technical names (like "Digital Systems", "Binary Labs")
- Creative names (like "Cosmic Games", "Star Software")
- Simple corporate names (like "Interactive Inc", "Software Corp")

Return only the company names, one per line, no explanations or numbering."""

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            data = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 300,
                "temperature": 0.8
            }

            response = requests.post(self.base_url, headers=headers, json=data, timeout=10)
            logger.info(f"DeepSeek API response status: {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content'].strip()
                names = [name.strip() for name in content.split('\n') if name.strip()]

                # Ensure we have exactly 20 names
                if len(names) >= 20:
                    return names[:20]
                else:
                    # If we got fewer than 20, pad with fallback names
                    fallback = self._get_fallback_competitor_names()
                    while len(names) < 20:
                        names.append(fallback[len(names) % 20])
                    return names[:20]
            else:
                logger.error(f"DeepSeek API error: {response.status_code} - {response.text}")
                return self._get_fallback_competitor_names()

        except requests.exceptions.RequestException as e:
            logger.error(f"Network error calling DeepSeek API: {e}")
            return self._get_fallback_competitor_names()
        except Exception as e:
            logger.error(f"Error calling DeepSeek API: {e}")
            return self._get_fallback_competitor_names()

    def generate_game_names(self, prompt: str, count: int = 2) -> List[str]:
        """
        Generate game names based on a prompt using DeepSeek API

        Args:
            prompt: The prompt describing what kind of names to generate
            count: Number of names to request (default 2)

        Returns:
            List of generated game names
        """
        if not self.api_key:
            # Return more creative fallback names even without API
            import random

            adjectives = ["Super", "Ultra", "Mega", "Epic", "Legendary", "Mystic", "Cosmic", "Quantum", "Tiny", "Giant", "Flying", "Running", "Sleeping", "Dancing"]
            verbs = ["Jumping", "Running", "Flying", "Crying", "Laughing", "Standing", "Sitting", "Crawling", "Swimming", "Fighting", "Racing", "Hiding", "Sleeping", "Dancing", "Singing"]
            nouns = ["Rabbit", "Dragon", "Office", "Robot", "Wizard", "Knight", "Pirate", "Ninja", "Cat", "Dog", "Monster", "Hero", "Alien", "Ghost", "Warrior", "Manager", "Plumber", "Farmer"]
            suffixes = ["Quest", "Adventure", "Saga", "Chronicles", "Legacy", "Odyssey", "Journey", "Tales", "Simulator", "World", "Story", "Challenge"]

            names = []
            for i in range(count):
                # Randomly choose pattern
                pattern = random.randint(1, 5)

                if pattern == 1:
                    # Adjective + Noun
                    name = f"{random.choice(adjectives)} {random.choice(nouns)}"
                elif pattern == 2:
                    # Verb + Noun
                    name = f"{random.choice(verbs)} {random.choice(nouns)}"
                elif pattern == 3:
                    # Adjective + Verb + Noun
                    name = f"{random.choice(adjectives)} {random.choice(verbs)} {random.choice(nouns)}"
                elif pattern == 4:
                    # Noun + Suffix
                    name = f"{random.choice(nouns)} {random.choice(suffixes)}"
                else:
                    # Verb + Noun + Suffix
                    name = f"{random.choice(verbs)} {random.choice(nouns)} {random.choice(suffixes)}"

                names.append(name)
            return names

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            data = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 200,
                "temperature": 0.8
            }

            response = requests.post(self.base_url, json=data, headers=headers, timeout=10)
            response.raise_for_status()

            result = response.json()
            content = result.get('choices', [{}])[0].get('message', {}).get('content', '')

            # Parse the names from the response
            names = [name.strip() for name in content.strip().split('\n') if name.strip()]

            # Ensure we return at least the requested count
            while len(names) < count:
                names.append(f"Game {len(names)+1}")

            return names[:count]

        except Exception as e:
            print(f"Error generating game names: {e}")
            # Return more creative fallback names on error
            import random

            adjectives = ["Amazing", "Incredible", "Awesome", "Fantastic", "Marvelous", "Stellar", "Ultimate", "Prime", "Brave", "Happy", "Angry", "Sneaky"]
            verbs = ["Bouncing", "Sliding", "Spinning", "Exploding", "Shrinking", "Growing", "Teleporting", "Transforming", "Building", "Breaking"]
            nouns = ["Penguin", "Unicorn", "Taco", "Banana", "Spaceship", "Mushroom", "Crystal", "Thunder", "Shadow", "Phoenix", "Tiger", "Eagle"]
            suffixes = ["Madness", "Fever", "Mania", "Rampage", "Revolution", "Uprising", "Mayhem", "Chaos", "Party", "Festival"]

            names = []
            for i in range(count):
                pattern = random.randint(1, 6)

                if pattern == 1:
                    # Just a verb
                    name = random.choice(verbs)
                elif pattern == 2:
                    # Just a noun
                    name = random.choice(nouns)
                elif pattern == 3:
                    # Verb + Noun
                    name = f"{random.choice(verbs)} {random.choice(nouns)}"
                elif pattern == 4:
                    # Adjective + Noun
                    name = f"{random.choice(adjectives)} {random.choice(nouns)}"
                elif pattern == 5:
                    # Noun + Suffix
                    name = f"{random.choice(nouns)} {random.choice(suffixes)}"
                else:
                    # Adjective + Verb + Noun
                    name = f"{random.choice(adjectives)} {random.choice(verbs)} {random.choice(nouns)}"

                names.append(name)
            return names

    def _get_fallback_competitor_names(self) -> List[str]:
        """
        Fallback competitor names when API is not available

        Returns:
            List of 20 predetermined competitor company names
        """
        return [
            "Pixel Dynamics",
            "Binary Arts",
            "Cosmic Software",
            "MicroVision Games",
            "Arcade Masters",
            "Digital Frontier",
            "Byte Works",
            "Silicon Dreams",
            "Vector Graphics Inc",
            "Quantum Entertainment",
            "Data Storm Studios",
            "Circuit Board Games",
            "Neon Software",
            "Mainframe Studios",
            "Logic Gate Games",
            "Synth Wave Interactive",
            "Electron Entertainment",
            "RAM Raiders",
            "Motherboard Media",
            "Transistor Games"
        ]

    def _get_fallback_player_names(self) -> List[str]:
        """
        Fallback player names when API is not available

        Returns:
            List of 10 predetermined player names
        """
        import random

        american_names = [
            "Alex", "Jordan Smith", "Taylor", "Casey Johnson", "Morgan",
            "Riley Davis", "Cameron", "Quinn Miller", "Avery", "Dakota Brown",
            "Sage Wilson", "River", "Phoenix Garcia", "Sky Martinez", "Kai",
            "Blake Anderson", "Drew", "Lane Cooper", "Rowan", "Ember"
        ]

        # Shuffle and return 10 names
        random.shuffle(american_names)
        return american_names[:10]

# Convenience function for easy import
def get_random_studio_names() -> List[str]:
    """
    Get 5 random studio names

    Returns:
        List of 5 studio names
    """
    service = DeepSeekNamingService()
    return service.generate_studio_names()

# Convenience function for player names
def get_random_player_names() -> List[str]:
    """
    Get 10 random player names

    Returns:
        List of 10 player names
    """
    service = DeepSeekNamingService()
    return service.generate_player_names()

# Get competitor company names for 1978 era
def get_competitor_companies() -> List[str]:
    """
    Get 20 competitor game company names appropriate for 1978 era using DeepSeek API

    Returns:
        List of 20 competitor company names
    """
    service = DeepSeekNamingService()
    return service.generate_competitor_companies()

# Get default competitor companies from database
def get_default_competitor_companies() -> List[str]:
    """
    Get default competitor companies from our database

    Returns:
        List of 20 competitor company names from our default list
    """
    import random
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from npcs.npc_database import COMPANY_NAMES

    # Return 20 random companies from our list
    return random.sample(COMPANY_NAMES, min(20, len(COMPANY_NAMES)))

# Test function
def test_naming_service():
    """Test the naming service"""
    print("Testing DeepSeek Naming Service...")
    service = DeepSeekNamingService()
    names = service.generate_studio_names()

    print("\nGenerated Studio Names:")
    print(f"1. Descriptive: {names[0]}")
    print(f"2. Fierce/Elemental: {names[1]}")
    print(f"3. Simple/Brandable: {names[2]}")

if __name__ == "__main__":
    test_naming_service()