"""
NPC System Package
Contains all NPC-related data and generation systems for the game
"""

from .npc_database import (
    NPCGenerator,
    generate_all_npcs,
    FIRST_NAMES,
    LAST_NAMES,
    COMPANY_NAMES
)

from .game_names_database import (
    get_names_for_year,
    get_all_period_names,
    get_total_names,
    PERIOD_NAMES
)

__all__ = [
    'NPCGenerator',
    'generate_all_npcs',
    'get_names_for_year',
    'get_all_period_names',
    'get_total_names',
    'FIRST_NAMES',
    'LAST_NAMES',
    'COMPANY_NAMES',
    'PERIOD_NAMES'
]