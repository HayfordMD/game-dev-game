"""
NPC Persistence System
Handles saving and loading NPC progress across game sessions and new playthroughs

This system ensures NPC growth carries over between runs, making each playthrough
feel connected while maintaining game balance through salary adjustments.
"""

# TODO: Implement the following persistence features:

# 1. PERMANENT NPC DATA FILE (npc_permanent_progress.json)
#    Structure:
#    {
#      "npc_id": {
#        "times_hired": 0,
#        "total_projects": 0,
#        "skill_gains": {
#          "engineering": 0,
#          "marketing": 0,
#          "leadership": 0,
#          "design": 0,
#          "research": 0,
#          "communication": 0
#        },
#        "discovered_traits": ["trait_name1", "trait_name2"],
#        "relationship_score": 0,
#        "first_met": {
#          "date": "1984-01-01",
#          "location": "grocery_store",
#          "playthrough": 1
#        },
#        "career_highlights": [
#          {"game": "Space Quest", "rating": "MASTERPIECE", "role": "Lead Designer"}
#        ],
#        "lifetime_earnings": 0,
#        "best_performance": {},
#        "salary_history": []
#      }
#    }

# 2. SKILL PROGRESSION RULES
#    - Each project completed: +0.1 to relevant skills (max +0.5 per project)
#    - Successful project (Good+): Additional +0.2 to primary skill
#    - Masterpiece contribution: +0.5 to all involved skills
#    - Skills cap at 10, but experience continues tracking
#    - Working with better developers: Learn faster (+0.2 if working with 8+ skill)

# 3. SALARY CALCULATIONS
#    - Base Salary = (Skill Total * 100) + (Experience Years * 50)
#    - First Hire: 100% of calculated salary
#    - Rehire Same Playthrough: 110% (knows their worth)
#    - New Playthrough Discount: 70% (30% off due to relationship)
#    - Legendary Status: Never below certain minimum based on achievements

# 4. HIDDEN TRAIT DISCOVERY
#    - Once discovered, trait is permanently revealed
#    - Discovery adds note about when/how it was discovered
#    - Some traits might evolve/upgrade after multiple discoveries
#    - Player can see hints about undiscovered traits after working together

# 5. RELATIONSHIP TRACKING
#    - Increases through successful projects together
#    - Decreases if fired or if projects fail
#    - Affects recruitment ease and salary negotiations
#    - Unlocks special dialogue and story events

# 6. CROSS-PLAYTHROUGH FEATURES
#    - "Remember me?" dialogue if previously worked together
#    - Reference past games made together
#    - Loyalty bonus: Easier to recruit if good history
#    - Grudges: Harder/impossible if bad history
#    - Mentor System: Can teach other NPCs faster if experienced

# 7. ACHIEVEMENT TRACKING
#    - Track each NPC's greatest accomplishments
#    - "Hall of Fame" developers become legends
#    - Industry recognition affects all future interactions
#    - Some NPCs can "retire" after great success (unavailable but remembered)

# 8. SAVE MIGRATION
#    - Version compatibility checking
#    - Graceful handling of missing data
#    - Backup before major updates
#    - Can reset individual NPCs if needed

# Implementation pending - will integrate with save system and NPC manager