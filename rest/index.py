from flask import Flask
from flask import jsonify
from flask import request
import mysqlapi
import json

# Open create the database interface
creds_file = open("mysql-creds.json")
creds_file = json.loads(creds_file.read())
database_interface = mysqlapi.SQLAPI(
    host="127.0.0.1",
    username=creds_file["username"],
    password=creds_file["password"],
    database="stf"
)



app = Flask(__name__)

@app.route('/players')
def get_players():
    uname = request.args.get("un")
    uid = request.args.get("id")

    if uname != None:
        uname = uname.split(",")
    if uid != None:
        uid = uid.split(",")
        for i in range(len(uid)):
            uid[i] = int(uid[i])
    
    response = []

    if uname != None: response.extend(database_interface.get_players_by_username(uname))
    if uid != None: response.extend(database_interface.get_players_by_id(uid))

    response_json = [i.json() for i in response]

    return jsonify(response_json)

if __name__ == "__main__":
    app.run("stf.nbti.net", 8080)