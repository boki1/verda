from string import punctuation as PUNCTUATORS
import logging
from components import Keyword, PhraseParser, DecompositionRuleNotFoundException, ReassemblyRuleNotFoundException
from memory import PhraseMemory, ContextMemory
import random


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


class VerdaEngine:
    def __init__(self):
        self.context_memory = ContextMemory()
        self.phrases = PhraseMemory()
        self.answers = []


    @staticmethod
    def clear_punctuation(sentence: str) -> str:
        logging.debug("Before de-punctuation: '{sentence}'")
        filtered = str(list(filter(lambda symbol: symbol not in PUNCTUATORS)))
        logging.debug("After de-punctuation: '{filtered}'")
        return filtered


    def get_output(self, ks: Keystack, sentence: str) -> str:
        pass


    def answer_to(self, question: str) -> str:
        sentence = self.clear_punctuation(question)
        ks = Keystack(sentence, self.phrases)

        try:
            self.answers.append(self.get_output(ks, sentence))
        except DecompositionRuleNotFoundException:
            pass
        except ReassemblyRuleNotFoundException:
            pass


    def conversation_begin(self) -> str:
        return self.phrases.hello_greeting()


    def conversation_end(self) -> str:
        return self.phrases.goodbye_greeting()
