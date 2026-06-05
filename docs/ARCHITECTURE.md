# Архитектура

## Технологический стек

| Компонент | Технология |
|-----------|------------|
| Среда выполнения | Python 3.10+ |
| Фреймворк бота | pyTelegramBotAPI |
| База данных | SQLite |
| Сборка пакета | hatchling |
| Документация | Sphinx + myst-parser |

## Слои архитектуры

```
┌─────────────────────────────────┐
│         Telegram API            │
├─────────────────────────────────┤
│     app/bot.py (точка входа)    │
├─────────────────────────────────┤
│  app/handlers/habits.py         │
│  app/handlers/goals.py          │
├─────────────────────────────────┤
│  src/hg_bot_tracker/ (ядро)     │
│  src/database.py                │
├─────────────────────────────────┤
│         SQLite БД               │
└─────────────────────────────────┘
```

## Описание компонентов

### 1. Точка входа (`app/bot.py`)
- Загружает переменные окружения
- Инициализирует базу данных
- Регистрирует все обработчики команд
- Запускает цикл polling только при прямом запуске (`if __name__ == "__main__"`)

### 2. Обработчики (`app/handlers/`)
- **habits.py** — обрабатывает `/add_habit`, `/habits`, `/done`
- **goals.py** — обрабатывает `/add_goal`, `/goals`, `/progress`
- Каждый обработчик парсит ввод пользователя, вызывает функции ядра и базы данных

### 3. Ядро (`src/hg_bot_tracker/`)
- **classes.py** — модели данных: `Habit`, `Completion`, `Goal`
- **habits.py** — логика привычек: `is_completed_today()`, `calculate_streak()`
- **goals.py** — логика целей: `get_goal_status()`, `add_progress()`, `is_overdue()`, `days_remaining()`

### 4. Слой базы данных (`src/database.py`)
- Управление подключением к SQLite
- CRUD-операции для привычек, отметок и целей
- Без ORM — прямые SQL-запросы

## Потоки данных

### Отметка выполнения привычки
```
Пользователь → /done → bot.py → обработчик привычек → get_habits()
                                                     → get_completions()
                                                     → is_completed_today()
                                                     → add_completion()
                                                     → calculate_streak()
                                                     → ответ пользователю
```

### Добавление прогресса цели
```
Пользователь → /progress → bot.py → обработчик целей → get_goals()
                                                      → add_progress()
                                                      → update_goal_status()
                                                      → update_goal_progress()
                                                      → ответ пользователю
```

## Граф зависимостей

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
