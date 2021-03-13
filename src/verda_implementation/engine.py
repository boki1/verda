from string import punctuation as PUNCTUATORS
import logging
from components import DecompositionRuleNotFoundException, ReassemblyRuleNotFoundException, KeywordProcessingFailedException
from memory import PhraseMemory, Keystack
from enum import IntEnum
from copy import copy as shallow_copy
from decomposer import Decomposer
from reassembler import Reassembler


class Globals(IntEnum):
    HELLO_IDX = 0
    GOODBYE_IDX = 1


class VerdaEngine:

    def __init__(self):
        self.phrasing_memory = PhraseMemory.instance()

        self.context_memory = []
        self.decomposer = Decomposer(self.context_memory)
        self.reassembler = Reassembler()

        # self.answers = []
        self.done_greetings = [False, False]

    @staticmethod
    def clear_punctuation(sentence: str) -> str:
        logging.debug("Before de-punctuation: '{sentence}'")
        filtered = ''.join(list(filter(lambda symbol: symbol not in PUNCTUATORS, sentence)))
        logging.debug("After de-punctuation: '{filtered}'")
        return filtered

    def loop(self):
        if not self.done_greetings[Globals.HELLO_IDX]:
            self.conversation_begin()

        while True:
            inp = input('> ')
            if inp in PhraseMemory.goodbye_messages():
                self.conversation_end()
                break

            answer = self.answer_to(inp)
            print(answer)

    def answer_to(self, question: str) -> str:
        sentence = self.clear_punctuation(question)
        sentence = sentence.lower()
        keywords = Keystack(sentence, shallow_copy(self.phrasing_memory))
        keywords = keywords.prioritize()

        response = ""

        try:
            response: str = self.decomposer.process_keywords(keywords, sentence)
        except ReassemblyRuleNotFoundException as r_err: 
            logging.exception(r_err.msg)
        except DecompositionRuleNotFoundException as d_err:
            logging.exception(d_err.msg)
        except KeywordProcessingFailedException as k_err:
            logging.exception(k_err.msg)

        return response

    def conversation_begin(self):
        print(PhraseMemory.hello_greeting())
        self.done_greetings[Globals.HELLO_IDX] = True

    def conversation_end(self):
        print(PhraseMemory.goodbye_greeting())
        self.done_greetings[Globals.GOODBYE_IDX] = True
