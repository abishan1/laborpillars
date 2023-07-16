import os, sys, string

class DataParser:

    def __init__(self, dictfile, catfile):
        translation = {char: ' ' for char in string.punctuation}
        self.filter = str.maketrans(translation)
        self.keywords = {}
        self.category_keywords = {}
        with open(dictfile) as f:
            lines = f.readlines()
            for line in lines:
                self.keywords[line.strip().lower()] = 0

        with open(catfile) as f:
            lines = f.readlines()
            for line in lines:
                self.category_keywords[line.strip().lower()] = dict(self.keywords)

    def extract_file(self, filename, category): 
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
                line = line.translate(self.filter)
                for word in line.split():
                    if word.lower() in self.keywords:
                        self.category_keywords[category.lower()][word.lower()] += 1
        targ_line = targ_line.translate(self.filter)
        # print(targ_line)
        """
        for word in targ_line.split():
            if word.lower() in self.keywords:
                self.category_keywords[category.lower()][word.lower()] += 1
        """
        return targ_line
    
    def get_keywords(self):
        return self.category_keywords

dp = DataParser("keywords.txt", "categories.txt")
for filename in os.listdir('Administrative_Accounting'):  # This just recursively scans the whole thing
    # print(filename)
    dp.extract_file("Administrative_Accounting/" + filename, "admin")
for filename in os.listdir('Airport'):  
    dp.extract_file("Airport/" + filename, "airport")
for filename in os.listdir('Electric_Mechanic'):  
    dp.extract_file("Electric_Mechanic/" + filename, "mechanic")
for filename in os.listdir('Medical'):  
    dp.extract_file("Medical/" + filename, "medical")
print(dp.get_keywords())
    