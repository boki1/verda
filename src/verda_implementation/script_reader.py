class Keyword:
    def __init__(self, word, weight, decomposition):
        self.word = word
        self.weight = weight
        self.decomposition = decomposition


class Decomposition:
    def __init__(self, parts, save_enabled, reassembly_rules):
        self.parts = parts
        self.save_enable = save_enabled
        self.reassembly = reassembly_rules


class PhraseParser:
    def __init__(self):
        self.initials = []
        self.finals = []
        self.quits = []
        self.pres = []
        self.posts = []
        self.synonyms = []
        self.keys = {}
        self.memory = []


    def __str__(self):
        return f"Initials:  + {self.initials} + \
Finals: {self.finals}\
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
                    self.initials.append(content)
                elif tag == 'final':
                    self.finals.append(content)
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
                    key.decomposition.append(decomposition)
                elif tag == 'reasmb':
                    words = content.split(" ")
                    decomposition.reassembly.append(words)
