from normalizer import normalizer
from reader import htmlInfos
from transcriber import insertData
from analyzer import parsePublication
import argparse

def main():
    parser = argparse.ArgumentParser(description='PONDOC')
    parser.add_argument('-y','--year', type=str, help='ex: "2017" or "2021-2024"')
    parser.add_argument('-f','--file', type=str, default='default.xlsx', help="file's name + .xlsx")
    args = parser.parse_args()
    anos = args.year
    file = args.file

    if len(str(anos))==4: period = [str(anos)]*2
    elif len(anos)==9: period = anos.split('-')
    
    resultsJournals, resultsConferences = [], []
    rJauthorsnorm, rCauthorsnorm, discauthorsJ, discauthorsC= [], [], [], []

    for ano in range(int(period[0]), int(period[1])+1):
        infosp = htmlInfos(str(f'https://eic.cefet-rj.br/lattes/ppcic-{ano}/PB0-0.html'))
        infosa = htmlInfos(str(f'https://eic.cefet-rj.br/lattes/ppcic-{ano}/PB7-0.html'))
        infosc = htmlInfos(str(f'https://eic.cefet-rj.br/lattes/ppcic-{ano}/PB4-0.html'))

        print(f'Tratando dados de Periodicos - {ano}')
        for i in infosp:
            result = parsePublication(i.upper())
            resultsJournals.append(result)
            doc, dis = normalizer(result[0])
            rJauthorsnorm.append(doc)
            discauthorsJ.append(dis)

        print(f'Tratando dados de Publicações Aceitas - {ano}')
        for i in infosa:
            result = parsePublication(i.upper())
            resultsJournals.append(result)
            doc, dis = normalizer(result[0])
            rJauthorsnorm.append(doc)
            discauthorsJ.append(dis)

        print(f'Tratando dados de Conferência - {ano}')
        for i in infosc:
            result = parsePublication(i.upper())
            resultsConferences.append(result)
            doc, dis = normalizer(result[0])
            rCauthorsnorm.append(doc)
            discauthorsC.append(dis)

    print('Inserindo dados...')
    insertData(period, file, rJauthorsnorm, resultsJournals, discauthorsJ, rCauthorsnorm, resultsConferences, discauthorsC)

main()
