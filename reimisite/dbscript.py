from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os
import imp
import config

dbconfig = imp.load_source('config', os.path.join(config.ROOT_PATH, 'instance/config.py'))
config.__dict__.update(dbconfig.__dict__)

USERNAME = config.USERNAME 
PASSWORD = config.PASSWORD 
DEFAULT_DBNAME = config.DB_NAME
CONN_URL = 'postgresql+psycopg2://%s:%s@%s/%s'

Session = scoped_session(sessionmaker())

def get_conn_url(host='localhost', dbname="template1", username=None, password=None):
    if username is None:
        username = USERNAME
    if password is None:
        password = PASSWORD
    return CONN_URL % (username, password, host, dbname)

session_engine = create_engine(get_conn_url(dbname=DEFAULT_DBNAME), echo=config.SQLALCHEMY_ECHO)
Session.configure(bind=session_engine, autoflush=False, expire_on_commit=False)

def execute_on(sql, conn=None, dbname=None, callback=None):
    if not conn:
        if not dbname:
            raise ValueError('dbname can not be empty!')
        engine = create_engine(get_conn_url(dbname=dbname))
        conn = engine.connect()
        close = True
    else:
        close = False
    result = conn.execute(sql)
    ret = None
    if callback is not None and callable(callback):
        ret = callback(result)
    else: 
        ret = [rt for rt in result]
    result.close()
    if close:
        conn.close()
    return ret

def get_all_tables_in_db(conn=None, dbname=None):
    sql = "select table_name from information_schema.tables where table_schema = 'public';" 
    return execute_on(sql, conn=conn, dbname=dbname, callback = lambda x: [tbname for (tbname,) in x])

def get_all_sequence_in_db(conn=None, dbname=None):
    sql = "select sequence_name from information_schema.sequences where sequence_schema = 'public'"
    return execute_on(sql, conn=conn, dbname=dbname, callback = lambda x: [sqname for (sqname,) in x])
    
def drop_all_tables_seqences(dbname):
    engine = create_engine(get_conn_url(dbname=dbname), echo=True)
    conn = engine.connect()
    for table in get_all_tables_in_db(conn = conn):
        conn.execute('drop table %s cascade' % table)
    for seq in get_all_sequence_in_db(conn = conn):
        conn.execute('drop sequence %s cascade' % seq)
    conn.close()

def get_default_engine(echo=False):
    return create_engine(get_conn_url(), echo=echo)

def create_database(dbname, echo=False):
    engine = get_default_engine(echo)
    conn = engine.connect()
    conn.execute('commit')
    conn.execute('drop database if exists %s;' % dbname)
    conn.execute('commit')
    conn.execute('create database %s;' % dbname)
    conn.close()

if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    if len(args) != 0:
        create_database(args[0], bool(args[1] if len(args) > 1 else False))
    else:
        create_database(DEFAULT_DBNAME, True)
