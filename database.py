import sqlite3
import hashlib
import datetime


'''
Global variables to store the file location of 
the database files.
'''
agent_db_file = "database/agents.db"
hospital_db_file = "database/hospitals.db"
places_db_file = "database/places.db"
visitor_db_file = "database/visitors.db"
visitor_to_places_db_file = "database/visitor_to_places.db"

'''
    Registrations for Hospitals, places, visitors and admins
'''

def register_hospitals(id, uname, pw):
    # Hospitals are allowed to register but the can only 
    # login when their status is approved by the admin
    # Status Code meanings are
    # 0 waiting for Approved
    # 1 for Approved
    # 2 rejected
    _conn = sqlite3.connect(hospital_db_file)
    _cur = _conn.cursor()
    _cur.execute("INSERT INTO Hospitals values(?, ?, ?, ?)", (id,  uname, hashlib.sha256(pw.encode()).hexdigest(), 0))
    _conn.commit()
    _conn.close()

def register_visitors(id, uname, pw, name, addr, contact_type, pnum, email, deviceid, infected):
    _conn = sqlite3.connect(visitor_db_file)
    _cur = _conn.cursor()
    _cur.execute("INSERT INTO Visitors values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (id , uname , hashlib.sha256(pw.encode()).hexdigest() , name , addr , contact_type , pnum , email , deviceid , infected)) 
    _conn.commit()
    _conn.close()

def register_places(id, uname, pw, pname, addr, qr):
    _conn = sqlite3.connect(places_db_file)
    _cur = _conn.cursor()
    _cur.execute("INSERT INTO Places values(?, ?, ?, ?, ?, ?)", (id,uname, hashlib.sha256(pw.encode()).hexdigest(), pname, addr, qr))
    _conn.commit()
    _conn.close()


'''
    For Adding new agents into the system 
'''

def add_agent(id, uname, pw):
    # A method only accessable for logged in agents only
    _conn = sqlite3.connect(agent_db_file)
    _cur = _conn.cursor()
    _cur.execute("INSERT INTO Agents values(?, ?, ?)", (id, uname, hashlib.sha256(pw.encode()).hexdigest()))
    _conn.commit()
    _conn.close()


'''
    Login methods for Agents, Visitors, Places and Hospitals
'''

def verify_agent(uname, pw):
    _conn = sqlite3.connect(agent_db_file)
    _cur = _conn.cursor()
    _cur.execute("SELECT password FROM Agents WHERE username = '" + uname + "';")
    result = _cur.fetchone()[0] == hashlib.sha256(pw.encode()).hexdigest()
    _conn.close()
    return result

def verify_visitor(uname, pw):
    _conn = sqlite3.connect(visitor_db_file)
    _cur = _conn.cursor()
    _cur.execute("SELECT password FROM Visitors WHERE username = '" + uname + "';")
    result = _cur.fetchone()[0] == hashlib.sha256(pw.encode()).hexdigest()
    _conn.close()
    return result

def verify_place(uname, pw):
    _conn = sqlite3.connect(places_db_file)
    _cur = _conn.cursor()
    _cur.execute("SELECT password FROM Places WHERE username = '" + uname + "';")
    result = _cur.fetchone()[0] == hashlib.sha256(pw.encode()).hexdigest()
    _conn.close()
    return result

def verify_hospitals(uname, pw):
    _conn = sqlite3.connect(hospital_db_file)
    _cur = _conn.cursor()
    _cur.execute("SELECT password FROM Hospitals WHERE username = '" + uname + "';")
    result = _cur.fetchone()[0] == hashlib.sha256(pw.encode()).hexdigest()
    _conn.close()
    return result

'''
    The following method simplifies the login process
'''

def list_visitors():
    _conn = sqlite3.connect(visitor_db_file)
    _curr = _conn.cursor()
    _curr.execute("SELECT username FROM Visitors;")
    result = [x[0] for x in _curr.fetchall()]
    _conn.close()
    return result

def list_agents():
    _conn = sqlite3.connect(agent_db_file)
    _curr = _conn.cursor()
    _curr.execute("SELECT username FROM Agents;")
    result = [x[0] for x in _curr.fetchall()]
    _conn.close()
    return result

def list_places():
    _conn = sqlite3.connect(places_db_file)
    _curr = _conn.cursor()
    _curr.execute("SELECT username FROM Places;")
    result = [x[0] for x in _curr.fetchall()]
    _conn.close()
    return result

def list_hospitals():
    _conn = sqlite3.connect(hospital_db_file)
    _curr = _conn.cursor()
    _curr.execute("SELECT username FROM Hospitals;")
    result = [x[0] for x in _curr.fetchall()]
    _conn.close()
    return result

'''
    Method to add a visit into the database 
    (makes possible the connection between a visitor and a place)
'''
def visit(id, qrcode, device, entrytime, endtime):
    _conn = sqlite3.connect(visitor_to_places_db_file)
    _cur = _conn.cursor()
    _cur.execute("INSERT INTO VisitorsToPlace values(?, ?, ?, ?, ?)", (id, qrcode, str(device), entrytime, endtime))
    _conn.commit()
    _conn.close()


'''
    Unnecessary to execute but for reference, this is
    how to create tables in the db files
'''

def create_tables():
    query_agent = 'CREATE TABLE Agents (agent_id INT NOT NULL, username VARCHAR, password VARCHAR, PRIMARY KEY (agent_id, username))'
    query_hospitals = 'CREATE TABLE Hospitals (hospital_id INT NOT NULL, username VARCHAR, password VARCHAR, status INT, PRIMARY KEY (hospital_id, username))'
    query_places = 'CREATE TABLE Places (place_id INT NOT NULL, username VARCHAR, password VARCHAR, place_name VARCHAR, address VARCHAR, qrcode VARCHAR, PRIMARY KEY (place_id, username))'
    query_visitors = 'CREATE TABLE Visitors (citizen_id INT NOT NULL, username VARCHAR, password VARCHAR, visitor_name VARCHAR, address VARCHAR, contact_type VARCHAR, phone_number VARCHAR, email VARCHAR, device_id VARCHAR, infected BOOL, PRIMARY KEY (citizen_id, username))'
    visitor_to_places = 'CREATE TABLE VisitorsToPlace (vtp_id INT NOT NULL, qrcode VARCHAR, device_id VARCHAR, entry_time DATETIME, exit_time DATETIME, PRIMARY KEY (vtp_id, device_id), FOREIGN KEY (qrcode) REFERENCES Places(qrcode), FOREIGN KEY (device_id) REFERENCES Visitors(device_id))'
    try:
        with sqlite3.connect(agent_db_file) as _conn:
            _cur = _conn.cursor()
            _cur.execute(query_agent)
            _conn.commit()
            print("Agent table successfully created")
    except Exception as e:
        print("Oops!", e.__class__, "occurred. (Related to Agent)")
    
    try:
        with sqlite3.connect(hospital_db_file) as _conn:
            _cur = _conn.cursor()
            _cur.execute(query_hospitals)
            _conn.commit()
            print("Hospitals table successfully created")
    except Exception as e:
        print("Oops!", e.__class__, "occurred. (Related to Hospital)")

    try:
        with sqlite3.connect(places_db_file) as _conn:
            _cur = _conn.cursor()
            _cur.execute(query_places)
            _conn.commit()
            print("Places table successfully created")
    except Exception as e:
        print("Oops!", e.__class__, "occurred. (Related to Place)")

    try:
        with sqlite3.connect(visitor_db_file) as _conn:
            _cur = _conn.cursor()
            _cur.execute(query_visitors)
            _conn.commit()
            print("Visitors table successfully created")
    except Exception as e:
        print("Oops!", e.__class__, "occurred. (Related to Visitor)")

    try:
        with sqlite3.connect(visitor_to_places_db_file) as _conn:
            _cur = _conn.cursor()
            _cur.execute(visitor_to_places)
            _conn.commit()
            print("VisitorsToPlaces table successfully created")
    except Exception as e:
        print("Oops!", e.__class__, "occurred. (VisitorsToPlaces to Agent)")

'''
    Query for resetting the database
'''
def drop_all_tables():
    query_agent = "DROP TABLE IF EXISTS Agents"
    query_hospital = "DROP TABLE IF EXISTS Hospitals"
    query_visitor = "DROP TABLE IF EXISTS Visitors"
    query_place = "DROP TABLE IF EXISTS Places"
    query_visitstoplace = "DROP TABLE IF EXISTS VisitorsToPlace"
    try:
        with sqlite3.connect(agent_db_file) as _conn:
            _cur = _conn.cursor()
            _cur.execute(query_agent)
            _conn.commit()
            
        with sqlite3.connect(hospital_db_file) as _conn:
            _cur = _conn.cursor()
            _cur.execute(query_hospital)
            _conn.commit()
            
        with sqlite3.connect(visitor_db_file) as _conn:
            _cur = _conn.cursor()
            _cur.execute(query_visitor)
            _conn.commit()
            
        with sqlite3.connect(places_db_file) as _conn:
            _cur = _conn.cursor()
            _cur.execute(query_place)
            _conn.commit()
            
        with sqlite3.connect(visitor_to_places_db_file) as _conn:
            _cur = _conn.cursor()
            _cur.execute(query_visitstoplace)
            _conn.commit()

    except Exception as e:
        print("Oops!", e.__class__, "occurred. (Related to Agent)")


if __name__ == "__main__":
    print("Hi!")
