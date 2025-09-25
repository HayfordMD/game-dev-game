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
            unlocks['game_types'].extend(['Text Adventure', 'Arcade', 'RPG'])

        # Starting topics - Updated list
        if year >= 1978:
            unlocks['topics'].extend([
                'Zombies', 'Temple', 'Fantasy', 'Space', 'Table Tennis',
                'Postal Work', 'Questing Heroes', 'World War II', 'City Building',
                'Ocean Exploration', 'Golf', 'Painting', 'Bugs'
            ])

        return unlocks

    def check_game_creation_unlocks(self, game_name, topic, game_type):
        """Check for unlocks when creating a game"""
        unlocked = []

        # # Track Arcade game count for Racing unlock
        # # Commented out - Racing not in active game types list
        # if game_type == 'Arcade':
        #     if 'arcade_games_count' not in self.game_data.data:
        #         self.game_data.data['arcade_games_count'] = 0
        #     self.game_data.data['arcade_games_count'] += 1
        #
        #     # Racing game type - unlocked by creating 3 Arcade games
        #     if self.game_data.data['arcade_games_count'] >= 3:
        #         if 'Racing' not in self.permanent_unlocks['game_types']:
        #             self.permanent_unlocks['game_types'].append('Racing')
        #             self.save_permanent_unlocks()
        #             unlocked.append(('game_type', 'Racing', 'Created 3 Arcade games - Racing unlocked!'))

        # No special unlock for Ping game anymore (Office type removed)

        # # RPG game type - unlocked by creating Text Adventure + Fantasy
        # # Commented out - RPG now unlocked by year in generation_unlocks
        # if (topic == 'Fantasy' and game_type == 'Text Adventure'):
        #     if 'RPG' not in self.permanent_unlocks['game_types']:
        #         self.permanent_unlocks['game_types'].append('RPG')
        #         self.save_permanent_unlocks()
        #         unlocked.append(('game_type', 'RPG', 'Combined Fantasy with Text Adventures to discover RPGs!'))


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

        # # RPG game type - now available from start
        # # Commented out - RPG is in starting game types
        # if year >= 1989:
        #     if 'RPG' not in self.permanent_unlocks['game_types']:
        #         self.permanent_unlocks['game_types'].append('RPG')
        #         self.save_permanent_unlocks()
        #         unlocked.append(('game_type', 'RPG', 'Year 1989 reached - RPG games now available!'))

        # # Strategy game type - unlocked after 1992 or by making 2 board games
        # # Commented out - not in active game types list
        # if year >= 1992:
        #     if 'Strategy' not in self.permanent_unlocks['game_types']:
        #         self.permanent_unlocks['game_types'].append('Strategy')
        #         self.save_permanent_unlocks()
        #         unlocked.append(('game_type', 'Strategy', 'Year 1992 reached!'))

        # # Online game type - available 1994-2000
        # # Commented out - not in active game types list
        # if year >= 1994 and year <= 2000:
        #     if 'Online' not in self.game_data.data['unlocks']['game_types']:
        #         self.game_data.data['unlocks']['game_types'].append('Online')
        #         unlocked.append(('game_type', 'Online', 'Online gaming is now available (with connection issues)!'))

        # # Educational game type - unlocked by high happiness
        # # Commented out - not in active game types list
        # happiness = self.game_data.data.get('player_data', {}).get('happiness', 60)
        # if happiness >= 90:
        #     if 'Educational' not in self.permanent_unlocks['game_types']:
        #         self.permanent_unlocks['game_types'].append('Educational')
        #         self.save_permanent_unlocks()
        #         unlocked.append(('game_type', 'Educational', 'Achieved 90% happiness!'))

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
                {'year': 1978, 'topics': ['Zombies', 'Temple', 'Fantasy', 'Space', 'Table Tennis',
                                          'Postal Work', 'Questing Heroes', 'World War II', 'City Building',
                                          'Ocean Exploration', 'Golf', 'Painting', 'Bugs'],
                 'game_types': ['Text Adventure', 'Arcade', 'RPG']},
                {'year': 1983, 'topics': [],  # ['Dragons', 'Medieval Europe', 'Wild West', 'Pirates'],
                 'game_types': ['Platformer', 'Puzzle']},
                {'year': 1985, 'topics': [],  # ['Zombies', 'Cyberpunk', 'Ninjas'],
                 'game_types': ['Shooter']},  # 'Fighting' removed
                # {'year': 1987, 'topics': ['Post-Apocalyptic', 'Vampires', 'Alien Invasion', 'Golf'],
                #  'game_types': ['Adventure', 'Action']},  # Commented out
                {'year': 1990, 'topics': [],  # ['City Building', 'War', 'Mechs', 'Robots'],
                 'game_types': ['Simulation']},
                # {'year': 1995, 'topics': ['Gods & Titans', 'Ghosts', 'AI Uprising'],
                #  'game_types': ['Visual Novel']},  # Commented out
                # {'year': 1989, 'topics': [],
                #  'game_types': ['RPG']}  # RPG now available from start
            ],
            'special_unlocks': [
                {'name': 'Bugs', 'type': 'topic', 'requirement': 'Have < 40% hygiene between 1978-1983',
                 'permanent': True},
                {'name': 'Dinosaurs', 'type': 'topic', 'requirement': 'Create 3 successful adventure games',
                 'permanent': True},
                # {'name': 'Strategy', 'type': 'game_type', 'requirement': 'Reach year 1992 or create 2 board games',
                #  'permanent': True},
                # {'name': 'Online', 'type': 'game_type', 'requirement': 'Available from 1994 to 2000',
                #  'permanent': False},
                # {'name': 'Educational', 'type': 'game_type', 'requirement': 'Achieve 90% happiness',
                #  'permanent': True}
                # {'name': 'RPG', 'type': 'game_type', 'requirement': 'Available from start',
                #  'permanent': False}  # RPG now in starting types
            ],
            'current_permanent': self.permanent_unlocks,
            'current_save': self.game_data.data['unlocks']
        }