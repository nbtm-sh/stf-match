import mysql_api
import json
from flask import Flask
from flask import jsonify, make_response
from flask import request

creds_file = open("mysql-creds.json")
creds_file = json.loads(creds_file.read())
database_interface = mysql_api.SQLAPI(
    host="127.0.0.1",
    username=creds_file["username"],
    password=creds_file["password"],
    database="stf"
)

app = Flask(__name__)

@app.route('/tournaments')
def all_tournaments():
    result = database_interface.get_all_tournaments()
    result = [i.json() for i in result]

    return jsonify(result)

if __name__ == "__main__":
    app.run("127.0.0.1", 8080)