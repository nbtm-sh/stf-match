from flask import Flask
from flask import jsonify
from flask import request
import mysql_api
import json

# Open create the database interface
creds_file = open("mysql-creds.json")
creds_file = json.loads(creds_file.read())
database_interface = mysql_api.SQLAPI(
    host="127.0.0.1",
    username=creds_file["username"],
    password=creds_file["password"],
    database="stf"
)



app = Flask(__name__)

@app.route('/players')
def get_players():
    uname = request.args.get("un")
    print(uname)

if __name__ == "__main__":
    app.run("stf.nbti.net", 8080)