# LangGraph Time Bot
**Stateless чат-бот с инструментом времени**

## 📦 Установка
```bash
# Создание виртуального окружения (выполнить один раз)
python -m venv .venv

# Активация (Windows):
.venv\Scripts\activate
# Для Git Bash используйте:
source .venv/Scripts/activate

# Установка зависимостей (из requirements.txt)
pip install -r requirements.txt
```

## 🚀 Запуск
```bash
# Стандартный запуск через FastAPI
python bot.py

# Или альтернативно через uvicorn:
uvicorn bot:app --reload
```

## 🧪 Тестирование
```bash
# Проверка работы инструмента времени:
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"content": "What time is it?"}]}'

# Ожидаемый ответ (пример):
# {"response": {"utc": "2025-05-21T06:42:00Z"}}
```
