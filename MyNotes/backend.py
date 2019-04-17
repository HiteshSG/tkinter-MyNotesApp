import pymysql as mydb


HOST = 'localhost' #place your host here
USR = 'root' #place your username of mysql here
DB = 'sample_db' #place name of your db name
PWD = '' #place password of mysql here

def execute_query(query):

    with mydb.connect(HOST,USR,PWD,DB) as con:
        con.execute(query)
        all_notes_title = [(title[0],title[1],title[2]) for title in con.fetchall()]

    return all_notes_title


def execute_query_1(query):

    with mydb.connect(HOST,USR,PWD,DB) as con:
        con.execute(query)
        all_notes_title = con.fetchall()[0]

    return all_notes_title


def update_note(query):
    with mydb.connect(HOST,USR,PWD,DB) as con:
        con.execute(query)


def delete_note(query):
    with mydb.connect(HOST,USR,PWD,DB) as con:
        con.execute(query)
        

def store_note(query):
    with mydb.connect(HOST,USR,PWD,DB) as con:
        con.execute(query)
