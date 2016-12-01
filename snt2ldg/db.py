
import records

"""
postgres database: langauge_graph
tables: chbible, debible, enbible, ldc200201_back, ldc2002t01, pons, pons_back
"""

"""
connect to postgres database
rows = db.query("SELECT tablename from pg_tables where schemaname='public'")
"""

psqlDataBase = 'postgres://localhost/language_graph'

"""
connect to sqlite database
rows = db.query("select * from sqlite_master where type ='table'")
"""

sqliteDataBase = 'sqlite:///data/PONS.db'


table_kdic = [
    {"lan": "de",  "table": "pons",  "snt": "de_snt",  "ldg": "de_ldg"},
    {"lan": "ch", "table": "pons", "snt": "ch_snt", "ldg": "ch_ldg"},
    {"lan": "ch", "table": "ldc2002t01", "snt": "ch_snt", "ldg": "ch_ldg"},
    {"lan": "en",  "table": "ldc2002t01", "snt": "en_snt",  "ldg": "en_ldg"},
    {"lan": "de", "table": "debible", "snt": "snt", "ldg": "snt_lg"},
    {"lan": "ch", "table": "chbible", "snt": "snt", "ldg": "snt_lg"},
    {"lan": "en", "table": "enbible", "snt": "snt", "ldg": "snt_lg"},
    ]


def get_raw_ldg_with_id_from_pons(id, table='PONS', lan='ch'):
    assert table == 'PONS'
    global table_kdic, psqlDataBase, sqliteDataBase
    db = records.Database(psqlDataBase)
    if table == 'PONS' and lan == 'ch':
        sql_str = "SELECT ch_snt, ch_ldg FROM "+ table + " where id="+str(id)
    elif table == 'PONS' and lan == 'de':
        sql_str = "SELECT de_snt, de_ldg FROM "+ table + " where id="+str(id)

    rows = db.query(sql_str)
    for row in rows:
        print(row[1].replace('*', '\n'))
        return row[1]
    return None


def check_database(dbname='sqlite:///data/PONS.db'):
    """
    check whether database exist, or contains tables
    :param dbname:
    :return: -1, if either database not exist, or does not have tables,
             n, number of tables it has
    """
    db = records.Database(dbname)
    tables = db.get_table_names()
    if len(tables) == 0:
        return -1
    else:
        return len(tables)


def list_tables(dbname='sqlite:///data/PONS.db'):
    """
    print all tables in the  database
    :param dbname: database name
    :return: a list of tables in the data base
             [], if it has not tables
    """
    db = records.Database(dbname)
    return db.get_table_names()