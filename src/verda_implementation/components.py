from enum import IntEnum


class VerdaException(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def why(self) -> str:
        return self.msg


class DecompositionRuleNotFoundException(VerdaException):

    def __init__(self, sentence: str, expression: str, msg: str = None):
        self.sentence = sentence
        self.expression = expression
        if not msg:
            msg = f"Couldn't match '{self.expression}' to '{self.sentence}'."
        super().__init__(msg)


class KeywordProcessingFailedException(VerdaException):
    
    def __init__(self, keyword: str, keywords: list, rationale: str, msg: str = None):
        self.keywords = keywords
        self.keyword = keyword 
        self.rationale = rationale
        if not msg:
            msg = f"Failed processing keyword '{self.keyword}' from '{self.keywords}' keyword stack because: '{self.rationale}'."
        super().__init__(msg)


class ReassemblyRuleNotFoundException(VerdaException):

    def __init__(self, expression: str, decomposed: str, msg: str = None):
        self.expression = expression
        self.decomposed = decomposed
        if not msg:
            msg = "Couldn't reassembly '{decomposed}' by '{expression}')"
        super().__init__(msg)


class Keyword:
    def __init__(self, word=None, weight=None, decomposition=None):
        self.word = word
        self.weight = weight
        self.decomposition_rules = decomposition

    def __lt__(self, other):
        return self.weight > other.weight


class DecompositionRule:
    def __init__(self, parts, save_enabled, reassembly_rules):
        self.parts = parts
        self.save_enabled = save_enabled
        self.reassembly_rules = reassembly_rules


class FileParseType(IntEnum):
    Json = 0
    Txt = 1

