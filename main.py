from reader import htmlInfos
from transcriber import insertData

def main(urlp, urlc):
    infosp = htmlInfos(urlp)
    infosc = htmlInfos(urlc)

    insertData(infosp, infosc)