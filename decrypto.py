import requests
from bs4 import BeautifulSoup

# Simple version, make sure to grab extra pages, use page rankings to order 
#https://wordassociations.net/en/words-associated-with/Horatio

base = "https://wordassociations.net/en/words-associated-with/"

def parse(dict,word,mode) -> int:
    count = 0
    response = requests.get(base+word)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        words_div = soup.find('div', class_='wordscolumn')

        if words_div:
            li_elements = words_div.find_all('li')
            for li in li_elements:
                txt = li.get_text()
                if mode == 0:
                    if txt in dict: dict[txt] += 1
                    else: dict[txt] = 1
                else: 
                    if txt in dict: count += 1

        pages_table = soup.find('table', class_='pages')
        if pages_table:
            td_elements = pages_table.find_all('td')
            td_count = len(td_elements)
            for i in range(1,td_count-1):
                response = requests.get(base+word+"?start="+str(100 * i))
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    words_div = soup.find('div', class_='wordscolumn')
                    if words_div:
                        li_elements = words_div.find_all('li')
                        for li in li_elements:
                            txt = li.get_text()
                            if mode == 0:
                                if txt in dict: dict[txt] += i
                                else: dict[txt] = i
                            elif txt in dict: count += 1
                else: 
                    print("Failed to retrieve web page #",i,". Status code:", response.status_code)
    else:
        print("Failed to retrieve the web page. Status code:", response.status_code)
    return count

def currgame():
    intercepts = 0
    fails = 0
    # Current Game
    # Our Words
    our = [{},{},{},{}]

    # Opponent's Words
    opp = [{},{},{},{}]

    for i in range(4): parse(our[i],input("Input word " + str(i+1) + ":").strip(),0)
    
    # For each word, maximize associations with all the other given words
    # Minimize associations with other given words
    while(intercepts < 2 and fails < 2):
        turn = int(input("Enter whose turn it is (0 for our team, 1 for opposing team, 2 to generate clues)").strip())
        # Our team
        if turn < 2:
            for _ in range(2):
                clues = ["","",""]
                guesses = [-1,-1,-1]
                true = [-1,-1,-1]
                max_match = 0
                for i in range(3): clues[i] = input("Enter clue #"+ str(i+1) +" (As a one word answer)").strip()
                for i in range(3):
                    for j in range(4):
                        matchlvl = parse(our[j],clues[i],1)
                        if matchlvl > max_match:
                            max_match = matchlvl
                            guesses[i] = j+1
                print("Guesses are: " + str(guesses))
                for i in range(3): guesses[i] = int(input("Enter your guess for clue #"+ str(i+1)).strip())
                for i in range(3): true[i] = int(input("Enter true number for clue #"+ str(i+1)).strip())
                for i in range(3):
                    if turn == 0: parse(our[true[i]-1], clues[i], 0)
                    else: parse(opp[true[i]-1], clues[i], 0)
                if true != guesses and turn == 0: fails += 1
                turn = int(not turn)
        else:
            #TODO
            print("Not Yet Implemented")
            pass

    

if __name__ == "__main__":
    currgame()