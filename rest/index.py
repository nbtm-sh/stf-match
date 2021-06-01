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
    country = request.args.get("cn")

    if uname != None:
        uname = uname.split(",")
    if uid != None:
        uid = uid.split(",")
        for i in range(len(uid)):
            uid[i] = int(uid[i])
    
    response = []

    if uname != None: response.extend(database_interface.get_players_by_username(uname))
    if uid != None: response.extend(database_interface.get_players_by_id(uid))
    if country != None: response.extend(database_interface.get_players_by_country(country))

    response_json = [i.json() for i in response]

    return jsonify(response_json)

@app.route('/matches')
def get_matches():
    player1 = request.args.get("u1")
    player2 = request.args.get("u2")

    result = []

    players = [player1, player2]
    try:
        players.remove(None)
        players.remove(None)
    except Exception:
        pass

    for i in range(len(players)):
        if players[i] != None:
            try:
                players[i] = int(players[i])
                players[i] = database_interface.get_players_by_id(players[i])[0]
            except ValueError:
                players[i] = database_interface.get_players_by_username(players[i])[0]
    
    print(players)

    if len(players) == 0:
        result = database_interface.get_all_matches()
    elif len(players) == 1:
        result = database_interface.get_matches_played_by(players[0])
    elif len(players) == 2:
        result = database_interface.get_matchups(players[0], players[1])
    
    return jsonify([i.json() for i in result])

    

if __name__ == "__main__":
    app.run("stf.nbti.net", 8080)