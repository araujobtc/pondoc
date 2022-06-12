import database as db
import pandas as pd

# retorna lista com nome dos docentes e discentes que participaram normalizada. (SILVA, M. P. -> MARIA PEREIRA DA SILVA)
def normalizer(l):
    doc, dis = [], []
    for ref in l:
        surnameref = ref[0].strip() + ', '
        nameref = (surnameref+ ' '.join(ref[1:])).upper()

        docentes=pd.DataFrame(db.consult_db("SELECT referencia FROM researchers"))
        for ref in docentes[0]:
            if nameref == ref:
                sql = f"SELECT nome FROM researchers WHERE referencia = '{ref}'"
                fullname = pd.DataFrame(db.consult_db(sql))[0][0]
                doc.append(fullname)

        discentes=pd.DataFrame(db.consult_db("SELECT referencia FROM students"))
        for ref in discentes[0]:
            if nameref == ref:
                sql = f"SELECT nome FROM students WHERE referencia = '{ref}'"
                fullname = pd.DataFrame(db.consult_db(sql))[0][0]
                dis.append(fullname)
              
    return doc, dis
