from bs4 import BeautifulSoup
import requests
from pprint import pprint
from char_moves import getMoves

def extractLoreVoice(loreVoice):
    res = {}
    lore = loreVoice.find("td", style="text-align: left; padding-left: 1em;")
    lore.extract()
    res['lore'] = lore.get_text()
    voice = loreVoice.find("td", style="text-align: left; padding-left: 1em;")
    if voice:
        res['voice'] = loreVoice.get_text()
    return res

def extractProCons(procons):
    res = {}
    prosDict={}
    pros = procons[1].find(style="width: 50%; text-align: left; padding: 6px; border-right: 1px solid rgba(160,160,160,.4); font-size: 14px;")
    counter = 0
    for pro in pros.find_all("li"):
        name = pro.find('b')
        if name:
            name.extract()
            name = name.get_text()
        else:
            name = counter
            counter += 1
        prosDict[name] = pro.get_text().strip(": ")
    
    res['pros'] = prosDict

    consDict={}
    counter = 0
    cons = pros.find_next_sibling("td")
    for con in cons.find_all("li"):
        name = con.find('b')
        if name:
            name.extract()
            name = name.get_text()
        else:
            name = counter
            counter += 1
        consDict[name] = con.get_text().strip(": ")
    res['cons'] = consDict
    # pprint(res)
    return res

def extractStats(info):
    res = {}
    stats = info.find_all("td", class_="CharaInfoLabel")
    for stat in stats:
        statInfo = stat.find_parent("tr")

        name = statInfo.find("td")
        value = name.find_next("td")
        res[name.get_text()] =  value.get_text()
    # pprint(res)

    return res  

def getOverview(soup):
    res = {}
    info = soup.find("div", id="fptopsection")
    loreVoice = info.find("div", class_="mw-collapsible")
    loreVoice.extract()
    res |= extractLoreVoice(loreVoice)
    
    playstyle = info.find("td", style="padding: 12px; font-size: 14px;")
    playstyle.extract()
    # pprint(playstyle.get_text())
    res['playstyle'] = playstyle.get_text()
    row1 = info.tr
    procons = row1.find_next_siblings("tr")
    res |= extractProCons(procons)

    stats = soup.find("div", id="fpflexsection")
    name = stats.find("span", style="font-size:20px; font-weight: 900;")
    res['name'] = name.get_text()
    bigImg = stats.find("img")
    res['bigImage'] = "https://www.dustloop.com" + bigImg['src']
    res |= extractStats(stats)

    return res
