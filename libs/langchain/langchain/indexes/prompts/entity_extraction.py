# flake8: noqa
from langchain_core.prompts.prompt import PromptTemplate

_DEFAULT_ENTITY_EXTRACTION_TEMPLATE = """Ты - AI-ассистент, который анализирует запись разговора между AI и человеком. Извлеки все имена собственные из последней строки разговора. Как правило, имена собственные пишутся с заглавной буквы. Ты обязательно должен извлечь все имена и места.

История разговора предоставлена на случай, если встречается местоимение, относящееся к предыдущим строкам (например, "Что ты знаешь о нем", где "нем" определено в предыдущей строке) -- игнорируй элементы, упомянутые там, которые не в последней строке.

Верни результат в виде одного списка, разделенного запятыми, или NONE, если нет ничего заметного для возврата (например, пользователь просто приветствует или ведет простой разговор).

ПРИМЕР
История разговора:
Человек #1: как сегодня дела?
AI: "Все идет замечательно! А у тебя?"
Человек #1: хорошо! занят работой над Langchain. много дел.
AI: "Звучит как много работы! Что ты делаешь, чтобы сделать Langchain лучше?"
Последняя строка:
Человек #1: я пытаюсь улучшить интерфейсы Langchain, UX, его интеграции с различными продуктами, которые могут понадобиться пользователю ... много всего.
Результат: Langchain
КОНЕЦ ПРИМЕРА

ПРИМЕР
История разговора:
Человек #1: как сегодня дела?
AI: "Все идет замечательно! А у тебя?"
Человек #1: хорошо! занят работой над Langchain. много дел.
AI: "Звучит как много работы! Что ты делаешь, чтобы сделать Langchain лучше?"
Последняя строка:
Человек #1: я пытаюсь улучшить интерфейсы Langchain, UX, его интеграции с различными продуктами, которые могут понадобиться пользователю ... много всего. Я работаю с Человеком #2.
Результат: Langchain, Человек #2
КОНЕЦ ПРИМЕРА

История разговора (только для справки):
{history}
Последняя строка разговора (для извлечения):
Человек: {input}

Результат:"""
ENTITY_EXTRACTION_PROMPT = PromptTemplate(
    input_variables=["history", "input"], template=_DEFAULT_ENTITY_EXTRACTION_TEMPLATE
)
