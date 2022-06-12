import pandas as pd
import database as db

# retorna o qualis (A1 ~ NI) e o valor do qualis (1.000 ~ 0.000) de acordo com o titulo ou com o issn pego no site
def qualisInfos(journals, issn):
    jis = []
    for i in range(len(journals)):
        jis.append([journals[i], issn[i]])

    qualisDB = pd.DataFrame(db.consult_db("SELECT * FROM qualis"))
    qualis, nota = [], []

    qualisNota={
        'A1': '1.000', 'A2': '0.875', 'A3': '0.750', 'A4': '0.625', 'B1': '0.500', 'B2': '0.200',
        'B3': '0.100', 'B4': '0.050', 'B5': '0.000', 'C': '0.000', 'NA': '0.000', 'NI': '0.000'}

    for i in jis:
        for q in range(len(qualisDB)):
            m = qualisDB[0][q].upper()
            p = qualisDB[1][q].replace('"', "'").upper()
            print(p)
            n = qualisDB[2][q].upper()
            if i[1] == m:                                                   #compara ISSNs
                print(i[1], m)
                qualis.append(n)
                nota.append(qualisNota.get(n))
                break  
            elif i[0].upper() in p:                                         #compara nomes
                print(i[0], p)
                qualis.append(n)
                nota.append(qualisNota.get(n))
                break 
        if len(qualis) < jis.index(i)+1 and len(nota) < jis.index(i)+1:     #caso não haja correspondencia entre nomes ou ISSNs
            qualis.append('NI')
            nota.append(qualisNota.get('NI'))

    return qualis, nota

# separa as informações em lista para cada tipo
def refInfos(resultsJournals, resultsConferences):
    titlesj, journals, issn, yearj, qualisj, titlesc, conferences, yearc, qualisc = [], [], [], [], [], [], [], [], []

    for i in resultsJournals:
        titlesj.append(i[1])
        journals.append(i[2])
        issn.append(i[3])
        yearj.append(i[4])
        if 'NÃO IDENTIFICADO' in i[5].upper(): qualisj.append('NI')
        else: qualisj.append(i[5][:2])
    
    qualis, nota = qualisInfos(journals, issn)
       
    for i in resultsConferences:
        titlesc.append(i[1])
        conferences.append(i[2])
        yearc.append(i[3])
        if 'NÃO IDENTIFICADO' in i[4].upper(): qualisc.append('NI')
        else: qualisc.append(i[4][:2])

    return titlesj, journals, issn, yearj, qualisj, qualis, nota, titlesc, conferences, yearc, qualisc

# cria dicionário para a correlação dos docentes e projetos
def dictResearchers():
    rc = {}
    docentes=pd.DataFrame(db.consult_db("SELECT nome FROM researchers"))
    for i in docentes[0]:
        rc[i]=[]
    return rc

# insere no dicionário a correlação dos docentes e projetos
def researchersCorrelation(list):
    rc = dictResearchers()
    for i in list:
        for r in rc:
            if r in i: rc[r].append(1)
            elif r not in i: rc[r].append(0)
    return rc
