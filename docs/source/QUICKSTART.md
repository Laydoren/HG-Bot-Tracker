# Quick start

This page describes how to install and use HG-Bot-Tracker.

## Install

```bash
pip install hg-bot-tracker
```

## Example

```python
from datetime import date
from src.hg_bot_tracker.classes import Goal
from src.hg_bot_tracker.goals import add_progress

goal = Goal(id=1, title="Read 10 books", target=10, current=3, deadline=date(2026, 12, 31))
add_progress(goal, 2)
print(goal.status_completion)
```
