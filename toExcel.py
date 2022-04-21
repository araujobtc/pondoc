import pandas as pd
import database as db
from BSoup import htmlInfos
from parsing import parseJournalPublication, parseConferencePublication

def qualisJournal(titleL):
    qualis = pd.DataFrame(db.consult_db("SELECT qualis, nome FROM qualis"))
    qualisL, qualisAval = [], []

    qAval={'A1': 1.000, 'A2': 0.875, 'A3': 0.750, 'A4': 0.625, 'B1': 0.500, 'B2': 0.200,
        'B3': 0.100, 'B4': 0.050, 'B5': 0.000, 'C': 0.000, 'NA': 0.000, 'NI': 0.000
    }

    for t in titleL:
        m=0
        for i in qualis[1]:
            if i == title:
                qualisL.append(qualis[0][m])
                qualisAval.append(qAval.get(qualis[0][m]))
            m+=1

    return qualisL, qualisAval

def refInfos(file, l):
    authorsL, titleL, conferJournalL, yearL, index, i = [], [], [], [], [], 1
    for infos in htmlInfos(file):
        # 0 - confer 1 - period
        if l == 0: authors, title, conferJournal, year = parseConferencePublication(infos)
        elif l == 1: authors, title, conferJournal, year = parseJournalPublication(infos)
        authorsL.append(authors)
        titleL.append(title)
        conferJournalL.append(conferJournal)
        yearL.append(year)
        index.append(i)
        i+=1

    qualisL, qualisAval = qualisJournal(titleL)

    return authorsL, titleL, conferJournalL, yearL, index, qualisL, qualisAval

# sheets

def geralData():
    Geral = {}
    #
    return Geral

def conferData():
    Confer={}
    authorsL, titleL, journalL, yearL, index, qualisL, qualisAval = refInfos('PPCIC scriptLattes - conferencias.html', 0)

    Confer['Ano'] = yearL
    Confer['Numero'] = index
    Confer['Artigo'] = titleL
    Confer['Fórum'] = journalL
    Confer['Discente'] = ['']*len(index)
    Confer['Qualis'] =  qualisL
    Confer['Área'] = ['']*len(index)
    Confer['Restrito'] = ['']*len(index)
    Confer['Discente Programa'] = ['']*len(index)

    docentes=pd.DataFrame(db.consult_db("SELECT nome_completo FROM researchers"))
    for n in range(len(docentes)):
        Confer[docentes[0][n]]=['']*len(index)


    Confer['Qualis'] = qualisAval
    Confer['Docentes'] = ['']*len(index)
    Confer['Fator'] = ['']*len(index)
    Confer['Credenciamento'] = ['']*len(index)

    return Confer

def periodData():
    Period = {}
    authorsL, titleL, journalL, yearL, index, qualisL, qualisAval = refInfos('PPCIC scriptLattes - periodicos.html')

    Period['Ano'] = yearL
    Period['Numero'] = index
    Period['Artigo'] = titleL
    Period['Fórum'] = journalL
    Period['Discente'] = ['']*len(index)
    Period['Qualis'] =  qualisL
    Period['Área'] = ['']*len(index)
    Period['Restrito'] = ['']*len(index)
    Period['Discente Programa'] = ['']*len(index)

    docentes=pd.DataFrame(db.consult_db("SELECT nome_completo FROM researchers"))
    for n in range(len(docentes)):
        Period[docentes[0][n]]=[0]*len(index)


    Period['Qualis'] = qualisAval
    Period['Docentes'] = ['']*len(index)
    Period['Fator'] = ['']*len(index)
    Period['Credenciamento'] = ['']*len(index)

    return Period

def lconferData():
    LConfer = {}
    return LConfer

def lperiodData():
    Lperiod = {}
    return Lperiod

def tabelasData():
    Tabelas = {
        'Qualis': ['A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B4', 'B5', 'C', 'NA', 'NI'],
        'Ponto': [1.000, 0.875, 0.750, 0.625, 0.500, 0.200, 0.100, 0.050, 0.000, 0.000, 0.000, 0.000],
        'Restrito': [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        '': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        '': [1.000, 0.875, 0.750, 0.625, 0.500, 0.200, 0.100, 0.050, 0.000, 0.000, 0.000, 0.000]
    }
    return Tabelas

def producaoData():
    Producao = {}
    #
    return Producao

def hindexData():
    HIndex = {}
    #
    return HIndex

def insertData():

    arq = input('Nome para o arquivo: ')+'.xlsx'
    writer = pd.ExcelWriter(arq, engine='xlsxwriter')

    # Formatação

    geral = pd.DataFrame(geralData(), index=None)
    confer = pd.DataFrame(conferData(), index=None)
    period = pd.DataFrame(periodData(), index=None)
    lconfer = pd.DataFrame(lconferData(), index=None)
    lperiod = pd.DataFrame(lperiodData(), index=None)
    tabelas = pd.DataFrame(tabelasData(), index=None)
    prod = pd.DataFrame(producaoData(), index=None)
    hindex = pd.DataFrame(hindexData(), index=None)

    geral.to_excel(writer, sheet_name='Geral')
    confer.to_excel(writer, sheet_name='Conferencias')
    period.to_excel(writer, sheet_name='Periodicos')
    lconfer.to_excel(writer, sheet_name='LConferencias')
    lperiod.to_excel(writer, sheet_name='LPeriodicos')
    tabelas.to_excel(writer, sheet_name='Tabelas')
    prod.to_excel(writer, sheet_name='Producao')
    hindex.to_excel(writer, sheet_name='HIndex')

    writer.save()

insertData()