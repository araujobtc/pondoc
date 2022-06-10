from normalizer import normalizer
from reader import htmlInfos
from transcriber import insertData
from analyzer import parseJournalPublication, parseConferencePublication
import argparse

def main(anos = '0'):
    if anos == '0':
        parser = argparse.ArgumentParser(description='PONDOC')
        parser.add_argument('-y','--year', type=str, default='2021-2024', help='Write the year or period | ex: "2017" or "2021-2024"')
        args = parser.parse_args()
        anos = args.year

    anos = anos.strip()
    if len(anos)==4: periodo = [anos]*2
    elif len(anos)==9: periodo = anos.split('-')
    
    resultsJournals, resultsConferences = [], []
    rJauthorsnorm, rCauthorsnorm, discauthorsJ, discauthorsC= [], [], [], []

    for ano in range(int(periodo[0]), int(periodo[1])+1):

        infosp = htmlInfos(str(f'https://eic.cefet-rj.br/lattes/ppcic-{ano}/PB0-0.html'))
        infosa = htmlInfos(str(f'https://eic.cefet-rj.br/lattes/ppcic-{ano}/PB7-0.html'))
        infosc = htmlInfos(str(f'https://eic.cefet-rj.br/lattes/ppcic-{ano}/PB4-0.html'))

        for i in infosp:
            result = parseJournalPublication(i.upper())
            resultsJournals.append(result)
            doc, dis = normalizer(result[0])
            rJauthorsnorm.append(doc)
            discauthorsJ.append(dis)

        for i in infosa:
            result = parseJournalPublication(i.upper())
            resultsJournals.append(result)
            doc, dis = normalizer(result[0])
            rJauthorsnorm.append(doc)
            discauthorsJ.append(dis)

        for i in infosc:
            result = parseConferencePublication(i.upper())
            resultsConferences.append(result)
            doc, dis = normalizer(result[0])
            rCauthorsnorm.append(doc)
            discauthorsC.append(dis)

    insertData(periodo, rJauthorsnorm, resultsJournals, discauthorsJ, rCauthorsnorm, resultsConferences, discauthorsC)

main()