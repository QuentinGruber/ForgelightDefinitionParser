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

        # md_data += "# " + data.name + "\n"

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
        if pathos.isdir(outdirectory) is not True:
            mkdir(outdirectory)
        with open(outdirectory+"/" + data.name + '.md', 'a', encoding='utf-8') as f:
            f.write(md_data)
    GenerateIndexFile(outdirectory)


def GenerateIndexFile(dataDirectory):
    if pathos.isdir(dataDirectory) is not True:
        print("data directory doesn't exist")
        exit(1)
    pathlist = Path(dataDirectory).rglob('*.md')
    print("Creating index file")
    indexFile = ""
    for path in pathlist:
        path_in_str = str(path)
        with open(path_in_str, 'r', encoding='utf-8') as f:
            indexFile += "* ["+path_in_str[len(dataDirectory)+1:-3] + \
                "]"+"("+path_in_str+")" + "\n"

    with open(dataDirectory+".md", 'w+', encoding='utf-8') as f:
        f.write(indexFile)
