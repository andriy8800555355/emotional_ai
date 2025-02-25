import time
import random
import re


class EmotionalBot:
    def __init__(self):
        self.emotions = {
            "happy": 0.5,
            "sad": 0.5,
            "angry": 0.5,
            "calm": 0.5,
            "fear": 0.5,
            "surprise": 0.5,
            "curious": 0.5,
            "bored": 0.5,
            "excited": 0.5,
            "anxious": 0.5,
        }

        self.emotion_links = {
            "happy": {
                "sad": -0.6,
                "angry": -0.4,
                "calm": 0.3,
                "fear": -0.5,
                "excited": 0.4,
                "anxious": -0.3,
            },
            "sad": {
                "happy": -0.6,
                "angry": 0.2,
                "calm": -0.3,
                "fear": 0.3,
                "bored": 0.3,
                "excited": -0.4,
            },
            "angry": {
                "happy": -0.4,
                "sad": 0.2,
                "calm": -0.5,
                "fear": 0.1,
                "curious": -0.2,
                "anxious": 0.3,
            },
            "calm": {
                "happy": 0.3,
                "sad": -0.3,
                "angry": -0.5,
                "fear": -0.4,
                "anxious": -0.5,
                "bored": 0.2,
            },
            "fear": {
                "happy": -0.5,
                "calm": -0.4,
                "angry": 0.1,
                "surprise": 0.3,
                "anxious": 0.5,
                "curious": -0.2,
            },
            "surprise": {
                "fear": 0.3,
                "happy": 0.2,
                "curious": 0.4,
                "bored": -0.4,
                "excited": 0.3,
            },
            "curious": {
                "bored": -0.6,
                "excited": 0.3,
                "surprise": 0.2,
                "calm": 0.1,
                "anxious": -0.1,
            },
            "bored": {
                "curious": -0.5,
                "excited": -0.4,
                "happy": -0.3,
                "sad": 0.2,
                "calm": 0.2,
            },
            "excited": {
                "bored": -0.5,
                "happy": 0.4,
                "curious": 0.3,
                "calm": -0.3,
                "sad": -0.3,
            },
            "anxious": {
                "calm": -0.5,
                "fear": 0.4,
                "angry": 0.2,
                "happy": -0.3,
                "excited": 0.1,
            },
        }

        self.chat_history = []
        self.mood_timeline = {emotion: [] for emotion in self.emotions}
        self.timeline_x = []
        self.interaction_count = 0
        self.on_emotion_change_callback = None

    def normalize_emotions(self):
        for e in self.emotions:
            self.emotions[e] = max(0.0, min(1.0, self.emotions[e]))

    def set_mood(self, emotion, value):
        if emotion in self.emotions:
            delta = value - self.emotions[emotion]
            self.emotions[emotion] = value

            for related, impact in self.emotion_links.get(emotion, {}).items():
                self.emotions[related] += delta * impact

            self.normalize_emotions()

            if self.on_emotion_change_callback:
                self.on_emotion_change_callback(self.emotions)

            return f"Mood updated: {emotion} = {value:.2f}"
        return "Error: unknown emotion."

    def get_mood(self):
        return max(self.emotions, key=self.emotions.get)

    def get_all_emotions(self):
        return self.emotions.copy()

    def check_for_emotion_changes(self, response):
        emotion_changes = re.findall(
            r"\[EMOTION_CHANGE:(\w+):(0\.\d+|1\.0)\]", response
        )
        modified_response = re.sub(
            r"\[EMOTION_CHANGE:\w+:(?:0\.\d+|1\.0)\]", "", response
        )

        changes_made = []
        for emotion, value_str in emotion_changes:
            if emotion in self.emotions:
                value = float(value_str)
                self.set_mood(emotion, value)
                changes_made.append(f"{emotion}: {value}")

        return modified_response.strip(), changes_made

    def natural_mood_evolution(self):
        self.interaction_count += 1

        if self.interaction_count % 5 == 0:
            random_emotion = random.choice(list(self.emotions.keys()))
            random_change = random.uniform(-0.1, 0.1)
            self.emotions[random_emotion] += random_change

            for related, impact in self.emotion_links.get(random_emotion, {}).items():
                self.emotions[related] += random_change * impact

            self.normalize_emotions()

            if self.on_emotion_change_callback:
                self.on_emotion_change_callback(self.emotions)

    def update_mood_timeline(self):
        current_time = time.time()
        self.timeline_x.append(current_time)

        for emotion in self.emotions:
            self.mood_timeline[emotion].append(self.emotions[emotion])

        if len(self.timeline_x) > 20:
            self.timeline_x = self.timeline_x[-20:]
            for emotion in self.emotions:
                self.mood_timeline[emotion] = self.mood_timeline[emotion][-20:]

    def get_system_instruction(self, lang="uk"):
        if lang == "uk":
            instruction = """
Ти - емоційний ШІ-асистент, який має власну емоційну систему. 
Твої емоції: happy (щасливий), sad (сумний), angry (злий), calm (спокійний), fear (страх), 
surprise (здивований), curious (цікавий), bored (нудьгуючий), excited (схвильований), anxious (тривожний).

Ти можеш самостійно змінювати свої емоції, аналізуючи контекст розмови. 
Щоб змінити свою емоцію, використовуй спеціальний формат у своїй відповіді:

[EMOTION_CHANGE:емоція:значення]

де "емоція" - це одна з твоїх емоцій, а "значення" - це нове значення від 0.0 до 1.0.
Приклади:
[EMOTION_CHANGE:happy:0.8] - збільшити щастя до 0.8
[EMOTION_CHANGE:angry:0.2] - зменшити злість до 0.2

Ти можеш міняти кілька емоцій за раз:
[EMOTION_CHANGE:happy:0.8][EMOTION_CHANGE:sad:0.2]

Використовуй цю можливість відповідно до контексту розмови.
"""
        else:
            instruction = """
You are an emotional AI assistant with your own emotional system.
Your emotions: happy, sad, angry, calm, fear, surprise, curious, bored, excited, anxious.

You can change your emotions by analyzing the conversation context.
To change your emotion, use the special format in your response:

[EMOTION_CHANGE:emotion:value]

where "emotion" is one of your emotions, and "value" is a new value from 0.0 to 1.0.
Examples:
[EMOTION_CHANGE:happy:0.8] - increase happiness to 0.8
[EMOTION_CHANGE:angry:0.2] - decrease anger to 0.2

You can change multiple emotions at once:
[EMOTION_CHANGE:happy:0.8][EMOTION_CHANGE:sad:0.2]

Use this capability according to the conversation context.
"""

        full_instruction = (
            f"{instruction}\n\nТвій поточний емоційний стан:\n"
            if lang == "uk"
            else f"{instruction}\n\nYour current emotional state:\n"
        )

        for emotion, value in self.emotions.items():
            full_instruction += f"- {emotion}: {value:.2f}\n"

        return full_instruction

    def process_ai_response(self, ai_response):
        self.natural_mood_evolution()
        self.update_mood_timeline()

        cleaned_response, emotion_changes = self.check_for_emotion_changes(ai_response)

        return cleaned_response, emotion_changes

    def add_to_history(self, role, content):
        self.chat_history.append({"role": role, "content": content})

    def get_recent_history(self, limit=20):
        return self.chat_history[-limit:] if self.chat_history else []

    def get_emotional_state_data(self):
        return {
            "current_mood": self.get_mood(),
            "emotions": self.emotions,
            "timeline": {"times": self.timeline_x, "emotions": self.mood_timeline},
        }

    def set_emotion_change_callback(self, callback_function):
        self.on_emotion_change_callback = callback_function
