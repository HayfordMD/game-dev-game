# Game Dev Simulator - Design Document

## Key Questions
- **Core Goal**: What makes a successful indie game studio? we wqaant to level up from solo dev to major studio.
- **Player Role**: players are managing a studio

- **Player Motivation**: How do we balance creativity vs commercial success?
- **Risk vs Reward**: Should players play it safe or take creative risks? players should be able to go bankrupt. and they should be able to take out loans. if they lose money then thier life can fall apart. divorce, health issues, friends leave them sell house, etc.
- **Game Creation Process**: How detailed should the game development be? lets make a lot of the game dev process happen in front of the player. they should see a pc screen with code, art, design docs, etc. we will make some mini games for these.
- **Team Dynamics**: How important is team chemistry and individual skills? we want team skills to matter. chemestiry is not as important as skills. 
- the player sets the culture of the studio. overworked and creative vs balanced and slow. or coporate focus profits are key. 
- **Resource Management**: What resources critical to success time, money, energy, reputation, creativity
- **Social Elements**: How important are networking and team chemistry? no important dfont need
- **Progression**: What unlocks as players succeed (or fail)? more money. events, more team memebres, more complex games, more complex features, more complex genres

## Game Flow Overview - Solo to Major Studio Progression

### Phase 1: Broke Solo Developer (Tutorial)
**Start Menu Flow:**
- Start New Game
- Name Your Studio
- Choose Starting Background: Programmer, Artist, Designer, Business (affects initial stats and starting money)

**Character Creation:**
- Top-down view of cramped studio apartment
- Click to name your character
- Starting stats: Programming, Art, Design, Marketing, Energy, Money ($500-2000 depending on background)
- Starting debt: Student loans, credit cards

**Survival Mode:**
- Studio apartment: desk/computer, bed, shower, kitchen, front door
- Must pay rent ($800/month) or get evicted
- Basic needs: Energy, food costs money
- No hygiene requirements (solo dev life)

### Phase 2: First Commercial Game
**PC Screen Interface:**
When clicking desk, player sees actual computer screen with:
- **Code Editor**: Mini-game for programming
- **Art Software**: Mini-game for creating sprites/models
- **Design Documents**: Planning and balancing gameplay
- **Email**: Publishers, fans, hate mail
- **Bank Account**: Track money in real-time

**Work Schedule System:**
- **Ideal Schedule**: 8 hours work + 1 hour break = optimal productivity
- **Crunch Mode**: Up to 16 hours/day but decreases efficiency and health
- **Schedule UI**: Set daily/weekly schedules in advance
- **Time Skip**: Can skip days/weeks if schedule is set
- **Energy Management**: Overwork decreases productivity exponentially
- **Break Benefits**: Breaks restore creativity and prevent burnout

**Game Creation Mini-Games:**
1. **Programming Mini-Game**: Tetris-like code blocks, faster = better code quality
2. **Art Mini-Game**: Pixel art creator or 3D modeling puzzles
3. **Design Mini-Game**: Balance sliders for difficulty, fun, innovation
4. **Bug Testing**: Whack-a-mole style bug hunting

**Financial Pressure:**
- Must release games to pay rent and eat
- Can take loans from bank (high interest)
- Failed games = deeper debt
- Success = more money to invest

### Phase 3: Small Team (2-5 people)
**Hiring System:**
- Interview candidates with different skill levels
- Higher skilled = higher salary demands
- Must manage payroll monthly
- Skills matter more than personality

**Studio Culture Settings:**
- **Crunch Culture**: Overworked but creative, high burnout risk
- **Work-Life Balance**: Slower but sustainable, lower turnover
- **Corporate Focus**: Profit-driven, efficient but less innovative

### Phase 4: Mid-Size Studio (6-20 people)
**Office Management:**
- Rent larger office space
- Multiple teams working on different projects
- Department heads manage sub-teams
- More complex financial management

### Phase 5: Large Studio (20-100 people)
**Corporate Operations:**
- Multiple offices in different cities
- Publisher relationships and contracts
- Marketing departments and PR teams
- Shareholder meetings and quarterly reports

### Phase 6: Major Studio/Publisher (100+ people)
**Industry Leader:**
- Acquire smaller studios
- Fund external developers
- Create gaming platforms
- Influence industry trends

## Critical Resource Management

### Essential Resources (Survival)
- **Money**: Pay rent, food, salaries, equipment, marketing
- **Time**: Development deadlines, market windows, competition
- **Energy**: Personal stamina for solo work, decreases with stress
- **Reputation**: Industry standing, affects sales and hiring
- **Creativity**: Innovation points, depletes with repetitive/corporate work

### Financial Risk System
- **Monthly Expenses**: Rent, salaries, utilities, loan payments
- **Loan System**: Take out loans with interest, bankruptcy if defaulted
- **Credit Rating**: Affects loan availability and interest rates
- **Emergency Funds**: Reserve money for failed projects

### Life Consequences of Failure
- **Bankruptcy**: Lose office, fire all employees, move back to apartment
- **Health Issues**: Stress-related problems from overwork/financial pressure
- **Relationship Strain**: Divorce/breakups from neglecting personal life
- **Social Isolation**: Friends leave due to constant work focus
- **Asset Loss**: Sell house, car, personal belongings to pay debts

## Skill-Focused Team System

### Employee Attributes (Skills Priority)
- **Primary Skills**: Programming, Art, Design, Audio, QA, Marketing, Business
- **Skill Levels**: 1-10 rating in each area
- **Specializations**: Mobile, PC, Console, VR, AI, etc.
- **Salary Demands**: Higher skills = higher cost
- **Productivity**: Directly tied to skill level and studio culture
- **Learning Rate**: How fast they improve with experience

### Studio Culture Impact
**Crunch Culture:**
- +50% productivity short-term
- High burnout risk (employees quit)
- +Creativity bonus
- Health issues for staff

**Balanced Culture:**
- Normal productivity
- Low turnover
- Steady skill improvement
- Higher employee satisfaction

**Corporate Culture:**
- +30% efficiency
- -Creativity penalty
- Focus on proven formulas
- Higher profits, lower innovation

## Visual Game Development Process

### PC Screen Development Interface
When working on games, players see actual development tools:

**Programming Screen:**
- Code editor with syntax highlighting
- Mini-game: Arrange code blocks Tetris-style
- Bug counter increases with rushed work
- Performance meter shows optimization level

**Art Creation Screen:**
- Pixel art editor for 2D games
- 3D modeling interface for 3D games
- Color palette and animation tools
- Art quality visible in real-time

**Design Document Screen:**
- Feature list with checkboxes
- Balance sliders for difficulty/fun
- Player feedback integration
- Scope creep warnings

### Development Mini-Games
1. **Code Mini-Game**: Tetris blocks represent functions, faster placement = better code
2. **Art Mini-Game**: Pixel perfect drawing challenges, 3D model assembly
3. **Debug Mini-Game**: Whack-a-mole bug hunting, logic puzzle solving
4. **Balance Mini-Game**: Adjust sliders while watching player satisfaction meter
5. **Marketing Mini-Game**: Create trailers, write press releases, social media campaigns

### Complexity Progression
- **Simple Games**: Pong, Tetris clones (1-2 features)
- **Casual Games**: Mobile puzzlers (3-5 features)
- **Indie Games**: Platformers, roguelikes (5-10 features)
- **AA Games**: Complex mechanics (10-20 features)
- **AAA Games**: Multiple systems (20+ features, multiplayer, live services)

### Random Events & Market Dynamics
- **Market Trends**: Genres rise and fall in popularity
- **Platform Changes**: New consoles, mobile updates, VR adoption
- **Competitor Releases**: Other studios release competing games
- **Economic Events**: Recessions affect game sales
- **Viral Moments**: Unexpected social media attention
- **Industry Drama**: Scandals and controversies affect market

## Progression Systems

### Skill Development
- **Programming**: Faster development, better optimization, new platforms
- **Art**: Better visuals, faster asset creation, new art styles
- **Design**: More engaging mechanics, better balance, player psychology
- **Marketing**: Better launch campaigns, community building, influencer relations
- **Business**: Better negotiations, financial management, strategic planning

### Unlockables
- **New Genres**: Start with 3-4, unlock more complex types
- **Advanced Features**: Multiplayer, VR support, mod tools, live services
- **Better Tools**: Faster development, higher quality output
- **Larger Teams**: Start solo, grow to small team, then full studio
- **Publishing Options**: Self-publish, indie publisher, major publisher deals

### Studio Growth Stages
1. **Bedroom Developer**: Solo in apartment
2. **Indie Team**: Small rented office, 2-5 people
3. **Small Studio**: Proper office space, 6-15 people
4. **Mid-Size Developer**: Multiple teams, 16-50 people
5. **Large Studio**: Multiple projects, 50+ people, multiple offices

## Success & Failure Mechanics

### Success Metrics
- **Critical Reception**: Review scores from press and players
- **Commercial Success**: Units sold and revenue generated
- **Cultural Impact**: How much the game influences other developers
- **Community Building**: Active player base and mod scene
- **Personal Growth**: Skill improvement and industry reputation

### Failure Recovery
- **Learning from Mistakes**: Failed projects provide experience points
- **Reputation Repair**: Successful follow-ups restore credibility
- **Financial Recovery**: Freelance work, publisher deals, investor funding
- **Team Retention**: Keep key talent motivated during tough times

### Victory Conditions - Studio Evolution
1. **Solo Success**: Release 5 profitable games as solo developer
2. **Small Team Leader**: Manage 5-person team for 2 years without bankruptcy
3. **Mid-Size Studio**: 20+ employees, multiple concurrent projects
4. **Large Studio**: 50+ employees, AAA game releases
5. **Major Publisher**: 100+ employees, acquire other studios
6. **Industry Titan**: Multiple studios worldwide, platform creation

### Failure States
- **Bankruptcy**: All money lost, start over in apartment
- **Health Breakdown**: Stress-induced inability to work
- **Team Exodus**: All employees quit due to poor management
- **Market Irrelevance**: Unable to adapt to industry changes
- **Legal Troubles**: Lawsuits, IP theft, regulatory issues

## Random Result Systems

### Development Surprises
- **Happy Accidents**: Bugs become features, unexpected mechanics emerge
- **Technical Breakthroughs**: Solve difficult problems faster than expected
- **Creative Blocks**: Team struggles with design decisions
- **Scope Creep**: Features grow beyond original plan
- **Crunch Time**: Deadline pressure affects team and quality

### Market Randomness
- **Seasonal Variations**: Holiday sales, summer lulls, back-to-school
- **Platform Policies**: App store changes, console certification issues
- **Influencer Coverage**: Streamers and YouTubers discover your game
- **Awards and Recognition**: Unexpected nominations and wins
- **Piracy and Leaks**: Builds leak early, affecting launch timing

### Personal Events
- **Team Life Changes**: Marriages, babies, family emergencies
- **Health Issues**: Burnout, RSI, mental health challenges
- **Industry Opportunities**: Job offers from other studios
- **Personal Inspiration**: Life experiences inspire new game ideas 