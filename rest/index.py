from flask import Flask
from flask import jsonify
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

@app.route('/')
def hello_world():
    return jsonify({"response": True})

if __name__ == "__main__":
    app.run("127.0.0.1", 8080)