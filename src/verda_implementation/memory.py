from script_reader import PhraseParser
import logging
from engine import Keystack
from random import choice as random_choice

class ContextMemory:

    def __init__(self):
        self.memory = []


class PhraseMemory:

    def __init__(self, filename: str = "../../misc/eco.phrases"):
        self.phrases = PhraseParser(filename)


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

    
    @staticmethod
    def get_decomposition_rule(ks: Keystack):
        pass

