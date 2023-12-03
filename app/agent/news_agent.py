from langchain.prompts import load_prompt
from langchain.chat_models import GigaChat
from langchain.schema import SystemMessage

class NewsAgent:
    def __init__(self, auditory_name: str):
        self.llm = GigaChat(
            verbose=True,
            temperature=1,
            model="GigaChat:latest",
            credentials="MjhlMGRkYzYtNTdmNC00N2FmLTk5MmMtNmI0N2EzODJhOTM3OjgzYzZmZDQ3LWU5N2MtNDA3Ni1hOGI4LThhN2Q4ZmNiZWU2Mw==",
            scope="GIGACHAT_API_PERS",
            timeout=300,
        )
        self.auditory_name = auditory_name

    def run(self, news: str):
        is_stop: bool = False
        steps = self.generate_plan()

        step_prompt = load_prompt('prompts/step.yaml')

        previous_step = f'''
{{
    "data": "{news}",
    "stop": "false",
    "args": {{
        "target": "{self.auditory_name}"
    }}
}}
        '''
        for step in steps:
            if not step:
                continue
            step_content = step_prompt.format(plan=step, 
                                              previous_step=previous_step)
            previous_step = self.llm([SystemMessage(content=step_content)]).content

        return previous_step


    def generate_plan(self):
        plan_prompt = load_prompt('prompts/plan.yaml')
        plan = plan_prompt.format(auditory_name=self.auditory_name)

        steps = plan.split('\n')

        return steps
