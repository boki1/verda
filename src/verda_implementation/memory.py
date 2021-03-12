import logging
from engine import Keystack
from random import choice as random_choice
from random import randrange as random_randrange
from components import DecompositionRuleNotFoundException, Decomposition, PhraseParser, Keyword, ReassemblyRuleNotFoundException
from copy import deepcopy

class ContextMemory:

    def __init__(self):
        self.memory = []


class PhraseMemory:

    MATCH_ANYTHING = '*'
    MATCH_SYNONYM = '@'

    def __init__(self, filename: str = "../../misc/eco.phrases"):
        self.phrases = PhraseParser(filename)
        self.context_memory = ContextMemory()
        self.possible_decompositions = []

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
        logging.debug("After pre-replacement: {output}")
        return output

    @staticmethod
    def next_reassembly(decomposition):
        return random_choice(decomposition.reassembly)

    @staticmethod
    def reassemble(reassembly_rule: list, results):
        reassembly_rule_words = reassembly_rule.split(' ')
        output = list()
        for word in reassembly_rule_words:
            if not word:
                continue
            if word[0] == '(' and word[-1] == ')':
                index = int(word[1:-1])
                if index < 1 or index > len(results):
                    raise ReassemblyRuleNotFoundException(expression=reassembly_rule, decomposed=results)
                insert = results[index - 1]
                output.extend(insert)
            else:
                output.append(word)
        return output

    def parse_synonym(self, words: list[str], expression: list[str])  -> bool:
        root = expression[-1][1:]
        if not root in self.synonyms:
            raise ValueError("Unknown synonym root {}".format(root))
        if not words[-1].lower() in self.synonyms[root]:
            return False
        self.possible_decompositions.append([words[-1]])
        return self.decompose(expression[0:], words[1:]) 


    def parse_asterisk(self, sentence: list, expression: list) -> bool:
        words = sentence.split(' ')

        for index in range(len(words), -1, -1):
            self.possible_decompositions.append(words[:index])
            if PhraseMemory.get_decomposition_rules(expression[0:], words[index:], self.possible_decompositions):
                return True
            self.possible_decompositions.pop()
        return False

    def decompose(self, sentence: list, expression: list) -> bool:
        if not (sentence and expression):
            return

        if not expression:
            return False

        if not sentence and str(expression) != PhraseMemory.MATCH_ANYTHING:
            return False

        first_token: str = expression[0]
        first_word: str = sentence[0]

        if first_token == PhraseMemory.MATCH_ANYTHING:
            return self.parse_asterisk(sentence, expression)

        if first_token.startswith(PhraseMemory.MATCH_SYNONYM):
            return self.parse_synonym(sentence, expression)

        if first_token.lower() != first_word.lower():
            return False

        self.decompose(sentence[1:], expression[1:])

    def get_decomposition_rules(self, sentence: str, expression: list) -> list:
        self.possible_decompositions.clear()

        if self.decompose(sentence, expression):
            return deepcopy(self.possible_decompositions)

        raise DecompositionRuleNotFoundException(sentence, ' '.join(expression))
    
    def get_output(self, keystack, keys):
        output = None
        for key in keys:
            output = self.match_key(keystack, key)
            if output:
                logging.debug("Output from key: %s", output)
                break

        if not output:
            if self.context_memory:
                index = random_randrange(len(self.memcontext))
                output = self.context_memory.memory.pop(index)
                logging.debug("Output from memory: {output}")
            else:
                output = self.next_reassembly(self.keyword("xnone").decomposition_rules[0])
                logging.debug("Output from xnone: {output}")

        return " ".join(output)

    def match_decomposition_rule(self, keyword: Keyword, sentence: str):
        words = sentence.split(' ')

        for rule in keyword.decomposition_rules:
            results = self.get_decomposition_rules(rule.parts, words)
            if results is None:
                logging.debug('Decomposition did not match: {rule.parts}')
                continue
            logging.debug('Decomposition matched: {rule.parts} and gave results {results}.')
            results = [self.replace(words, self.post_substitors) for words in results]
            logging.debug('Decomposition results after post-substitution: {results}')
            return results

    def match_key(self, words: list, key: Keyword):
        for rule in key.decomposition_rules:
            decomposed = self.match_decomposition_rule(keyword=key, sentence=' '.join(words))
            reassembly_rule = self.next_reassembly(rule)
            logging.debug('Using reassembly: {reassembly_rule}')

            if reassembly_rule[0] == "goto":
                goto_key = reassembly_rule[1]
                if not goto_key in self.keywords:
                    raise ValueError("Invalid `goto` keyword syntax {}".format(goto_key))
                logging.debug("Goto key: %s", goto_key)
                return self.match_key(words, self.keyword(goto_key))

            try:
                output = self.reassemble(reassembly_rule, decomposed)
            except ReassemblyRuleNotFoundException:
                return None

            if rule.save_enable:
                self.context_memory.memory.append(output)
                logging.debug("Saved to memory: %s", output)
                continue
            return output
        return None

    @property
    def post_substitors(self):
        return self.phrases.posts

    @property
    def pre_substitutors(self):
        return self.phrases.pres

    @property
    def synonyms(self):
        return self.phrases.synonyms

    @property
    def keywords(self):
        return self.phrases.keys

    def keyword(self, kw: str) -> Keyword:
        return self.keywords[kw]

    @property
    def memcontext(self) -> list:
        if self.context_memory:
            return self.context_memory.memory


