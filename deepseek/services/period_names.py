import requests
import json
import os
from typing import List, Dict, Optional
import random

class PeriodNameGenerator:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Period Name Generator with DeepSeek API
        """
        self.api_key = api_key or os.getenv('DEEPSEEK_API_KEY')
        self.base_url = "https://api.deepseek.com/v1/chat/completions"

        # Define eras and their characteristics
        self.eras = {
            "1970-1974": {
                "description": "Early 70s - Disco era beginning, Vietnam War ending, Watergate",
                "popular_names": "Classic American names, some hippie influence"
            },
            "1975-1979": {
                "description": "Late 70s - Disco peak, Star Wars, punk rock emerging",
                "popular_names": "Traditional names with some creative spellings starting"
            },
            "1980-1984": {
                "description": "Early 80s - MTV generation, Reagan era, arcade games boom",
                "popular_names": "Preppy names, Dynasty/Dallas influence, Jennifer/Jason peak"
            },
            "1985-1989": {
                "description": "Late 80s - Wall Street era, Nintendo, hair metal",
                "popular_names": "Ashley/Jessica popular, unique spellings increase"
            },
            "1990-1994": {
                "description": "Early 90s - Grunge era, early internet, Gulf War",
                "popular_names": "90s classics like Brittany/Brandon, nature names emerging"
            },
            "1995-1999": {
                "description": "Late 90s - Dot-com boom, Y2K prep, Pokemon",
                "popular_names": "Tech-influenced names, international names becoming popular"
            },
            "2000-2004": {
                "description": "Early 2000s - 9/11 era, reality TV boom, early social media",
                "popular_names": "Madison/Aiden trend, last names as first names"
            },
            "2005-2009": {
                "description": "Late 2000s - iPhone launch, Facebook opens to public, Obama election",
                "popular_names": "Unique spellings peak, celebrity baby name influence"
            },
            "2010-2014": {
                "description": "Early 2010s - Instagram era, millennials entering workforce",
                "popular_names": "Old-fashioned names revival, gender-neutral names rising"
            },
            "2015-2019": {
                "description": "Late 2010s - Streaming services dominate, gig economy",
                "popular_names": "Nature names popular, multicultural names mainstream"
            },
            "2020-2024": {
                "description": "Early 2020s - Pandemic era, remote work, AI emergence",
                "popular_names": "Tech-inspired names, nostalgic throwbacks, unique spellings"
            },
            "2025-2030": {
                "description": "Late 2020s - AI integration, climate focus, space exploration",
                "popular_names": "Futuristic names, environmental themes, global fusion names"
            }
        }

        # Storage for generated names
        self.period_names = {}

    def generate_names_for_period(self, period: str, count: int = 75) -> List[str]:
        """
        Generate period-appropriate names using DeepSeek API

        Args:
            period: Time period string (e.g., "1970-1974")
            count: Number of names to generate

        Returns:
            List of period-appropriate names
        """
        if not self.api_key:
            return self._get_fallback_names_for_period(period, count)

        era_info = self.eras.get(period, {})

        prompt = f"""Generate {count} American names that would be common for people born or named during {period}.

Context: {era_info.get('description', '')}
Name style: {era_info.get('popular_names', '')}

Mix of:
- Common/popular names for that era (40%)
- Traditional names that persist through time (30%)
- Unique or trendy names specific to that period (30%)

Include both first names only and full names (first + last).
Mix male, female, and some gender-neutral names.

Return ONLY the names, one per line, no explanations, numbers, or categories."""

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
                "max_tokens": 1500,
                "temperature": 0.9
            }

            response = requests.post(self.base_url, headers=headers, json=data, timeout=15)

            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content'].strip()
                names = [name.strip() for name in content.split('\n') if name.strip()]

                # Ensure we have the requested count
                if len(names) >= count:
                    return names[:count]
                else:
                    # Pad with fallback names
                    fallback = self._get_fallback_names_for_period(period, count - len(names))
                    names.extend(fallback)
                    return names[:count]
            else:
                print(f"DeepSeek API error: {response.status_code} - {response.text}")
                return self._get_fallback_names_for_period(period, count)

        except Exception as e:
            print(f"Error calling DeepSeek API: {e}")
            return self._get_fallback_names_for_period(period, count)

    def _get_fallback_names_for_period(self, period: str, count: int) -> List[str]:
        """
        Get fallback names for a specific period when API is unavailable
        """
        # Period-specific fallback names
        period_names = {
            "1970-1974": [
                "David Johnson", "Susan", "Michael Smith", "Linda Brown", "John",
                "Patricia Davis", "Robert", "Barbara Wilson", "James Miller", "Mary",
                "Richard Anderson", "Jennifer", "Thomas", "Carol Martinez", "Christopher"
            ],
            "1975-1979": [
                "William Johnson", "Lisa", "Mark Thompson", "Karen White", "Steven",
                "Nancy Harris", "Gary", "Betty Martin", "Kenneth Jackson", "Dorothy",
                "Jason Williams", "Amy", "Jeff Davis", "Michelle", "Brian"
            ],
            "1980-1984": [
                "Jennifer Smith", "Matthew", "Jessica Brown", "Joshua Davis", "Amanda",
                "Christopher Miller", "Ashley", "Andrew Wilson", "Stephanie", "Daniel",
                "Brandon Taylor", "Heather", "Justin Anderson", "Nicole", "Ryan"
            ],
            "1985-1989": [
                "Michael Johnson", "Sarah", "David Martinez", "Laura Rodriguez", "Robert",
                "Megan Garcia", "James", "Rachel Hernandez", "John Lopez", "Samantha",
                "Kevin Brown", "Emily", "Eric Davis", "Brittany", "Jonathan"
            ],
            "1990-1994": [
                "Tyler Smith", "Taylor", "Brandon Johnson", "Brittany Williams", "Austin",
                "Kayla Brown", "Kyle", "Alexis Jones", "Jordan Miller", "Morgan",
                "Dylan Davis", "Hannah", "Zachary Wilson", "Madison", "Nathan"
            ],
            "1995-1999": [
                "Jacob Anderson", "Emma", "Ethan Martinez", "Olivia Taylor", "Noah",
                "Isabella Thomas", "Mason", "Sophia Jackson", "Logan White", "Ava",
                "Alexander Harris", "Mia", "Lucas Martin", "Charlotte", "Mason"
            ],
            "2000-2004": [
                "Aiden Smith", "Madison", "Jayden Brown", "Emma Johnson", "Ethan",
                "Abigail Davis", "Mason", "Olivia Miller", "Noah Wilson", "Isabella",
                "Liam Anderson", "Sophia", "Jackson Martinez", "Ava", "Lucas"
            ],
            "2005-2009": [
                "Mason Taylor", "Emma", "Liam Johnson", "Olivia Brown", "Noah",
                "Sophia Davis", "Ethan", "Isabella Miller", "Aiden Wilson", "Mia",
                "Jackson Anderson", "Charlotte", "Lucas Martinez", "Amelia", "Oliver"
            ],
            "2010-2014": [
                "Liam Smith", "Emma", "Noah Johnson", "Olivia Brown", "Oliver",
                "Ava Davis", "Elijah", "Sophia Miller", "William Wilson", "Isabella",
                "James Anderson", "Mia", "Benjamin Martinez", "Charlotte", "Lucas"
            ],
            "2015-2019": [
                "Oliver Chen", "Luna", "Mateo Rodriguez", "Aurora Smith", "Kai",
                "Nova Johnson", "Ezra", "Willow Brown", "River Davis", "Hazel",
                "Atlas Miller", "Ivy Wilson", "Phoenix Anderson", "Sage", "Rowan"
            ],
            "2020-2024": [
                "Luca Martin", "Luna", "Kai Patel", "Nova Chen", "Zion",
                "Aurora Kim", "River", "Aria Singh", "Phoenix Lee", "Ivy",
                "Atlas Wong", "Sage Zhang", "Orion Davis", "Willow", "Neo"
            ],
            "2025-2030": [
                "Zephyr Nova", "Aria", "Quantum Smith", "Luna Ray", "Orion",
                "Stella Mars", "Neo", "Aurora Sky", "Phoenix Blaze", "Sage",
                "River Cloud", "Nova", "Atlas Storm", "Echo", "Zen"
            ]
        }

        base_names = period_names.get(period, period_names["1990-1994"])

        # Generate variations and expand the list
        expanded_names = []
        for _ in range((count // len(base_names)) + 1):
            expanded_names.extend(base_names)

        random.shuffle(expanded_names)
        return expanded_names[:count]

    def generate_all_periods(self) -> Dict[str, List[str]]:
        """
        Generate names for all time periods

        Returns:
            Dictionary with period as key and list of names as value
        """
        print("Generating names for all time periods...")

        for period in self.eras.keys():
            print(f"Generating names for {period}...")
            # Generate 50-100 names per period (using 75 as average)
            names = self.generate_names_for_period(period, 75)
            self.period_names[period] = names
            print(f"  Generated {len(names)} names for {period}")

        return self.period_names

    def get_names_for_year(self, year: int, count: int = 10) -> List[str]:
        """
        Get appropriate names for a specific year

        Args:
            year: The year to get names for
            count: Number of names to return

        Returns:
            List of period-appropriate names
        """
        # Find the appropriate period for the year
        period = None
        for period_key in self.eras.keys():
            start_year, end_year = map(int, period_key.split('-'))
            if start_year <= year <= end_year:
                period = period_key
                break

        if not period:
            # Default to 1990s if year is out of range
            period = "1990-1994"

        # Generate names if not already generated
        if period not in self.period_names:
            self.period_names[period] = self.generate_names_for_period(period, 75)

        names = self.period_names[period]

        # Return random selection of names
        if len(names) >= count:
            return random.sample(names, count)
        else:
            return names

    def save_to_file(self, filename: str = "period_names.json"):
        """
        Save generated names to a JSON file
        """
        with open(filename, 'w') as f:
            json.dump(self.period_names, f, indent=2)
        print(f"Saved {sum(len(names) for names in self.period_names.values())} names to {filename}")

    def load_from_file(self, filename: str = "period_names.json"):
        """
        Load names from a JSON file
        """
        try:
            with open(filename, 'r') as f:
                self.period_names = json.load(f)
            print(f"Loaded {sum(len(names) for names in self.period_names.values())} names from {filename}")
            return True
        except FileNotFoundError:
            print(f"File {filename} not found")
            return False


# Convenience functions
def generate_all_period_names():
    """
    Generate names for all time periods and save to file
    """
    generator = PeriodNameGenerator()
    names = generator.generate_all_periods()
    generator.save_to_file()
    return names


def get_names_for_game_year(year: int, count: int = 10) -> List[str]:
    """
    Get period-appropriate names for a specific game year

    Args:
        year: The game year
        count: Number of names to return

    Returns:
        List of period-appropriate names
    """
    generator = PeriodNameGenerator()

    # Try to load from file first
    if not generator.load_from_file():
        # Generate if file doesn't exist
        generator.generate_all_periods()
        generator.save_to_file()

    return generator.get_names_for_year(year, count)


# Test function
if __name__ == "__main__":
    print("Testing Period Name Generator...")

    # Generate all names
    generator = PeriodNameGenerator()
    all_names = generator.generate_all_periods()

    # Display summary
    total = 0
    for period, names in all_names.items():
        print(f"{period}: {len(names)} names")
        total += len(names)
        # Show first 5 names as example
        print(f"  Examples: {', '.join(names[:5])}")

    print(f"\nTotal names generated: {total}")

    # Save to file
    generator.save_to_file()

    # Test getting names for specific years
    print("\nTesting year-specific retrieval:")
    for year in [1972, 1985, 1999, 2010, 2025]:
        names = generator.get_names_for_year(year, 5)
        print(f"{year}: {', '.join(names)}")