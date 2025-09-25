# NPC Creation Guide for Game Dev Tycoon

## Overview
This document provides comprehensive instructions for creating NPCs that integrate with all game systems, including hidden abilities that impact gameplay.

## File Structure

### 1. Main Registry (npcs/npcs.yml)
Add basic entry:
```yaml
- name: [Full Name]
  id: [Unique Number]
  gender: [male/female/other]
  job: [Job Title]
```

### 2. Individual NPC File (npcs/npcslist/[id]_[firstname_lastname].yml)

## Complete NPC Template

```yaml
character:
  name: "[Full Name]"
  id: [Unique ID - must match npcs.yml]
  gender: "[male/female/other]"

  skills:
    engineering: [0-10]      # Technical ability, bug fixing, optimization
    marketing: [0-10]        # Promotion, market analysis, sales
    leadership: [0-10]       # Team coordination, morale boost, project management
    design: [0-10]           # Creative vision, gameplay, aesthetics
    research: [0-10]         # Innovation, new techniques, trend spotting
    communication: [0-10]    # Team collaboration, PR, documentation

  job: [Job Title - see Job Categories below]

  personality:
    description: "[2-3 sentences covering work style, strengths, quirks, and interactions]"

  background:
    education: "[Relevant degree/certification/self-taught path]"
    work_history: "[Previous roles and experience]"
    personal_history: "[Formative experiences that shape their approach]"

  ### max 3 hidden traits
  hidden_traits:
    - trait: "[trait name]"
      ability: "[specific game effect]"
    - trait: "[trait name]"
      ability: "[specific game effect]"
    - trait: "[trait name]"
      ability: "[specific game effect]"
```

## Skill Guidelines

### Engineering (0-10)
- **0-2**: Beginner, makes frequent mistakes
- **3-4**: Junior level, needs supervision
- **5-6**: Competent, reliable work
- **7-8**: Senior level, excellent quality
- **9-10**: Expert, revolutionary techniques

**Impacts**: Technical score, bug reduction, development speed, optimization

### Marketing (0-10)
- **0-2**: No market sense
- **3-4**: Basic understanding
- **5-6**: Good instincts
- **7-8**: Strategic thinking
- **9-10**: Trendsetter

**Impacts**: Sales multiplier, hype generation, audience targeting

### Leadership (0-10)
- **0-2**: Follower only
- **3-4**: Can lead small tasks
- **5-6**: Good team coordinator
- **7-8**: Inspiring leader
- **9-10**: Visionary director

**Impacts**: Team morale, productivity bonus, conflict resolution

### Design (0-10)
- **0-2**: No creative vision
- **3-4**: Basic aesthetic sense
- **5-6**: Solid design skills
- **7-8**: Innovative creator
- **9-10**: Artistic genius

**Impacts**: Gameplay, graphics, story, innovation scores

### Research (0-10)
- **0-2**: Stuck in old ways
- **3-4**: Learns slowly
- **5-6**: Good learner
- **7-8**: Quick adapter
- **9-10**: Pioneer

**Impacts**: Innovation score, unlock speed, trend discovery

### Communication (0-10)
- **0-2**: Creates confusion
- **3-4**: Basic clarity
- **5-6**: Clear communicator
- **7-8**: Excellent collaborator
- **9-10**: Master facilitator

**Impacts**: Team synergy, morale, documentation quality, PR success

## Job Categories

### Core Development
- Game Designer
- Programmer/Software Engineer
- Artist
- Audio Designer/Sound Engineer
- Producer
- Quality Assurance Tester
- Narrative Designer
- Level Designer

### Technical Specialists
- Gameplay Programmer
- Engine Programmer
- Graphics/Rendering Programmer
- AI Programmer
- Physics Programmer
- Network/Multiplayer Programmer
- UI Programmer
- Tools Programmer
- Shader Developer/Technical Artist

### Management
- Game Director
- Technical Director
- Art Director
- Executive Producer
- Project Manager

### Support Roles
- Marketing Manager/Director
- Public Relations Specialist
- Community Manager
- Business Development Manager
- Human Resources
- Finance/Accounting
- IT Support

## Hidden Traits System

### Categories & Examples

#### Production Modifiers
```yaml
- trait: "crunch veteran"
  ability: "immune to fatigue during final month of development"

- trait: "perfectionist"
  ability: "10% chance to remove 1 bug per day but 5% slower development"

- trait: "speed coder"
  ability: "completes programming tasks 20% faster when morale >80"
```

#### Point Generation
```yaml
- trait: "golden ear"
  ability: "5% chance to add +1 Sound/Audio and innovation"

- trait: "secret hunter"
  ability: "always includes hidden areas, +5 Gameplay points"

- trait: "trend spotter"
  ability: "doubles innovation points when using current year mechanics"
```

#### Team Effects
```yaml
- trait: "mentor"
  ability: "junior team members gain 2x experience when on same project"

- trait: "inspirational"
  ability: "all team members get +1 to their highest skill when working together"

- trait: "mood maker"
  ability: "team morale never drops below 50% when present"
```

#### Special Triggers
```yaml
- trait: "night owl"
  ability: "produces 2x points during evening development sessions"

- trait: "vintage enthusiast"
  ability: "+3 all scores when making retro/pixel art games"

- trait: "platform specialist"
  ability: "+5 technical when developing for [specific platform]"
```

#### Economic Effects
```yaml
- trait: "budget hawk"
  ability: "reduces development costs by 10%"

- trait: "trustworthy"
  ability: "reduces loan interest rates by 25% due to good reputation"

- trait: "efficiency expert"
  ability: "reduces time per development stage by 1 day"
```

#### Conditional Abilities
```yaml
- trait: "comeback kid"
  ability: "after a game rates below 'Good', next game gets +10 all scores"

- trait: "franchise builder"
  ability: "sequels get +15% rating boost"

- trait: "genre master [RPG]"
  ability: "RPG games get +2 in all categories"
```

## Integration with Game Systems

### Points Generation System
- Skills directly modify point ranges during development
- Hidden traits can trigger bonus points or multipliers
- Communication affects team collaboration bonuses

### Morale System
- Leadership skills affect morale decay rate
- Certain traits can set morale floors or provide boosts
- Personality conflicts based on trait combinations

### Random Events
Hidden traits can:
- Increase/decrease event chances
- Unlock unique events
- Modify event outcomes

### Financial System
- Marketing skills affect sales projections
- Some traits reduce costs or attract funding
- Salary expectations based on skill totals

### Development Stages
Each NPC contributes differently:
- **Planning**: Design + Research skills dominate
- **Development**: Engineering + Design balance
- **Production**: All skills contribute
- **Bug Squashing**: Engineering + Communication critical

## Personality Description Guidelines

Include:
1. **Work Style**: How they approach tasks
2. **Strengths**: What they excel at
3. **Weaknesses/Quirks**: Humanizing flaws
4. **Team Dynamics**: How they interact

Example:
"Passionate about creating immersive soundscapes, James has an excellent ear for detail and atmosphere. He's patient and methodical, often working late to get the perfect sound mix. Tends to be quiet in meetings but speaks up confidently about audio matters."

## Balancing Considerations

### Skill Distribution
- **Total Skills**: Aim for 20-30 points total
- **Specialists**: High in 1-2 areas, low elsewhere
- **Generalists**: Moderate (4-6) across multiple areas
- **Seniors**: Higher totals (25-35) with experience
- **Juniors**: Lower totals (15-25) with growth potential

### Hidden Trait Power Levels
- **Minor**: Small consistent bonuses (1-5%)
- **Moderate**: Situational medium bonuses (10-20%)
- **Major**: Rare but significant effects (25%+)
- **Unique**: One-of-a-kind abilities

### Rarity Guidelines
- Common NPCs: 1-2 minor traits
- Uncommon NPCs: 2 moderate traits or 1 major
- Rare NPCs: 2-3 traits including 1 major
- Legendary NPCs: 3 powerful synergistic traits

## Prompt Template for AI Generation

"Create an NPC for a game development tycoon game:

**Basic Info**: [Name, Gender, Job Role]

**Personality Focus**: [e.g., perfectionist, innovator, team player]

**Skill Distribution**: [e.g., technical specialist, creative generalist]

**Era Specialty**: [e.g., 1980s arcade, modern indie, AAA production]

Generate:
1. Skills (0-10 scale) totaling 20-30 points
2. Personality description (2-3 sentences)
3. Background (education, work history, personal history)
4. 2-3 hidden traits with specific game mechanics effects

Consider how this character would impact:
- Point generation during development
- Team morale and dynamics
- Random event chances
- Financial aspects
- Special synergies with game types/topics"

## Special Considerations

### Era-Specific NPCs
- 1978-1985: Lower overall skills, pioneering traits
- 1985-1995: Emerging specialists, platform expertise
- 1995-2005: Online/3D revolution traits
- 2005+: Modern development, social media savvy

### Synergy Opportunities
Design NPCs that work well together:
- Complementary skills
- Trait combinations that unlock bonuses
- Personality matches for morale boosts

### Story NPCs
Some NPCs can have special story significance:
- Industry legends with unique events
- Rival developers who compete
- Mentors who provide learning bonuses

---

## Quick Checklist

- [ ] Unique ID assigned
- [ ] Skills total 20-30 points (adjust for seniority)
- [ ] Job matches skill distribution
- [ ] Personality includes work style and quirks
- [ ] Background explains skill origins
- [ ] 1-3 hidden traits with clear mechanics
- [ ] Balanced for game difficulty
- [ ] Interesting synergies considered
- [ ] File named correctly: `[id]_[firstname_lastname].yml`
- [ ] Added to main registry `npcs.yml`