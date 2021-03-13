import logging
from random import choice as random_choice
from random import randrange as random_randrange
from components import DecompositionRule, Keyword
from components import ReassemblyRuleNotFoundException, DecompositionRuleNotFoundException, \
    KeywordProcessingFailedException
from memory import PhraseMemory, Keystack
from reassembler import Reassembler


class Decomposer:

    def __init__(self, context_memory: list = None):
        self.possible_decompositions = []
        self.decomposed_sentence_as_list = []
        self.context_memory = context_memory

    def parse_synonym(self, sentence: str, expression_parts: list) -> bool:
        words = sentence.split(' ')
        root = expression_parts[0][1:]
        if root not in PhraseMemory.synonyms():
            raise ValueError(f"Unknown synonym root {root}")
        if words[0].lower() not in PhraseMemory.synonyms[root]:
            return False
        self.possible_decompositions.append([words[0]])
        return self.decompose(expression_parts[1:], words[1:])

    def parse_asterisk(self, sentence: str, expression_parts: list) -> bool:
        words = sentence.split(' ')
        for i in range(len(words), -1, -1):
            self.decomposed_sentence_as_list.append(words[:i])
            short_sentence = ''.join(words[i:])
            if self.decompose(short_sentence, expression_parts[1:]):
                return True
            self.decomposed_sentence_as_list.pop()
        return False

    def decompose(self, sentence: str, expression_parts: list) -> bool:
        if not sentence and not expression_parts:
            return True
        if not expression_parts:
            return False
        if not sentence and ''.join(expression_parts) != PhraseMemory.MATCH_ANYTHING:
            return False

        words = sentence.split(' ')
        first_token: str = expression_parts[0]
        first_word: str = words[0]

        if first_token == PhraseMemory.MATCH_ANYTHING:
            return self.parse_asterisk(sentence, expression_parts)
        if first_token.startswith(PhraseMemory.MATCH_SYNONYM):
            return self.parse_synonym(sentence, expression_parts)
        if first_token.lower() != first_word.lower():
            return False

        return self.decompose(sentence[1:], expression_parts[1:])

    @classmethod
    def assess_decomposition_rules(cls, available_rules: list):
        if not available_rules:
            return None
        picked = random_choice(available_rules)
        logging.info(f"'{picked}' picked over other options as decomposition rule.")
        return picked

    def apply_decomposition_rule(self, rule: DecompositionRule, sentence: str):
        self.possible_decompositions.clear()
        try:
            if self.decompose(sentence, rule.parts):
                return
        except ValueError as v_err:
            raise DecompositionRuleNotFoundException(sentence, ' '.join(rule.parts), msg=str(v_err))

        logging.debug(f'Decomposition results before post-substitution: {self.decomposed_sentence_as_list}')
        self.decomposed_sentence_as_list = [Reassembler.replace(words, PhraseMemory.post_substitutors) for words in
                                        self.decomposed_sentence_as_list]
        logging.debug(f'Decomposition results after post-substitution: {self.decomposed_sentence_as_list}')
        return self.possible_decompositions

    def process_keywords(self, keystack: Keystack, sentence: str) -> str:
        output = None
        for key in keystack:
            try:
                output = self.process_keyword(sentence, key)
            except ValueError as val_err:
                e = f"{str(val_err)} Keyword processing failed."
                logging.exception(e)
                raise KeywordProcessingFailedException(key, keystack, e)

            if output:
                logging.debug(f"Output from key: {output}")
                break

        if not output:
            if self.context_memory:
                index = random_randrange(len(self.context_memory))
                output = self.context_memory.pop(index)
                logging.debug(f"Output from memory: {output}")
            else:
                output = Reassembler.next_reassembly(PhraseMemory.keyword("xnone").decomposition_rules[0])
                logging.debug(f"Output from xnone: {output}")

        return ' '.join(output)

    def process_keyword(self, sentence: str, key: Keyword) -> str:
        for rule in key.decomposition_rules:
            self.apply_decomposition_rule(rule, sentence)
            if not self.decomposed_sentence_as_list:
                logging.debug(f'Decomposition did not match: {rule.parts}')
                raise DecompositionRuleNotFoundException(sentence, ' '.join(rule.parts))
            else:
                print(" ".join(self.decomposed_sentence_as_list[0]))
                self.possible_decompositions.append(" ".join(self.decomposed_sentence_as_list[0]))
                logging.debug(f'Decomposition successfully matched: {rule.parts} '
                              f'and gave results {self.decomposed_sentence_as_list}.')
                logging.info(f'Possible decomposition now: {self.possible_decompositions}')

            reassembly_rule = Reassembler.next_reassembly(rule)
            logging.debug(f'Using reassembly: {reassembly_rule}')

            if reassembly_rule[0] == "goto":
                goto_key = reassembly_rule[1]
                if goto_key not in PhraseMemory.keywords():
                    raise ValueError(f"Invalid `goto` keyword syntax {goto_key}")
                logging.debug(f"Goto key: {goto_key}")
                return self.process_keyword(sentence, PhraseMemory.keyword(goto_key))
            try:
                print(reassembly_rule)
                output = Reassembler.reassemble(" ".join(reassembly_rule), self.decomposed_sentence_as_list)
            except ReassemblyRuleNotFoundException:
                raise
            if rule.save_enabled:
                self.context_memory.append(output)
                logging.debug(f"Saved to memory: {output}")
                continue
            return output
        return ""
