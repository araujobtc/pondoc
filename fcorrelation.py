import pandas as pd
import database as db

def dictFaculty():
    rd = {}
    docentes=pd.DataFrame(db.consult_db("SELECT nome FROM researchers"))
    for i in docentes[0]:
        rd[i]=[]
    return rd


def facultyCorrelation(list):
    rd = dictFaculty()
    for i in list:
        for r in rd:
            if r in i: rd[r].append(1)
            elif r not in i: rd[r].append(0)
    return rd
