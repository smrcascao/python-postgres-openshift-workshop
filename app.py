from flask import Flask, render_template, request, url_for, send_from_directory
import psycopg2
import os
import socket
import json
import time
import logging
logging.basicConfig(level=logging.INFO)

TEMPLATE_DIR = os.path.abspath('templates')
STATIC_DIR = os.path.abspath('static')
if 'TEMPLATES_DIR_BASE_URL' in os.environ:
    TEMPLATE_DIR=os.environ.get('TEMPLATES_DIR_BASE_URL')+"/templates"

if 'STATIC_DIR_BASE_URL' in os.environ:
    TEMPLATE_DIR=os.environ.get('STATIC_DIR_BASE_URL')+"/static"


app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

db_user = os.environ.get('POSTGRES_DB_USER')
db_psw = os.environ.get('POSTGRES_DB_PSW')
db_host = os.environ.get('SERVICE_POSTGRES_SERVICE_HOST')
db_name = os.environ.get('POSTGRES_DB_NAME')



def table_exists(table_str):
    exists = False
    try:
        cursor = conn.cursor()
        cursor.execute("select exists(select relname from pg_class where relname='" + table_str + "')")
        exists = cursor.fetchone()[0]
    except psycopg2.Error as e:
        logging.info(e)
    finally:
        if (conn):
            cursor.close()
            logging.info("PostgreSQL cursor is closed")
    return exists


if db_name == None:
    db_name = "workshopdb"
else:
    logging.info("database name: " + str(db_name))

conn = None

try:
    conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_psw, host=db_host, port="5432")
    logging.info(conn)
    logging.info("connected database: " + str(db_name))
except Exception as e:
    logging.info("Error: " + str(e))

if not table_exists("users"):
    try:
        cur = conn.cursor()
        cur.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, email VARCHAR(255) NOT NULL);")
        cur.close()
        conn.commit()
        logging.info("Table users was Created")
    except Exception as e:
        logging.info("Error: " + str(e))
else:
    logging.info("Table users already exists")



@app.route('/')
def index():

    htmlTitlePage = "Runtime 20"
    if 'HTML_Title' in os.environ:
        htmlTitlePage = os.environ.get('HTML_Title')

    backgroudColorPage = "black"
    if 'backgroudColorPage' in os.environ:
        backgroudColorPage = os.environ.get('backgroudColorPage')

    baseURL = ""
    if 'BASE_URL' in os.environ:
        baseURL = os.environ.get('BASE_URL')

    return render_template('index.html', title=htmlTitlePage, baseURL=baseURL, backgroudColorPage=backgroudColorPage)


@app.route('/success')
def success():
    htmlTitlePage = "Runtime 20"
    if 'HTML_Title' in os.environ:
        htmlTitlePage = os.environ.get('HTML_Title')

    baseURL = ""
    if 'BASE_URL' in os.environ:
        baseURL = os.environ.get('BASE_URL')

    return render_template('success.html', baseURL=baseURL, title=htmlTitlePage)


@app.route('/healthz')
def healthz():
    return "OK"

@app.route('/headers')
def headers():
    logging.info("\nHeaders Start:\n"+str(request.headers)+"\nEnd Headers")
    return str(request.headers)


@app.route('/healthx')
def healthx():
    time.sleep(2);
    return "OK"



@app.route('/system')
def systemInfo():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    data = {}
    data['ContainerName'] = hostname
    data['ContainerIP'] = IPAddr
    json_data = json.dumps(data)
    return json_data


@app.route('/prereg', methods=['POST'])
def prereg():
    htmlTitlePage = "Runtime 20"
    if 'HTML_Title' in os.environ:
        htmlTitlePage = os.environ.get('HTML_Title')

    baseURL = ""
    if 'BASE_URL' in os.environ:
        baseURL = os.environ.get('BASE_URL')

    email = None
    cursor = conn.cursor()
    if request.method == 'POST':
        email = request.form['email']

        try:
            cursor.execute(" select exists ( select email from users where email = %s )", (email,))
            if not cursor.fetchone()[0]:
                logging.info("Email:" + str(email) + " was added")
                cursor.execute("INSERT INTO users (email) VALUES(%s)", (email,))

                cursor.close()
                conn.commit()
                return render_template('success.html', title=htmlTitlePage, baseURL=baseURL)
            else:
                logging.info(str(email) + " already exists!")

        except Exception as e:
            logging.info("Error: " + str(e))


    return render_template('index.html', title=str(email) + " already exists!", baseURL="/")


@app.route('/getdata', methods=['GET'])
def contextget():
    cursor = conn.cursor()
    data = None
    response = []
    try:
        cursor.execute("SELECT * FROM users")
        data = cursor.fetchall()
    except Exception as e:
        logging.info("Error: " + str(e))
    finally:
        # closing database connection.
        if (conn):
            cursor.close()

    for result in data:
        regist = {"id": result[0], "email": result[1]}
        response.append(regist)
    response = json.dumps(response)
    return response

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(host='0.0.0.0')

