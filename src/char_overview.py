import requests
import json
import pprint

from bs4 import BeautifulSoup

URL = "https://www.dustloop.com/wiki/index.php?title=GGST/Ramlethal_Valentine"

page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")


outer_div = soup.find(id="mw-content-text")

for pair in outer_div.find_all(lambda tag: tag.name== "h3"):
    # if (pair.big.text.strip() == "j.S"):
        # big json set
        moveData = {}
        
        # get the title
        title = pair.big.text.strip()
        moveData['title'] = title

        
        description = pair.find_next_sibling('div', class_="attack-container")

        # get the imgs and their descriptions
        imgDict = {}
        hitboxDict = {}

        imgBox = description.find("ul", class_="gallery mw-gallery-nolines")
        for img in imgBox.find_all("li"):
            imgSrc = img.find("img")['src']
            imgDescription = "img"
            if img.find("p"):
                imgDescription = img.find("p").text.strip()
            
            imgDict[imgDescription] = imgSrc    
        moveData['imgs'] = imgDict
        
        hitBox = imgBox.find_next("ul", class_="gallery mw-gallery-nolines")

        for img in hitBox.find_all("li"):
            imgSrc = img.find("img")['src']
            imgDescription = "img"
            if img.find("p"):
                imgDescription = img.find("p").text.strip()
            
            hitboxDict[imgDescription] = imgSrc    

        moveData['hitboxes'] = hitboxDict
        

        # get the table
        atkTable = description.find("table", class_="wikitable attack-data")

        # form a list for headers
        headings = []
        atkHeaders = atkTable.find_all("th")
        
        for header in atkHeaders:
            if len(header.find_all('span')) != 0:
                header.span.span.extract()
                headings.append(header.select_one('span[class="tooltip"]').text.strip())
            elif len(header.find_all('a')) != 0:
                headings.append(header.find('a').text.strip()) 
            elif len(header.find_all()) == 0:
                headings.append(header.text.strip()) 

        # form a list of values    
        data = atkTable.find_all('td')
        cleaned_data = []

        for each in data:
            cleaned_data.append(each.text.strip())
        
        # merge together
        atkData = dict(zip(headings,cleaned_data))
        moveData['atkInfo'] = atkData

        propData = []
        properties = description.find(class_='attack-info').find_all('li')
        for prop in properties:
            propData.append(prop.text.strip())
        
        moveData['properties'] = propData

        notes = ''
        for p in description.find(class_='attack-info').find_all('p'):
            notes = notes + p.text.strip() + "\n"

        moveData['notes'] = notes

        pprint.pprint(moveData)