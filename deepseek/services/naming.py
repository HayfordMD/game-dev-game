import requests
import json
import os
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class DeepSeekNamingService:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize DeepSeek naming service

        Args:
            api_key: DeepSeek API key. If None, will try to get from environment variable DEEPSEEK_API_KEY
        """
        self.api_key = api_key or os.getenv('DEEPSEEK_API_KEY')
        self.base_url = "https://api.deepseek.com/v1/chat/completions"

        if not self.api_key:
            print("Warning: No DeepSeek API key found. Set DEEPSEEK_API_KEY environment variable or pass api_key parameter.")

    def generate_studio_names(self) -> List[str]:
        """
        Generate 3 game studio names using DeepSeek API

        Returns:
            List of 3 studio names:
            [descriptive_name, fierce_elemental_name, simple_brandable_name]
        """
        if not self.api_key:
            return self._get_fallback_names()

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

            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content'].strip()
                names = [name.strip() for name in content.split('\n') if name.strip()]

                # Ensure we have exactly 5 names
                if len(names) >= 5:
                    return names[:5]
                else:
                    # If we got fewer than 5, pad with fallback names
                    fallback = self._get_fallback_names()
                    while len(names) < 5:
                        names.append(fallback[len(names) % 5])
                    return names[:5]
            else:
                print(f"DeepSeek API error: {response.status_code} - {response.text}")
                return self._get_fallback_names()

        except requests.exceptions.RequestException as e:
            print(f"Network error calling DeepSeek API: {e}")
            return self._get_fallback_names()
        except Exception as e:
            print(f"Error calling DeepSeek API: {e}")
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
            return self._get_fallback_player_names()

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
                print(f"DeepSeek API error: {response.status_code} - {response.text}")
                return self._get_fallback_player_names()

        except requests.exceptions.RequestException as e:
            print(f"Network error calling DeepSeek API: {e}")
            return self._get_fallback_player_names()
        except Exception as e:
            print(f"Error calling DeepSeek API: {e}")
            return self._get_fallback_player_names()

    def generate_competitor_companies(self) -> List[str]:
        """
        Generate 20 competitor game company names using DeepSeek API for 1978 era

        Returns:
            List of 20 competitor company names
        """
        if not self.api_key:
            return self._get_fallback_competitor_names()

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
                print(f"DeepSeek API error: {response.status_code} - {response.text}")
                return self._get_fallback_competitor_names()

        except requests.exceptions.RequestException as e:
            print(f"Network error calling DeepSeek API: {e}")
            return self._get_fallback_competitor_names()
        except Exception as e:
            print(f"Error calling DeepSeek API: {e}")
            return self._get_fallback_competitor_names()

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