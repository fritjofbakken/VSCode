
#Slicing / Tokenization
def tokenize(lines):
    words = []
    for line in lines:
        start = 0
        end = start
        while start < len(line):
            while start < (len(line) - 1) and line[start].isspace():
                start += 1

            if line[start].isalpha(): # Recognize words only containing letters
                end = start
                while end < len(line) and line[end].isalpha():
                    end += 1
                words.append(line[start:end].lower())
                start = end - 1

            elif line[start].isdigit(): # Recognizing digits
                end = start
                while end < len(line) and line[end].isdigit():
                    end += 1
                words.append(line[start:end])
                start = end - 1
            
            elif line[start].isspace(): # Recognizing blanks
                pass

            else: # Everything else are special characters
                words.append(line[start])

            start += 1
              
    return words

#Counting
def countWords(words, stopWords):
    wordSorter = {}
    for word in words:
        if word not in stopWords:
            if word not in wordSorter.keys():
                wordSorter.update({word:1})
            else:
                wordSorter[word] += 1
    
    return wordSorter

#Printing function
def printTopMost(frequencies, n):
    keyPairs = frequencies.items()
    sortList = sorted(keyPairs, key=lambda x: -x[1])
    
    #Optional descriptions and framing for columns
    print("|-----           ---------|\n|Words           Frequency|\n|-----           ---------|")
    
    i = 0
    while i < n and i < len(sortList):
        print("|" + str(sortList[i][0]).ljust(20) + str(sortList[i][1]).rjust(5) + "|")
        i += 1

