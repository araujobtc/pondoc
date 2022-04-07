import pandas as pd
import database as db
import BSoup

def geralData():
    Geral = {}
    #
    return Geral

def conferData():
    Conferencias = {}
    #
    return Conferencias

def periodData():
    Periodicos = {}
    #
    return Periodicos

def lconferData():
    LConferencias = {}
    #
    return LConferencias

def lperiodData():
    LConferencias = {}
    #
    return LConferencias

def tabelasData():
    Tabelas = {
        'Qualis': ['A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B4', 'B5', 'C', 'NA', 'NI'],
        'Ponto': [1.000, 0.875, 0.750, 0.625, 0.500, 0.200, 0.100, 0.050, 0.000, 0.000, 0.000, 0.000],
        'Restrito': [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        '': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        '': [1.000, 0.875, 0.750, 0.625, 0.500, 0.200, 0.100, 0.050, 0.000, 0.000, 0.000, 0.000]
    }
    return Tabelas

def producaoData():
    Producao = {}
    #
    return LConferencias

def hindexData():
    HIndex = {}
    #
    return LConferencias

def insertData():

    arq = input('Nome para o arquivo: ')+'.xlsx'
    writer = pd.ExcelWriter(arq, engine='xlsxwriter')

    fileName = 'PPCIC scriptLattes - periodicos.html'
    infos = htmlInfos(fileName)

    # Formatação

    # Tabelas
    Tabelas = tabelasData()
    # Geral
    Geral = geralData()
    # Conferencias
    Conferencias = conferData()
    # Periodicos
    Periodicos = periodData()
    # LConferencias
    LConferencias = lconferData()
    # LPeriodicos
    LPeriodicos = lperiodData()
    # Producao
    Producao = producaoData()
    # HIndex
    HIndex = hindexData()

    geral = pd.DataFrame(Geral)
    confer = pd.DataFrame(Conferencias)
    period = pd.DataFrame(Periodicos)
    lconfer = pd.DataFrame(LConferencias)
    lperiod = pd.DataFrame(LPeriodicos)
    tabelas = pd.DataFrame(Tabelas)
    prod = pd.DataFrame(Producao)
    hindex = pd.DataFrame(HIndex)

    geral.to_excel(writer, sheet_name='Geral')
    confer.to_excel(writer, sheet_name='Conferencias')
    period.to_excel(writer, sheet_name='Periodicos')
    lconfer.to_excel(writer, sheet_name='LConferencias')
    lperiod.to_excel(writer, sheet_name='LPeriodicos')
    tabelas.to_excel(writer, sheet_name='Tabelas')
    prod.to_excel(writer, sheet_name='Producao')
    hindex.to_excel(writer, sheet_name='HIndex')

    writer.save()