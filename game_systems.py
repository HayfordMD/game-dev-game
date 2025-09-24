import datetime
from enum import Enum
import time

"""
Future Employee System Notes:
- Employees will have visible "Energy Level" rating (0-100)
- Employees will have hidden "Work/Life Balance" rating
- Work schedules will be settable for employees
- Employee productivity affected by both energy and work/life balance
- Crunch time affects employee morale and retention
"""

class SleepSchedule(Enum):
    CRUNCH = "Crunch Time"
    NORMAL = "Normal"
    RESTORATIVE = "Restorative"
    CUSTOM = "Custom"

class TimeSystem:
    def __init__(self, game_data):
        self.game_data = game_data
        self.last_update_time = time.time()

        # Time scale presets:
        # 1 = Real-time (1:1)
        # 960 = Quick Day (1 day = 90 seconds)
        # 6720 = Quick Week (1 week = 90 seconds)
        # 25920 = Quick Month (1 month = 100 seconds, ~30 days)
        # 64800 = Quick Quarter (3 months = 120 seconds, ~90 days)
        # 55000 = Max speed allowed

        self.time_scale_presets = {
            "realtime": 1,           # 1:1 real-time
            "quick_day": 960,        # 1 day in 90 seconds
            "quick_week": 6720,      # 1 week in 90 seconds
            "quick_month": 25920,    # 1 month in 100 seconds
            "quick_quarter": 64800,  # 3 months in 120 seconds
            "max_speed": 55000       # Maximum allowed speed
        }

        # Default to real-time (1:1)
        self.time_scale = 1

        # Initialize time tracking if not present
        if 'time' not in self.game_data.data:
            # Get current real time and map to 1978
            now = datetime.datetime.now()

            # Set game time to same month/day/hour as real time but in 1978
            self.game_data.data['time'] = {
                'year': 1978,
                'month': now.month,
                'day': now.day,
                'hour': now.hour,
                'minute': now.minute,
                'second': now.second,
                'current_day': now.day,
                'current_week': (now.day - 1) // 7 + 1,
                'current_month': now.month,
                'total_days': 0,
                'sleep_schedule': SleepSchedule.NORMAL.value,
                'crunch_weeks': 0,
                'hours_worked_today': 0,
                'breaks_taken_today': 0,
                'is_real_time': True,
                'time_multiplier': 1.0  # Can speed up/slow down time
            }

        # Sleep schedule configurations
        self.schedules = {
            SleepSchedule.CRUNCH.value: {
                'sleep_hours': 5,
                'work_hours': 16,
                'break_count': 3,
                'break_duration': 0.25,  # 15 minutes
                'energy_drain': 3,  # Energy drains faster
                'max_weeks': 5,  # Maximum 5 weeks in a row
                'productivity_bonus': 1.3  # 30% productivity boost
            },
            SleepSchedule.NORMAL.value: {
                'sleep_hours': 8,
                'work_hours': 8,
                'break_count': 2,
                'break_duration': 1,  # 1 hour
                'energy_drain': 1,
                'max_weeks': float('inf'),
                'productivity_bonus': 1.0
            },
            SleepSchedule.RESTORATIVE.value: {
                'sleep_hours': 10,
                'work_hours': 6,
                'break_count': 3,
                'break_duration': 1,
                'energy_drain': 0.5,
                'max_weeks': float('inf'),
                'productivity_bonus': 0.8,
                'stress_reduction': 5  # Extra stress reduction
            }
        }

    def update_real_time(self):
        """Update game time based on real time elapsed"""
        current_time = time.time()
        elapsed = current_time - self.last_update_time
        self.last_update_time = current_time

        # Calculate game time elapsed (with time scale)
        game_seconds_elapsed = elapsed * self.time_scale * self.game_data.data['time'].get('time_multiplier', 1.0)

        # At higher speeds, skip seconds and go straight to minutes for efficiency
        if self.time_scale > 960:  # Faster than 2x speed
            # Convert to minutes and only update if we have at least 1 minute
            game_minutes_elapsed = game_seconds_elapsed / 60
            if game_minutes_elapsed >= 1:
                self.advance_time_minutes(int(game_minutes_elapsed))
                # Don't track seconds at high speeds
                self.game_data.data['time']['second'] = 0
        else:  # At 1x or 2x speed, track seconds
            if game_seconds_elapsed >= 1:
                self.advance_time_seconds(int(game_seconds_elapsed))

    def advance_time_seconds(self, seconds):
        """Advance game time by specified seconds"""
        time_data = self.game_data.data['time']

        time_data['second'] = time_data.get('second', 0) + seconds

        # Handle minute rollover
        while time_data['second'] >= 60:
            time_data['second'] -= 60
            time_data['minute'] = time_data.get('minute', 0) + 1

            # Handle hour rollover
            if time_data['minute'] >= 60:
                time_data['minute'] = 0
                time_data['hour'] = time_data.get('hour', 8) + 1

                # Handle day rollover
                if time_data['hour'] >= 24:
                    time_data['hour'] = 0
                    self.advance_day()

    def advance_time_minutes(self, minutes):
        """Advance game time by specified minutes"""
        # At high speeds, skip seconds tracking
        if self.time_scale > 960:
            time_data = self.game_data.data['time']
            time_data['minute'] = time_data.get('minute', 0) + minutes

            # Handle hour rollover
            while time_data['minute'] >= 60:
                time_data['minute'] -= 60
                time_data['hour'] = time_data.get('hour', 8) + 1

                # Handle day rollover
                if time_data['hour'] >= 24:
                    time_data['hour'] = 0
                    self.advance_day()
        else:
            # At lower speeds, go through seconds
            self.advance_time_seconds(minutes * 60)

    def advance_day(self):
        """Advance by one day"""
        time_data = self.game_data.data['time']
        time_data['day'] = time_data.get('day', 1) + 1
        time_data['total_days'] = time_data.get('total_days', 0) + 1
        time_data['hours_worked_today'] = 0
        time_data['breaks_taken_today'] = 0

        # Get days in current month
        days_in_month = self.get_days_in_month(time_data.get('month', 1), time_data.get('year', 1978))

        # Handle month rollover
        if time_data['day'] > days_in_month:
            time_data['day'] = 1
            time_data['month'] = time_data.get('month', 1) + 1

            # Handle year rollover
            if time_data['month'] > 12:
                time_data['month'] = 1
                time_data['year'] = time_data.get('year', 1978) + 1

        # Update week tracking
        time_data['current_week'] = (time_data['day'] - 1) // 7 + 1

        # Check crunch time limits
        if time_data['current_week'] != time_data.get('last_week', 0):
            time_data['last_week'] = time_data['current_week']
            schedule = time_data['sleep_schedule']
            if schedule == SleepSchedule.CRUNCH.value:
                time_data['crunch_weeks'] += 1
            else:
                time_data['crunch_weeks'] = 0

    def get_days_in_month(self, month, year):
        """Get number of days in a given month"""
        if month in [1, 3, 5, 7, 8, 10, 12]:
            return 31
        elif month in [4, 6, 9, 11]:
            return 30
        elif month == 2:
            # Check for leap year
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                return 29
            return 28
        return 30

    def advance_time(self, hours):
        """Advance game time by specified hours (for sleep, etc.)"""
        self.advance_time_minutes(hours * 60)
        # Reset seconds after sleeping
        self.game_data.data['time']['second'] = 0

    def get_schedule_info(self):
        """Get current schedule information"""
        schedule_name = self.game_data.data['time']['sleep_schedule']
        return self.schedules.get(schedule_name, self.schedules[SleepSchedule.NORMAL.value])

    def set_schedule(self, schedule_type):
        """Set sleep schedule"""
        time_data = self.game_data.data['time']

        # Check if can switch to crunch
        if schedule_type == SleepSchedule.CRUNCH.value:
            if time_data.get('crunch_weeks', 0) >= 5:
                return False, "You've been crunching for 5 weeks! You need rest."

        time_data['sleep_schedule'] = schedule_type
        return True, f"Schedule set to {schedule_type}"

    def get_time_string(self):
        """Get formatted time string"""
        time_data = self.game_data.data['time']
        hour = int(time_data.get('hour', 8))
        minute = int(time_data.get('minute', 0))
        am_pm = "AM" if hour < 12 else "PM"
        display_hour = hour if hour <= 12 else hour - 12
        if display_hour == 0:
            display_hour = 12

        return f"{display_hour:02d}:{minute:02d} {am_pm}"

    def get_date_string(self):
        """Get formatted date string"""
        time_data = self.game_data.data['time']
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        month = months[time_data.get('month', 1) - 1]
        day = time_data.get('day', 1)
        year = time_data.get('year', 1978)
        return f"{month} {day}, {year}"

class EnergySystem:
    def __init__(self, game_data):
        self.game_data = game_data

        # Initialize energy data if not present
        if 'energy_system' not in self.game_data.data:
            self.game_data.data['energy_system'] = {
                'current_energy': 100,
                'max_energy': 100,
                'energy_drinks': 5,  # Start with some energy drinks
                'adderall': 0,
                'adderall_cooldown': 0,  # Days until can use again
                'caffeine_tolerance': 0  # Reduces effectiveness over time
            }

    def get_energy(self):
        """Get current energy level"""
        return self.game_data.data['energy_system']['current_energy']

    def set_energy(self, value):
        """Set energy to specific value"""
        energy_data = self.game_data.data['energy_system']
        energy_data['current_energy'] = max(0, min(energy_data['max_energy'], value))

    def drain_energy(self, amount):
        """Reduce energy by amount"""
        current = self.get_energy()
        self.set_energy(current - amount)

    def restore_energy(self, amount):
        """Restore energy by amount"""
        current = self.get_energy()
        self.set_energy(current + amount)

    def get_productivity_modifier(self):
        """Calculate productivity based on energy level"""
        energy = self.get_energy()

        if energy >= 80:
            return 1.0  # Full productivity
        elif energy >= 50:
            return 0.8  # Slightly reduced
        elif energy >= 30:
            return 0.5  # Half productivity
        else:
            return 0.2  # Massive decrease

    def use_energy_drink(self):
        """Use an energy drink"""
        energy_data = self.game_data.data['energy_system']

        if energy_data['energy_drinks'] <= 0:
            return False, "No energy drinks available!"

        energy_data['energy_drinks'] -= 1

        # Effectiveness reduced by tolerance
        base_boost = 30
        tolerance_reduction = energy_data['caffeine_tolerance'] * 2
        actual_boost = max(10, base_boost - tolerance_reduction)

        self.restore_energy(actual_boost)
        energy_data['caffeine_tolerance'] = min(10, energy_data['caffeine_tolerance'] + 1)

        return True, f"Energy restored by {actual_boost}! (Drinks left: {energy_data['energy_drinks']})"

    def use_adderall(self):
        """Use adderall (stronger but with cooldown)"""
        energy_data = self.game_data.data['energy_system']

        if energy_data['adderall'] <= 0:
            return False, "No adderall available!"

        if energy_data['adderall_cooldown'] > 0:
            return False, f"Must wait {energy_data['adderall_cooldown']} days before using again!"

        energy_data['adderall'] -= 1
        energy_data['adderall_cooldown'] = 3  # 3-day cooldown

        # Fully restore energy and add bonus
        self.set_energy(120)  # Temporary boost above max

        # Increase stress as side effect
        stress = self.game_data.data['player_data'].get('stress_level', 0)
        self.game_data.data['player_data']['stress_level'] = min(100, stress + 15)

        return True, f"Energy boosted to 120%! (Pills left: {energy_data['adderall']})\nWarning: Stress increased!"

    def daily_update(self):
        """Update energy system for new day"""
        energy_data = self.game_data.data['energy_system']

        # Reduce cooldowns
        if energy_data['adderall_cooldown'] > 0:
            energy_data['adderall_cooldown'] -= 1

        # Slowly reduce caffeine tolerance
        if energy_data['caffeine_tolerance'] > 0:
            energy_data['caffeine_tolerance'] = max(0, energy_data['caffeine_tolerance'] - 0.5)