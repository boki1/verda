import ast


class Converter:
    def __init__(self, filename: str = None):
        self._filename = filename
        self._quits = list()
        self._specials = {"pre": list(), "post": list(), "synon": list()}
        self._keys = list()
        self._decomposition = dict()
        self._reassembly = dict()
        if filename is not None:
            self.get_from_file(filename)

    def get_from_file(self, path):
        with open(path) as file:
            with open("echo_phrases.json", "w+") as cr_file:
                cr_file.write("{\n")
                key_count = 0
                decomposition_count = 0
                reassembly = list()
                decomposition = list()
                for line in file:
                    if not line.strip():
                        continue
                    tag, content = [part.strip() for part in line.split(':')]
                    if tag == 'initial':
                        cr_file.write(f'"{tag}": "{content}",\n')
                    elif tag == 'final':
                        cr_file.write(f'"{tag}": "{content}",\n')
                    elif tag == 'quit':
                        self._quits.append(content)
                    elif tag == 'pre':
                        self._specials["pre"].append(content.split(" "))
                    elif tag == 'post':
                        self._specials["post"].append(content.split(" "))
                    elif tag == 'synon':
                        self._specials["synon"].append(content.split(" "))
                    elif tag == 'key':
                        key_count += 1
                        decomposition = list()
                        self._keys.append(content)
                    elif tag == 'decomp':
                        decomposition_count += 1
                        reassembly = list()
                        decomposition.append(content)
                        self._decomposition[key_count] = decomposition
                    elif tag == 'reasmb':
                        reassembly.append(content)
                        self._reassembly[decomposition_count] = reassembly
                cr_file.write('"quit": [')
                for quits in self._quits:
                    if self._quits.index(quits) != (len(self._quits) - 1):
                        cr_file.write(f'"{quits}",')
                    else:
                        cr_file.write('"' + quits + '"],\n')

                for special in self._specials:
                    cr_file.write('"' + special + '": {')
                    for lists in self._specials[special]:
                        for word in lists:
                            if self._specials[special][self._specials[special].index(lists)].index(word) ==\
                                    (len(self._specials[special][self._specials[special].index(lists)]) - 1):
                                if self._specials[special].index(lists) == (len(self._specials[special]) - 1):
                                    if len(self._specials[special][self._specials[special].index(lists)]) == 2:
                                        cr_file.write(f'["{word}"]')
                                    else:
                                        cr_file.write(f'"{word}"]')
                                elif len(self._specials[special][self._specials[special].index(lists)]) == 2:
                                    cr_file.write(f'["{word}"],')
                                else:
                                    cr_file.write(f'"{word}"],')
                            elif self._specials[special][self._specials[special].index(lists)].index(word) == 0:
                                cr_file.write(f'"{word}":')
                            elif self._specials[special][self._specials[special].index(lists)].index(word) == 1:
                                cr_file.write(f'["{word}",')
                            else:
                                cr_file.write(f'"{word}",')
                    cr_file.write("},\n")
                index_key = 0
                index_decomposition = 0
                for key in self._keys:
                    cr_file.write('"' + key + '":\n{\n')
                    index_key += 1
                    for word in self._decomposition[index_key]:
                        cr_file.write('    "' + word + '": [')
                        index_decomposition += 1
                        for reassembly in self._reassembly[index_decomposition]:
                            if self._reassembly[index_decomposition].index(reassembly) ==\
                                    (len(self._reassembly[index_decomposition]) - 1):
                                if self._decomposition[index_key].index(word) == \
                                        (len(self._decomposition[index_key]) - 1):
                                    cr_file.write(f'"{reassembly}"]\n')
                                else:
                                    cr_file.write(f'"{reassembly}"],\n')
                            else:
                                cr_file.write(f'"{reassembly}", ')
                    if self._keys.index(key) == (len(self._keys) - 1):
                        cr_file.write('}\n')
                    else:
                        cr_file.write('},\n')
                cr_file.write('}\n')


if __name__ == '__main__':
    converter = Converter("eco.phrases")