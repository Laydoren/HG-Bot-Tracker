# HG-Bot-Tracker
Telegram-бот для отслеживания привычек и целей.

## Установка и запуск
```bash
make install   # установить зависимости
make run       # запустить бота
```

## Тесты
```bash
make test      # запустить тесты
```

## Структура

```shell
app/bot.py         — точка входа
app/handlers/      — обработчики команд
src/               — библиотека и БД
src/hg_bot_tracker/ — модели и логика
src/database.py    — SQLite
docs/              — документация Sphinx
tests/             — тесты
```

