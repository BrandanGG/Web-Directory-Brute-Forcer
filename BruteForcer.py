import os
import requests
from typing import List
# returns list with all words from the wordlist directory
def getWordList(d_path:str) -> List[str]: # param is the word list directory returns list of words
    words = []
    directory = os.listdir(d_path)
    for file in directory:
        file_path = os.path.join(d_path, file) # doesn't like file name since its not at the same level, need to join here with path
        with open(file_path , "r") as f:
            words.extend(f.read().splitlines()) # use extend to ensure a flat list
    return words

# Void method -- will output each successful response
#Params are IP / Domain, wordlist
def dirBuster(url:str, words:List, secure:bool):
    if secure:
        scheme = "HTTPS://"
    else:
        scheme = "HTTP://"
    for word in words:
        link = f"{scheme}{url}/{word}"
        response = requests.get(link)
        if response.status_code == 200:
            print(word)

# asking user if its HTTPS or HTTP, defaults to HTTP if no valid response
def isSecure() -> bool:
    isSecure = input("Is the scheme HTTPS? (Y/n) -- Will default to no\n")
    if isSecure[0].lower() == 'y':
        return True
    else:
        return False
        
if __name__ == "__main__":
    domain = input("enter domain name \n")
    words = getWordList("wordlist-files")
    print(f"Loaded {len(words)} words from your directory.\n")
    dirBuster(domain, words, isSecure())
