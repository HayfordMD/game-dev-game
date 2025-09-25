"""
NPC System
Manages NPC data, progression, hidden traits, and persistence across playthroughs

This system handles:
- Loading NPC data from YAML files
- Tracking which NPCs have been met
- Managing hidden trait discovery
- Skill progression over time
- Persistence across game saves and new runs
- Salary calculations based on experience
"""

# TODO: Implement the following systems:

# 1. NPC Data Manager
#    - Load NPC base stats from YAML files
#    - Merge with persistent progression data
#    - Track current stats vs base stats

# 2. Hidden Trait System
#    - Track which traits have been discovered
#    - Reveal traits when triggered during gameplay
#    - Store discovery state permanently

# 3. NPC Progression Tracking
#    - Experience gains per project
#    - Skill improvements over time
#    - Salary progression (with 30% discount on new playthroughs)

# 4. Persistence System
#    - Save NPC state to permanent file (npc_progress.json)
#    - Carry over improvements between playthroughs
#    - Track relationship status with player

# 5. Meeting Status
#    - Not Met / Met / Recruited / Former Employee
#    - Where and when first met
#    - Recruitment availability

# Structure will be implemented here once meeting system is ready