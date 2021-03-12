class VerdaException(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def why(self) -> str:
        return self.msg

class DecompositionRuleNotFoundException(VerdaException):

    def __init__(self, sentence: str, expression: str):
        super().__init__(f"Couldn't match '{expression}' to '{sentence}'.")


class ReassemblyRuleNotFoundException(VerdaException):

    def __init__(self):
        super().__init__("<reassembly failed>")


class Keyword:
    def __init__(self, word=None, weight=None, decomposition=None):
        self.word = word
        self.weight = weight
        self.decomposition_rules = decomposition

    def __le__(self, other):
        return self.weight >= other.weight


class Decomposition:
    def __init__(self, parts, save_enabled, reassembly_rules):
        self.parts = parts
        self.save_enable = save_enabled
        self.reassembly = reassembly_rules


class PhraseParser:

    def __init__(self, filename: str = None):
        self.filename = filename
        self.initial: str = ""
        self.final: str = ""
        self.quits = []
        self.pres = []
        self.posts = []
        self.synonyms = []
        self.keys = {}

        if filename is not None:
            self.get_from_file(filename)
            

    def __str__(self):
        return f"Initials:  + {self.initial} + \
Finals: {self.final}\
Quits: {self.quits} \
Pres: {self.pres}\
Posts: {self.posts}\
Synonyms: {self.synonyms}\
Keys: {self.keys}"

    def get_from_file(self, path):
        key = None
        decomposition = None
        with open(path) as file:
            for line in file:
                if not line.strip():
                    continue
                tag, content = [part.strip() for part in line.split(':')]

                if tag == 'initial':
                    self.initial = content
                elif tag == 'final':
                    self.final = content
                elif tag == 'quit':
                    self.quits.append(tuple(content.split(" ")))
                elif tag == 'pre':
                    self.pres.append(tuple(content.split(" ")))
                elif tag == 'post':
                    self.posts.append(tuple(content.split(" ")))
                elif tag == 'synon':
                    self.synonyms.append(tuple(content.split(" ")))
                elif tag == 'key':
                    words = content.split(" ")
                    for word in words:
                        word.lower()
                    word = words[0]
                    weight = int(words[1]) if len(words) > 1 else 1
                    key = Keyword(word, weight, [])
                    self.keys[word] = key
                elif tag == 'decomp':
                    words = content.split(" ")
                    for word in words:
                        word.lower()
                    word = words[0]
                    save = False
                    if word == '$':
                        save = True
                        words = words[1:]
                    decomposition = Decomposition(words, save, [])
                    key.decomposition_rules.append(decomposition)
                elif tag == 'reasmb':
                    words = content.split(" ")
                    decomposition.reassembly.append(words)

    def at_key(self, keyword: str) -> Keyword:
        return self.keys[keyword]