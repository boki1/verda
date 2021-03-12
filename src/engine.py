from logging import Logger

class ContextMemory:

    def __init__(self):
        self.memory = []


class PhraseMemory:

    def hello_greeting(self) -> str:
        return ""

    def goodbye_greeting(self) -> str:
        return ""


class VerdaEngine:

    def __init__(self):
        self.context_memory = ContextMemory()
        self.phrases = PhraseMemory()

    def answer_to(self, qustion: str) -> str:
        pass

    def conversation_begin(self) -> str:
        return self.phrases.hello_greeting()

    def conversation_end(self) -> str:
        return self.phrases.goodbye_greeting()