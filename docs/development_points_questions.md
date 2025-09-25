# Game Development Points Generation - Design Questions

## Overview
This document outlines questions about how developer stats should affect point generation during different stages of game development.

## Development Stages

### 1. Planning Stage
**Primary Focus:** Gameplay, Innovation, Story
**Current Generation:**
- Gameplay: 2-5 points per bounce
- Innovation: 2-4 points per bounce
- Story: 1-4 points per bounce
- Technical: 0-1 points per bounce
- Graphics: 0-1 points per bounce
- Sound/Audio: 0 points per bounce

### 2. Development Stage
**Primary Focus:** Technical, Graphics
**Current Generation:**
- Technical: 3-5 points per bounce
- Graphics: 2-5 points per bounce
- Gameplay: 0-2 points per bounce
- Innovation: 0-1 points per bounce
- Story: 0 points per bounce
- Sound/Audio: 0-1 points per bounce

### 3. Production Stage
**Primary Focus:** Sound/Audio, Story
**Current Generation:**
- Sound/Audio: 3-5 points per bounce
- Story: 2-4 points per bounce
- Graphics: 1-2 points per bounce
- Technical: 0-1 points per bounce
- Gameplay: 0-1 points per bounce
- Innovation: 0 points per bounce

### 4. Bug Squashing Stage
**Primary Focus:** Technical (fixing), Gameplay (polish)
**Current Generation:**
- Technical: 2-4 points per bounce
- Gameplay: 1-3 points per bounce
- Graphics: 0-1 points per bounce
- Innovation: 0 points per bounce
- Story: 0 points per bounce
- Sound/Audio: 0 points per bounce

## Questions for Developer Stats System

### 1. Developer Skill Categories
**Question:** What skill categories should developers have?
    engineering: 6      # 0-10 scale
    marketing: 2        # 0-10 scale
    leadership: 1       # 0-10 scale
    design: 5          # 0-10 scale
    research: 4        # 0-10 scale
    communication: 2   # 0-10 scale


Options:
- 0-10 scale (beginner to expert)

### 3. Point Calculation Formula
**Question:** How should developer skills affect point generation?

 **Mixed System:**
   - Base range affected by skill tier
   - Critical success chance based on skill level
   - Consistency improves with experience

yearsd of experiance with the same company we need to track how long they have worked for us. and if they leave for a while it slowly degreases. a month is owrht .25 points and you max a chacrater at 100 points so 400 months is max to get to best skill level for a person. if they leave it decreasea at 2 points per month. 

### 4. Multiple Developer Contributions
**Question:** When multiple developers work on a stage, how should their skills combine?
communcation skill plays a big role 


lead developer determins the min. if the lead deverloper as a 5 development skill then the min score a game could have for technical is 5. 



 Average of all developer skills

- Sum of contributions (with diminishing returns or increasess based on communication skills


### 5. Developer Specializations
**Question:** Should developers have specializations that provide extra bonuses?

developers have specalities and abilities but we will wait to add thso e in. 

### 6. Experience and Growth
**Question:** Should developers improve their skills over time?

- Gain experience from completed projects
- Skills improve based on what they worked on
- Can attend training 


### 7. Morale and Performance
**Question:** Should developer morale affect point generation? yes

Morale factors:
- Consecutive projects (fatigue)
- Project success/failure

- Work environment
- Team overall communication score. If the whole company has a high communcation score then there will be higher company morale. The average communication score of all employees must be above 8.3 in order for the company to have 100% morale. if the average communication score is below 8.3 then the company will have a morale penalty of -5% for every 1 point below 8.3.

Potential effects:
- Low morale under 30: -20% to all point generation
- High morale over 90: +20% to all point generation





### 9. Technology and Tools
**Question:** Should the game engine or tools affect point generation?

Considerations:
- Better engines provide base bonuses


### 10. Random Events
**Question:** Should there be random events during development? yes make a list

Examples:
- "Eureka moment": Double points for one bounce
- "Creative block": Reduced points for stage
- "Technical breakthrough": +5 Technical permanently


## Implementation Priority

1. **Phase 1 - Basic Skills:**
   - Add 3-5 basic skills to developers
   - Simple linear scaling of points
   - Player character starts with moderate skills

2. **Phase 2 - Specializations:**
   - Add developer types/roles
   - Implement specialization bonuses
   - Hire system with different developer types

3. **Phase 3 - Advanced Systems:**
   - Experience and skill growth
   - Morale system
   - Team synergy
   - Random events

## Current Implementation Status
- [] Multi-stage development system created
- [] Stage-specific point generation
- [] Bouncing animation for visual feedback
- [] Developer selection per stage
- [ ] Developer skill stats
- [ ] Skill-based point modifiers
- [ ] Experience system
- [ ] Morale/fatigue system
- [ ] Team synergy bonuses

## Next Steps
1. Define initial developer stats structure
2. Implement basic skill-based modifiers
3. Create hiring system with different developer types
4. Add experience gain from completed projects
5. Implement morale/fatigue for repeated development