"""
Grocery Store Items System
Items that can be purchased to provide various benefits
"""

from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass

class ItemCategory(Enum):
    FOOD = "Food & Drinks"
    PRODUCTIVITY = "Productivity Boosters"
    HEALTH = "Health & Wellness"
    TECH = "Tech Supplies"
    OFFICE = "Office Supplies"
    ENTERTAINMENT = "Entertainment"

@dataclass
class GroceryItem:
    id: str
    name: str
    category: ItemCategory
    price: float
    description: str
    effect_description: str
    duration_hours: int = 0  # 0 means permanent or instant effect
    quantity: int = 1  # How many you get per purchase
    max_stack: int = 10  # Maximum you can hold

# PLACEHOLDER ITEMS - Waiting for review
GROCERY_ITEMS = {
    # FOOD & DRINKS - Energy and morale boosters
    "coffee": GroceryItem(
        id="coffee",
        name="Premium Coffee",
        category=ItemCategory.FOOD,
        price=5,
        description="High-quality arabica beans",
        effect_description="Increases productivity by 10% for 8 hours. Reduces fatigue.",
        duration_hours=8,
        quantity=1,
        max_stack=20
    ),
    "energy_drink": GroceryItem(
        id="energy_drink",
        name="Energy Drink (6-pack)",
        category=ItemCategory.FOOD,
        price=15,
        description="Maximum caffeine boost",
        effect_description="Instant +20% speed boost for 4 hours, but -5% accuracy. Crash after.",
        duration_hours=4,
        quantity=6,
        max_stack=24
    ),
    "pizza": GroceryItem(
        id="pizza",
        name="Developer's Pizza",
        category=ItemCategory.FOOD,
        price=12,
        description="The classic late-night fuel",
        effect_description="Team morale +5 for one day. Allows working through dinner.",
        duration_hours=24,
        quantity=1,
        max_stack=5
    ),
    "healthy_snacks": GroceryItem(
        id="healthy_snacks",
        name="Healthy Snack Pack",
        category=ItemCategory.FOOD,
        price=8,
        description="Nuts, fruits, and protein bars",
        effect_description="Sustained energy without crash. +5% to all stats for 12 hours.",
        duration_hours=12,
        quantity=1,
        max_stack=10
    ),
    "instant_ramen": GroceryItem(
        id="instant_ramen",
        name="Instant Ramen (12-pack)",
        category=ItemCategory.FOOD,
        price=10,
        description="Quick and cheap sustenance",
        effect_description="Saves time on meals. -1 hour per day but -2 health after 3 uses.",
        duration_hours=0,
        quantity=12,
        max_stack=36
    ),

    # PRODUCTIVITY BOOSTERS
    "noise_cancel_headphones": GroceryItem(
        id="noise_cancel_headphones",
        name="Noise-Canceling Headphones",
        category=ItemCategory.PRODUCTIVITY,
        price=200,
        description="Premium quality sound isolation",
        effect_description="Permanent +15% focus. Reduces distractions. One-time purchase.",
        duration_hours=0,
        quantity=1,
        max_stack=1
    ),
    "ergonomic_chair": GroceryItem(
        id="ergonomic_chair",
        name="Ergonomic Office Chair",
        category=ItemCategory.PRODUCTIVITY,
        price=500,
        description="Professional-grade seating",
        effect_description="Permanent +10% productivity, +5 health. Reduces crunch fatigue by 20%.",
        duration_hours=0,
        quantity=1,
        max_stack=1
    ),
    "fidget_toy": GroceryItem(
        id="fidget_toy",
        name="Developer's Fidget Cube",
        category=ItemCategory.PRODUCTIVITY,
        price=15,
        description="Helps maintain focus during debugging",
        effect_description="Reduces bug generation by 5% when debugging.",
        duration_hours=0,
        quantity=1,
        max_stack=3
    ),
    "motivational_posters": GroceryItem(
        id="motivational_posters",
        name="Motivational Poster Set",
        category=ItemCategory.PRODUCTIVITY,
        price=25,
        description="'Ship It' and other classics",
        effect_description="Team morale +3 permanently. Stacks up to 3 times.",
        duration_hours=0,
        quantity=1,
        max_stack=3
    ),

    # HEALTH & WELLNESS
    "vitamins": GroceryItem(
        id="vitamins",
        name="Developer Vitamins",
        category=ItemCategory.HEALTH,
        price=30,
        description="30-day supply of essential nutrients",
        effect_description="Prevents illness. +2 health per week when used regularly.",
        duration_hours=720,  # 30 days
        quantity=1,
        max_stack=3
    ),
    "gym_membership": GroceryItem(
        id="gym_membership",
        name="Monthly Gym Pass",
        category=ItemCategory.HEALTH,
        price=50,
        description="Access to fitness facilities",
        effect_description="Allows gym visits any day (not just Mondays). +10 max health.",
        duration_hours=720,
        quantity=1,
        max_stack=1
    ),
    "sleeping_pills": GroceryItem(
        id="sleeping_pills",
        name="Sleep Aid",
        category=ItemCategory.HEALTH,
        price=20,
        description="For those crunch-time sleep issues",
        effect_description="Guarantees good rest. Removes fatigue but can't be used daily.",
        duration_hours=0,
        quantity=10,
        max_stack=30
    ),
    "stress_ball": GroceryItem(
        id="stress_ball",
        name="Stress Relief Ball",
        category=ItemCategory.HEALTH,
        price=5,
        description="Squeeze away the bugs",
        effect_description="Reduces stress during crunch. -10% burnout rate.",
        duration_hours=0,
        quantity=1,
        max_stack=5
    ),

    # TECH SUPPLIES
    "backup_drives": GroceryItem(
        id="backup_drives",
        name="Backup Hard Drives",
        category=ItemCategory.TECH,
        price=100,
        description="Never lose work again",
        effect_description="Prevents catastrophic data loss events. Auto-saves every hour.",
        duration_hours=0,
        quantity=2,
        max_stack=4
    ),
    "cable_organizers": GroceryItem(
        id="cable_organizers",
        name="Cable Management Kit",
        category=ItemCategory.TECH,
        price=20,
        description="Tame the cable chaos",
        effect_description="Clean workspace bonus: +2% to all work efficiency.",
        duration_hours=0,
        quantity=1,
        max_stack=1
    ),
    "mechanical_keyboard": GroceryItem(
        id="mechanical_keyboard",
        name="Mechanical Keyboard",
        category=ItemCategory.TECH,
        price=150,
        description="Satisfying clicks for coding",
        effect_description="Permanent +5% coding speed. Improved accuracy.",
        duration_hours=0,
        quantity=1,
        max_stack=1
    ),
    "monitor_upgrade": GroceryItem(
        id="monitor_upgrade",
        name="4K Monitor",
        category=ItemCategory.TECH,
        price=400,
        description="Crystal clear code visibility",
        effect_description="Permanent +8% to graphics and technical work. Reduces eye strain.",
        duration_hours=0,
        quantity=1,
        max_stack=2
    ),

    # OFFICE SUPPLIES
    "whiteboard": GroceryItem(
        id="whiteboard",
        name="Large Whiteboard",
        category=ItemCategory.OFFICE,
        price=80,
        description="For planning and brainstorming",
        effect_description="Planning stage generates 20% more points. Better team coordination.",
        duration_hours=0,
        quantity=1,
        max_stack=1
    ),
    "sticky_notes": GroceryItem(
        id="sticky_notes",
        name="Sticky Notes (Mega Pack)",
        category=ItemCategory.OFFICE,
        price=15,
        description="Colorful reminders everywhere",
        effect_description="Never forget tasks. Reduces feature creep by 10%.",
        duration_hours=0,
        quantity=1,
        max_stack=5
    ),
    "notebooks": GroceryItem(
        id="notebooks",
        name="Developer Notebooks (3-pack)",
        category=ItemCategory.OFFICE,
        price=20,
        description="For design sketches and notes",
        effect_description="+5% to design and planning activities.",
        duration_hours=0,
        quantity=3,
        max_stack=9
    ),

    # ENTERTAINMENT
    "game_console": GroceryItem(
        id="game_console",
        name="Retro Game Console",
        category=ItemCategory.ENTERTAINMENT,
        price=300,
        description="For 'research' purposes",
        effect_description="Team morale +10. Unlocks game history knowledge. Can study competitors.",
        duration_hours=0,
        quantity=1,
        max_stack=1
    ),
    "board_games": GroceryItem(
        id="board_games",
        name="Board Game Collection",
        category=ItemCategory.ENTERTAINMENT,
        price=60,
        description="Team building through tabletop",
        effect_description="Weekly game night option. +5 team cohesion, +3 morale.",
        duration_hours=0,
        quantity=1,
        max_stack=1
    ),
    "streaming_subscription": GroceryItem(
        id="streaming_subscription",
        name="Streaming Service (Monthly)",
        category=ItemCategory.ENTERTAINMENT,
        price=15,
        description="Background noise for coding",
        effect_description="Reduces monotony. +2 morale for the month.",
        duration_hours=720,
        quantity=1,
        max_stack=1
    ),
    "rubber_duck": GroceryItem(
        id="rubber_duck",
        name="Debugging Duck",
        category=ItemCategory.ENTERTAINMENT,
        price=10,
        description="Classic rubber duck for debugging",
        effect_description="Rubber duck debugging: 15% chance to instantly solve a bug.",
        duration_hours=0,
        quantity=1,
        max_stack=1
    )
}

class GroceryStore:
    """Manages the grocery store and player inventory"""

    def __init__(self, game_state: Dict):
        self.game_state = game_state

        # Initialize inventory if not exists
        if "inventory" not in game_state:
            game_state["inventory"] = {}

        # Initialize active effects if not exists
        if "active_effects" not in game_state:
            game_state["active_effects"] = []

    def get_available_items(self, budget: float) -> List[GroceryItem]:
        """Get list of items player can afford"""
        return [item for item in GROCERY_ITEMS.values() if item.price <= budget]

    def get_items_by_category(self, category: ItemCategory) -> List[GroceryItem]:
        """Get all items in a specific category"""
        return [item for item in GROCERY_ITEMS.values() if item.category == category]

    def can_purchase(self, item_id: str, quantity: int = 1) -> tuple[bool, str]:
        """Check if player can purchase an item"""
        if item_id not in GROCERY_ITEMS:
            return False, "Item not found"

        item = GROCERY_ITEMS[item_id]
        total_cost = item.price * quantity

        # Check money
        if self.game_state.get("money", 0) < total_cost:
            return False, f"Not enough money (need ${total_cost})"

        # Check stack limit
        current_owned = self.game_state["inventory"].get(item_id, 0)
        if current_owned + (item.quantity * quantity) > item.max_stack:
            return False, f"Would exceed stack limit of {item.max_stack}"

        return True, "OK"

    def purchase_item(self, item_id: str, quantity: int = 1) -> bool:
        """Purchase an item and add to inventory"""
        can_buy, reason = self.can_purchase(item_id, quantity)
        if not can_buy:
            return False

        item = GROCERY_ITEMS[item_id]
        total_cost = item.price * quantity

        # Deduct money
        self.game_state["money"] -= total_cost

        # Add to inventory
        if item_id not in self.game_state["inventory"]:
            self.game_state["inventory"][item_id] = 0

        self.game_state["inventory"][item_id] += item.quantity * quantity

        return True

    def use_item(self, item_id: str) -> bool:
        """Use an item from inventory"""
        if item_id not in self.game_state["inventory"] or self.game_state["inventory"][item_id] <= 0:
            return False

        # Consume item
        self.game_state["inventory"][item_id] -= 1

        # Apply effect (placeholder for now)
        item = GROCERY_ITEMS[item_id]
        if item.duration_hours > 0:
            # Add timed effect
            self.game_state["active_effects"].append({
                "item_id": item_id,
                "name": item.name,
                "effect": item.effect_description,
                "hours_remaining": item.duration_hours
            })

        return True

    def get_inventory_display(self) -> Dict[str, Dict]:
        """Get formatted inventory for display"""
        display = {}
        for item_id, quantity in self.game_state["inventory"].items():
            if quantity > 0 and item_id in GROCERY_ITEMS:
                item = GROCERY_ITEMS[item_id]
                display[item_id] = {
                    "name": item.name,
                    "quantity": quantity,
                    "category": item.category.value,
                    "effect": item.effect_description
                }
        return display

# Item Ideas List for Review:
"""
POTENTIAL ADDITIONAL ITEMS TO CONSIDER:

FOOD & DRINKS:
- Green Tea: Gentle energy boost without crash
- Microwave Meals: Quick food, saves time but low morale
- Vending Machine Snacks: Instant but expensive
- Team Lunch Catering: Big morale boost for team events

PRODUCTIVITY:
- Standing Desk: Alternate between sitting/standing
- Blue Light Glasses: Reduce eye strain for night work
- Timer/Pomodoro Clock: Better time management
- Second Monitor: Significant productivity boost
- Desk Plants: Small morale and air quality boost

HEALTH:
- First Aid Kit: Handle minor injuries/illness
- Massage Voucher: Reduce crunch stress significantly
- Meditation App: Daily stress reduction
- Air Purifier: Better health in office

TECH:
- UPS Battery Backup: Prevent work loss from power outages
- Webcam: Better remote meetings
- Drawing Tablet: For artists and designers
- High-Speed Internet Upgrade: Faster everything

OFFICE:
- Filing Cabinet: Better organization
- Label Maker: Ultimate organization
- Desk Lamp: Better lighting for night work
- Coffee Machine: Team coffee without leaving office

ENTERTAINMENT:
- Music Speakers: Background music for team
- Ping Pong Table: Team breaks and bonding
- Bookshelf with Game Dev Books: Learn new skills
- Magazine Subscriptions: Stay current with industry

SPECIAL/SEASONAL:
- Holiday Decorations: Seasonal morale boosts
- Birthday Supplies: Celebrate team birthdays
- Conference Tickets: Learn and network
- Online Course Credits: Skill improvement
"""