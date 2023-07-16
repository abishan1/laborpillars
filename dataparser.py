import os, sys, string, csv

class DataParser:

    def __init__(self, dictfile, catfile):
        translation = {char: ' ' for char in string.punctuation}
        self.filter = str.maketrans(translation)
        self.keywords = {}
        self.category_keywords = {}
        self.category_wc = {}
        self.rootdir = catfile
        with open(dictfile) as f:
            lines = f.readlines()
            for line in lines:
                self.keywords[line.strip().lower()] = 0

        for line in os.listdir(catfile):
            self.category_keywords[line] = dict(self.keywords)
            self.category_wc[line] = 0

    def extract_file(self, filename, category): 
        targ_line = ""
        with open(filename) as f:
            lines = f.readlines()
            in_section = False
            
            for line in lines:
                # if (in_section and len(line) > 2):  # Line not empty
                #     targ_line = line
                #     in_section = False
                # if (line == "DUTIES\n"):
                #     in_section = True
                line = line.translate(self.filter)
                for word in line.split():
                    self.category_wc[category] += 1
                    if word.lower() in self.keywords:
                        self.category_keywords[category][word.lower()] += 1
        targ_line = targ_line.translate(self.filter)
        # print(targ_line)
        """
        for word in targ_line.split():
            if word.lower() in self.keywords:
                self.category_keywords[category.lower()][word.lower()] += 1
        """
        return targ_line
    
    def extract_all(self):
        for category in os.listdir(self.rootdir):
            for file in os.listdir(self.rootdir + '/' + category):
                self.extract_file(self.rootdir + "/" + category + '/' + file, category)
            for key, val in self.category_keywords[category].items():
                self.category_keywords[category][key] = round(val / self.category_wc[category] * 1000000, 2)

    def get_keyword_freq(self):
        return self.category_keywords
    
    def write_csv(self, filename):
        catheads = ["Category_Name"]
        for key, val in self.keywords.items():
            catheads.append(key)
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=catheads)
            writer.writeheader()
            for category in self.category_keywords.keys():
                csvdict = dict(self.category_keywords[category])
                csvdict["Category_Name"] = category
                writer.writerow(csvdict)


dp = DataParser("keywords.txt", "Categorized_Jobs")
dp.extract_all()
dp.write_csv('keyword_frequencies.csv')
# print(dp.get_keyword_freq())

# for filename in os.listdir('Administrative_Accounting'):  # This just recursively scans the whole thing
#     # print(filename)
#     dp.extract_file("Administrative_Accounting/" + filename, "admin")
# for filename in os.listdir('Airport'):  
#     dp.extract_file("Airport/" + filename, "airport")
# for filename in os.listdir('Electric_Mechanic'):  
#     dp.extract_file("Electric_Mechanic/" + filename, "mechanic")
# for filename in os.listdir('Medical'):  
#     dp.extract_file("Medical/" + filename, "medical")
# print(dp.get_keywords())
