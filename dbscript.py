from sqlalchemy import create_engine
import imp
config = imp.load_source('config', 'instance/config.py')

USERNAME = config.USERNAME 
PASSWORD = config.PASSWORD 
DEFAULT_DBNAME = config.DB_NAME
CONN_URL = 'postgresql+psycopg2://%s:%s@%s/%s'

def get_conn_url(host='localhost', dbname="template1", username=None, password=None):
    if username is None:
        username = USERNAME
    if password is None:
        password = PASSWORD
    return CONN_URL % (username, password, host, dbname)

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
