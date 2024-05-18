import os
import requests
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed
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
# Takes the URL, word passed from dirBuster(), and if its HTTP(S) from isSecure()
def check_word(url: str, word: str, scheme: str):
    link = f"{scheme}{url}/{word}"
    try:
        response = requests.get(link)
        if response.status_code == 200:
            print(word)
    except requests.RequestException:
        pass

# Converted to support multi threading, runs multiple instances of check word.
# runs check_word with the params and loops through word list (words). 10 MAX threads.
def dirBuster(url:str, words:List, secure:bool):
    scheme = "https://" if secure else "http://"
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(check_word, url, word, scheme) for word in words]
        for future in as_completed(futures):
            future.result()

# asking user if its HTTPS or HTTP, defaults to HTTP if no valid response
def isSecure() -> bool:
    isSecure = input("Is the scheme HTTPS? (Y/n) -- Will default to no\n")
    if isSecure[0].lower() == 'y':
        return True
    else:
        return False
        
if __name__ == "__main__":
    domain = input("enter domain name \n")
    userWL = input("Please enter the directory of the word lists you'd like to use (leave blank to use default)")
    words = getWordList("wordlist-files") if userWL == "" else getWordList(userWL)
    print(f"Loaded {len(words)} words from your directory.\n")
    dirBuster(domain, words, isSecure())
