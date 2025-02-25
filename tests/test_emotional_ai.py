from emotional_ai import EmotionalBot


def test_mood_setting():
    bot = EmotionalBot()
    bot.set_mood("happy", 0.9)
    assert bot.get_mood() == "happy"
