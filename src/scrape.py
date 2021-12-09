import sys
from bs4 import BeautifulSoup
import requests
import json

from pprint import pprint
from char_moves import getMoves
from char_overview import getOverview

# AS OF 09/12/2021
validGGST = ['Anji_Mito', 'Axl_Low', 'Chipp_Zanuff', 'Faust', 'Giovanna', 
'Goldlewis_Dickinson', 'Happy_Chaos', 'I-No', 'Jack-O', 
'Ky_Kiske', 'Leo_Whitefang', 'May', 'Millia_Rage', 'Nagoriyuki', 
'Potemkin', 'Ramlethal_Valentine', 'Sol_Badguy', 'Zato-1']


if __name__=='__main__':
    if len(sys.argv) != 2:
        print("Usage: python char_overview ([character name] or [dustloop character URL]")
        print("Valid GGST character names:")
        pprint(validGGST)
        exit(1)
    URL = ""
    if sys.argv[1] in validGGST:
        character = sys.argv[1]
        print(f"Collecting Data on {character}...")
        URL = f"https://www.dustloop.com/wiki/index.php?title=GGST/{character}" 
    elif sys.argv[1] == "help":
        print("Scrape dustloop characters into JSON format")
        print("Usage: python char_overview ([character name] or [dustloop character URL]")
        print("Valid GGST character names:")
        pprint(validGGST)
        exit(0)
    else:
        print('Assuming arg as URL')
        URL = sys.argv[1]
    
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    charInfo = {}
    try:
        charInfo |= getOverview(soup)
        charInfo['moves'] = getMoves(soup)
        pprint(charInfo)
        
        f = open("output.json","w")
        json.dump(charInfo, f)
        f.close()
    except Exception as err:
        print("Extraction Error: ", err)
    