from sqlalchemy import create_engine
from itsdangerous import URLSafeSerializer

_serializer = URLSafeSerializer('ImRhdGFiYXNlIg.shLu-DN7Hsq9827VtuFf2IWaE6o')
USERNAME = _serializer.loads('InFpdWxpIg.SG37e0WIwAYnZ1QfdRTwZfA6iBk')
PASSWORD = _serializer.loads('Ijg2MDIyNnFsLiI.4dnVbZ6UCWbZ3NK2i9rkEPQlz_4')

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

