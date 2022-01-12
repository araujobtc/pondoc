from bs4 import BeautifulSoup
from tkinter import filedialog
import pandas as pd
import codecs
import requests


def nameLink():
    nL = input("link or name: ")
    if nL == 'name':
        name = filedialog.askopenfilename()
        file = codecs.open(name, "r", "utf-8")
        return file
        
    if nL == 'link':
        response = requests.get(input('link: '))
        content = response.content
        return content


def htmlInfos():
    # content = response.content
    
    type = input('|confer| or |period|: ')

    content = BeautifulSoup(nameLink(), 'html.parser')

    works = content.findAll('tr')
    year = content.find('h3', attrs={'class': 'year'})

    infos = []
    for work in works:
        title = work.select('b')[0].text
        confer = work.select('font')[0].text
        qualis = work.select('b')[1].text

        td = str(work.select('td')[1])
        authors = td.split(". <b")[0][0:].split("td>")[1][0:]

        if type == 'confer':
            infos.append([authors, title, confer, year.text, qualis[8:]])
        if type == 'period':
            issn = td.split("issn:")[1][0:].split(",")[0][1:]
            infos.append([authors, title, confer, issn, year.text, qualis[8:]])
    
    crtExcel(type, infos, year.text)

    return()
    file.close()

def crtExcel(type, infos, year):
    if type == 'confer':    table = pd.DataFrame(infos, columns=['Lista de autores', 'Título do artigo', 'Nome da conferência', 'Ano', 'Qualis'])
    if type == 'period':    table = pd.DataFrame(infos, columns=['Lista de autores', 'Título do artigo', 'Nome da conferência', 'ISSN', 'Ano', 'Qualis'])
    
    table.to_excel('PPCIC-{}-{}.xlsx'.format(type, year), index=False)