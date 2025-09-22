import requests
import json
import os
from typing import List, Optional

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

        prompt = """Give me a name for a game studio. I need exactly 3 options:

1. One descriptive/technical name like "Sun Systems Development" or "ID Software"
2. One fierce/elemental name like "Shark Systems", "Shadow Games", "Light House Studios", or "Fast Games"
3. One simple/brandable name like "Bungie", "Blizzard", "FOREDATING", "AXEL", or "QUBIT"

Return only the three names, one per line, no explanations."""

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

                # Ensure we have exactly 3 names
                if len(names) >= 3:
                    return names[:3]
                else:
                    # If we got fewer than 3, pad with fallback names
                    fallback = self._get_fallback_names()
                    while len(names) < 3:
                        names.append(fallback[len(names) % 3])
                    return names[:3]
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
            List of 3 predetermined studio names
        """
        import random

        descriptive_names = [
            "Digital Systems Development",
            "Code Forge Studios",
            "Pixel Engine Works",
            "Interactive Media Labs",
            "Game Logic Studios"
        ]

        fierce_elemental_names = [
            "Storm Games",
            "Iron Wolf Studios",
            "Lightning Studios",
            "Fire Mountain Games",
            "Thunder Bay Studios"
        ]

        simple_brandable_names = [
            "Zenith",
            "Apex",
            "Nexus",
            "Prism",
            "Flux"
        ]

        return [
            random.choice(descriptive_names),
            random.choice(fierce_elemental_names),
            random.choice(simple_brandable_names)
        ]

# Convenience function for easy import
def get_random_studio_names() -> List[str]:
    """
    Get 3 random studio names

    Returns:
        List of 3 studio names
    """
    service = DeepSeekNamingService()
    return service.generate_studio_names()

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