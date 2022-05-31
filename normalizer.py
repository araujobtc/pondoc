import database as db
import pandas as pd

def normalizer(l):
    n = []
    for ref in l:
        surnameref = ref[0].strip() + ', '
        ref.pop(0)
        nameref = (surnameref+ ' '.join(ref)).upper()

        docentes=pd.DataFrame(db.consult_db("SELECT referencia FROM researchers"))

        for i in docentes[0]:
            if nameref == i:
                sql = f"SELECT nome FROM researchers WHERE referencia = '{i}'"
                fullname = pd.DataFrame(db.consult_db(sql))[0][0]
                n.append(fullname)
    return n
