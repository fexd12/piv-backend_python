import flask
from flask import request, jsonify
import psycopg2

app = flask.Flask(__name__)
app.config["DEBUG"] = True

database = r"api/test.db"

# Simple Functions


def create_connection():
    c = None
    con_string = "dbname=pi_v user=postgres password=1234"
    
    c = psycopg2.connect(con_string)
    return c

# def create_table(conn, create_table_sql):
#     try:
#         c = conn.cursor()
#         c.execute(create_table_sql)
#     except Error as e:
#         print(e)
#     finally:
#         if c:
#             c.close()

# def dict_factory(cursor, row):
#     d = {}
#     for idx, col in enumerate(cursor.description):
#         d[col[0]] = row[idx]
#     return d


def execute(sql, isSelect=True):
    # LOCAL DATABASE
    # conn = sqlite3.connect(database)
    
    # REMOTE DATABASE
    conn = create_connection()
    result = None
    try:
        with conn.cursor() as cursor:
            if isSelect:
                cursor.execute(sql)
                result = cursor.fetchall()
                # print(f"result = {result}")
            else:
                cursor.execute(sql)
                result = conn.insert_id()
                conn.commit()
    except Exception as exc:
        print(exc)
    finally:
        conn.close()
    return result

# def start_db():

#     # create a database connection
#     conn = create_connection()

#     create tables
#     if conn is not None:
#         user_table_sql = """ CREATE TABLE IF NOT EXISTS user (
#                             id integer PRIMARY KEY AUTOINCREMENT,
#                             age integer NOT NULL,
#                             name text NOT NULL
#                         ); """
#         create_table(conn, user_table_sql)
#     else:
#         print("Error! cannot create the database connection.")

# HTTP functions

@app.route('/',methods=['GET'])
def index():
    return jsonify('hello World!')

# Add new user
@app.route('/user', methods=['POST'])
def post_users():
    user = request.get_json()
    _age = user['age']
    _name = user['name']

    sql = f"INSERT INTO user (age, name) VALUES ({_age}, '{_name}');"

    user['id'] = execute(sql, False)
    return jsonify(user)

# Update user
@app.route('/users', methods=['PUT'])
def put_users():
    user = request.get_json()
    _id = user['id']
    _age = user['age']
    _name = user['name']

    sql = f"UPDATE user SET age = {_age}, name = '{_name}' WHERE id = {_id};"
    execute(sql, False)
    return {}

# List all users
@app.route('/users', methods=['GET'])
def get_users():

    _id = request.args['id'] if 'id' in request.args else 0
    _age = request.args['email'] if 'email' in request.args else 0
    _name = request.args['name'] if 'name' in request.args else ''

    sql = f"""SELECT * FROM users"""

    users = execute(sql)
    return jsonify(users)

# Delete user by id
@app.route('/users/<_id>', methods=['DELETE'])
def delete_users(_id):
    sql = f"DELETE FROM user WHERE id = {int(_id)};"
    execute(sql, False)
    return {}

# LOCAL DATABASE

app.run(port=2020)