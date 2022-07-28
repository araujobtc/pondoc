import openpyxl
from openpyxl.styles import Font
import pandas as pd
from handler import refInfos, researchersCorrelation

def conferData(wb, discauthorsC, titlesc, conferences, yearc):
    for i in range(2, len(titlesc)+2):
        wb[f'A{i}']= yearc[i-2]
        wb[f'B{i}']= i-1
        wb[f'C{i}']= titlesc[i-2]
        wb[f'D{i}']= conferences[i-2]
        # if colorc[i-2] == 1: wb[f'D{i}'].font = Font(color='FF0000')
        if discauthorsC[i-2] != []: wb[f'E{i}']= discauthorsC[i-2]
        wb[f'F{i}']= f'=VLOOKUP(D{i},LConferencias!A:B,2,FALSE)'
        wb[f'G{i}']= f'=VLOOKUP(D{i},LConferencias!A:C,3,FALSE)'
        wb[f'H{i}']= f'=VLOOKUP(D{i},LConferencias!A:D,4,FALSE)'
        wb[f'I{i}']= f'=IF(E{i}<>"",1,0)'
        wb[f'AB{i}']= f'=VLOOKUP(F{i},Tabelas!A:C,2,FALSE)'
        wb[f'AC{i}']= f'=SUM(K{i}:Z{i})'
        wb[f'AD{i}']= f'=IF(AC{i}<=2,1,1-LOG(AC{i}-1))'
        wb[f'AE{i}']= f'=VLOOKUP(D{i},LConferencias!A:E,5,FALSE)*IF(I{i}>0,1.1,1)*AD{i}'

def periodData(wb, discauthorsJ, titlesj, journals, yearj, colorj):
    for i in range(2, len(titlesj)+2):
        wb[f'A{i}']= yearj[i-2]
        wb[f'B{i}']= i-1
        wb[f'C{i}']= titlesj[i-2]
        wb[f'D{i}']= journals[i-2]
        if colorj[i-2] == 1: wb[f'D{i}'].font = Font(color='FF0000')
        if discauthorsJ[i-2] != []: wb[f'E{i}']= discauthorsJ[i-2]
        wb[f'F{i}']= f'=VLOOKUP(D{i},LPeriodicos!A:B,2,FALSE)'
        wb[f'G{i}']= f'=VLOOKUP(D{i},LPeriodicos!A:C,3,FALSE)'
        wb[f'H{i}']= f'=VLOOKUP(D{i},LPeriodicos!A:D,4,FALSE)'
        wb[f'I{i}']= f'=IF(E{i}<>"",1,0)'
        wb[f'AB{i}']= f'=VLOOKUP(F{i},Tabelas!A:C,2,FALSE)'
        wb[f'AC{i}']= f'=SUM(K{i}:Z{i})'
        wb[f'AD{i}']= f'=IF(AC{i}<=2,1,1-LOG(AC{i}-1))'
        wb[f'AE{i}']= f'=VLOOKUP(D{i},LPeriodicos!A:E,5,FALSE)*IF(I{i}>0,1.1,1)*AD{i}'

def lconferData(wb, conferences, qualisurlc):
    for i in range(2, len(conferences)+2):
        wb[f'A{i}']= conferences[i-2]
        # if colorc[i-2] == 1: wb[f'A{i}'].font = Font(color='FF0000')
        wb[f'B{i}']= qualisurlc[i-2]
        wb[f'C{i}']= f'=IF(B{i}<>"NI",1,0)'
        wb[f'D{i}']= f'=VLOOKUP(B{i},Tabelas!A:C,3,FALSE)'
        wb[f'E{i}']= f'=VLOOKUP(B{i},Tabelas!A:C,2,FALSE)'

def lperiodData(wb, journals, issn, qualisj, colorj):
    for i in range(2, len(journals)+2):
        wb[f'A{i}']= journals[i-2]
        if colorj[i-2] == 1: wb[f'A{i}'].font = Font(color='FF0000')
        wb[f'B{i}']= f'=IF(M{i}>1-1/8,"A1",IF(M{i}>1-2/8,"A2",IF(M{i}>1-3/8,"A3",IF(M{i}>1/2,"A4",IF(M{i}>1-5/8,"B1",IF(M{i}>=0.2,"B2",IF(M{i}>=0.1,"B3",IF(M{i}>=0.05,"B4","NA"))))))))'
        wb[f'D{i}']= f'=VLOOKUP(B{i},Tabelas!A:C,3,FALSE)'
        wb[f'E{i}']= f'=VLOOKUP(B{i},Tabelas!A:C,2,FALSE)'
        wb[f'G{i}']= issn[i-2]
        wb[f'J{i}']= qualisj[i-2]
        wb[f'K{i}']= f'=IF(H{i}>1-1/8,"A1",IF(H{i}>1-2/8,"A2",IF(H{i}>1-3/8,"A3",IF(H{i}>1/2,"A4",IF(H{i}>1-5/8,"B1",IF(H{i}>1-6/8,"B2",IF(H{i}>1-7/8,"B3",IF(H{i}>0,"B4","NA"))))))))'
        wb[f'L{i}']= f'=IF(I{i}>1-1/8,"A1",IF(I{i}>1-2/8,"A2",IF(I{i}>1-3/8,"A3",IF(I{i}>1/2,"A4",IF(I{i}>1-5/8,"B1",IF(I{i}>1-6/8,"B2",IF(I{i}>1-7/8,"B3",IF(I{i}>0,"B4","NA"))))))))'
        wb[f'M{i}']= f'=MAX(VLOOKUP(L{i},Tabelas!A:C,2,FALSE),VLOOKUP(J{i},Tabelas!A:C,2,FALSE),VLOOKUP(J{i},Tabelas!A:C,2,FALSE))'

def insertData(period, file, rJauthorsnorm, resultsJournals, discauthorsJ, rCauthorsnorm, resultsConferences, discauthorsC):
    wb = openpyxl.load_workbook(filename = file)
    titlesj, journals, issn, yearj, qualisj, colorj, titlesc, conferences, yearc, qualisurlc = refInfos(resultsJournals, resultsConferences) #qualisurlj, qualisc, colorc

    wb['Conferencias'].delete_rows(2, 150)
    wb['Periodicos'].delete_rows(2, 150)
    wb['LConferencias'].delete_rows(2, 200)
    wb['LPeriodicos'].delete_rows(2, 200)

    conferData(wb['Conferencias'], discauthorsC, titlesc, conferences, yearc)    #colorc
    periodData(wb['Periodicos'], discauthorsJ, titlesj, journals, yearj, colorj)
    lconferData(wb['LConferencias'], conferences, qualisurlc)       #qualisurlc -> qualisc, colorc
    lperiodData(wb['LPeriodicos'], journals, issn, qualisj, colorj)
    
    if file == 'default.xlsx': 
        file = f'producao{"-".join(period)}.xlsx'
        wb.save(file)
    else: wb.save(file)
    wb.close()
    
    with pd.ExcelWriter(file, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:   
        pd.DataFrame(researchersCorrelation(rCauthorsnorm)).to_excel(writer, sheet_name='Conferencias', startrow=1, startcol=10, index=False, header=False)
        pd.DataFrame(researchersCorrelation(rJauthorsnorm)).to_excel(writer, sheet_name='Periodicos', startrow=1, startcol=10,  index=False, header=False)
        writer.save()
