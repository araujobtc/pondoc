from bs4 import BeautifulSoup
import codecs
import requests

def htmlInfos(fileName):    
    file = codecs.open(fileName, "r", "utf-8")
    content = BeautifulSoup(file, 'html.parser')

    works = content.findAll('tr')

    infos=[]
    for work in works:
        td = work.select('td')[1].text
        for char in range(len(td)):
            if td[char] == '[':
                infos.append(str(td[:char-11]))
    
    file.close()
    return infos
