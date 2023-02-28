from random import choice
from string import ascii_uppercase, digits

def randStr(N=16, chars = ascii_uppercase + digits): # Generate random string of length 16
	return ''.join(choice(chars) for _ in range(N))

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn