"""
Points Generation System
Handles point calculation based on developer stats, experience, and morale
"""

import random
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
from datetime import datetime, timedelta

class DeveloperSkill(Enum):
    """Developer skill categories"""
    ENGINEERING = "engineering"
    MARKETING = "marketing"
    LEADERSHIP = "leadership"
    DESIGN = "design"
    RESEARCH = "research"
    COMMUNICATION = "communication"

class DevelopmentStage(Enum):
    """Development stage types"""
    PLANNING = "Planning"
    DEVELOPMENT = "Development"
    PRODUCTION = "Production"
    BUG_SQUASHING = "Bug Squashing"

@dataclass
class DeveloperStats:
    """Stats for a single developer"""
    name: str

    # Core skills (0-10 scale)
    engineering: int = 5
    marketing: int = 2
    leadership: int = 1
    design: int = 5
    research: int = 4
    communication: int = 2

    # Experience tracking
    months_with_company: float = 0.0  # Each month = 0.25 points, max 400 months (100 points)
    months_away: float = 0.0  # Decreases at 2 points per month when away
    last_work_date: Optional[str] = None

    # Performance tracking
    projects_completed: int = 0
    consecutive_projects: int = 0
    last_project_rating: Optional[str] = None

    def get_composite_score(self) -> int:
        """Calculate composite score (max 60 from 6 skills * 10 max)"""
        return (self.engineering + self.marketing + self.leadership +
                self.design + self.research + self.communication)

    def get_composite_percentage(self) -> float:
        """Get composite score as percentage (0-100%)"""
        return (self.get_composite_score() / 60.0) * 100

    def get_experience_bonus(self) -> float:
        """Calculate experience bonus based on time with company"""
        # Max 100 points from 400 months of experience
        experience_points = min(100.0, self.months_with_company * 0.25)

        # Decay from time away
        if self.months_away > 0:
            decay = self.months_away * 2.0
            experience_points = max(0, experience_points - decay)

        # Convert to 0-1 multiplier (100 points = 1.0 bonus)
        return experience_points / 100.0

    def update_time_with_company(self, months: float):
        """Update time with company"""
        self.months_with_company += months
        self.months_away = 0  # Reset time away
        self.last_work_date = datetime.now().strftime("%Y-%m-%d")

    def update_time_away(self, months: float):
        """Update time away from company"""
        self.months_away += months

    def get_fatigue_modifier(self) -> float:
        """Calculate fatigue based on consecutive projects"""
        if self.consecutive_projects <= 2:
            return 1.0
        elif self.consecutive_projects <= 4:
            return 0.9
        elif self.consecutive_projects <= 6:
            return 0.8
        else:
            return 0.7  # Max fatigue

@dataclass
class TeamMorale:
    """Tracks team morale based on communication and other factors"""
    company_communication_avg: float = 5.0
    last_project_success: bool = True
    work_environment_quality: float = 0.7  # 0-1 scale

    def calculate_morale(self) -> float:
        """
        Calculate overall morale percentage (0-100)
        Based on communication score and other factors
        """
        base_morale = 50.0

        # Communication impact (8.3+ gives 100% morale)
        if self.company_communication_avg >= 8.3:
            comm_morale = 100.0
        else:
            # -5% for every point below 8.3
            penalty = (8.3 - self.company_communication_avg) * 5
            comm_morale = max(0, 100 - penalty)

        # Weight factors
        morale = (
            comm_morale * 0.5 +  # Communication is 50% of morale
            (100 if self.last_project_success else 50) * 0.3 +  # Project success is 30%
            self.work_environment_quality * 100 * 0.2  # Environment is 20%
        )

        return min(100, max(0, morale))

    def get_morale_modifier(self) -> float:
        """Get the point generation modifier based on morale"""
        morale = self.calculate_morale()

        if morale < 30:
            return 0.8  # -20% penalty
        elif morale > 90:
            return 1.2  # +20% bonus
        else:
            # Linear scale between 0.8 and 1.2
            return 0.8 + (morale / 100) * 0.4

class RandomEvent:
    """Random events during development with conditional requirements"""

    @staticmethod
    def get_all_events():
        """Get all possible events with their conditions"""
        return [
            # Positive Events
            {
                "name": "Team Synergy",
                "description": "Everyone working perfectly together - all stats +50%!",
                "effect": "all_boost",
                "chance": 0.08,
                "conditions": {
                    "min_morale": 90,
                    "min_team_tenure": 24,  # All team members 2+ years
                    "min_communication": 7
                }
            },
            {
                "name": "Bug Extermination",
                "description": "Research breakthrough eliminates ALL bugs instantly!",
                "effect": "remove_all_bugs",
                "chance": 0.06,
                "conditions": {
                    "min_research": 8,
                    "has_bugs": True
                }
            },
            {
                "name": "Investor Interest",
                "description": "Major investor impressed - funding boost!",
                "effect": "money_boost",
                "chance": 0.04,
                "conditions": {
                    "min_projects_completed": 3,
                    "last_rating": ["EXCELLENT", "OUTSTANDING", "LEGENDARY", "MASTERPIECE"]
                }
            },
            {
                "name": "Industry Recognition",
                "description": "Your work catches industry attention - reputation soars!",
                "effect": "reputation_boost",
                "chance": 0.05,
                "conditions": {
                    "min_year": 1985,
                    "min_consecutive_successes": 2
                }
            },
            {
                "name": "Eureka Moment",
                "description": "Brilliant breakthrough - double points this stage!",
                "effect": "double_points",
                "chance": 0.05,
                "conditions": {
                    "min_research": 6
                }
            },
            {
                "name": "Perfect Flow State",
                "description": "Team in the zone - productivity skyrockets!",
                "effect": "triple_speed",
                "chance": 0.03,
                "conditions": {
                    "min_morale": 95,
                    "min_engineering": 8
                }
            },
            {
                "name": "Community Contribution",
                "description": "Open source community adds amazing features!",
                "effect": "free_features",
                "chance": 0.04,
                "conditions": {
                    "min_year": 1990,
                    "engine": "OpenEngine"
                }
            },
            {
                "name": "Veteran Insight",
                "description": "Experience pays off - massive efficiency boost!",
                "effect": "experience_boost",
                "chance": 0.06,
                "conditions": {
                    "min_experience": 50  # 200 months = 16+ years
                }
            },

            # Neutral/Mixed Events
            {
                "name": "Press Coverage",
                "description": "Gaming magazine wants early preview!",
                "effect": "publicity",
                "chance": 0.05,
                "conditions": {
                    "min_year": 1982,
                    "stage": "PRODUCTION"
                }
            },
            {
                "name": "Platform Opportunity",
                "description": "Console manufacturer offers exclusive deal!",
                "effect": "platform_deal",
                "chance": 0.03,
                "conditions": {
                    "min_year": 1985,
                    "min_projects_completed": 2
                }
            },
            {
                "name": "Tech Conference Invite",
                "description": "Invited to speak - lose time but gain reputation!",
                "effect": "conference",
                "chance": 0.04,
                "conditions": {
                    "min_leadership": 6,
                    "min_projects_completed": 4
                }
            },

            # Negative Events
            {
                "name": "Creative Block",
                "description": "Team struggling with ideas - half points",
                "effect": "half_points",
                "chance": 0.04,
                "conditions": {
                    "max_morale": 40
                }
            },
            {
                "name": "Burnout Risk",
                "description": "Team exhausted - major productivity drop!",
                "effect": "burnout",
                "chance": 0.06,
                "conditions": {
                    "min_consecutive_projects": 5,
                    "max_morale": 50
                }
            },
            {
                "name": "Technical Debt",
                "description": "Old code causing problems - progress slowed",
                "effect": "technical_penalty",
                "chance": 0.05,
                "conditions": {
                    "max_engineering": 4,
                    "min_projects_completed": 2
                }
            },
            {
                "name": "Hardware Failure",
                "description": "Computer crashes - lost progress!",
                "effect": "lose_progress",
                "chance": 0.03,
                "conditions": {
                    "max_year": 1990,  # More common in early years
                    "no_backup": True
                }
            },
            {
                "name": "Copyright Claim",
                "description": "Similar game released - must redesign features!",
                "effect": "redesign_required",
                "chance": 0.02,
                "conditions": {
                    "min_year": 1988,
                    "stage": "PRODUCTION"
                }
            },
            {
                "name": "Team Conflict",
                "description": "Personality clash disrupting work!",
                "effect": "morale_drop",
                "chance": 0.04,
                "conditions": {
                    "min_team_size": 3,
                    "max_communication": 4
                }
            },
            {
                "name": "Market Shift",
                "description": "Your genre suddenly unpopular - expectations rise!",
                "effect": "rating_penalty",
                "chance": 0.03,
                "conditions": {
                    "min_year": 1990
                }
            },

            # Rare Special Events
            {
                "name": "Legend Visits",
                "description": "Gaming legend offers advice - massive boost!",
                "effect": "legend_boost",
                "chance": 0.01,
                "conditions": {
                    "min_year": 1985,
                    "min_reputation": 50
                }
            },
            {
                "name": "Office Pizza Party",
                "description": "Spontaneous celebration - morale through the roof!",
                "effect": "pizza_party",
                "chance": 0.02,
                "conditions": {
                    "friday": True,
                    "min_morale": 60
                }
            },
            {
                "name": "Competitor Flops",
                "description": "Major competitor fails - your game looks better!",
                "effect": "competitor_fail",
                "chance": 0.02,
                "conditions": {
                    "min_year": 1988
                }
            },
            {
                "name": "Power Outage",
                "description": "No electricity - development halted!",
                "effect": "development_stop",
                "chance": 0.02,
                "conditions": {
                    "max_year": 1995,
                    "summer": True
                }
            },

            # Conditional chain events
            {
                "name": "Breakthrough Discovery",
                "description": "Research leads to revolutionary technique!",
                "effect": "tech_revolution",
                "chance": 0.02,
                "conditions": {
                    "min_research": 9,
                    "min_engineering": 8,
                    "min_projects_completed": 5
                }
            },
            {
                "name": "Perfect Storm",
                "description": "Everything going wrong at once!",
                "effect": "disaster",
                "chance": 0.01,
                "conditions": {
                    "max_morale": 30,
                    "has_bugs": True,
                    "max_engineering": 3
                }
            }
        ]

    @staticmethod
    def check_condition(condition_name: str, condition_value, context: Dict) -> bool:
        """Check if a single condition is met"""

        # Morale conditions
        if condition_name == "min_morale":
            return context.get("morale", 0) >= condition_value
        elif condition_name == "max_morale":
            return context.get("morale", 100) <= condition_value

        # Team conditions
        elif condition_name == "min_team_tenure":
            team = context.get("team", [])
            if not team:
                return False
            return all(dev.months_with_company >= condition_value for dev in team)
        elif condition_name == "min_team_size":
            return len(context.get("team", [])) >= condition_value

        # Skill conditions
        elif condition_name == "min_research":
            lead = context.get("lead_developer")
            return lead and lead.research >= condition_value
        elif condition_name == "min_engineering":
            lead = context.get("lead_developer")
            return lead and lead.engineering >= condition_value
        elif condition_name == "max_engineering":
            lead = context.get("lead_developer")
            return lead and lead.engineering <= condition_value
        elif condition_name == "min_communication":
            lead = context.get("lead_developer")
            return lead and lead.communication >= condition_value
        elif condition_name == "max_communication":
            lead = context.get("lead_developer")
            return lead and lead.communication <= condition_value
        elif condition_name == "min_leadership":
            lead = context.get("lead_developer")
            return lead and lead.leadership >= condition_value

        # Experience conditions
        elif condition_name == "min_experience":
            lead = context.get("lead_developer")
            return lead and lead.months_with_company >= condition_value * 4  # Convert to months
        elif condition_name == "min_projects_completed":
            lead = context.get("lead_developer")
            return lead and lead.projects_completed >= condition_value
        elif condition_name == "min_consecutive_projects":
            lead = context.get("lead_developer")
            return lead and lead.consecutive_projects >= condition_value
        elif condition_name == "min_consecutive_successes":
            return context.get("consecutive_successes", 0) >= condition_value

        # Game state conditions
        elif condition_name == "has_bugs":
            return context.get("bug_count", 0) > 0
        elif condition_name == "stage":
            return context.get("stage") == condition_value
        elif condition_name == "last_rating":
            last_rating = context.get("last_rating")
            return last_rating in condition_value if isinstance(condition_value, list) else last_rating == condition_value

        # Time conditions
        elif condition_name == "min_year":
            return context.get("year", 1978) >= condition_value
        elif condition_name == "max_year":
            return context.get("year", 2024) <= condition_value
        elif condition_name == "friday":
            return context.get("day_of_week") == "Friday"
        elif condition_name == "summer":
            month = context.get("month", 1)
            return month in [6, 7, 8]

        # Other conditions
        elif condition_name == "engine":
            return context.get("engine") == condition_value
        elif condition_name == "no_backup":
            return not context.get("has_backup", False)
        elif condition_name == "min_reputation":
            return context.get("reputation", 0) >= condition_value

        return True  # Unknown conditions pass by default

    @staticmethod
    def check_for_event(context: Dict = None) -> Optional[Dict]:
        """Check if a random event occurs based on current context"""
        if context is None:
            context = {}

        eligible_events = []

        for event in RandomEvent.get_all_events():
            # Check if all conditions are met
            conditions_met = True
            if "conditions" in event:
                for cond_name, cond_value in event["conditions"].items():
                    if not RandomEvent.check_condition(cond_name, cond_value, context):
                        conditions_met = False
                        break

            # If conditions are met, add to eligible events
            if conditions_met:
                eligible_events.append(event)

        # Check each eligible event for occurrence
        for event in eligible_events:
            if random.random() < event["chance"]:
                return event

        return None

class BounceCalculator:
    """Calculates number of bounces based on developer stats"""

    @staticmethod
    def calculate_bounces(developer: DeveloperStats) -> Tuple[int, Dict]:
        """
        Calculate number of bounces using bell curve distribution
        Based on composite score (max 60 points)

        Returns: (bounce_count, calculation_details)
        """
        composite_score = developer.get_composite_score()
        composite_percentage = developer.get_composite_percentage()

        # Mean bounces based on percentage (50% = 5 bounces)
        mean_bounces = (composite_percentage / 100) * 10

        # Standard deviation (smaller = more predictable)
        std_dev = 1.5

        # Generate random value from normal distribution
        random_normal = random.gauss(mean_bounces, std_dev)

        # Store the raw value before clamping for accurate percentile
        raw_value = random_normal

        # Clamp between 1 and 10
        bounce_count = max(1, min(10, round(random_normal)))

        # Calculate percentile based on the actual distribution
        # This uses the cumulative distribution function (CDF) of the normal distribution
        z_score = (raw_value - mean_bounces) / std_dev if std_dev > 0 else 0

        # Use error function to calculate CDF
        # CDF = 0.5 * (1 + erf(z / sqrt(2)))
        from scipy import special
        try:
            percentile = 50 * (1 + special.erf(z_score / math.sqrt(2)))
        except:
            # Fallback if scipy not available - use approximation
            # Approximation of erf for percentile calculation
            def erf_approx(x):
                # Approximation with maximum error of 1.5×10⁻⁷
                a1 =  0.254829592
                a2 = -0.284496736
                a3 =  1.421413741
                a4 = -1.453152027
                a5 =  1.061405429
                p  =  0.3275911

                sign = 1 if x >= 0 else -1
                x = abs(x)

                t = 1.0 / (1.0 + p * x)
                y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-x * x)

                return sign * y

            percentile = 50 * (1 + erf_approx(z_score / math.sqrt(2)))

        # Calculate luck factor
        expected = round(mean_bounces)
        luck_factor = "Lucky!" if bounce_count > expected else "Unlucky" if bounce_count < expected else "Average"

        return bounce_count, {
            'composite_score': composite_score,
            'max_score': 60,
            'percentage': composite_percentage,
            'expected_bounces': round(mean_bounces),
            'actual_bounces': bounce_count,
            'percentile': round(percentile, 1),
            'luck_factor': luck_factor,
            'skills': {
                'engineering': developer.engineering,
                'marketing': developer.marketing,
                'leadership': developer.leadership,
                'design': developer.design,
                'research': developer.research,
                'communication': developer.communication
            }
        }

class PointsGenerator:
    """Main class for generating points based on developer stats"""

    def __init__(self, game_data=None):
        self.game_data = game_data
        self.team_morale = TeamMorale()
        self.bounce_calculator = BounceCalculator()

    def calculate_stage_points(self,
                              stage: DevelopmentStage,
                              lead_developer: DeveloperStats,
                              support_developers: List[DeveloperStats] = None,
                              context: Dict = None) -> Tuple[Dict[str, int], Optional[Dict]]:
        """
        Calculate points for a development stage based on developer stats

        Returns tuple of (points_dict, event_dict)
        """
        if support_developers is None:
            support_developers = []
        if context is None:
            context = {}

        # Get base ranges for the stage
        base_ranges = self._get_stage_base_ranges(stage)

        # Calculate skill modifiers
        skill_mods = self._calculate_skill_modifiers(stage, lead_developer, support_developers)

        # Get morale modifier
        morale_mod = self.team_morale.get_morale_modifier()

        # Build context for random events
        event_context = {
            "morale": self.team_morale.calculate_morale(),
            "lead_developer": lead_developer,
            "team": support_developers,
            "stage": stage.value.upper().replace(' ', '_'),
            "year": self._get_current_year(),
            **context  # Include any additional context passed in
        }

        # Check for random events with full context
        event = RandomEvent.check_for_event(event_context)
        event_mod = self._get_event_modifier(event) if event else 1.0

        # Generate points for each category
        points = {}
        for category, (base_min, base_max) in base_ranges.items():
            # Lead developer determines minimum (based on their skill level)
            skill_bonus = skill_mods.get(category, 0)

            # Apply all modifiers
            min_val = int((base_min + skill_bonus) * morale_mod * event_mod)
            max_val = int((base_max + skill_bonus * 1.5) * morale_mod * event_mod)

            # Cap for early years (1978-1985)
            current_year = self._get_current_year()
            if current_year <= 1985:
                # Hard cap at 2 points max for early years
                min_val = min(min_val, 1)
                max_val = min(max_val, 2)

            # Ensure valid range
            min_val = max(0, min_val)
            max_val = max(min_val + 1, max_val)

            # Generate points with some variance
            points[category] = self._generate_with_variance(min_val, max_val)

        return points, event

    def _get_stage_base_ranges(self, stage: DevelopmentStage) -> Dict[str, tuple]:
        """Get base point ranges for each stage - adjusted for year"""
        # Get current year if available
        current_year = self._get_current_year()

        # Early years (1978-1985) have much lower point generation
        if current_year <= 1985:
            if stage == DevelopmentStage.PLANNING:
                return {
                    'gameplay': (0, 2),  # Max 2 points
                    'innovation': (0, 1),
                    'story': (0, 1),
                    'technical': (0, 0),
                    'graphics': (0, 0),
                    'sound_audio': (0, 0)
                }
            elif stage == DevelopmentStage.DEVELOPMENT:
                return {
                    'technical': (0, 2),  # Max 2 points
                    'graphics': (0, 1),
                    'gameplay': (0, 1),
                    'innovation': (0, 0),
                    'story': (0, 0),
                    'sound_audio': (0, 0)
                }
            elif stage == DevelopmentStage.PRODUCTION:
                return {
                    'sound_audio': (0, 2),  # Max 2 points
                    'story': (0, 1),
                    'graphics': (0, 1),
                    'technical': (0, 0),
                    'gameplay': (0, 0),
                    'innovation': (0, 0)
                }
            else:  # BUG_SQUASHING
                return {
                    'technical': (0, 2),
                    'gameplay': (0, 1),
                    'graphics': (0, 0),
                    'innovation': (0, 0),
                    'story': (0, 0),
                    'sound_audio': (0, 0)
                }
        # Mid years (1986-1995)
        elif current_year <= 1995:
            if stage == DevelopmentStage.PLANNING:
                return {
                    'gameplay': (1, 3),
                    'innovation': (1, 2),
                    'story': (0, 2),
                    'technical': (0, 1),
                    'graphics': (0, 1),
                    'sound_audio': (0, 0)
                }
            elif stage == DevelopmentStage.DEVELOPMENT:
                return {
                    'technical': (1, 3),
                    'graphics': (1, 3),
                    'gameplay': (0, 1),
                    'innovation': (0, 1),
                    'story': (0, 0),
                    'sound_audio': (0, 1)
                }
            elif stage == DevelopmentStage.PRODUCTION:
                return {
                    'sound_audio': (1, 3),
                    'story': (1, 2),
                    'graphics': (0, 2),
                    'technical': (0, 1),
                    'gameplay': (0, 1),
                    'innovation': (0, 0)
                }
            else:  # BUG_SQUASHING
                return {
                    'technical': (1, 3),
                    'gameplay': (0, 2),
                    'graphics': (0, 1),
                    'innovation': (0, 0),
                    'story': (0, 0),
                    'sound_audio': (0, 0)
                }
        # Modern years (1996+)
        else:
            if stage == DevelopmentStage.PLANNING:
                return {
                    'gameplay': (2, 5),
                    'innovation': (2, 4),
                    'story': (1, 4),
                    'technical': (0, 1),
                    'graphics': (0, 1),
                    'sound_audio': (0, 0)
                }
            elif stage == DevelopmentStage.DEVELOPMENT:
                return {
                    'technical': (3, 5),
                    'graphics': (2, 5),
                    'gameplay': (0, 2),
                    'innovation': (0, 1),
                    'story': (0, 0),
                    'sound_audio': (0, 1)
                }
            elif stage == DevelopmentStage.PRODUCTION:
                return {
                    'sound_audio': (3, 5),
                    'story': (2, 4),
                    'graphics': (1, 2),
                    'technical': (0, 1),
                    'gameplay': (0, 1),
                    'innovation': (0, 0)
                }
            else:  # BUG_SQUASHING
                return {
                    'technical': (2, 4),
                    'gameplay': (1, 3),
                    'graphics': (0, 1),
                    'innovation': (0, 0),
                    'story': (0, 0),
                    'sound_audio': (0, 0)
                }

    def _calculate_skill_modifiers(self,
                                  stage: DevelopmentStage,
                                  lead: DeveloperStats,
                                  support: List[DeveloperStats]) -> Dict[str, float]:
        """Calculate skill-based modifiers for each category"""
        modifiers = {}

        # Map skills to categories
        skill_mapping = {
            'gameplay': ['design', 'research'],
            'technical': ['engineering'],
            'graphics': ['design'],
            'innovation': ['research', 'design'],
            'story': ['design', 'communication'],
            'sound_audio': ['design']
        }

        # Get current year for scaling
        current_year = self._get_current_year()

        # Scale skill impact based on year
        if current_year <= 1985:
            skill_multiplier = 0.1  # Very low skill impact in early years
            exp_multiplier = 0.5
        elif current_year <= 1995:
            skill_multiplier = 0.3
            exp_multiplier = 1.0
        else:
            skill_multiplier = 0.5
            exp_multiplier = 2.0

        # Calculate modifiers for each category
        for category, skills in skill_mapping.items():
            # Lead developer provides base modifier
            lead_skill_avg = sum(getattr(lead, skill) for skill in skills) / len(skills)
            lead_bonus = lead_skill_avg * skill_multiplier

            # Experience bonus
            exp_bonus = lead.get_experience_bonus() * exp_multiplier

            # Fatigue modifier
            fatigue_mod = lead.get_fatigue_modifier()

            # Support developers provide additional bonus (with communication factor)
            support_bonus = 0
            if support:
                for dev in support:
                    dev_skill_avg = sum(getattr(dev, skill) for skill in skills) / len(skills)
                    # Communication affects collaboration effectiveness
                    comm_factor = dev.communication / 10.0
                    support_bonus += dev_skill_avg * 0.2 * comm_factor * skill_multiplier

            # Total modifier
            modifiers[category] = (lead_bonus + exp_bonus + support_bonus) * fatigue_mod

        # Leadership affects all categories (but less in early years)
        leadership_bonus = lead.leadership * 0.05 if current_year <= 1985 else lead.leadership * 0.1
        for category in modifiers:
            modifiers[category] += leadership_bonus

        return modifiers

    def _get_current_year(self) -> int:
        """Get the current game year"""
        if self.game_data and 'game_time' in self.game_data.data:
            date_str = self.game_data.data['game_time'].get('current_date', '1984-01-01')
            return int(date_str.split('-')[0])
        return 1984

    def _generate_with_variance(self, min_val: int, max_val: int) -> int:
        """Generate points with variance and critical chances"""
        base = random.randint(min_val, max_val)

        # Critical chances (reduced for early years)
        current_year = self._get_current_year()

        if current_year <= 1985:
            # Very limited critical chances in early years
            crit_roll = random.random()
            if crit_roll < 0.03:  # 3% critical failure
                base = max(0, base - 1)
            elif crit_roll > 0.97:  # 3% critical success
                base = min(2, base + 1)  # Still cap at 2 for early years
        else:
            # Standard critical chances
            crit_roll = random.random()
            if crit_roll < 0.05:  # 5% critical failure
                base = max(0, base - random.randint(1, 3))
            elif crit_roll > 0.95:  # 5% critical success
                base = base + random.randint(2, 5)

        return base

    def _get_event_modifier(self, event: Optional[Dict]) -> float:
        """Get modifier based on random event"""
        if not event:
            return 1.0

        effect = event.get("effect")

        # Point modifiers
        if effect == "double_points":
            return 2.0
        elif effect == "triple_speed":
            return 3.0
        elif effect == "half_points":
            return 0.5
        elif effect in ["technical_boost", "creativity_boost", "all_boost"]:
            return 1.5
        elif effect == "experience_boost":
            return 1.8
        elif effect == "legend_boost":
            return 2.5
        elif effect == "tech_revolution":
            return 2.2
        elif effect == "free_features":
            return 1.4

        # Penalty modifiers
        elif effect == "technical_penalty":
            return 0.7
        elif effect == "burnout":
            return 0.3
        elif effect == "lose_progress":
            return 0.4
        elif effect == "redesign_required":
            return 0.5
        elif effect == "development_stop":
            return 0.0  # Complete stop
        elif effect == "disaster":
            return 0.2

        # Some effects don't modify points directly
        elif effect in ["remove_all_bugs", "money_boost", "reputation_boost",
                       "publicity", "platform_deal", "conference", "morale_drop",
                       "rating_penalty", "pizza_party", "competitor_fail"]:
            return 1.0  # These have other effects handled elsewhere

        return 1.0

    def update_team_communication(self, developers: List[DeveloperStats]):
        """Update team morale based on average communication score"""
        if not developers:
            return

        avg_comm = sum(dev.communication for dev in developers) / len(developers)
        self.team_morale.company_communication_avg = avg_comm


# Helper function to create default player stats
def create_player_developer() -> DeveloperStats:
    """Create the player character with starting skills of 1 (will progress over time)"""
    return DeveloperStats(
        name="You (Player)",
        engineering=1,
        marketing=1,
        leadership=1,
        design=1,
        research=1,
        communication=1,
        months_with_company=0,
        projects_completed=0
    )

# Example usage
if __name__ == "__main__":
    # Create player and team
    player = create_player_developer()

    # Create points generator
    generator = PointsGenerator()

    # Generate points for planning stage
    points, event = generator.calculate_stage_points(
        DevelopmentStage.PLANNING,
        player
    )

    print(f"Planning Stage Points: {points}")
    if event:
        print(f"Random Event: {event['name']} - {event['description']}")