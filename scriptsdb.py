import json
import database as db
import csv

tables = ['researchers', 'students', 'qualis']

# Dropando a tabelas caso elas já existam
for table in tables:
    sql = f'DROP TABLE IF EXISTS {table}'
    db.create_db(sql)

# Criando a tabelas
sql = '''CREATE TABLE researchers( 
        nome                VARCHAR(255), 
        referencia          VARCHAR(50),
        PRIMARY KEY (nome, referencia)
        )'''

db.create_db(sql)

sql = '''CREATE TABLE students( 
        nome                VARCHAR(255), 
        referencia          VARCHAR(50),
        PRIMARY KEY (nome, referencia)
        )'''

db.create_db(sql)

sql = '''CREATE TABLE qualis(
        issn          VARCHAR(9), 
        nome          VARCHAR(255), 
        qualis        VARCHAR(2),
        PRIMARY KEY (issn, nome)
        )'''

db.create_db(sql)

# inserindo dados na tabela
# researchers 
with open('PPCICresearchers.json', encoding='utf-8') as arq:
    researchers = json.load(arq)
    
    for category in researchers:
        for researcher in researchers[category]:
            for citations in researchers[category][researcher]:
                db.insert_db(f"INSERT INTO researchers (nome, referencia) VALUES ('{researcher.upper()}', '{citations.upper()}')")

# students
with open('discentes.csv', encoding='utf-8') as arq:
    discentes = csv.reader(arq)
    
    for line in discentes:
        if 'nome' not in line:
            db.insert_db(f"INSERT INTO students (nome, referencia) VALUES ('{line[0].upper()}', '{line[1].upper()}')")
            db.insert_db(f"INSERT INTO students (nome, referencia) VALUES ('{line[0].upper()}', '{line[2].upper()}')")
# qualis
with open('qualis.csv', encoding='utf-8') as arq:
    qualis = csv.reader(arq)
    
    for line in qualis:
        if 'ISSN' not in line:
            line[1] = line[1].replace("'", '"')
            db.insert_db(f"INSERT INTO qualis (issn, nome, qualis) VALUES ('{line[0]}', '{line[1]}', '{line[2]}')")
