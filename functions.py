from bs4 import BeautifulSoup
from tkinter import filedialog
import pandas as pd
import codecs
import requests

def nameLink():
    nL = input("link or file: ")
    if nL == 'file':
        file = filedialog.askopenfilename()
        return file
        
    if nL == 'link':
        response = requests.get(input('link: '))
        content = response.content
        return content

def htmlInfos():    
    type = input('|confer| or |period|: ')

    file = codecs.open(nameLink(), "r", "utf-8")
    content = BeautifulSoup(file, 'html.parser')

    works = content.findAll('tr')

    infos = []
    for work in works:
        title = work.select('b')[0].text
        confer = work.select('font')[0].text
        qualis = work.select('b')[1].text

        td = str(work.select('td')[1])
        authors = td.split(". <b")[0][0:].split("td>")[1][0:]

        if type == 'confer':          
            year = content.find('h3', attrs={'class': 'year'}).text
            infos.append([authors, title, confer, year, qualis[8:]]) 
        if type == 'period':
            issn = td.split("issn:")[1][0:].split(",")[0][1:]
            year = td.split("issn:")[1][0:].split(",")[1][:].split(".")[0][:]
            infos.append([authors, title, confer, issn, year, qualis[8:]])
    
    crtExcel(type, infos)
    file.close()

def crtExcel(type, infos):
    if type == 'confer':    table = pd.DataFrame(infos, columns=['Lista de autores', 'Título do artigo', 'Nome da conferência', 'Ano', 'Qualis'])
    if type == 'period':    table = pd.DataFrame(infos, columns=['Lista de autores', 'Título do artigo', 'Nome da conferência', 'ISSN', 'Ano', 'Qualis'])
    
    year = input('Ano: ')

    table.to_excel('PPCIC-{}-{}.xlsx'.format(type, year), index=False)
