import psycopg2

# Função para criar conexão no banco
def conect_db():
    db = psycopg2.connect(host='localhost', 
                        dbname='infosProducao',
                        user='postgres', 
                        password='postgres',
                        port='5432')
    return db

  # Função para criar ou dropar uma tabela no banco
def create_drop_db(sql):
    con = conect_db()
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()
    
# Função para inserir dados no banco
def insert_delete_db(sql):
    con = conect_db()
    cur = con.cursor()
    try:
        cur.execute(sql)
        con.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        con.rollback()
        cur.close()
        return 1
    cur.close()

    
def consult_db(sql):
    con = conect_db()
    cur = con.cursor()
    cur.execute(sql)
    recset = cur.fetchall()
    registros = []
    for rec in recset:
        registros.append(rec)
    con.close()
    return registros
    