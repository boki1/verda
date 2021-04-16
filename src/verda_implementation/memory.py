from .parser import PhraseParser
from .components import DecompositionRule, Keyword
import logging


class PhraseMemory:

    __instance = None
    phrases = None

    MATCH_ANYTHING = '*'
    MATCH_SYNONYM = '@'

    @classmethod
    def instance(cls, filename: str = "misc/eco.phrases"):
        if PhraseMemory.__instance:
            return PhraseMemory.__instance
        cls.phrases = PhraseParser(filename)
        return cls.phrases

    @classmethod
    def hello_greeting(cls) -> str:
        if cls.phrases:
            return cls.phrases.initial

    @classmethod
    def goodbye_greeting(cls) -> str:
        if cls.phrases:
            return cls.phrases.final

    @classmethod
    def post_substitutors(cls):
        if cls.phrases:
            return cls.phrases.posts

    @classmethod
    def pre_substitutors(cls):
        if cls.phrases:
            return cls.phrases.pres

    @classmethod
    def synonyms(cls):
        if cls.phrases:
            return {tup[0]: tup[0:] for tup in cls.phrases.synonyms if len(tup) >= 2}

    @classmethod
    def keywords(cls):
        if cls.phrases:
            return cls.phrases.keys

    @classmethod
    def goodbye_messages(cls):
        return cls.phrases.quits

    @classmethod
    def keyword(cls, kw: str) -> Keyword:
        if cls.phrases:
            return cls.keywords()[kw]


class Keystack(list):

    def __init__(self, sentence: str, phrasing_memory=None):
        super().__init__()
        for word in sentence.split(' '):
            try:
                key_obj = PhraseMemory.phrases.at_key(word)
                self.append(key_obj)
            except KeyError:
                logging.info(f"Word '{word}' is not matched to any of the keywords.")

    def prioritize(self):
        return sorted(self)
