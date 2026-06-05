# Architecture

## Technology Stack

| Component | Technology |
|-----------|------------|
| Runtime | Python 3.10+ |
| Bot framework | pyTelegramBotAPI |
| Database | SQLite |
| Build | hatchling |
| Docs | Sphinx + myst-parser |

## Layer Architecture

```
┌─────────────────────────────────┐
│         Telegram API            │
├─────────────────────────────────┤
│     app/bot.py (entry point)    │
├─────────────────────────────────┤
│  app/handlers/habits.py         │
│  app/handlers/goals.py          │
├─────────────────────────────────┤
│  src/hg_bot_tracker/ (core lib) │
│  src/database.py                │
├─────────────────────────────────┤
│         SQLite DB               │
└─────────────────────────────────┘
```

## Component Description

### 1. Entry Point (`app/bot.py`)
- Loads environment variables
- Initializes database
- Registers all command handlers
- Starts bot polling only when run directly (`if __name__ == "__main__"`)

### 2. Handlers (`app/handlers/`)
- **habits.py** — handles `/add_habit`, `/habits`, `/done`
- **goals.py** — handles `/add_goal`, `/goals`, `/progress`
- Each handler parses user input, calls core logic and database functions

### 3. Core Library (`src/hg_bot_tracker/`)
- **classes.py** — data models: `Habit`, `Completion`, `Goal`
- **habits.py** — habit logic: `is_completed_today()`, `calculate_streak()`
- **goals.py** — goal logic: `get_goal_status()`, `add_progress()`, `is_overdue()`, `days_remaining()`

### 4. Database Layer (`src/database.py`)
- SQLite connection management
- CRUD operations for habits, completions, goals
- No ORM — raw SQL queries

## Data Flow

### Habit Completion Flow
```
User → /done → bot.py → habits handler → get_habits()
                                       → get_completions()
                                       → is_completed_today()
                                       → add_completion()
                                       → calculate_streak()
                                       → response to user
```

### Goal Progress Flow
```
User → /progress → bot.py → goals handler → get_goals()
                                          → add_progress()
                                          → update_goal_status()
                                          → update_goal_progress()
                                          → response to user
```

## Dependency Graph

```
app/bot.py
  ├── app/handlers/habits.py
  │     ├── src/hg_bot_tracker/classes.py
  │     ├── src/hg_bot_tracker/habits.py
  │     └── src/database.py
  └── app/handlers/goals.py
        ├── src/hg_bot_tracker/classes.py
        ├── src/hg_bot_tracker/goals.py
        └── src/database.py
```
