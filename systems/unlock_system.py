"""
Unlock System for Topics and Game Types
Manages permanent and per-save unlocks based on generation and requirements
"""

import json
import os
from datetime import datetime


class UnlockSystem:
    """Manages unlocked content for the game"""

    def __init__(self, game_data):
        self.game_data = game_data
        self.permanent_unlocks_file = "permanent_unlocks.json"

        # Load permanent unlocks (persist across all saves)
        self.permanent_unlocks = self.load_permanent_unlocks()

        # Initialize save-specific unlocks if not present
        if 'unlocks' not in self.game_data.data:
            self.game_data.data['unlocks'] = {
                'topics': [],
                'game_types': []
            }

    def load_permanent_unlocks(self):
        """Load permanent unlocks from file"""
        if os.path.exists(self.permanent_unlocks_file):
            try:
                with open(self.permanent_unlocks_file, 'r') as f:
                    return json.load(f)
            except:
                pass

        # Default structure
        return {
            'topics': [],
            'game_types': [],
            'achievements': []
        }

    def save_permanent_unlocks(self):
        """Save permanent unlocks to file"""
        with open(self.permanent_unlocks_file, 'w') as f:
            json.dump(self.permanent_unlocks, f, indent=2)

    def get_generation_unlocks(self):
        """Get unlocks based on current year/generation"""
        year = self.game_data.data.get('time', {}).get('year', 1978)

        unlocks = {
            'topics': [],
            'game_types': []
        }

        # Starting game types (only these at beginning)
        if year >= 1978:
            unlocks['game_types'].extend(['Text Adventure', 'Arcade'])

        # Starting topics
        if year >= 1978:
            unlocks['topics'].extend(['Table Tennis', 'Fantasy', 'Space', 'Temple', 'Adventure'])

        return unlocks

    def check_game_creation_unlocks(self, game_name, topic, game_type):
        """Check for unlocks when creating a game"""
        unlocked = []

        # Track Arcade game count for Racing unlock
        if game_type == 'Arcade':
            if 'arcade_games_count' not in self.game_data.data:
                self.game_data.data['arcade_games_count'] = 0
            self.game_data.data['arcade_games_count'] += 1

            # Racing game type - unlocked by creating 3 Arcade games
            if self.game_data.data['arcade_games_count'] >= 3:
                if 'Racing' not in self.permanent_unlocks['game_types']:
                    self.permanent_unlocks['game_types'].append('Racing')
                    self.save_permanent_unlocks()
                    unlocked.append(('game_type', 'Racing', 'Created 3 Arcade games - Racing unlocked!'))

        # Office game type - unlocked by creating Ping game with Table Tennis and Arcade
        if (game_name and game_name.lower() == 'ping' and
            topic == 'Table Tennis' and
            game_type == 'Arcade'):
            if 'Office' not in self.permanent_unlocks['game_types']:
                self.permanent_unlocks['game_types'].append('Office')
                self.save_permanent_unlocks()
                unlocked.append(('game_type', 'Office', 'Created the legendary Ping game!'))

        # RPG game type - unlocked by creating Text Adventure + Fantasy
        if (topic == 'Fantasy' and game_type == 'Text Adventure'):
            if 'RPG' not in self.permanent_unlocks['game_types']:
                self.permanent_unlocks['game_types'].append('RPG')
                self.save_permanent_unlocks()
                unlocked.append(('game_type', 'RPG', 'Combined Fantasy with Text Adventures to discover RPGs!'))

        # Motion-Control game type - unlocked by creating Rhythm + Music topic
        if (game_type == 'Rhythm' and
            (topic in ['Music Creation', 'Music', 'Rhythm Games', 'Dance'])):
            if 'Motion-Control' not in self.permanent_unlocks['game_types']:
                self.permanent_unlocks['game_types'].append('Motion-Control')
                self.save_permanent_unlocks()
                unlocked.append(('game_type', 'Motion-Control', 'Music and rhythm games inspired motion controls!'))

        return unlocked

    def check_special_requirements(self):
        """Check for special unlock requirements"""
        unlocked = []

        # Get current time data
        time_data = self.game_data.data.get('time', {})
        year = time_data.get('year', 1978)
        month = time_data.get('month', 1)
        day = time_data.get('day', 1)

        # Track last desktop usage
        if 'last_desktop_use' not in self.game_data.data:
            self.game_data.data['last_desktop_use'] = {'year': year, 'month': month, 'day': day}

        # Calculate time since last desktop use
        last_use = self.game_data.data['last_desktop_use']
        years_passed = year - last_use['year']
        months_passed = (month - last_use['month']) + (years_passed * 12)

        # Idle game type - unlocked by not developing for 1 year
        if months_passed >= 12:
            if 'Idle' not in self.permanent_unlocks['game_types']:
                self.permanent_unlocks['game_types'].append('Idle')
                self.save_permanent_unlocks()
                unlocked.append(('game_type', 'Idle', 'What if you never did anything ever?'))

        # Bug topic - unlocked by low hygiene in early years
        hygiene = self.game_data.data.get('player_data', {}).get('hygiene', 100)

        if year >= 1978 and year <= 1983 and hygiene < 40:
            if 'Bugs' not in self.permanent_unlocks['topics']:
                self.permanent_unlocks['topics'].append('Bugs')
                self.save_permanent_unlocks()
                unlocked.append(('topic', 'Bugs', 'Low hygiene in early years!'))

        # Dinosaur topic - unlocked by making 3 successful adventure games
        completed_games = self.game_data.data.get('completed_games', {})
        if isinstance(completed_games, dict):
            adventure_games = completed_games.get('Adventure', 0)
        else:
            adventure_games = 0

        if adventure_games >= 3:
            if 'Dinosaurs' not in self.permanent_unlocks['topics']:
                self.permanent_unlocks['topics'].append('Dinosaurs')
                self.save_permanent_unlocks()
                unlocked.append(('topic', 'Dinosaurs', 'Created 3 adventure games!'))

        # Retro game type - unlocked by reaching year 2000 (special unlock)
        if year >= 2000:
            if 'Retro' not in self.permanent_unlocks['game_types']:
                self.permanent_unlocks['game_types'].append('Retro')
                self.save_permanent_unlocks()
                unlocked.append(('game_type', 'Retro', 'Reached the millennium!'))

        # Educational game type - unlocked by high happiness
        happiness = self.game_data.data.get('player_data', {}).get('happiness', 60)
        if happiness >= 90:
            if 'Educational' not in self.permanent_unlocks['game_types']:
                self.permanent_unlocks['game_types'].append('Educational')
                self.save_permanent_unlocks()
                unlocked.append(('game_type', 'Educational', 'Achieved 90% happiness!'))

        return unlocked

    def get_all_unlocked_topics(self):
        """Get all currently unlocked topics (generation + permanent + save-specific)"""
        topics = set()

        # Add generation-based unlocks
        gen_unlocks = self.get_generation_unlocks()
        topics.update(gen_unlocks['topics'])

        # Add permanent unlocks
        topics.update(self.permanent_unlocks['topics'])

        # Add save-specific unlocks
        topics.update(self.game_data.data['unlocks']['topics'])

        return sorted(list(topics))

    def get_all_unlocked_game_types(self):
        """Get all currently unlocked game types"""
        game_types = set()

        # Add generation-based unlocks
        gen_unlocks = self.get_generation_unlocks()
        game_types.update(gen_unlocks['game_types'])

        # Add permanent unlocks
        game_types.update(self.permanent_unlocks['game_types'])

        # Add save-specific unlocks
        game_types.update(self.game_data.data['unlocks']['game_types'])

        return sorted(list(game_types))

    def unlock_topic(self, topic, permanent=False):
        """Manually unlock a topic"""
        if permanent:
            if topic not in self.permanent_unlocks['topics']:
                self.permanent_unlocks['topics'].append(topic)
                self.save_permanent_unlocks()
        else:
            if topic not in self.game_data.data['unlocks']['topics']:
                self.game_data.data['unlocks']['topics'].append(topic)

    def unlock_game_type(self, game_type, permanent=False):
        """Manually unlock a game type"""
        if permanent:
            if game_type not in self.permanent_unlocks['game_types']:
                self.permanent_unlocks['game_types'].append(game_type)
                self.save_permanent_unlocks()
        else:
            if game_type not in self.game_data.data['unlocks']['game_types']:
                self.game_data.data['unlocks']['game_types'].append(game_type)

    def get_unlock_info(self):
        """Get information about all possible unlocks and their requirements"""
        return {
            'generation_unlocks': [
                {'year': 1978, 'topics': ['Space', 'Fantasy', 'Adventure', 'Mystery'],
                 'game_types': ['Text Adventure', 'Arcade']},
                {'year': 1983, 'topics': ['Sci-Fi', 'Medieval', 'Western', 'Pirates'],
                 'game_types': ['Platformer', 'Puzzle']},
                {'year': 1988, 'topics': ['Horror', 'Cyberpunk', 'Ninjas', 'Racing'],
                 'game_types': ['RPG', 'Racing', 'Fighting']},
                {'year': 1993, 'topics': ['Post-Apocalyptic', 'Zombies', 'Aliens', 'Sports'],
                 'game_types': ['3D Platformer', 'FPS', 'Sports']},
                {'year': 1998, 'topics': ['Modern', 'Historical', 'Steampunk', 'Superheroes'],
                 'game_types': ['Strategy', 'Simulation', 'MMORPG']},
                {'year': 2003, 'topics': ['Mythology', 'Time Travel', 'Vampires', 'Robots'],
                 'game_types': ['Open World', 'Battle Royale', 'MOBA']}
            ],
            'special_unlocks': [
                {'name': 'Bugs', 'type': 'topic', 'requirement': 'Have < 40% hygiene between 1978-1983',
                 'permanent': True},
                {'name': 'Dinosaurs', 'type': 'topic', 'requirement': 'Create 3 successful adventure games',
                 'permanent': True},
                {'name': 'Retro', 'type': 'game_type', 'requirement': 'Reach year 2000',
                 'permanent': True},
                {'name': 'Educational', 'type': 'game_type', 'requirement': 'Achieve 90% happiness',
                 'permanent': True}
            ],
            'current_permanent': self.permanent_unlocks,
            'current_save': self.game_data.data['unlocks']
        }