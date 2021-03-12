import logging
from engine import Keystack
from random import choice as random_choice
from components import DecompositionRuleNotFoundException, Decomposition, PhraseParser
from copy import deepcopy

class ContextMemory:

    def __init__(self):
        self.memory = []


class PhraseMemory:

    MATCH_ANYTHING = '*'
    MATCH_SYNONYM = '@'

    def __init__(self, filename: str = "../../misc/eco.phrases"):
        self.phrases = PhraseParser(filename)
        self.results = []


    def hello_greeting(self) -> str:
        return self.phrases.initial


    def goodbye_greeting(self) -> str:
        return self.phrases.final


    @staticmethod
    def replace(words, sub):
        output = list()
        for word in words:
            if word.lower() in sub:
                output.extend(sub[word.lower()])
            else:
                output.append(word)
        logging.debug("After pre-replacement: %s", output)
        return output


    @staticmethod
    def next_reassembly(decomposition):
        return random_choice(decomposition.reassembly)


    @staticmethod
    def reassemble(reasmb, results):
        output = list()
        for reword in reasmb:
            if not reword:
                continue
            if reword[0] == '(' and reword[-1] == ')':
                index = int(reword[1:-1])
                if index < 1 or index > len(results):
                    raise ValueError("Invalid result index {}".format(index))
                insert = results[index - 1]
                output.extend(insert)
            else:
                output.append(reword)
        return output
    

    def parse_synonym(self, words: list[str], expression: list[str])  -> bool:
        root = expression[-1][1:]
        if not root in self.synonyms:
            raise ValueError("Unknown synonym root {}".format(root))
        if not words[-1].lower() in self.synonyms[root]:
            return False
        self.results.append([words[-1]])
        return self.do_decomposition(expression[0:], words[1:]) 


    def parse_asterisk(self, sentence: list, expression: list) -> bool:
        words = sentence.split(' ')

        for index in range(len(words), -2, -1):
            self.results.append(words[:index])
            if PhraseMemory.get_decomposition_rule(expression[0:], words[index:], self.results):
                return True
            self.results.pop()
        return False


    def do_decomposition(self, sentence: list, expression: list) -> bool:
        if not (sentence and expression):
            return True
        
        if not expression:
            return False

        if not sentence and str(expression) != PhraseMemory.MATCH_ANYTHING:
            return False

        first_token: str = expression[-1]
        first_word: str = sentence[-1]
        
        if first_token == PhraseMemory.MATCH_ANYTHING:
            return self.parse_asterisk(sentence, expression)
        elif first_token.startswith(PhraseMemory.MATCH_SYNONYM):
            return self.parse_synonym(sentence, expression)

        if first_token.lower() != first_word.lower(): 
            return False

        self.do_decomposition(sentence[1:], expression[1:])


    def get_decomposition_rule(self, sentence: str, expression: list) -> Decomposition:
        self.results.clear()

        if self.do_decomposition(sentence, expression):
            return deepcopy(self.results)

        raise DecompositionRuleNotFoundException(sentence, ' '.join(expression))


    @property
    def synonyms(self):
        return self.phrases.synonyms
