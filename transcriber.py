import pandas as pd
from handler import refInfos, researchersCorrelation

# sheets
def geralData():
    Geral = {}
    #
    return Geral

def conferData(rCauthorsnorm, discauthorsC, titlec, conferences, yearc, qualisc):
    Confer={}

    Confer['Ano'] = yearc
    Confer['Numero'] = range(1, len(titlec)+1)
    Confer['Artigo'] = titlec
    Confer['Fórum'] = conferences
    Confer['Discente'] = discauthorsC
    Confer['Qualis-site'] = qualisc
    Confer['Área'] = ['']*len(titlec)
    Confer['Restrito'] = ['']*len(titlec)
    Confer['Discente Programa'] = ['']*len(titlec)

    Confer.update(researchersCorrelation(rCauthorsnorm))

    Confer['Qualis'] = ['-']*len(titlec)
    Confer['Docentes'] = ['']*len(titlec)
    Confer['Fator'] = ['']*len(titlec)
    Confer['Credenciamento'] = ['']*len(titlec)

    return Confer

def periodData(rJauthorsnorm, discauthorsJ, titlej, journals, yearj, qualis, nota):
    Period = {}
    Period['Ano'] = yearj
    Period['Numero'] = range(1, len(titlej)+1)
    Period['Artigo'] = titlej
    Period['Fórum'] = journals
    Period['Discente'] = discauthorsJ
    Period['Qualis-pdf'] =  qualis
    Period['Área'] = ['']*len(titlej)
    Period['Restrito'] = ['']*len(titlej)
    Period['Discente Programa'] = ['']*len(titlej)

    Period.update(researchersCorrelation(rJauthorsnorm))

    Period['Qualis_'] = nota
    Period['Docentes'] = ['']*len(titlej)
    Period['Fator'] = ['']*len(titlej)
    Period['Credenciamento'] = ['']*len(titlej)

    return Period

def lconferData(conferences, qualisc):
    LConfer = {}

    LConfer['Conferencias'] = conferences
    LConfer['Qualis-site'] = qualisc
    LConfer['CS'] = ['']*len(conferences)
    LConfer['Restrito'] = ['']*len(conferences)
    LConfer['Value'] = ['']*len(conferences)

    return LConfer

def lperiodData(journals, issn, qualisj, qualis, nota):
    LPeriod = {}

    LPeriod['Periodicos'] = journals
    LPeriod['Qualis-site'] = qualisj
    LPeriod['CS'] = [0]*len(journals)
    LPeriod['Restrito'] = [0]*len(journals)
    LPeriod['Value'] = nota
    LPeriod['ISSN/eISSN']=issn
    LPeriod['JIF (Percentil)'] = [0]*len(journals)
    LPeriod['Scopus'] = [0]*len(journals)
    LPeriod['Qualis-PDF'] = qualis
    LPeriod['QJIF'] = [0]*len(journals)
    LPeriod['Qscopus'] = [0]*len(journals)
    LPeriod['Max(PDF:Scopus)'] = nota

    return LPeriod

def tabelasData():
    Tabelas = {
        'Qualis': ['A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B4', 'B5', 'C', 'NA', 'NI'],
        'Ponto': [1.000, 0.875, 0.750, 0.625, 0.500, 0.200, 0.100, 0.050, 0.000, 0.000, 0.000, 0.000],
        'Restrito': [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        '': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
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

def insertData(anos, rJauthorsnorm, resultsJournals, discauthorsJ, rCauthorsnorm, resultsConferences, discauthorsC):
    
    arq = str(f'producao{str(anos[0])}-{str(anos[1]-1)}.xlsx')
    writer = pd.ExcelWriter(arq, engine='xlsxwriter')

    g, c, p, lc, lp, t, pr, h = {}, {}, {}, {}, {}, {}, {}, {}


    titlesj, journals, issn, yearj, qualisj, qualis, nota, titlesc, conferences, yearc, qualisc = refInfos(resultsJournals, resultsConferences)
    print(len(titlesj), len(journals), len(issn), len(yearj), len(qualisj), len(qualis), len(nota))

    # dicts
    g.update(geralData())
    c.update(conferData(rCauthorsnorm, discauthorsC, titlesc, conferences, yearc, qualisc))
    p.update(periodData(rJauthorsnorm, discauthorsJ, titlesj, journals, yearj, qualis, nota))
    lc.update(lconferData(conferences, qualisc))
    lp.update(lperiodData(journals, issn, qualisj, qualis, nota))
    t.update(tabelasData())
    pr.update(producaoData())
    h.update(hindexData())

    # tables
    geral = pd.DataFrame(g, index=None)
    confer = pd.DataFrame(c, index=None)
    period = pd.DataFrame(p, index=None)
    lconfer = pd.DataFrame(lc, index=None)
    lperiod = pd.DataFrame(lp, index=None)
    tabelas = pd.DataFrame(t, index=None)
    producao = pd.DataFrame(pr, index=None)
    hindex = pd.DataFrame(h, index=None)

    # worksheets
    geral.to_excel(writer, sheet_name='Geral', index=False)
    confer.to_excel(writer, sheet_name='Conferencias', index=False)
    period.to_excel(writer, sheet_name='Periodicos', index=False)
    lconfer.to_excel(writer, sheet_name='LConferencias', index=False, freeze_panes=(1,1))
    lperiod.to_excel(writer, sheet_name='LPeriodicos', index=False, freeze_panes=(1,1))
    tabelas.to_excel(writer, sheet_name='Tabelas', index=False)
    producao.to_excel(writer, sheet_name='Producao', index=False)
    hindex.to_excel(writer, sheet_name='HIndex', index=False)

    writer.save()
