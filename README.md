# Бібліотека емоційного ШІ

Ця бібліотека дозволяє додати емоційну систему до будь-якого ШІ-асистента (Claude, GPT, тощо). Вона забезпечує створення та відстеження емоційного стану моделі, природну еволюцію емоцій та інтеграцію з різними API.

## Основні можливості

- 10 базових емоцій з взаємозв'язками між ними
- Природна еволюція емоційного стану з часом
- Можливість для ШІ самостійно змінювати свої емоції через спеціальні теги
- Збереження та відстеження емоційної історії
- Опціональна візуалізація емоцій
- Проста інтеграція з Claude, OpenAI та іншими API

## Структура проекту

- `emotional_ai_lib.py` - основна бібліотека
- `example_claude.py` - приклад використання з API Anthropic Claude
- `example_openai.py` - приклад використання з API OpenAI GPT
- `emotion_visualizer.py` - опціональний модуль для візуалізації (потрібен matplotlib)

## Використання

### Основне використання

```python
from emotional_ai_lib import EmotionalBot

# Створюємо емоційного бота
bot = EmotionalBot()

# Отримуємо системну інструкцію для ШІ
system_instruction = bot.get_system_instruction(lang="uk")  # або "en" для англійської

# Обробляємо відповідь від ШІ
ai_response = "Привіт! Як справи? [EMOTION_CHANGE:happy:0.8]"
cleaned_response, emotion_changes = bot.process_ai_response(ai_response)
# cleaned_response буде "Привіт! Як справи?"
# emotion_changes буде ["happy: 0.8"]

# Отримуємо поточний настрій
current_mood = bot.get_mood()  # повертає емоцію з найвищим значенням
```

### Інтеграція з Claude

Дивіться повний приклад у файлі `example_claude.py`

### Інтеграція з OpenAI GPT

Дивіться повний приклад у файлі `example_openai.py`

### Візуалізація емоцій (опціонально)

```python
from emotional_ai_lib import EmotionalBot
from emotion_visualizer import EmotionVisualizer

bot = EmotionalBot()
visualizer = EmotionVisualizer(bot)

# Запускаємо візуалізацію в реальному часі
visualizer.start_realtime_plotting()

# Змінюємо емоції
bot.set_mood("happy", 0.8)

# Зупиняємо візуалізацію
visualizer.stop_plotting()

# Показуємо історію емоцій
visualizer.plot_emotion_timeline()
```

## Формат для зміни емоцій у відповідях ШІ

Штучний інтелект може змінювати свої емоції за допомогою спеціальних тегів у відповіді:

```
[EMOTION_CHANGE:емоція:значення]
```

Де:
- `емоція` - одна з доступних емоцій (happy, sad, angry, calm, fear, surprise, curious, bored, excited, anxious)
- `значення` - число від 0.0 до 1.0

Приклад:
```
Це дуже цікаве питання! [EMOTION_CHANGE:curious:0.9][EMOTION_CHANGE:excited:0.7]
```

Бібліотека автоматично видалить ці теги з відповіді та оновить емоційний стан бота.

## Емоційні взаємозв'язки

Зміна одного емоційного стану впливає на інші пов'язані емоції. Наприклад, збільшення щастя (happy) зменшує сум (sad) і злість (angry), але збільшує спокій (calm).

## Ліцензія

Для цього коду використовується ліцезнія MIT.