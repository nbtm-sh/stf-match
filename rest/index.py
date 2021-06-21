from flask import Flask
from flask import jsonify
from flask import request
import api.database_api
import api.ranking

db = api.database_api.STF(
    username="demoauth",
    password="ZhJ3bGjgfoyL9chU284fRGSqPN9dXnypi2MFPLMokXkNKE2JGH",
    host="stf.nbti.net",
    database="stf"
)

rank = api.ranking.Ranking(database=db)

app = Flask(__name__)

@app.route("/players")
def players():
    players = db.get_player()

    players = [i.json() for i in players]
    js = { "players": players }
    resp = jsonify(js)
    resp.headers['Access-Control-Allow-Origin'] = '*'

    del js
    return resp

@app.route("/matches")
def matches():
    data = request.args

    u1 = data['u1'] if 'u1' in data else None
    u2 = data['u2'] if 'u2' in data else None

    if u1 != None:
        try:
            int(u1)
        except ValueError:
            u1 = str(db.get_player(player_username=u1)[0].id)
    
    if u2 != None:
        try:
            int(u2)
        except ValueError:
            u2 = str(db.get_player(player_username=u2)[0].id)

    matches = db.get_match(players = [u1, u2], tournament=1)
    if matches == None:
        resp = jsonify({"matches": []})
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    matches = [i.json() for i in matches]
    js = {"matches": matches}
    resp = jsonify(js)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

app.run(host="0.0.0.0")