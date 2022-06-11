import json
import database as db
import pandas as pd
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
        referencia1          VARCHAR(50),
        referencia2          VARCHAR(50),
        PRIMARY KEY (nome, referencia1, referencia2)
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
with open('PPCICresearchers.json', encoding='utf-8') as fileR:
    researchers = json.load(fileR)
    
    for category in researchers:
        for researcher in researchers[category]:
            for citations in researchers[category][researcher]:
                sql = f"INSERT INTO researchers (nome, referencia) VALUES ('{researcher.upper()}', '{citations.upper()}')"
                db.insert_db(sql)

# students
with open('discentes.csv', encoding='utf-8') as arq:
    table = csv.reader(arq)
    
    for line in table:
        if (line[0]!='nome'):
            sql = f"INSERT INTO students (nome, referencia1, referencia2) VALUES ('{line[0].upper()}', '{line[1].upper()}', '{line[2].upper()}')"
            db.insert_db(sql)

# qualis
with open('qualis.csv', encoding='utf-8') as fileQ:
    table = csv.reader(fileQ)
    
    for line in table:
        if 'ISSN' not in line:
            line[1] = line[1].replace("'", '"')
            sql = f"INSERT INTO qualis (issn, nome, qualis) VALUES ('{line[0]}', '{line[1]}', '{line[2]}')"
            db.insert_db(sql)
