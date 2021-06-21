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
    u2 = data['u1'] if 'u1' in data else None

    matches = db.get_match(players = [u1, u2])
    
app.run()