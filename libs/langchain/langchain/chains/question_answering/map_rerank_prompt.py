# flake8: noqa
from langchain.output_parsers.regex import RegexParser
from langchain_core.prompts import PromptTemplate

output_parser = RegexParser(
    regex=r"(.*?)\nScore: (\d*)",
    output_keys=["answer", "score"],
)

prompt_template = """Используй следующие части контекста, чтобы ответить на вопрос в конце. Если ты не знаешь ответа, просто скажи, что не знаешь, не пытайся придумать ответ.

В дополнение к ответу, также верни оценку того, насколько полно он отвечает на вопрос пользователя. Это должно быть в следующем формате:

Question: [вопрос здесь]
Полезный ответ: [ответ здесь]
Оценка: [оценка от 0 до 100]

Как определить оценку:
- Чем выше, тем лучше ответ
- Лучше отвечает полностью на заданный вопрос, с достаточным уровнем детализации
- Если ты не знаешь ответа на основе контекста, то это должна быть оценка 0
- Не будь чересчур уверенным!

Пример #1

Контекст:
---------
Яблоки красные
---------
Вопрос: какого цвета яблоки?
Полезный ответ: красные
Оценка: 100

Пример #2

Контекст:
---------
была ночь, и свидетель забыл свои очки. он не был уверен, была ли это спортивная машина или внедорожник
---------
Вопрос: какого типа была машина?
Полезный ответ: спортивная машина или внедорожник
Оценка: 60

Пример #3

Контекст:
---------
Груши бывают красные или оранжевые
---------
Question: какого цвета яблоки?
Полезный ответ: Этот документ не отвечает на вопрос
Оценка: 0

Начнем!

Контекст:
---------
{context}
---------
Question: {question}
Полезный ответ:"""
PROMPT = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"],
    output_parser=output_parser,
)
