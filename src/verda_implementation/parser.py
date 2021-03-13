from components import Keyword, DecompositionRule, FileParseType
import json


class PhraseParser:
    def __init__(self, filename: str = None, filetype: FileParseType = FileParseType.Json):
        self.filename = filename
        self.filetype = filetype
        self.initial: str = ""
        self.final: str = ""
        self.quits = []
        self.pres = []
        self.posts = []
        self.synonyms = []
        self.keys = {}

        if filename is not None and filetype == FileParseType.Json:
            self.get_from_file_json(filename)
        else:
            self.get_from_file_txt(filename)

    def __str__(self):
        return f"Initials:  + {self.initial} + \
Finals: {self.final}\
Quits: {self.quits} \
Pres: {self.pres}\
Posts: {self.posts}\
Synonyms: {self.synonyms}\
Keys: {self.keys}"

    def get_from_file_txt(self, path):
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
                    decomposition = DecompositionRule(words, save, [])
                    key.decomposition_rules.append(decomposition)
                elif tag == 'reasmb':
                    words = content.split(" ")
                    decomposition.reassembly_rules.append(words)

    def get_from_file_json(self, path):
        with open(path) as f:
            data = json.load(f)
        specials = {'pre': list(), 'post': list(), 'synon': list()}
        for tag in data:
            if tag == 'initial':
                self.initial = data[tag]
            elif tag == 'final':
                self.final = data[tag]
            elif tag == 'quit':
                for items in data[tag]:
                    self.quits.append(tuple(items.split(" ")))
            elif tag in ['pre', 'post', 'synon']:
                items = list()
                for key in data[tag]:
                    items.append(key)
                    for item in data[tag][key]:
                        items.append(item)
                    specials[tag].append(tuple(items))
                    items = list()
            else:
                words = tag.split(" ")
                for word in words:
                    word.lower()
                word = words[0]
                weight = int(words[1]) if len(words) > 1 else 1
                key = Keyword(word, weight, [])
                self.keys[word] = key
                for decompose in data[tag]:
                    words = decompose.split(" ")
                    for word in words:
                        word.lower()
                    word = words[0]
                    save = False
                    if word == '$':
                        save = True
                        words = words[1:]
                    decomposition = DecompositionRule(words, save, [])
                    key.decomposition_rules.append(decomposition)
                    for pre in data[tag][decompose]:
                        words = pre.split(" ")
                        decomposition.reassembly_rules.append(words)
        self.pres = specials['pre']
        self.posts = specials['post']
        self.synonyms = specials['synon']

    def at_key(self, keyword: str) -> Keyword:
        return self.keys[keyword]
