from flask import Flask, render_template, request
import psycopg2
import os
import socket
import json
import time

app = Flask(__name__)

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
        print(e)
    finally:
        if (conn):
            cursor.close()
            print("PostgreSQL cursor is closed")
    return exists


if db_name == None:
    db_name = "workshopdb"
else:
    print("database name: " + str(db_name))

conn = None

try:
    conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_psw, host=db_host, port="5432")
    print(conn)
    print("connected database: " + str(db_name))
except Exception as e:
    print("Error: " + str(e))

if not table_exists("users"):
    try:
        cur = conn.cursor()
        cur.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, email VARCHAR(255) NOT NULL);")
        cur.close()
        conn.commit()
        print("Table users was Created")
    except Exception as e:
        print("Error: " + str(e))
else:
    print("Table users already exists")



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/healthz')
def healthz():
    return "OK"



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
    print("---prereg---")
    email = None
    cursor = conn.cursor()
    print(request)
    print(request.form)
    if request.method == 'POST':
        email = request.form['email']

        try:
            cursor.execute(" select exists ( select email from users where email = %s )", (email,))
            if not cursor.fetchone()[0]:
                print("Email:" + str(email) + " was added")
                cursor.execute("INSERT INTO users (email) VALUES(%s)", (email,))

                cursor.close()
                conn.commit()
                return render_template('success.html')
            else:
                print(str(email) + " already exists!")
        except Exception as e:
            print("Error: " + str(e))
    print("---end prereg---")
    return render_template('index.html')


@app.route('/getdata', methods=['GET'])
def contextget():
    print("---getdata---")
    print(request, request.endpoint)
    cursor = conn.cursor()
    data = None
    response = []
    try:
        cursor.execute("SELECT * FROM users")
        data = cursor.fetchall()
    except Exception as e:
        print("Error: " + str(e))
    finally:
        # closing database connection.
        if (conn):
            cursor.close()
            print("PostgreSQL cursor is closed")

    for result in data:
        regist = {"id": result[0], "email": result[1]}
        response.append(regist)
    response = json.dumps(response)
    print(response)
    print("---end getdata---")
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0')

