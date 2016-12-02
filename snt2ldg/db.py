
import records
import codecs
import os
from .new_snt_to_ldg import get_dep_str
from .pickle_util import get_bible_pickle
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


def sample_snt_to_ldg_in_table(id, table='pons', lan='ch'):
    """
    id range from the table
    :param id:
    :param table:
    :param lan:
    :return: a graph in cnll10 format
    """
    global psqlDataBase
    tableInfo = find_table(table=table, lan=lan)
    if tableInfo:
        db = records.Database(psqlDataBase)
        ldgColumn = tableInfo['ldg']
        sqlStr = "SELECT " + ldgColumn + " from " + table
        rows = db.query(sqlStr)
        try:
            return rows[id].get(ldgColumn)
        except:
            return ""
    return ""


def find_table(table='pons', lan='ch'):
    global table_kdic
    for dic in table_kdic:
        if dic['lan'] == lan and dic['table'] == table:
            return dic
    return False


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



def insert_2snt_into_db_table(db='language_graph', dbuser='postgres', table='ldc2002t01',
                              id = 0, fname='', en_sub='', seg_id=0, ch_snt='', en_snt=''):
    """
        table ldc2002t01: id | fname | en_sub |  seg_id  |ch_snt | en_snt | ch_ldg | ch_sdg | en_ldg | en_sdg
    """
    db = records.Database(psqlDataBase)
    ch_snt = ch_snt.replace("'", "\'")
    en_snt = en_snt.replace("'", "''")
    sql_str = "INSERT INTO " + table + "(id, fname, en_sub,  seg_id, ch_snt, en_snt) VALUES({0}, '{1}', '{2}', {3}, '{4}', '{5}')".format(id, fname, en_sub, seg_id, ch_snt, en_snt)
    print(sql_str)
    db.query(sql_str)




def insert_snt_into_db_table(fname, encode='utf-8', db='language_graph', dbuser='postgres', table=''):
    """
    table ldc2002t01: id | fname | en_sub | ch_snt | en_snt | ch_ldg | ch_sdg | en_ldg | en_sdg
    table chbible: id | bbid | snt | snt_lg | snt_sdg
    table debible: id | bbid | snt | snt_lg | snt_sdg
    table enbible: id | bbid | snt | snt_lg | snt_sdg

    :param fname:
    :param encode:
    :param db:
    :param dbuser:
    :param table:
    :return:
    """
    db = records.Database(psqlDataBase)
    fhandle = codecs.open(os.path.join("..", fname), "r", encode)
    i = 0
    for line in fhandle.readlines():
            line = line.strip('\n').strip('\r')
            bbid = ''
            snt = ''
            lst = line.split(' ')
            if len(lst) < 3:
                bbid = lst[0] + ' ' + lst[1]
            elif ':' in lst[1]:
                bbid = lst[0] + ' ' + lst[1]
                snt = ' '.join(lst[2:])
            else:
                print('**', lst)
            print(bbid, snt)
            db.query("INSERT INTO "+table+"(id, bbid, snt) VALUES(%s, %s, %s)",(i, bbid, snt))
            i += 1



def insert_lg_into_table(fname, lan='', encode='utf-8', db='language_graph', dbuser='postgres', table=''):
    """
    ldg is the conll 10 format
    :param fname:
    :param lan:
    :param encode:
    :param db:
    :param dbuser:
    :param table:
    :return:
    """
    db = records.Database(psqlDataBase)
    fhandle = codecs.open(os.path.join("..", fname), "r", encode)
    for line in fhandle.readlines():
            line = line.strip('\n').strip('\r')
            bbid = ''
            snt = ''
            lst = line.split(' ')
            if len(lst) < 3:
                bbid = lst[0] + ' ' + lst[1]
            elif ':' in lst[1]:
                bbid = lst[0] + ' ' + lst[1]
                snt = ' '.join(lst[2:])
            else:
                print('**', lst)
            print(bbid, snt)
            lg = get_dep_str(snt, lan=lan)
            db.query("INSERT INTO " + table + "(snt_lg) VALUES(%s) where bbid=%s", (lg, bbid))


"""
def copy_sqlite_table_into_postgres():
    #
    # To do
    # load snt table into postgres
    # :return:
    #
    try:
        con = psycopg2.connect(host='localhost', database="language_graph", user="postgres")

        print('connecting postgre')
        cur = con.cursor()
        import sqlite3
        conn_sqlite = sqlite3.connect(os.path.join("..", 'PONS.db'))
        c_sqlite = conn_sqlite.cursor()
        for row in c_sqlite.execute("SELECT * FROM snt"):
            print(row)
            id = row[0]
            ch_snt = row[2]
            de_snt = row[1]
            sql_str = "INSERT INTO pons (id, ch_snt, de_snt) VALUES({0}, '{1}', '{2}')".format(id,  ch_snt, de_snt)
            print(sql_str)
            cur.execute(sql_str)
        con.commit()
    except psycopg2.DatabaseError:
        if con:
            con.rollback()
        print('Error %s' % psycopg2.DatabaseError)
        sys.exit(1)
    finally:
        if con:
            con.close()

"""

#
# load LDG to three tables
#
def load_ldg_into_table(lan=''):
    """
    table 1: chbible: id | bbid | snt | snt_lg | snt_sdg
    table 2: debible: id | bbid | snt | snt_lg | snt_sdg
    table 3: enbible: id | bbid | snt | snt_lg | snt_sdg
    table 4: pons:    id | ch_snt | de_snt | ch_ldg | ch_sdg | de_ldg | de_sdg
    table 5: ldc2002t01: id | fname | en_sub | ch_snt | en_snt | seg_id | ch_ldg | ch_sdg | en_ldg | en_sdg
    :param lan:
    :return:
    """
    batch_lst =[
        #{"lan": "de",  "table": "pons",  "snt": "de_snt",  "ldg": "de_ldg"},
        {"lan": "ch", "table": "pons", "snt": "ch_snt", "ldg": "ch_ldg"},
        {"lan": "ch",  "table": "ldc2002t01",  "snt": "ch_snt",  "ldg": "ch_ldg"},
        #{"lan": "en",  "table": "ldc2002t01", "snt": "en_snt",  "ldg": "en_ldg"},
        #{"lan": "de", "table": "debible", "snt": "snt", "ldg": "snt_lg"},
        #{"lan": "ch", "table": "chbible", "snt": "snt", "ldg": "snt_lg"},
        #{"lan": "en", "table": "enbible", "snt": "snt", "ldg": "snt_lg"},
        ]
    db = records.Database(psqlDataBase)
    for dic in batch_lst:
            lan = dic['lan']
            table = dic['table']
            snt = dic['snt']
            ldg_col = dic['ldg']
            rows = db.query("SELECT id," + snt +", "+ldg_col+ " FROM "+ table )
            for row in rows:
                print(type(row[2]))
                if row[2] is None or row[2] == '':
                    id = row[0]
                    print(row[1])
                    ldg = get_dep_str(row[1], lan=lan).replace('\t', ' ').replace('\n', ' * ').replace("'", "''")
                    print(dic, row)
                    print(ldg)
                    sql_str = """update {0} set {1} = '{2}' where id = {3}""".format(table, ldg_col, ldg, id)
                    print(sql_str)
                    db.query(sql_str)


def load_bible_ldg_into_table():
        """
        table 1: chbible: id | bbid | snt | snt_lg | snt_sdg
        table 2: debible: id | bbid | snt | snt_lg | snt_sdg
        table 3: enbible: id | bbid | snt | snt_lg | snt_sdg
        do in parallel
        :param lan:
        :return:
        """
        batch_lst = [
            {"lan": "ch", "table": "chbible", "snt": "snt", "ldg": "snt_lg"},
            {"lan": "de", "table": "debible", "snt": "snt", "ldg": "snt_lg"},
            {"lan": "en", "table": "enbible", "snt": "snt", "ldg": "snt_lg"}
        ]
        db = records.Database(psqlDataBase)
        print('connecting postgre')

        ch_lan = batch_lst[0]['lan']
        de_lan = batch_lst[1]['lan']
        en_lan = batch_lst[2]['lan']
        ch_table = batch_lst[0]['table']
        de_table = batch_lst[1]['table']
        en_table = batch_lst[2]['table']
        snt = batch_lst[0]['snt']
        ldg_col = batch_lst[0]['ldg']

        ch_rows = db.query("SELECT id," + snt + ", " + ldg_col+ " FROM " + ch_table )
        de_rows = db.query("SELECT id," + snt + ", " + ldg_col+ " FROM " + de_table)
        en_rows = db.query("SELECT id," + snt + ", " + ldg_col+ " FROM " + en_table)

        for i in range(len(ch_rows)):
                print(i,ch_rows[i])
                id = ch_rows[i][0]
                if ch_rows[i][2] is None:
                    ldg_ch =  get_dep_str(ch_rows[i][1], lan=ch_lan, ch_parser='stanford').replace('\t', ' ').replace("'", "''")
                    sql_str = """UPDATE {0} SET {1} = '{2}' WHERE id = {3}""".format(ch_table, ldg_col, ldg_ch, id)
                    print(sql_str)
                    db.query(sql_str)

                id = de_rows[i][0]
                print(i, de_rows[i][0])
                if de_rows[i][2] is None:
                    ldg_de =  get_dep_str(de_rows[i][1], lan=de_lan).replace('\t', ' ').replace('\n', ' * ').replace("'", "''")
                    sql_str = """UPDATE {0} SET {1} = '{2}' WHERE id = {3}""".format(de_table, ldg_col, ldg_de, id)
                    print(sql_str)
                    db.query(sql_str)

                id = en_rows[i][0]
                print(i, en_rows[i][0])
                if en_rows[i][2] is None:
                    ldg_en =  get_dep_str(en_rows[i][1], lan=en_lan).replace('\t', ' ').replace('\n', ' * ').replace("'", "''")
                    sql_str = """UPDATE {0} SET {1} = '{2}' WHERE id = {3}""".format(en_table, ldg_col, ldg_en, id)
                    print(sql_str)
                    db.query(sql_str)


def load_bible_ldg_into_table_from_pickle(lans=['de','ch','en']):
    """
    table 1: chbible: id | bbid | snt | snt_lg | snt_sdg
    table 2: debible: id | bbid | snt | snt_lg | snt_sdg
    table 3: enbible: id | bbid | snt | snt_lg | snt_sdg
    do in parallel
    :param lan:
    :return:
    """
    batch_lst = [
        {"lan": "ch", "table": "chbible", "snt": "snt", "ldg": "snt_lg"},
        {"lan": "de", "table": "debible", "snt": "snt", "ldg": "snt_lg"},
        {"lan": "en", "table": "enbible", "snt": "snt", "ldg": "snt_lg"}
    ]
    db = records.Database(psqlDataBase)
    print('connecting postgre')

    ch_lan = batch_lst[0]['lan']
    de_lan = batch_lst[1]['lan']
    en_lan = batch_lst[2]['lan']
    ch_table = batch_lst[0]['table']
    de_table = batch_lst[1]['table']
    en_table = batch_lst[2]['table']
    snt = batch_lst[0]['snt']
    ldg_col = batch_lst[0]['ldg']

    ch_rows = db.query("SELECT id," + snt + ", " + ldg_col + " FROM " + ch_table)
    de_rows = db.query("SELECT id," + snt + ", " + ldg_col + " FROM " + de_table)
    en_rows = db.query("SELECT id," + snt + ", " + ldg_col + " FROM " + en_table)

    dePickle = get_bible_pickle(lan='de')
    enPickle = get_bible_pickle(lan='en')
    chPickle = get_bible_pickle(lan='ch')

    count = 0

    if 'de' in lans:
        id = len(de_rows)
        tx = db.transaction()
        try:
            for key, ldg in dePickle.items():
                ldg = ldg.replace('\t', ' ').replace('\n', ' * ').replace("'", "''")
                snt = ' '.join([w[1] for w in [words.strip().split(' ') for words in ldg.split('*')]])
                sql_str = """INSERT INTO {0} VALUES({1}, '{2}', '{3}', '{4}')""".format(de_table, id, key, snt, ldg)
                print(sql_str)
                db.query(sql_str)

                id += 1
                count += 1
            tx.commit()
        except:
            tx.rollback()

    return count
