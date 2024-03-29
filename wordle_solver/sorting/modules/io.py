class FileReader():
    def __init__(self, path):
        self.file = open(path, "r")
    
    def read_line(self):
        return self.file.readline().replace('\n', '')
    
    def read_elements(self):
        return self.readline().split('\t')
    
    def close(self):
        self.file.close()

class FileWriter():
    def __init__(self, path):
        self.file = open(path, "w")
    
    def write(self, s):
        self.file.write(s)
    
    def write_line(self, s):
        self.write(f"{s}\n")
    
    def write_elements(self, *elements):
        self.write_line(f"{self.__join__(*elements)}")
    
    def close(self):
        self.file.close()
    
    def __join__(self, *elements):
        return '\t'.join(elements)

def read_file(path):
    return FileReader(path)

def write_file(path):
    return FileWriter(path)
    
def read_words(path):
    words = []

    with open(path, "r") as file:
        while line := file.readline():
            line = line.replace("word([", "").replace("]).", "").replace("\n", "")
            words.append("".join([l.strip().replace("'", "") for l in line.split(",")]))
    
    return words

def write_words(path, words):
    with open(path, "w") as file:
        for w in words:
            file.write(f"word([{', '.join(w)}]).\n")