from pathlib import Path
from os import path as pathos
from os import mkdir


class DataFile:
    def __init__(self, name, headers, items):
        self.headers = headers
        self.items = items
        self.name = name


def ExtractData(filepath):
    print("Extract data from ", filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        Lines = f.readlines()
        items = []
        for line in Lines:
            if line[0] == '#':
                headers = line[2:-2].split("^")
            else:
                items.append(line[:-2].split("^"))
        Data = DataFile(filepath[5:-4], headers, items)
        return Data


def GenerateMdFiles(directory, outdirectory):
    pathlist = Path(directory).rglob('*.txt')
    for path in pathlist:
        # because path is object not string
        path_in_str = str(path)
        data = ExtractData(path_in_str)

        md_data = ""

        # Title

        md_data += "# " + data.name + "\n"

        # table headers
        for header in data.headers:
            md_data += "| " + header
        md_data += "|\n"

        # separator
        for header in data.headers:
            md_data += "| - "
        md_data += "|\n"

        for item in data.items:
            for value in item:
                md_data += "| " + value
            md_data += "|\n"
        print(md_data)
        if pathos.isdir(outdirectory) is not True:
            mkdir(outdirectory)
        with open("md_data/" + data.name + '.md', 'a', encoding='utf-8') as f:
            f.write(md_data)
