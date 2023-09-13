from wordfreq import * 
import sys #Terminal interpreter
import urllib.request #fetch from web

def main():
    stopWordsRaw = open(sys.argv[1], encoding="utf-8")

    if sys.argv[2][:8] == "https://" or sys.argv[2][:7] == "http://": # Import files from web
        response = urllib.request.urlopen(sys.argv[2])
        fileRaw = response.read().decode("utf8").splitlines()
    else:
        fileRaw = open(sys.argv[2], encoding = "utf-8")
        
    printTopMost(countWords(tokenize(fileRaw), tokenize(stopWordsRaw)), int(sys.argv[3])) 
    stopWordsRaw.close()
    fileRaw.close()

main()