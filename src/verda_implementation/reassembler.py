import logging
from components import ReassemblyRuleNotFoundException
from random import choice as random_choice


class Reassembler:
    @staticmethod
    def replace(words, subscribtors):
        output = list()
        for word in words:
            if word in subscribtors.keys():
                output.append(subscribtors[word])
            else:
                output.append(word)
        logging.debug(f"After replacement: {output}")
        return output

    @staticmethod
    def next_reassembly(decomposition) -> str:
        return random_choice(decomposition.reassembly_rules)

    @staticmethod
    def reassemble(reassembly_rule: str, words: list):
        reassembly_rule_words = reassembly_rule.split(' ')
        output = list()
        for word in reassembly_rule_words:
            if not word:
                continue
            if word[0] == '(' and word[-1] == ')':
                index = int(word[1:-1])
                if index < 1 or index > len(words):
                    raise ReassemblyRuleNotFoundException(expression=reassembly_rule, decomposed=" ".join(words))
                insert = words[index - 1]
                output.extend(insert)
            else:
                output.append(word)
        return output

