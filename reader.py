from bs4 import BeautifulSoup
import requests

def htmlInfos(url):
    file = requests.get(url).content
    content = BeautifulSoup(file, 'html.parser')

    works = content.findAll('tr')

    infos=[]
    for work in works:
        td = work.select('td')[1].text
        for char in range(len(td)):
            if td[char] == '[':
                infos.append(str(td[:char-11]))
    
    return infos
