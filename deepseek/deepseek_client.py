"""
DeepSeek API Client for game generation
"""

import os
import json
import requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class DeepSeekClient:
    """Client for DeepSeek API interactions"""

    def __init__(self):
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY not found in environment variables")

        self.base_url = "https://api.deepseek.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def generate_adventure_game(self, topic: str) -> Dict[str, Any]:
        """Generate a text adventure game based on topic"""

        # Create the prompt based on topic
        prompt = self.create_game_prompt(topic)

        # Make API request
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a creative game designer who creates engaging text adventure games in valid JSON format."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.8,
                    "max_tokens": 4000
                },
                timeout=60  # 60 second timeout
            )

            response.raise_for_status()
            result = response.json()

            # Extract the generated content
            content = result['choices'][0]['message']['content']

            # Parse JSON from the response
            # Try to extract JSON if it's wrapped in markdown code blocks
            if "```json" in content:
                json_start = content.find("```json") + 7
                json_end = content.find("```", json_start)
                json_str = content[json_start:json_end].strip()
            elif "```" in content:
                json_start = content.find("```") + 3
                json_end = content.find("```", json_start)
                json_str = content[json_start:json_end].strip()
            else:
                json_str = content

            # Parse the JSON
            game_data = json.loads(json_str)
            return game_data

        except requests.exceptions.Timeout as e:
            print(f"API request timed out after 60 seconds. The service may be slow or unavailable.")
            print(f"Error details: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response status: {e.response.status_code}")
                print(f"Response text: {e.response.text[:500]}")
            return None
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON response: {e}")
            print(f"Response content: {content[:500]}...")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    def create_game_prompt(self, topic: str) -> str:
        """Create the prompt for game generation"""

        # Generate a unique boon name based on topic
        boon_name = self.generate_boon_name(topic)

        prompt = f"""Create a JSON-formatted text adventure game called "{topic} of the {boon_name}" with the following specifications:

GAME STRUCTURE:
- 10 sequential rooms (numbered 1-10)
- Room 10 contains the winning BOON: {boon_name}
- Each room has 3-5 choices (vary the number per room)
- Choice outcomes for each room: 1 kills player (DEATH), 1 sends player back one room (RETREAT), remaining choices advance to next room (ADVANCE)
- Randomize which choice letters correspond to which outcome in each room
- PROGRESSIVE DIFFICULTY: Make choices increasingly ambiguous as player advances through rooms

THEME: {topic}
- Create a setting appropriate for "{topic}"
- Include thematic hazards and obstacles
- Make descriptions match the {topic} theme

CHOICE CLARITY PROGRESSION:
- Rooms 1-3: Choices should be relatively clear about their nature
- Rooms 4-6: Moderate ambiguity - choices hint at consequences but aren't obvious
- Rooms 7-10: High ambiguity - all choices appear equally viable

JSON STRUCTURE REQUIRED:
{{
  "game_title": "{topic} of the {boon_name}",
  "welcome_message": "[Atmospheric intro describing the setting and quest]",
  "boon_description": "[What the {boon_name} is and its power]",
  "rooms": {{
    "1": {{
      "description": "[Room description 50-75 words]",
      "choice_count": 3,
      "choices": {{
        "A": {{"text": "[Choice description]", "outcome": "DEATH", "result_text": "[What happens]"}},
        "B": {{"text": "[Choice description]", "outcome": "RETREAT", "result_text": "[What happens]"}},
        "C": {{"text": "[Choice description]", "outcome": "ADVANCE", "result_text": "[What happens]"}}
      }}
    }},
    [Continue for rooms 2-10 with varying choice_count between 3-5]
  }},
  "victory_message": "[Winning text when player reaches room 10 and claims the boon]"
}}

IMPORTANT:
- Each room MUST have exactly ONE choice with outcome "DEATH"
- Each room MUST have exactly ONE choice with outcome "RETREAT"
- All other choices must have outcome "ADVANCE"
- Randomize which letter (A, B, C, D, E) gets which outcome
- Make the {topic} theme consistent throughout
- Room descriptions should be atmospheric and build tension
- Death descriptions should be dramatic and specific to each room
- The final room (10) should be epic and contain the {boon_name}

Generate the complete JSON now:"""

        return prompt

    def generate_boon_name(self, topic: str) -> str:
        """Generate an appropriate boon name for the topic"""
        boon_names = {
            "AI Uprising": "Core of the Singularity",
            "Space": "Quantum Navigator's Key",
            "Dragon": "Heart of the Ancient Wyrm",
            "Temple": "Sacred Eye of Eternity",
            "Fantasy": "Crown of Infinite Magic",
            "Horror": "Mirror of Forgotten Souls",
            "Cyberpunk": "Neural Interface Prime",
            "Steampunk": "Clockwork Heart of Time",
            "Zombie": "Serum of the First Cure",
            "Alien": "Xenomorph Queen's Crown"
        }

        # Return specific boon or generate based on topic
        return boon_names.get(topic, f"Sacred {topic} Artifact")