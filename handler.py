import pandas as pd
import database as db
from fuzzywuzzy import fuzz

# retorna o qualis (A1 ~ NI) de acordo com o titulo ou com o issn pego no site
def qualisInfos(conferjournals, issn = 0):
    cjis, qualis, color = [], [], []
    for i in range(len(conferjournals)):
        cjis.append([conferjournals[i], issn[i]])

    qualisDB = db.consult_db("SELECT * FROM qualis")

    for i in cjis:
        for q in range(len(qualisDB)):
            issn = qualisDB[q][0]  
            nome = qualisDB[q][1]
            qdb = qualisDB[q][2]
            if fuzz.ratio(i[0], nome) == 100: 
                color.append(0)
                qualis.append(qdb)
                break
            elif 95 <= fuzz.ratio(i[0], nome):
                color.append(1)
                qualis.append(qdb)
                break
            elif fuzz.ratio(i[1], issn) == 100:
                color.append(1)
                qualis.append(qdb)
                break
            
        if len(qualis) < cjis.index(i)+1:
            color.append(1) 
            qualis.append('NI')  

    return qualis, color

# separa as informações em lista para cada tipo
def refInfos(resultsJournals, resultsConferences):
    titlesj, journals, issn, yearj, qualisurlj, titlesc, conferences, yearc, qualisurlc = [], [], [], [], [], [], [], [], []

    for i in resultsJournals:
        titlesj.append(i[1])
        journals.append(i[2])
        issn.append(i[3])
        yearj.append(i[4])
        if 'NÃO IDENTIFICADO' in i[5].upper(): qualisurlj.append('NI')
        else: qualisurlj.append(i[5][:2])
    
    qualisj, colorj = qualisInfos(journals, issn)
       
    for i in resultsConferences:
        titlesc.append(i[1])
        conferences.append(i[2])
        yearc.append(i[3])
        if 'NÃO IDENTIFICADO' in i[4].upper(): qualisurlc.append('NI')
        else: qualisurlc.append(i[4][:2])

    # qualisc, colorc = qualisInfos(conferences)

    return titlesj, journals, issn, yearj, qualisj, colorj, titlesc, conferences, yearc, qualisurlc #qualisurlj, qualisc, colorc

# insere no dicionário a correlação dos docentes e projetos
def researchersCorrelation(list):
    rc = {}
    docentes=pd.DataFrame(db.consult_db("SELECT nome FROM researchers"))
    for i in docentes[0]:
        rc[i]=[]

    for r in rc:
        for i in list:
            if r in i: rc[r].append(1)
            elif r not in i: rc[r].append('')
    return rc
