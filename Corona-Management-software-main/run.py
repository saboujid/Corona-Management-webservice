import time

from flask import Flask, session, url_for, redirect, render_template, request, abort, flash
from database import add_agent, list_agents, list_visitors, list_hospitals, list_places, verify_agent, verify_hospitals, verify_place, verify_visitor, visit
from database import register_visitors, register_places, register_hospitals
from functions import randStr, create_connection
from flask_mail import Mail, Message
from config import mail_password, mail_username
import sqlite3
import datetime
from datetime import datetime


'''
Global variables to store the file location of 
the database files.
'''
agent_db_file = "database/agents.db"
hospital_db_file = "database/hospitals.db"
places_db_file = "database/places.db"
visitor_db_file = "database/visitors.db"
visitor_to_places_db_file = "database/visitor_to_places.db"


app = Flask(__name__)
app.config.from_object('config')
'''Configuring the mail, so that the users can contact us -(outlook smtp)'''
app.config['MAIL_SERVER'] ="smtp-mail.outlook.com"
app.config["MAIL_PORT"] =587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] =False
app.config["MAIL_USERNAME"] = mail_username
app.config["MAIL_PASSWORD"] = mail_password

mail =Mail(app)

@app.route("/")
def root():
    session['login_form_selector'] = None
    session.modified = True
    return render_template("index.html")


'''
    Login methods for the four type of users 
    that can use the system
'''

@app.route("/login_visitor", methods=["POST"])
def login_visitor():
    username_submitted = request.form.get("username")
    user_type = request.form.get("type")
    if user_type == 'Visitor':
        if (username_submitted in list_visitors()) and verify_visitor(username_submitted, request.form.get("pw")):
            session['current_user'] = username_submitted
            session['current_user_type'] = user_type
            session.modified = True
            return(redirect(url_for("dashboard_visitor")))  
        else:
            return abort(401)
    else:
        session.pop("current_user", None)
        return abort(401)


@app.route("/login_hospital", methods=["POST"])
def login_hospital():
    username_submitted = request.form.get("username")
    user_type = request.form.get("type")
    if user_type == 'Hospital':
        if (username_submitted in list_hospitals()) and verify_hospitals(username_submitted, request.form.get("pw")):
            session['current_user'] = username_submitted
            session['current_user_type'] = user_type
            session.modified = True
            conn = sqlite3.connect(hospital_db_file)
            cur = conn.cursor()
            cur.execute("SELECT status FROM Hospitals WHERE username=\'" + username_submitted + "\'")
            status = cur.fetchone()
            conn.close()
            session['status'] = status[0]
            return(redirect(url_for("dashboard_hospital")))
        else:
            return abort(401)
    else:
        session.pop("current_user", None)
        return abort(401)


@app.route("/login_place", methods=["POST"])
def login_place():
    username_submitted = request.form.get("username")
    user_type = request.form.get("type")
    if user_type == 'Place':
        if (username_submitted in list_places()) and verify_place(username_submitted, request.form.get("pw")):
            session['current_user'] = username_submitted
            session['current_user_type'] = user_type
            session.modified = True
            conn = sqlite3.connect(places_db_file)
            cur = conn.cursor()
            cur.execute("SELECT qrcode FROM Places WHERE username=\'" + username_submitted + "\'")
            qrcode = cur.fetchone()
            conn.close()
            session['qr'] = qrcode[0]
            return(redirect(url_for("dashboard_place")))
        else:
            return abort(401)
    else:
        session.pop("current_user", None)
        return abort(401)


@app.route("/login_agent", methods=["POST"])
def login_agent():
    username_submitted = request.form.get("username")
    user_type = request.form.get("type")
    if user_type == 'Agent':
        if (username_submitted in list_agents()) and verify_agent(username_submitted, request.form.get("pw")):
            session['current_user'] = username_submitted
            session['current_user_type'] = user_type
            session.modified = True
            return(redirect(url_for("dashboard_agent")))
        else:
            return abort(401)
    else:
        session.pop("current_user", None)
        return abort(401)


'''
    Only a loggedin admin can add a new admin
'''
@app.route("/add_new_agent", methods = ["POST"])
def add_new_agent():
    if session.get("current_user_type", None) == "Agents": # only Admin should be able to add user.
        # before we add the user, we need to ensure this is doesn't exsit in database. We also need to ensure the id is valid.
        if request.form.get('username') in list_agents():
            return abort(401)
        if " " in request.form.get('username') or "'" in request.form.get('username'):
           return abort(401)
        else:
            add_agent(round(time.time() * 1000)+request.form.get('username'), request.form.get('username'), request.form.get('password'))
            return(redirect(url_for("agent")))
    else:
        return abort(401)


'''
    The following methods are used for registering a new user onto
    the system

'''
@app.route("/register_visitor", methods = ["POST"])
def register_visitor():
    if request.form.get('username') in list_visitors():
        return abort(401)
    if " " in request.form.get('username') or "'" in request.form.get('username'):
        return abort(401)
    else:
        register_visitors(round(time.time() * 1000) , request.form.get('username') , request.form.get('pw') , request.form.get('name') , request.form.get('address') , request.form.get('contact_type') , request.form.get('phone') , request.form.get('email') , request.form.get('deviceid') , False)
        return(redirect(url_for("login_visitor_page")))

@app.route("/register_hospital", methods = ["POST"])
def register_hospital():
    if request.form.get('username') in list_hospitals():
        return abort(401)
    if " " in request.form.get('username') or "'" in request.form.get('username'):
        return abort(401)
    else:
        register_hospitals(round(time.time() * 1000), request.form.get('username'), request.form.get('pw'))
        return(redirect(url_for("login_hospital_page")))

@app.route("/register_place", methods = ["POST"])
def register_place():
    if request.form.get('username') in list_places():
        return abort(401)
    if " " in request.form.get('username') or "'" in request.form.get('username'):
        return abort(401)
    else:
        register_places(round(time.time() * 1000), request.form.get('username'), request.form.get('pw'), request.form.get('name'),request.form.get('address'),randStr())
        return(redirect(url_for("login_place_page")))   


''' Rendering Registeration Page '''

@app.route("/register_visitor_page")
def register_visitor_page():
    session['login_form_selector'] = "Visitor"
    session.modified = True
    return render_template("registration.html")

@app.route("/register_hospital_page")
def register_hospital_page():
    session['login_form_selector'] = "Hospital"
    session.modified = True
    return render_template("registration.html")

@app.route("/register_place_page")
def register_place_page():
    session['login_form_selector'] = "Place"
    session.modified = True
    return render_template("registration.html")


''' Render Waiting for Approval Hospitals '''

@app.route("/dashboard_hospital")
def dashboard_hospital():
    if session['current_user_type'] == "Hospital":
        if "current_user" in session:
            user = session["current_user"]
            conn2 = sqlite3.connect(visitor_db_file)
            cur2 = conn2.cursor()
            cur2.execute("SELECT username, infected FROM Visitors")
            visitors = cur2.fetchall()
            conn2.close()
            session['visitors'] = visitors
            return render_template("dashboards/dashboard_hospital.html",status=session['status'],visitor=session['visitors'])
        else:
            return render_template("logins.html")
    else:
        return render_template("error_pages/page_401.html")

''' Render Agent Dashboard Page '''

@app.route("/dashboard_agent")
def dashboard_agent():
    if session['current_user_type'] == "Agent":
        if "current_user" in session:
            user = session["current_user"]
            return render_template("dashboards/dashboard_agent.html")
        else:
            return render_template("logins.html")
    else:
        return render_template("error_pages/page_401.html")


''' Render Places Dashboard Page '''

@app.route("/dashboard_place")
def dashboard_place():
    if session['current_user_type'] == "Place":
        if "current_user" in session:
            user = session["current_user"]
            return render_template("dashboards/dashboard_place.html",user=session['current_user'],qr=session['qr'])
        else:
            return render_template("logins.html")
    else:
        return render_template("error_pages/page_401.html")


''' Render Visitors Dashboard Page '''

@app.route("/dashboard_visitor")
def dashboard_visitor():
    if session['current_user_type'] == "Visitor":
        if "current_user" in session:
            user = session["current_user"]
            return render_template("dashboards/dashboard_visitor.html",user = session["current_user"])
        else:
            return render_template("logins.html")
    else:
        return render_template("error_pages/page_401.html")


''' Visitor scans the QRcode and enters a place '''

flag=1
start = None
@app.route("/dashboard_visitor/timer", methods=["POST","GET"])
def timer():
    if session['current_user_type'] == "Visitor":
        if "current_user" in session:
            user = session["current_user"]
            global start
            global qr
            global flag
            if request.method=="POST" and flag==1:
                qr = request.form.get("final_result")
                if flag == 1:
                    start_time = datetime.now()
                    start = start_time.strftime('%Y-%m-%d %H:%M:%S')
            if request.method=="POST" and flag==0:
                end_time = datetime.now()
                end = end_time.strftime('%Y-%m-%d %H:%M:%S')
                conn = sqlite3.connect(visitor_db_file)
                cur = conn.cursor()
                cur.execute("SELECT device_id FROM Visitors WHERE username=\'" + user + "\'")
                device = cur.fetchone()
                conn.close()
                visit(round(time.time() * 1000) , qr , device[0] , start , end)
                flag=1
                return redirect(url_for("scan"))
            flag=0
            return render_template("timer.html", user = session["current_user"])
        else:
            return render_template("logins.html")
    else:
        return render_template("error_pages/page_401.html")


''' Login pages '''

@app.route("/login_visitor_page")
def login_visitor_page():
    session['login_form_selector'] = "Visitor"
    session.modified = True
    return render_template("logins.html")

@app.route("/login_hospital_page")
def login_hospital_page():
    session['login_form_selector'] = "Hospital"
    session.modified = True
    return render_template("logins.html")

@app.route("/login_place_page")
def login_place_page():
    session['login_form_selector'] = "Place"
    session.modified = True
    return render_template("logins.html")

@app.route("/login_agent_page")
def login_agent_page():
    session['login_form_selector'] = "Agent"
    session.modified = True
    return render_template("logins.html")

'''Contact Us Page''' 

@app.route("/contacts/", methods=["GET","POST"])
def contacts():
    if request.method == "POST":
        return "Message sent!"
        name = request.form.get('name')
        email =request.form.get('email')
        subject = request.form.get('subject')
        message =request.form.get('message')

        msg = Message(subject =f"Mail from {name}", body =f"Name: {name} \nE-mail:{email}\n Subject: {subject}\n\n\n{message}", sender=mail_username)

        mail.send(msg)

    return render_template("contacts.html", success=True)


''' About us Page '''

@app.route("/about_us/")
def about_us():
    return render_template("about_us.html")


''' Logout method '''

@app.route("/logout/")
def logout():
    session.pop("current_user", None)
    return(redirect(url_for("root")))


'''WebCam'''
@app.route("/scan")
def scan():
    if session['current_user_type'] == "Visitor":
        if "current_user" in session:
            user = session["current_user"]
            return render_template("scanning.html")
        else:
            return render_template("logins.html")
    else:
        return render_template("error_pages/page_401.html")
    

''' Error pages '''

@app.errorhandler(401)
def page_401(error):
    return render_template("error_pages/page_401.html"), 401


@app.errorhandler(403)
def page_403(error):
    return render_template("error_pages/page_403.html"), 403


@app.errorhandler(404)
def page_404(error):
    return render_template("error_pages/page_404.html"), 404


@app.errorhandler(405)
def page_405(error):
    return render_template("error_pages/page_405.html"), 405


@app.errorhandler(413)
def page_413(error):
    return render_template("error_pages/page_413.html"), 413


''' Change hospital registration status '''

@app.route("/hospital_status_update", methods=["POST"])
def hospital_status_update():
    hosp = request.form.get('username')
    conn = sqlite3.connect(hospital_db_file)
    cur = conn.cursor()
    cur.execute("UPDATE Hospitals SET status = 1 WHERE username=\'" + hosp +"\'")
    conn.commit()
    cur.close()
    session['login_form_selector'] = None
    session.modified = True
    return(redirect(url_for("hospital_table")))


''' Change visitor infection status '''

@app.route("/visitors_status_update_positive", methods=["POST"])
def visitors_status_update_positive():
    vis = request.form.get('username')
    conn = sqlite3.connect(visitor_db_file)
    cur = conn.cursor()
    cur.execute("UPDATE Visitors SET infected = 1 WHERE username=\'" + vis +"\'")
    conn.commit()
    cur.close()
    session['login_form_selector'] = None
    session.modified = True
    return(redirect(url_for("dashboard_hospital")))

@app.route("/visitors_status_update_negative", methods=["POST"])
def visitors_status_update_negative():
    vis = request.form.get('username')
    conn = sqlite3.connect(visitor_db_file)
    cur = conn.cursor()
    cur.execute("UPDATE Visitors SET infected = 0 WHERE username=\'" + vis +"\'")
    conn.commit()
    cur.close()
    session['login_form_selector'] = None
    session.modified = True
    return(redirect(url_for("dashboard_hospital")))


''' Display visitors and places table in Agent page '''

@app.route("/visitors_table")
def visitors_table():
    if session['current_user_type'] == "Agent":
        if "current_user" in session:
            user = session["current_user"]
            conn = sqlite3.connect(visitor_db_file)
            cur = conn.cursor()
            cur.execute("SELECT * FROM Visitors")
            vdata= cur.fetchall()
            return render_template("tables/visitors_table.html", vdata = vdata)
        else:
            return render_template("logins.html")
    else:
        return render_template("error_pages/page_401.html")

@app.route("/places_table")
def places_table():
    if session['current_user_type'] == "Agent":
        if "current_user" in session:
            user = session["current_user"]
            conn = sqlite3.connect(places_db_file)
            cur = conn.cursor()
            cur.execute("SELECT * FROM Places")
            pdata= cur.fetchall()
            return render_template("tables/places_table.html", pdata = pdata)
        else:
            return render_template("logins.html")
    else:
        return render_template("error_pages/page_401.html")


''' Display hospital and their status in Agent page '''

@app.route("/hospital_table")
def hospital_table():
    if session['current_user_type'] == "Agent":
        if "current_user" in session:
            user = session["current_user"]
            conn = sqlite3.connect(hospital_db_file)
            cur = conn.cursor()
            cur.execute("SELECT username, status FROM Hospitals")
            hospitals = cur.fetchall()
            conn.close()
            session['hospitals'] = hospitals
            return render_template("tables/hospital_table.html", hospitals=session['hospitals'])
        else:
            return render_template("logins.html")
    else:
        return render_template("error_pages/page_401.html")


''' Rendering to Search pages  '''

''' Search to which places a visitor has been  '''
@app.route("/visitor_visit")
def visitor_visit():
    return render_template("search/search_visit_byvisitor.html")


'''
Result from searching by visitor
'''
@app.route('/search', methods=["POST"])
def search_by_visitor():
    if session['current_user_type'] == "Agent":
        if "current_user" in session:
            name = request.form.get('visitor_name')
            from_ = request.form.get('entry')
            to_ = request.form.get('exit')

            con = sqlite3.connect(visitor_db_file)
            cur = con.cursor()
            cur.execute("SELECT device_id FROM Visitors WHERE username=\'" + name +"\'")
            device = cur.fetchone()
            con.close()
            
            conn = sqlite3.connect(visitor_to_places_db_file)

            cur = conn.cursor()
            attachdb = "ATTACH DATABASE ? AS place"
            cur.execute(attachdb, (places_db_file,))

            cur.execute('''
            SELECT p.username, p.address, v.entry_time, v.exit_time
            FROM main.VisitorsToPlace as v
            JOIN place.Places as p
            ON v.qrcode = p.qrcode AND v.device_id = ?
            WHERE entry_time BETWEEN ? AND ?''', (device[0], from_, to_))

            result = cur.fetchall()

            cur.execute("DETACH DATABASE place")
            conn.close()

            return render_template('search/searchvisitor.html', result=result, visitor=name, datefrom=from_, dateto=to_)
        else:
            return render_template("logins.html")
    else:
        return render_template("error_pages/page_401.html")



''' Search the visitors that have been to a certain place  '''
@app.route("/place_visit")
def place_visit():
    return render_template("search/search_visit_toplace.html")


'''
Result from searching by place
'''
@app.route('/searchv', methods=["POST"])
def search_by_place():
    if session['current_user_type'] == "Agent":
        if "current_user" in session:
            name = request.form.get('place_name')
            from_ = request.form.get('entry')
            to_ = request.form.get('exit')
            
            con = sqlite3.connect(places_db_file)
            cur = con.cursor()
            cur.execute("SELECT qrcode FROM Places WHERE username=\'" + name +"\'")
            qrcode = cur.fetchone()
            con.close()
            
            conn = sqlite3.connect(visitor_to_places_db_file)

            cur = conn.cursor()
            attachdb = "ATTACH DATABASE ? AS visitor"
            cur.execute(attachdb, (visitor_db_file,))

            cur.execute('''
            SELECT vi.visitor_name, vi.email, vi.phone_number, vi.address, v.entry_time, v.exit_time
            FROM main.VisitorsToPlace as v
            JOIN visitor.Visitors as vi
            ON v.device_id = vi.device_id  AND v.qrcode = ?
            WHERE entry_time BETWEEN ? AND ?''', (qrcode[0], from_, to_))

            result = cur.fetchall()

            cur.execute("DETACH DATABASE visitor")
            conn.close()

            return render_template('search/searchplace.html', result=result, place=name, datefrom=from_, dateto=to_)
        else:
            return render_template("logins.html")
    else:
        return render_template("error_pages/page_401.html")



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")