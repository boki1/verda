from string import punctuation as PUNCTUATORS
import logging
from script_reader import Keyword
import random
from src.verda_implementation.script_reader import PhraseParser


class ContextMemory:
    def __init__(self):
        self.memory = []


class PhraseMemory:
    def __init__(self):
        self.phrases = PhraseParser()
        self.phrases.get_from_file("../../misc/eco.phrases")
        self.context_memory = ContextMemory()

    def get_output(self, keystack, keys):
        output = None
        for key in keys:
            output = self.match_key(keystack, key)
            if output:
                logging.debug("Output from key: %s", output)
                break
        if not output:
            if self.context_memory:
                index = random.randrange(len(self.context_memory.memory))
                output = self.context_memory.memory.pop(index)
                logging.debug("Output from memory: %s", output)
            else:
                output = self.next_reassembly(self.phrases.keys["xnone"].decomposition[0])
                logging.debug("Output from xnone: %s", output)

        return " ".join(output)

    def match_key(self, keystack, key):
        for decomposition in key.decomposition:
            results = [self.replace(keystack, self.phrases.posts)]
            logging.debug('Decomposition results after posts: %s', results)

            reassembly = self.next_reassembly(decomposition)
            logging.debug('Using reassembly: %s', reassembly)
            if reassembly[0] == "goto":
                goto_key = reassembly[1]
                if not goto_key in self.phrases.keys:
                    raise ValueError("Invalid goto key {}".format(goto_key))
                logging.debug("Goto key: %s", goto_key)
                return self.match_key(keystack, self.phrases.keys[goto_key])
            output = self.reassemble(reassembly, results)
            if decomposition.save_enable:
                self.context_memory.memory.append(output)
                logging.debug("Saved to memory: %s", output)
                continue
            return output
        return None

    def hello_greeting(self) -> str:
        return ""

    def goodbye_greeting(self) -> str:
        return ""

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
        return random.choice(decomposition.reassembly)

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

    def match_decomposition_rule(self, parts, words):
        pass


class Keystack(list):
    # TODO: Maybe change `phrases` because we dont want to pass such big object with copy
    def __init__(self, sentence: str, phrases: PhraseMemory):
        super().__init__()
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

    def answer_to(self, question: str) -> str:
        pass

    def conversation_begin(self) -> str:
        return self.phrases.hello_greeting()

    def conversation_end(self) -> str:
        return self.phrases.goodbye_greeting()
