import re
import pandas as pd

def qualisInfos(line):
    # ISSN
    regex=r'[\S]{4}\-[\S]{4}'
    pattern = re.compile(regex, re.UNICODE)
    issn = pattern.findall(line)
    issn = ''.join(issn)

    # Classificação
    classificacao_qualis = line[-3:]

    # Nome
    nome = (line[9:-3].strip())

    return issn, nome, classificacao_qualis

def toCsv(cel):
    table = pd.DataFrame(cel, columns=['ISSN', 'Nome', 'Qualis'])
    table.to_csv('qualis.csv', index=False)

with open('Qualis.txt') as file:
    cel = []
    for line in file:
        issn, nome, qualis = qualisInfos(line)
        cel.append([issn, nome, qualis[:2]])
    toCsv(cel)