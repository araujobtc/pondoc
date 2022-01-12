from bs4 import BeautifulSoup
from tkinter import filedialog
import pandas as pd
import codecs

# # import requests

# # link = input('link: ')
# # name = input("Nome: ")

# # response = requests.get(link)
# # content = response.content

name = filedialog.askopenfilename()
file = codecs.open(name, "r", "utf-8")
content = BeautifulSoup(file, 'html.parser')

works = content.findAll('tr')
year = content.find('h3', attrs={'class': 'year'})

infos = []

for work in works:
    title = work.select('b')[0].text
    confer = work.select('font')[0].text
    qualis = work.select('b')[1].text

    authorsList = str(work.select('td')[1])
    l = len(authorsList)
    i=-1

    for a in range(l):
        if authorsList[i]=='.' and authorsList[i+3]=='b' and authorsList[i+4]=='>':
            n = l + i
            authors = authorsList[4:n]   #4 para apagar "<td>"
 
        i-=1
    
    infos.append([authors, title, confer, year.text, qualis[8:]])


table = pd.DataFrame(infos, columns=['Lista de autores', 'Título do artigo', 'Nome da conferência', 'Ano', 'Qualis'])

table.to_excel('{}.xlsx'.format(name), index=False)

file.close()
