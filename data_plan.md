# Save Data Plan - Game Dev Studio

## Overview
The game will use YAML files for save data storage, providing human-readable and easily editable save files. Python's built-in capabilities combined with PyYAML will handle serialization/deserialization.

## File Structure
```
/saves/
├── testsave1.yaml      # Primary save file
├── testsave2.yaml      # Additional save slots
└── autosave.yaml       # Automatic backup save
```

## Data Storage Solutions

### Primary: YAML Files
- **Pros**: Human-readable, easy debugging, version control friendly
- **Cons**: Larger file size than binary
- **Use Case**: Main save system

### Alternative: JSON
- **Pros**: Built into Python, widely supported
- **Cons**: Less human-readable than YAML
- **Use Case**: Backup format or settings

### Future: SQLite
- **Pros**: Relational data, queries, better for complex relationships
- **Cons**: More complex setup
- **Use Case**: If game grows significantly in complexity

## Save Data Structure

```yaml
# testsave1.yaml
game_metadata:
  version: "1.0.0"
  save_name: "My Studio Adventure"
  created_date: "2025-09-22T15:30:00Z"
  last_played: "2025-09-22T16:45:00Z"
  playtime_hours: 12.5

player_data:
  studio_name: "Awesome Games Inc"
  player_name: "John Developer"
  current_money: 50000
  reputation: 75
  stress_level: 30
  energy: 80

skills:
  programming: 65
  art: 45
  design: 70
  marketing: 30
  business: 55
  project_management: 40

studio_stats:
  games_published: 3
  total_sales: 150000
  awards_won: 1
  employees_hired: 8
  years_in_business: 2

current_projects:
  - project_id: "proj_001"
    name: "Space Adventure RPG"
    genre: "RPG"
    platform: "PC"
    progress_percent: 45
    team_assigned: ["emp_001", "emp_003", "emp_007"]
    deadline: "2025-11-15"
    budget_allocated: 25000
    budget_spent: 12000

employees:
  - id: "emp_001"
    name: "Alice Johnson"
    role: "Lead Programmer"
    skills:
      programming: 85
      teamwork: 70
    salary: 75000
    happiness: 80
    stress: 25
    hire_date: "2025-01-15"

  - id: "emp_002"
    name: "Bob Artist"
    role: "Senior Artist"
    skills:
      art: 90
      creativity: 85
    salary: 65000
    happiness: 75
    stress: 30
    hire_date: "2025-03-01"

completed_games:
  - id: "game_001"
    name: "Puzzle Master"
    genre: "Puzzle"
    platform: "Mobile"
    release_date: "2025-06-01"
    development_time_months: 4
    budget: 15000
    sales: 45000
    rating: 8.2
    team_size: 3

market_data:
  current_trends:
    - genre: "Battle Royale"
      popularity: 85
      saturation: 90
    - genre: "Indie Puzzle"
      popularity: 65
      saturation: 45
    - genre: "VR Games"
      popularity: 70
      saturation: 30

  platform_data:
    PC:
      market_share: 35
      difficulty: "Medium"
    Console:
      market_share: 40
      difficulty: "Hard"
    Mobile:
      market_share: 25
      difficulty: "Easy"

game_types:
  unlocked:
    - "Text Adventure"
    - "Platformer"
    - "Puzzle Game"
    - "Board Game"
  locked:
    - "RPG"
    - "FPS"
    - "Racing Game"
    - "MMO"

research_progress:
  "Advanced AI": 25
  "3D Graphics Engine": 60
  "Mobile Optimization": 80
  "VR Development": 15

events_history:
  - date: "2025-08-15"
    type: "market_crash"
    description: "Mobile market sees 20% decline"
    effects:
      - "mobile_sales_modifier: -0.2"

  - date: "2025-09-01"
    type: "employee_promotion"
    description: "Alice Johnson promoted to Lead Developer"
    effects:
      - "emp_001.role: Lead Programmer"
      - "emp_001.salary: 75000"

settings:
  auto_save_enabled: true
  auto_save_interval_minutes: 5
  difficulty: "Normal"
  tutorial_completed: true
```

## Data Management Classes

### SaveManager Class
```python
class SaveManager:
    def save_game(self, save_slot, game_data)
    def load_game(self, save_slot)
    def list_saves()
    def delete_save(self, save_slot)
    def auto_save(self, game_data)
```

### GameData Class
```python
class GameData:
    def __init__(self)
    def to_dict(self)  # For YAML serialization
    def from_dict(self, data)  # For YAML deserialization
    def validate(self)  # Data integrity checks
```

## Key-Value Storage Options

1. **Simple Dictionary + YAML** (Recommended for this project)
   - Native Python dictionaries
   - YAML serialization
   - Easy to implement and debug

2. **Shelve Module** (Built-in Python)
   - Persistent dictionary-like object
   - Binary storage
   - Good for simple key-value needs

3. **SQLite** (Built-in Python)
   - Full SQL database
   - Good for complex relationships
   - Overkill for current needs

4. **TinyDB** (Third-party)
   - Document-oriented database
   - JSON-based
   - Good middle ground

## Implementation Strategy

1. Start with YAML + dictionaries
2. Create comprehensive save/load system
3. Add data validation
4. Implement auto-save
5. Add save file management (list, delete, backup)

## Error Handling

- Corrupted save file detection
- Automatic backup creation
- Save file versioning
- Graceful degradation for missing data
- User-friendly error messages

## Security Considerations

- Save file validation
- Prevent save file injection
- Reasonable value bounds checking
- Backup save files before writing