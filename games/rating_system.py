"""
Game Rating System
Handles all game review scores and ratings throughout different eras
"""

import random
from datetime import datetime

class GameRatingSystem:
    def __init__(self, game_data):
        self.game_data = game_data

        # Rating categories with weights and visibility rules
        # Note: Random/X-Factor and Studio Reputation are applied AFTER the total calculation
        self.rating_categories = {
            'gameplay': {
                'name': 'Gameplay',
                'weight': 0.25,  # 25%
                'visible': True,
                'description': 'Fun factor, mechanics, controls, game design',
                'min_score': 0,
                'max_score': 100
            },
            'technical': {
                'name': 'Technical',
                'weight': 0.25,  # 25% (increased from 20%)
                'visible': True,
                'description': 'Engine performance, framerate, optimization, stability',
                'min_score': 0,
                'max_score': 100
            },
            'graphics': {
                'name': 'Graphics',
                'weight': 0.25,  # 25% (increased from 20%)
                'visible': True,
                'description': 'Visual quality, art style, animation, effects',
                'min_score': 0,
                'max_score': 100
            },
            'innovation': {
                'name': 'Innovation',
                'weight': 0.15,  # 15%
                'visible': True,
                'description': 'Originality, creativity, groundbreaking features',
                'min_score': 0,
                'max_score': 100
            },
            'sound': {
                'name': 'Sound/Audio',
                'weight': 0.05,  # 5%
                'visible': True,
                'description': 'Music, sound effects, voice acting',
                'min_score': 0,
                'max_score': 100
            },
            'story': {
                'name': 'Story',
                'weight': 0.05,  # 5%
                'visible': True,
                'description': 'Narrative, characters, dialogue, writing',
                'min_score': 0,
                'max_score': 100
            }
        }

        # Post-calculation modifiers (applied AFTER base score)
        self.random_factor = {
            'name': 'X-Factor',
            'range': (-15, 15),  # Can adjust final score by -15 to +15 points
            'visible': False,
            'description': 'Unpredictable market reception and timing'
        }

        self.reputation_modifier = {
            'name': 'Studio Reputation',
            'max_modifier': 7,  # Maximum ±7% modifier
            'visible_after_year': 1994,  # Becomes visible in 1994
            'visible': False,
            'description': 'Brand recognition effect on reception'
        }

        # Bug penalty system
        self.bug_penalty = {
            'per_bug': 5,  # Each bug removes 5 points from final score (out of 100)
            'max_penalty': 50,  # Maximum 50 point penalty from bugs
            'critical_bug_multiplier': 2  # Critical bugs count double
        }

        # Rating presentation formats for different eras and publications
        self.presentation_formats = {
            'percentage': lambda score: f"{int(score)}%",
            'out_of_10': lambda score: f"{score/10:.1f}/10",
            'out_of_5': lambda score: f"{score/20:.1f}/5",
            'stars': lambda score: '★' * int(score/20),
            'letter_grade': self.get_letter_grade,
            'thumbs': lambda score: '👍' if score >= 70 else '👎' if score < 50 else '👍👎',
            'buy_rent_skip': lambda score: 'BUY' if score >= 80 else 'RENT' if score >= 60 else 'SKIP',
            'metacritic': lambda score: self.get_metacritic_color(score)
        }

        # Studio reputation tracking
        if 'studio_reputation' not in self.game_data.data:
            self.game_data.data['studio_reputation'] = {
                'score': 5.0,  # Start at middle (0-10 scale)
                'games_released': 0,
                'total_revenue': 0,
                'average_rating': 5.0,
                'hit_games': 0,  # Games with 8+ rating
                'flop_games': 0,  # Games with 4- rating
                'consecutive_hits': 0,
                'consecutive_flops': 0
            }

    def calculate_technical_score(self, game_specs):
        """
        Calculate technical score based on game specifications
        Factors: framerate, engine quality, optimization, stability
        """
        # Placeholder calculation - will be expanded based on actual game development
        base_score = 5.0

        # Year-based expectations (higher standards over time)
        current_year = self.game_data.data['time'].get('year', 1978)
        year_modifier = (current_year - 1978) / 52  # 0 to 1 over 52 years

        # Example factors (to be replaced with actual game data)
        framerate_score = game_specs.get('framerate_quality', 0.5) * 10
        optimization_score = game_specs.get('optimization', 0.5) * 10
        engine_quality = game_specs.get('engine_version', 0.5) * 10
        stability_score = game_specs.get('stability', 0.5) * 10

        # Weight the technical aspects
        technical = (
            framerate_score * 0.30 +
            optimization_score * 0.30 +
            engine_quality * 0.25 +
            stability_score * 0.15
        )

        # Adjust for era expectations
        era_adjustment = 1.0 - (year_modifier * 0.3)  # Harder to impress over time

        final_score = technical * era_adjustment
        return max(0, min(100, final_score * 10))  # Convert to 0-100 scale

    def calculate_gameplay_score(self, game_specs):
        """
        Calculate gameplay score based on fun factor and game design
        Factors: mechanics depth, control responsiveness, difficulty balance, fun factor
        """
        # Year-based expectations
        current_year = self.game_data.data['time'].get('year', 1978)
        year_modifier = (current_year - 1978) / 52

        # Gameplay factors
        mechanics_score = game_specs.get('mechanics_depth', 0.5) * 100
        controls_score = game_specs.get('control_quality', 0.5) * 100
        balance_score = game_specs.get('difficulty_balance', 0.5) * 100
        fun_factor = game_specs.get('fun_factor', 0.5) * 100
        innovation = game_specs.get('innovation', 0.5) * 100

        # Weight the gameplay aspects
        gameplay = (
            fun_factor * 0.30 +  # Fun is most important
            mechanics_score * 0.25 +
            controls_score * 0.20 +
            balance_score * 0.15 +
            innovation * 0.10
        )

        # Era adjustment is minimal for gameplay (good fun is timeless)
        era_adjustment = 1.0 - (year_modifier * 0.1)  # Only 10% harder over time

        final_score = gameplay * era_adjustment
        return max(0, min(100, final_score))

    def calculate_innovation_score(self, game_specs):
        """
        Calculate innovation score based on originality and creativity
        Factors: new mechanics, genre-defining features, creative solutions
        """
        # Year-based expectations
        current_year = self.game_data.data['time'].get('year', 1978)
        year_modifier = (current_year - 1978) / 52

        # Innovation factors
        new_mechanics = game_specs.get('new_mechanics', 0.5) * 100
        genre_innovation = game_specs.get('genre_innovation', 0.5) * 100
        creative_solutions = game_specs.get('creative_solutions', 0.5) * 100
        first_of_kind = game_specs.get('first_of_kind', 0.5) * 100

        # Weight the innovation aspects
        innovation = (
            new_mechanics * 0.30 +
            genre_innovation * 0.35 +
            creative_solutions * 0.20 +
            first_of_kind * 0.15
        )

        # Innovation gets harder over time (more has been done)
        era_adjustment = 1.0 - (year_modifier * 0.5)  # 50% harder by 2030

        final_score = innovation * era_adjustment
        return max(0, min(100, final_score))

    def calculate_sound_score(self, game_specs):
        """
        Calculate sound/audio score
        Factors: music quality, sound effects, voice acting (if applicable)
        """
        # Year-based expectations
        current_year = self.game_data.data['time'].get('year', 1978)

        # Sound factors
        music_quality = game_specs.get('music_quality', 0.5) * 100
        sound_effects = game_specs.get('sound_effects', 0.5) * 100

        # Voice acting only matters after 1990
        if current_year >= 1990:
            voice_acting = game_specs.get('voice_acting', 0.5) * 100
            sound = (
                music_quality * 0.40 +
                sound_effects * 0.35 +
                voice_acting * 0.25
            )
        else:
            sound = (
                music_quality * 0.55 +
                sound_effects * 0.45
            )

        # Sound expectations increase moderately over time
        year_modifier = (current_year - 1978) / 52
        era_adjustment = 1.0 - (year_modifier * 0.25)

        final_score = sound * era_adjustment
        return max(0, min(100, final_score))

    def calculate_story_score(self, game_specs):
        """
        Calculate story/narrative score
        Factors: plot quality, character development, dialogue, world-building
        """
        # Story factors
        plot_quality = game_specs.get('plot_quality', 0.5) * 100
        characters = game_specs.get('character_development', 0.5) * 100
        dialogue = game_specs.get('dialogue_quality', 0.5) * 100
        world_building = game_specs.get('world_building', 0.5) * 100

        # Weight the story aspects
        story = (
            plot_quality * 0.35 +
            characters * 0.25 +
            dialogue * 0.20 +
            world_building * 0.20
        )

        # Story expectations don't change much over time (good story is timeless)
        current_year = self.game_data.data['time'].get('year', 1978)
        year_modifier = (current_year - 1978) / 52
        era_adjustment = 1.0 - (year_modifier * 0.1)  # Only 10% harder

        final_score = story * era_adjustment
        return max(0, min(100, final_score))

    def calculate_graphics_score(self, game_specs):
        """
        Calculate graphics score based on visual quality
        Factors: resolution, art style, animation quality, visual effects
        """
        # Year-based expectations
        current_year = self.game_data.data['time'].get('year', 1978)
        year_modifier = (current_year - 1978) / 52

        # Graphics factors
        resolution_score = game_specs.get('resolution_quality', 0.5) * 10
        art_style_score = game_specs.get('art_style', 0.5) * 10
        animation_score = game_specs.get('animation_quality', 0.5) * 10
        effects_score = game_specs.get('visual_effects', 0.5) * 10

        # Weight the graphics aspects
        graphics = (
            resolution_score * 0.25 +
            art_style_score * 0.35 +  # Art style matters more than pure tech
            animation_score * 0.25 +
            effects_score * 0.15
        )

        # Adjust for era (graphics expectations increase over time)
        era_adjustment = 1.0 - (year_modifier * 0.4)  # Graphics expectations rise faster

        final_score = graphics * era_adjustment
        return max(0, min(100, final_score * 10))  # Convert to 0-100 scale

    def calculate_random_modifier(self):
        """
        Calculate the random modifier to apply AFTER base score calculation
        Uses a bell curve - only 85th percentile and above can allow 100% scores
        Returns a value between -15 and +15 to add to final score
        Also returns percentile for tracking
        """
        # Generate a normal distribution (bell curve) value
        # Mean = 50th percentile, std dev chosen for good spread
        import numpy as np

        # Generate percentile (0-100)
        percentile = np.random.normal(50, 20)  # Mean 50, std dev 20
        percentile = max(0, min(100, percentile))  # Clamp to 0-100

        # Store percentile for reference
        self.last_random_percentile = percentile

        # Convert percentile to modifier range (-15 to +15)
        if percentile < 15:  # Bottom 15% - very bad luck
            modifier = -15 + (percentile / 15) * 5  # -15 to -10
        elif percentile < 30:  # 15-30% - bad luck
            modifier = -10 + ((percentile - 15) / 15) * 5  # -10 to -5
        elif percentile < 50:  # 30-50% - slightly bad
            modifier = -5 + ((percentile - 30) / 20) * 5  # -5 to 0
        elif percentile < 70:  # 50-70% - slightly good
            modifier = 0 + ((percentile - 50) / 20) * 5  # 0 to +5
        elif percentile < 85:  # 70-85% - good luck
            modifier = 5 + ((percentile - 70) / 15) * 5  # +5 to +10
        else:  # 85-100% - excellent luck (required for 100% scores)
            modifier = 10 + ((percentile - 85) / 15) * 5  # +10 to +15

        # Add some market volatility based on year
        current_year = self.game_data.data['time'].get('year', 1978)
        if 1983 <= current_year <= 1985:  # Video game crash era
            modifier -= 3
        elif 1995 <= current_year <= 2000:  # Dot-com boom
            modifier += 2
        elif 2007 <= current_year <= 2009:  # Financial crisis
            modifier -= 2

        # Clamp to final range
        return max(-15, min(15, modifier))

    def calculate_reputation_modifier(self):
        """
        Calculate studio reputation modifier to apply AFTER base score
        Returns a value between -7 and +7 based on reputation
        Higher reputation creates a bell curve favoring positive modifiers
        """
        rep_data = self.game_data.data['studio_reputation']

        # Base reputation score (0-10)
        base_score = rep_data['score']

        # Modifiers based on recent performance
        if rep_data['consecutive_hits'] >= 3:
            base_score = min(10, base_score + 1.5)  # Hot streak bonus
        elif rep_data['consecutive_flops'] >= 3:
            base_score = max(0, base_score - 1.5)  # Losing trust penalty

        # Games released influence (experience)
        games_released = rep_data['games_released']
        if games_released < 3:
            base_score *= 0.7  # New studio penalty
        elif games_released > 20:
            base_score = min(10, base_score * 1.1)  # Veteran bonus

        # Convert reputation (0-10) to modifier (-7 to +7)
        # At reputation 5: modifier is 0
        # At reputation 0: modifier is -7
        # At reputation 10: modifier is +7
        # With bell curve favoring positive at higher reputations
        if base_score >= 5:
            # Positive modifier (0 to +7)
            normalized = (base_score - 5) / 5  # 0 to 1
            # Use curve to favor higher values
            modifier = normalized ** 0.8 * 7
        else:
            # Negative modifier (-7 to 0)
            normalized = base_score / 5  # 0 to 1
            # Use curve to make negatives less harsh
            modifier = -7 * (1 - normalized ** 1.2)

        return modifier

    def update_studio_reputation(self, game_rating):
        """
        Update studio reputation based on game performance
        Game rating is now 0-100 scale
        """
        rep_data = self.game_data.data['studio_reputation']

        # Update games released
        rep_data['games_released'] += 1

        # Update average rating (weighted)
        old_avg = rep_data['average_rating']
        weight = min(rep_data['games_released'], 10)  # Cap influence at 10 games
        rep_data['average_rating'] = (old_avg * (weight - 1) + game_rating) / weight

        # Track hits and flops (adjusted for 0-100 scale)
        if game_rating >= 80:  # 80+ is a hit
            rep_data['hit_games'] += 1
            rep_data['consecutive_hits'] += 1
            rep_data['consecutive_flops'] = 0
            rep_data['score'] = min(10, rep_data['score'] + 0.5)
        elif game_rating <= 40:  # 40 or below is a flop
            rep_data['flop_games'] += 1
            rep_data['consecutive_flops'] += 1
            rep_data['consecutive_hits'] = 0
            rep_data['score'] = max(0, rep_data['score'] - 0.5)
        else:
            # Average game, reset streaks
            rep_data['consecutive_hits'] = 0
            rep_data['consecutive_flops'] = 0
            # Slowly trend toward middle
            if rep_data['score'] > 5:
                rep_data['score'] = max(5, rep_data['score'] - 0.1)
            else:
                rep_data['score'] = min(5, rep_data['score'] + 0.1)

    def calculate_overall_rating(self, game_specs):
        """
        Calculate the overall game rating combining all factors
        Returns both the final score and component breakdown
        """
        current_year = self.game_data.data['time'].get('year', 1978)

        # Calculate individual scores (only base categories, not modifiers)
        gameplay_score = self.calculate_gameplay_score(game_specs)
        technical_score = self.calculate_technical_score(game_specs)
        graphics_score = self.calculate_graphics_score(game_specs)
        innovation_score = self.calculate_innovation_score(game_specs)
        sound_score = self.calculate_sound_score(game_specs)
        story_score = self.calculate_story_score(game_specs)

        # Check visibility for studio reputation modifier
        if current_year >= self.reputation_modifier['visible_after_year']:
            self.reputation_modifier['visible'] = True

        # Calculate weighted average
        total_weight = 0
        weighted_sum = 0

        scores = {
            'gameplay': gameplay_score,
            'technical': technical_score,
            'graphics': graphics_score,
            'innovation': innovation_score,
            'sound': sound_score,
            'story': story_score
        }

        for category, score in scores.items():
            weight = self.rating_categories[category]['weight']
            weighted_sum += score * weight
            total_weight += weight

        overall_rating = weighted_sum / total_weight if total_weight > 0 else 50

        # Convert to 0-100 scale for bug penalty
        overall_rating_100 = overall_rating * 10

        # Apply bug penalty
        bugs = game_specs.get('bugs', 0)
        critical_bugs = game_specs.get('critical_bugs', 0)

        total_bug_penalty = (
            bugs * self.bug_penalty['per_bug'] +
            critical_bugs * self.bug_penalty['per_bug'] * self.bug_penalty['critical_bug_multiplier']
        )

        # Cap the penalty
        total_bug_penalty = min(total_bug_penalty, self.bug_penalty['max_penalty'])

        # Apply bug penalty
        rating_after_bugs = max(0, overall_rating - total_bug_penalty)

        # Apply post-calculation modifiers
        random_modifier = self.calculate_random_modifier()
        reputation_modifier = self.calculate_reputation_modifier()

        # Calculate final score
        final_rating_raw = rating_after_bugs + random_modifier + reputation_modifier

        # CRITICAL: If random percentile is below 85%, cap at 99%
        # Only games with 85th percentile or higher random factor can achieve 100%
        if hasattr(self, 'last_random_percentile') and self.last_random_percentile < 85:
            final_rating = min(99, final_rating_raw)
        else:
            final_rating = min(100, final_rating_raw)  # Can reach 100% with good luck

        # Prepare visible scores for display
        visible_scores = {}
        for category, score in scores.items():
            if self.rating_categories[category]['visible']:
                visible_scores[category] = {
                    'name': self.rating_categories[category]['name'],
                    'score': round(score, 1),
                    'description': self.rating_categories[category]['description']
                }

        # Add bug info if there are bugs
        bug_info = None
        if bugs > 0 or critical_bugs > 0:
            bug_info = {
                'bugs': bugs,
                'critical_bugs': critical_bugs,
                'penalty': total_bug_penalty,
                'warning': 'Bugs must be fixed before release!'
            }

        # Update studio reputation based on this game's performance
        self.update_studio_reputation(final_rating)

        return {
            'overall': round(final_rating, 1),
            'visible_scores': visible_scores,
            'hidden_scores': {
                'random_modifier': round(random_modifier, 1),
                'random_percentile': round(self.last_random_percentile, 1) if hasattr(self, 'last_random_percentile') else 50,
                'reputation_modifier': round(reputation_modifier, 1),
                'raw_final_score': round(final_rating_raw, 1),  # Can be >100
                'capped_at_99': self.last_random_percentile < 85 if hasattr(self, 'last_random_percentile') else False
            },
            'base_score_before_modifiers': round(rating_after_bugs, 1),
            'reputation_visible': self.reputation_modifier['visible'],
            'bug_info': bug_info,
            'year': current_year
        }

    def get_letter_grade(self, score):
        """Get letter grade for score (0-100)"""
        if score >= 97: return 'A+'
        elif score >= 93: return 'A'
        elif score >= 90: return 'A-'
        elif score >= 87: return 'B+'
        elif score >= 83: return 'B'
        elif score >= 80: return 'B-'
        elif score >= 77: return 'C+'
        elif score >= 73: return 'C'
        elif score >= 70: return 'C-'
        elif score >= 67: return 'D+'
        elif score >= 63: return 'D'
        elif score >= 60: return 'D-'
        else: return 'F'

    def get_metacritic_color(self, score):
        """Get Metacritic-style color coding"""
        if score >= 75:
            return f"\033[92m{int(score)}\033[0m"  # Green
        elif score >= 50:
            return f"\033[93m{int(score)}\033[0m"  # Yellow
        else:
            return f"\033[91m{int(score)}\033[0m"  # Red

    def get_rating_description(self, rating):
        """
        Get a text description for a rating value (0-100)
        """
        if rating >= 90:
            return "Masterpiece"
        elif rating >= 80:
            return "Excellent"
        elif rating >= 70:
            return "Good"
        elif rating >= 60:
            return "Above Average"
        elif rating >= 50:
            return "Average"
        elif rating >= 40:
            return "Below Average"
        elif rating >= 30:
            return "Poor"
        elif rating >= 20:
            return "Bad"
        else:
            return "Terrible"

    def get_era_technical_expectations(self):
        """
        Get the technical expectations for the current era
        Returns expected specs for an 'average' game
        """
        current_year = self.game_data.data['time'].get('year', 1978)

        expectations = {
            'resolution': '',
            'framerate': '',
            'colors': '',
            'sound': '',
            'storage': ''
        }

        if current_year < 1985:
            expectations['resolution'] = '256x192'
            expectations['framerate'] = '30 FPS'
            expectations['colors'] = '16 colors'
            expectations['sound'] = 'Beeper/Simple'
            expectations['storage'] = 'Cassette/Cartridge'
        elif current_year < 1990:
            expectations['resolution'] = '320x200'
            expectations['framerate'] = '30 FPS'
            expectations['colors'] = '256 colors'
            expectations['sound'] = 'FM Synthesis'
            expectations['storage'] = 'Floppy Disk'
        elif current_year < 1995:
            expectations['resolution'] = '640x480'
            expectations['framerate'] = '30 FPS'
            expectations['colors'] = '256 colors'
            expectations['sound'] = 'Digital Audio'
            expectations['storage'] = 'CD-ROM'
        elif current_year < 2000:
            expectations['resolution'] = '800x600'
            expectations['framerate'] = '60 FPS'
            expectations['colors'] = '16-bit'
            expectations['sound'] = '3D Positional'
            expectations['storage'] = 'CD-ROM'
        elif current_year < 2010:
            expectations['resolution'] = '1280x720'
            expectations['framerate'] = '60 FPS'
            expectations['colors'] = '32-bit'
            expectations['sound'] = 'Surround Sound'
            expectations['storage'] = 'DVD/Digital'
        elif current_year < 2020:
            expectations['resolution'] = '1920x1080'
            expectations['framerate'] = '60 FPS'
            expectations['colors'] = 'HDR'
            expectations['sound'] = '7.1 Surround'
            expectations['storage'] = 'Blu-ray/Digital'
        else:
            expectations['resolution'] = '3840x2160 (4K)'
            expectations['framerate'] = '120 FPS'
            expectations['colors'] = 'HDR10+'
            expectations['sound'] = 'Spatial Audio'
            expectations['storage'] = 'Digital/Cloud'

        return expectations