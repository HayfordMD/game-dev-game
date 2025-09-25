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

    def test_boon_request(self, topic: str) -> str:
        """Simple test to get a boon name for a topic"""
        print(f"[DEEPSEEK TEST] Requesting boon for {topic}")
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {
                            "role": "user",
                            "content": f"Give me the name of a special item of power or boon for a {topic} adventure game - what the player wins. 1 item only, just the name. Be quick and concise."
                        }
                    ],
                    "temperature": 0.7,
                    "max_tokens": 30
                },
                timeout=15  # Shorter timeout for simple request
            )

            print(f"[DEEPSEEK TEST] Response status: {response.status_code}")
            response.raise_for_status()
            result = response.json()
            boon = result['choices'][0]['message']['content'].strip()
            print(f"[DEEPSEEK TEST] Boon received: {boon}")
            return boon
        except Exception as e:
            print(f"[DEEPSEEK TEST] Error: {e}")
            return None

    def get_welcome_message(self, topic: str, boon: str) -> str:
        """Get just the welcome message for a game"""
        print(f"[DEEPSEEK] Requesting welcome message for {topic} with boon: {boon}")
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {
                            "role": "user",
                            "content": f"Write a welcome message for a {topic} text adventure game where the player seeks '{boon}'. 2-3 sentences. Set the scene and mention the treasure. Be quick."
                        }
                    ],
                    "temperature": 0.8,
                    "max_tokens": 150
                },
                timeout=20
            )

            response.raise_for_status()
            result = response.json()
            welcome = result['choices'][0]['message']['content'].strip()
            print(f"[DEEPSEEK] Welcome message received")
            return welcome
        except Exception as e:
            print(f"[DEEPSEEK] Welcome error: {e}")
            return None

    def generate_room(self, topic: str, boon: str, room_num: int, previous_context: str = "") -> Dict:
        """Generate a single room with context from previous rooms"""
        print(f"[DEEPSEEK] Generating room {room_num} for {topic}")

        # Build context message
        context = f"Text adventure game: {topic} theme, seeking '{boon}'.\n"
        if previous_context:
            context += f"Story so far: {previous_context}\n"

        prompt = f"""{context}
Generate room {room_num} of 10. {"This is the FINAL room where the player can win the " + boon if room_num == 10 else ""}
Provide 3-4 choices. Include at least one ADVANCE option {"to victory" if room_num == 10 else "to next room"}.
Format as JSON:
{{
  "description": "Room description",
  "choices": {{
    "A": {{"text": "Choice text", "outcome": "ADVANCE/RETREAT/DEATH", "result_text": "What happens"}},
    "B": {{"text": "Choice text", "outcome": "ADVANCE/RETREAT/DEATH", "result_text": "What happens"}}
  }}
}}
Be creative but quick. Short responses."""

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.8,
                    "max_tokens": 400
                },
                timeout=30
            )

            response.raise_for_status()
            result = response.json()
            content = result['choices'][0]['message']['content'].strip()

            # Try to parse JSON from response
            if "```json" in content:
                json_start = content.find("```json") + 7
                json_end = content.find("```", json_start)
                json_str = content[json_start:json_end].strip()
            else:
                json_str = content

            room_data = json.loads(json_str)
            room_data['choice_count'] = len(room_data.get('choices', {}))
            print(f"[DEEPSEEK] Room {room_num} generated with {room_data['choice_count']} choices")
            return room_data

        except Exception as e:
            print(f"[DEEPSEEK] Error generating room {room_num}: {e}")
            return None

    def generate_adventure_incremental(self, topic: str) -> Dict[str, Any]:
        """Generate adventure game incrementally with multiple quick API calls"""
        print(f"[DEEPSEEK INCREMENTAL] Starting incremental generation for {topic}")

        try:
            # Step 1: Get the boon
            boon = self.test_boon_request(topic)
            if not boon:
                print("[DEEPSEEK INCREMENTAL] Failed to get boon, using fallback")
                boon = f"The {topic} Crystal"

            # Step 2: Get welcome message
            welcome = self.get_welcome_message(topic, boon)
            if not welcome:
                print("[DEEPSEEK INCREMENTAL] Failed to get welcome, using fallback")
                welcome = f"You seek the legendary {boon} in this {topic} adventure. Many have tried, none returned."

            # Build the game structure
            game_data = {
                "game_title": f"{topic} Quest for {boon}",
                "welcome_message": welcome,
                "boon_description": f"{boon} - A legendary artifact of immense power.",
                "victory_message": f"You have claimed {boon}! Victory is yours!",
                "rooms": {}
            }

            # Step 3: Generate rooms one by one (can be done in parallel later)
            context = ""
            for room_num in range(1, 11):
                print(f"[DEEPSEEK INCREMENTAL] Generating room {room_num}/10")

                room = self.generate_room(topic, boon, room_num, context)
                if room:
                    game_data["rooms"][str(room_num)] = room
                    # Add to context for next room (keep it brief)
                    context += f"Room {room_num}: {room.get('description', '')[:50]}... "
                else:
                    # Use a fallback room if generation fails
                    print(f"[DEEPSEEK INCREMENTAL] Using fallback for room {room_num}")
                    game_data["rooms"][str(room_num)] = self.create_fallback_room(room_num)

            print(f"[DEEPSEEK INCREMENTAL] Game generation complete!")
            return game_data

        except Exception as e:
            print(f"[DEEPSEEK INCREMENTAL] Error: {e}")
            return None

    def create_fallback_room(self, room_num: int) -> Dict:
        """Create a simple fallback room if API fails"""
        is_final = room_num == 10
        return {
            "description": f"Room {room_num}: {'The final chamber!' if is_final else 'A mysterious chamber awaits.'}",
            "choice_count": 3,
            "choices": {
                "A": {
                    "text": "Take the left path",
                    "outcome": "ADVANCE",
                    "result_text": "You found the way!" if is_final else "You proceed forward."
                },
                "B": {
                    "text": "Take the right path",
                    "outcome": "RETREAT",
                    "result_text": "You must go back."
                },
                "C": {
                    "text": "Touch the mysterious object",
                    "outcome": "DEATH",
                    "result_text": "A trap! Your adventure ends."
                }
            }
        }

    def generate_adventure_game(self, topic: str) -> Dict[str, Any]:
        """Generate a text adventure game based on topic"""
        print(f"[DEEPSEEK] Starting API request for topic: {topic}")

        # Create the prompt based on topic
        prompt = self.create_game_prompt(topic)
        print(f"[DEEPSEEK] Prompt length: {len(prompt)} characters")

        # Make API request
        try:
            print(f"[DEEPSEEK] Sending request to {self.base_url}/chat/completions")
            print(f"[DEEPSEEK] Timeout set to 150 seconds (2.5 minutes)")

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
                timeout=150  # 2.5 minute timeout (API can take up to 2 minutes)
            )

            print(f"[DEEPSEEK] Response received! Status code: {response.status_code}")
            response.raise_for_status()
            result = response.json()
            print(f"[DEEPSEEK] Response JSON parsed successfully")

            # Extract the generated content
            content = result['choices'][0]['message']['content']
            print(f"[DEEPSEEK] Content extracted, length: {len(content)} characters")

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
            print(f"API request timed out after 2.5 minutes. The service may be slow or unavailable.")
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