import pandas as pd
import database as db
from analyzer import parseJournalPublication, parseConferencePublication


def qualis(titles):
    qualisDB = pd.DataFrame(db.consult_db("SELECT qualis, nome FROM qualis"))
    qualis, nota = [], []

    qualisNota={'A1': 1.000, 'A2': 0.875, 'A3': 0.750, 'A4': 0.625, 'B1': 0.500, 'B2': 0.200,
        'B3': 0.100, 'B4': 0.050, 'B5': 0.000, 'C': 0.000, 'NA': 0.000, 'NI': 0.000}

    for t in titles:
        m=0
        for i in qualisDB[1]:
            if i == t:
                qualis.append(qualisDB[0][m])
                nota.append(qualisNota.get(qualisDB[0][m]))
            m+=1

    return qualis, nota

def refInfos(infosp, infosc):
    authorsP, titleP, journals, yearP, indexP = [], [], [], [], []

    i = 1

    for infos in infosp:
        authors, title, journal, year = parseJournalPublication(infos)
        authorsP.append(authors)
        titleP.append(title)
        journals.append(journal)
        yearP.append(year)
        indexP.append(i)
        i+=1    
    
    qualisP, notaP = qualis(titleL)
    
    authorsC, titleC, conferences, yearC, indexC= [], [], [], [], []
    
    i = 1

    for infos in infosc:
        authors, title, conference, year = parseConferencePublication(infos)
        authorsC.append(authors)
        titleC.append(title)
        conferences.append(conference)
        yearC.append(year)
        indexC.append(i)
        i+=1

    qualisC, notaC = qualis(titleL)

    return authorsP, titleP, journals, yearP, indexP, qualisP, notaP, authorsC, titleC, conferences, yearC, indexC, qualisC, notaC

# sheets

def geralData(writer):
    Geral = {}

    geral = pd.DataFrame(Geral, index=None)

    geral.to_excel(writer, sheet_name='Geral')

def conferData(writer, authorsC, titleC, conferences, yearC, indexC, qualisC, notaC):
    Confer={}

    Confer['Ano'] = yearC
    Confer['Numero'] = indexC
    Confer['Artigo'] = titleC
    Confer['Fórum'] = conferences
    Confer['Discente'] = ['']*len(index)
    Confer['Qualis'] =  qualisC
    Confer['Área'] = ['']*len(index)
    Confer['Restrito'] = ['']*len(index)
    Confer['Discente Programa'] = ['']*len(index)

    docentes=pd.DataFrame(db.consult_db("SELECT nome_completo FROM researchers"))
    for n in range(len(docentes)):
        Confer[docentes[0][n]]=['']*len(index)


    Confer['Qualis'] = notaC
    Confer['Docentes'] = ['']*len(index)
    Confer['Fator'] = ['']*len(index)
    Confer['Credenciamento'] = ['']*len(index)

    confer = pd.DataFrame(Confer, index=None)

    confer.to_excel(writer, sheet_name='Conferencias')

def periodData(writer, authorsP, titleP, journals, yearP, indexP, qualisP, notaP):
    Period = {}

    Period['Ano'] = yearP
    Period['Numero'] = indexP
    Period['Artigo'] = titleP
    Period['Fórum'] = journals
    Period['Discente'] = ['']*len(index)
    Period['Qualis'] =  qualisP
    Period['Área'] = ['']*len(index)
    Period['Restrito'] = ['']*len(index)
    Period['Discente Programa'] = ['']*len(index)

    docentes=pd.DataFrame(db.consult_db("SELECT nome_completo FROM researchers"))
    for n in range(len(docentes)):
        Period[docentes[0][n]]=[0]*len(index)


    Period['Qualis'] = notaP
    Period['Docentes'] = ['']*len(index)
    Period['Fator'] = ['']*len(index)
    Period['Credenciamento'] = ['']*len(index)

    period = pd.DataFrame(Period, index=None)

    period.to_excel(writer, sheet_name='Periodicos')

def lconferData(writer, conferences, qualisC, notaC):
    LConfer = {}

    LConfer['Conferencias'] = conferences
    LConfer['Qualis'] = qualisC
    LConfer['CS'] = [0]*len(conferences)
    LConfer['Restrito'] = [0]*len(conferences)
    LConfer['Value'] = notaC

    lconfer = pd.DataFrame(LConfer, index=None)

    lconfer.to_excel(writer, sheet_name='LConferencias')

def lperiodData(writer, journals, qualisP, notaP):
    Lperiod = {}

    LPeriod['Conferencias'] = journals
    LPeriod['Qualis'] = qualisC
    LPeriod['CS'] = [0]*len(journals)
    LPeriod['Restrito'] = [0]*len(journals)
    LPeriod['Value'] = notaC

    issn=pd.DataFrame(db.consult_db("SELECT issn FROM qualis"))
    for n in range(len(issn)):
        LPeriod['ISSN/eISSN']=issn[0][n]

    LPeriod['JIF (Percentil)'] = [0]*len(journals)
    LPeriod['Scopus'] = [0]*len(journals)
    LPeriod['Qualis-PDF'] = qualisC
    LPeriod['QJIF'] = [0]*len(journals)
    LPeriod['Qscopus'] = [0]*len(journals)
    LPeriod['Max(PDF:Scopus)'] = notaC

    lperiod = pd.DataFrame(LPeriod, index=None)

    lperiod.to_excel(writer, sheet_name='LPeriodicos')

def tabelasData(writer):
    Tabelas = {
        'Qualis': ['A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B4', 'B5', 'C', 'NA', 'NI'],
        'Ponto': [1.000, 0.875, 0.750, 0.625, 0.500, 0.200, 0.100, 0.050, 0.000, 0.000, 0.000, 0.000],
        'Restrito': [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        '': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        '': [1.000, 0.875, 0.750, 0.625, 0.500, 0.200, 0.100, 0.050, 0.000, 0.000, 0.000, 0.000]
    }
    
    tabelas = pd.DataFrame(Tabelas, index=None)

    tabelas.to_excel(writer, sheet_name='Tabelas')

def producaoData(writer):
    Producao = {}
    # 
    producao = pd.DataFrame(Producao, index=None)

    producao.to_excel(writer, sheet_name='Producao')

def hindexData(writer):
    HIndex = {}
    #
    hindex = pd.DataFrame(HIndex, index=None)

    hindex.to_excel(writer, sheet_name='HIndex')

def insertData(infosp, infosc):
    
    (authorsP, titleP, journals,
    yearP, indexP, qualisP,
    notaP, authorsC, titleC,
    conferences, yearC, indexC,
    qualisC, notaC) = refInfos(infosp, infosc)

    arq = input('Nome para o arquivo: ')+'.xlsx'
    writer = pd.ExcelWriter(arq, engine='xlsxwriter')

    # tables

    geralData(writer)
    conferData(writer, authorsC, titleC, conferences, yearC, indexC, qualisC, notaC)
    periodData(writer, authorsP, titleP, journals, yearP, indexP, qualisP,  notaP)
    lconferData(writer, conferences, qualisC, notaC)
    lperiodData(writer, journals, qualisP, notaP)
    tabelasData(writer)
    producaoData(writer)
    hindexData(writer)

    writer.save()
