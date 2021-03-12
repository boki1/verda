from string import punctuation as PUNCTUATORS
import logging
from components import Keyword, PhraseParser, DecompositionRuleNotFoundException, ReassemblyRuleNotFoundException
from memory import PhraseMemory, ContextMemory
import random
from enum import IntEnum


class Keystack(list):
    # TODO: Maybe change `phrases` because we dont want to pass such big object with copy
    def __init__(self, sentence: str, phrasing_memory: PhraseMemory):
        super.__init__()
        for word in sentence.split(' '):
            try:
                key_obj = phrasing_memory.phrases.by_key(word)
                self.append(key_obj)
            except KeyError:
                logging.info("Word '{word}' is not matched to any of the keywords.")

    def prioratize(self):
        return sorted(self)


class Globals(IntEnum):
    HELLO_IDX = 0
    GOODBYE_IDX = 1
    END_CONVERSATION = 0
    RESULT_CONVERSATION = 1


class VerdaEngine:

    def __init__(self):
        self.context_memory = ContextMemory()
        self.phrases = PhraseMemory()
        self.answers = []
        self.done_greetings = [False, False]

    @staticmethod
    def clear_punctuation(sentence: str) -> str:
        logging.debug("Before de-punctuation: '{sentence}'")
        filtered = str(list(filter(lambda symbol: symbol not in PUNCTUATORS)))
        logging.debug("After de-punctuation: '{filtered}'")
        return filtered

    def loop(self):
        if self.done_greetings[Globals.HELLO_IDX]:
            self.conversation_begin()

        while True:
            inp = input('> ')
            res = self.answer_to(inp)
            if res[Globals.END_CONVERSATION]:
                self.conversation_end()
                return
            print(res[Globals.RESULT_CONVERSATION])

    def answer_to(self, question: str) -> (bool, str):
        sentence = self.clear_punctuation(question)
        _keystack = Keystack(sentence, self.phrases)

        return False, ''

    def conversation_begin(self) -> str:
        self.phrases.hello_greeting()
        self.done_greetings[Globals.HELLO_IDX] = True


    def conversation_end(self) -> str:
        self.phrases.goodbye_greeting()
        self.done_greetings[Globals.GOODBYE_IDX] = True

