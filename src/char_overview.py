import requests
import json
import pprint

from bs4 import BeautifulSoup

URL = "https://www.dustloop.com/wiki/index.php?title=GGST/Ramlethal_Valentine"

page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")


outer_div = soup.find(id="mw-content-text")

# print(outer_div.prettify())

for pair in outer_div.find_all(lambda tag: tag.name== "h3"):
    if (pair.big.text.strip() == "j.S"):
        # big json set
        moveData = {}
        
        # get the title
        title = pair.big.text.strip()
        moveData['title'] = title

        
        description = pair.find_next_sibling('div', class_="attack-container")

        # get the imgs and their descriptions
        imgDict = {}
        imgBox = description.find("ul", class_="gallery mw-gallery-nolines")
        for imgs in imgBox.find_all("li"):
            # print(imgs.prettify())
            imgSrc = imgBox.find("img")['src']
            imgDescription = "img"
            if imgs.find("p"):
                imgDescription = imgBox.find("p").text.strip()

            imgDict[imgDescription] = imgSrc    
        moveData['imgs'] = imgDict
        
        # get the table
        atkData = {}
        atkTable = description.find("table", class_="wikitable attack-data")

        atkHeaders = atkTable.find_all("th")
        for header in atkHeaders:
            if len(header.find_all()) == 0:
                # just a header
                # header = header.text.strip()
                atkData[header.text.strip()] = atkTable.find_next('td').text.strip()
            else:
                # header = header.find('a').text.strip()
                atkData[header.find('a').text.strip()] = atkTable.find_next('td').text.strip()
                # a tag inside 
        

        pprint.pprint(atkHeaders)
        # atkData['damage'] = atkTable.find_next('td').text.strip()
        # atkData['guard'] = atkTable.find_next('td').text.strip()

        rawValues = atkTable.find_all("td")
        pprint.pprint(rawValues)
        moveData['atkInfo'] = atkData
        pprint.pprint(moveData)