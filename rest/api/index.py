from flask import Flask
from flask import jsonify

import database_api
db = database_api.STF(
    username="demoauth",
    password="ZhJ3bGjgfoyL9chU284fRGSqPN9dXnypi2MFPLMokXkNKE2JGH",
    host="stf.nbti.net",
    database="stf"
)

app = Flask(__name__)

@app.route('/ranking')
def ranking():
    return_values = db.get_all_player_rankings()
    return jsonify(return_values)

app.run()