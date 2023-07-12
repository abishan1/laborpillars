import os, sys, string

class DataParser:

    def __init__(self, dictfile):
        translation = {char: ' ' for char in string.punctuation}
        self.filter = str.maketrans(translation)
        self.keywords = {}
        with open(dictfile) as f:
            lines = f.readlines()
            for line in lines:
                self.keywords[line.strip().lower()] = 0

    def extract_file(self, filename): 
        targ_line = ""
        with open(filename) as f:
            lines = f.readlines()
            in_section = False
            
            for line in lines:
                if (in_section and len(line) > 2):  # Line not empty
                    targ_line = line
                    in_section = False
                if (line == "DUTIES\n"):
                    in_section = True
        targ_line = targ_line.translate(self.filter)
        # print(targ_line)
        for word in targ_line.split():
            if word.lower() in self.keywords:
                self.keywords[word.lower()] += 1
        return targ_line
    
    def get_keywords(self):
        return self.keywords

dp = DataParser("keywords.txt")
for filename in os.listdir('Job Bulletins'):  # This just recursively scans the whole thing
    print(filename)
    dp.extract_file("Job Bulletins/" + filename)
print(dp.get_keywords())
    