import requests
import json
import pprint

from bs4 import BeautifulSoup

# Global Variables
URL = "https://www.dustloop.com/wiki/index.php?title=GGST/Ramlethal_Valentine"


def extractTitle(pair):
    ret = {}
    title =  pair.big.text.strip()
    ret['title'] = title
    return ret


def extractImages(description):
    ret = {}
    imgDict = {}
    hitboxDict = {}

    imgBox = description.find("ul", class_="gallery mw-gallery-nolines")
    for img in imgBox.find_all("li"):
        imgSrc = "None"
        if img.find("img"):
            imgSrc = img.find("img")['src']
        imgDescription = "img"
        if img.find("p"):
            imgDescription = img.find("p").text.strip()
        
        imgDict[imgDescription] = imgSrc    
    ret['imgs'] = imgDict
    
    hitBox = imgBox.find_next("ul", class_="gallery mw-gallery-nolines")

    for img in hitBox.find_all("li"):
        imgSrc = "None"
        if img.find("img"):
            imgSrc = img.find("img")['src']
        imgDescription = "hitbox"
        if img.find("p"):
            imgDescription = img.find("p").text.strip()
        
        hitboxDict[imgDescription] = imgSrc    

    ret['hitboxes'] = hitboxDict
    return ret

def extractAtkValues(description):
    ret = {}
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
    ret['atkInfo'] = atkData
    return ret

def extractNotes(description):
    ret = {}
    # get the notes of the move
    propData = []

    children = description.find(class_='attack-info').findAll(['li', 'dt', 'p'])

    # pprint.pprint(children)

    properties = description.find(class_='attack-info').find_all('li')
    for prop in properties:
        propData.append(prop.text.strip())
    
    ret['properties'] = propData
    
    notes = ''
    for line in description.find(class_='attack-info').find_all(['p', 'dl']):
        notes = notes + line.text.strip() + "\n"

    ret['notes'] = notes
    return ret

if __name__=='__main__':
    
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    outer_div = soup.find(id="mw-content-text")
    for pair in outer_div.find_all(lambda tag: tag.name== "h3"):
        description = pair.find_next_sibling('div', class_="attack-container")
        moveData = {}
        moveData |= extractTitle(pair)
        moveData |= extractImages(description)
        moveData |= extractAtkValues(description)
        moveData |= extractNotes(description)
        pprint.pprint(moveData)