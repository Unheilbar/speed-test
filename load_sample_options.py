import speedtest
import psycopg2
from configparser import ConfigParser

def config(filename='dbase.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


conn = None

def connect():
    # Connect to the PostgreSQL database server 

    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()

        #add sample server uls
        create_table(cur)


        cur.close()

        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        disconnect()
        
def disconnect():
    if conn is not None:
            conn.close()
            print('Database connection closed.')


def create_table(cur):
    init_command = (
        """
        CREATE TABLE options (
            servers_id INTEGER,
            enable BOOLEAN,
            url_download VARCHAR(255),
            url_upload VARCHAR(255),
            dscr VARCHAR(255)
        )
        """)

    cur.execute(init_command)

    s = speedtest.Speedtest()

    servers = s.get_servers()
    for i in servers:
        server_id = servers[i][0]['id']
        enable = True
        server_url = '' + servers[i][0]['url']
        server_dscr = servers[i][0]['name'] + ' ' + servers[i][0]['sponsor']
        command = f'''INSERT INTO options
                        VALUES ({server_id}, enable, {server_url}, {server_url}, {server_dscr}'''
        cur.execute(command)
        print(servers[i][0])




connect()





#s.download()
#s.upload()
#print(s.results)

