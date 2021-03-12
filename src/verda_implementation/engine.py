from string import punctuation as PUNCTUATORS
from collections import namedtuple
import logging
from script_reader import Keyword 



class ContextMemory:

    def __init__(self):
        self.memory = []


class PhraseMemory:

    def try_by_key(self, keyword: str) -> Keyword:
        return Keyword() 

    def hello_greeting(self) -> str:
        return ""

    def goodbye_greeting(self) -> str:
        return ""


class Keystack(list):

    # TODO: Maybe change `phrases` because we dont want to pass such big object with copy
    def __init__(self, sentence: str, phrases: PhraseMemory):
        for word in sentence.split(' '):
            try:
                key_obj = phrases.try_by_key(word)
                self.append(key_obj)
            except KeyError:
                logging.info("Word '{word}' is not matched to any of the keywords.")


    def prioratize(self):
        return sorted(self)


class VerdaEngine:

    def __init__(self):
        self.context_memory = ContextMemory()
        self.phrases = PhraseMemory()


    def clear_punctuation(self, sentence: str) -> str:
        logging.debug("Before de-punctuation: '{sentence}'")
        filtered = str(list(filter(lambda symbol: symbol not in PUNCTUATORS)))        
        logging.debug("After de-punctuation: '{filtered}'")
        return filtered


    def answer_to(self, qustion: str) -> str:
        pass


    def conversation_begin(self) -> str:
        return self.phrases.hello_greeting()


    def conversation_end(self) -> str:
        return self.phrases.goodbye_greeting()