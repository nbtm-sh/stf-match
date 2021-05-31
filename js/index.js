var express = require("express");
var sql_db = require("./mysql_api.js")

var app = express();

function send_matches(results, client_res) {
    var res_json = [];
    console.log(results);
}

app.get('/matches', (req, res) => {
    var player1 = req.query.u1;
    var player2 = req.query.u2;

    var query = `SELECT * FROM \`matches\` WHERE (uPlayer1=${player1} OR uPlayer2=${player1}) AND (uPlayer1=${player2} OR uPlayer2=${player2});`;
    sql_db.query(query, send_matches, res);
});

app.get('/all', (req, res) => {
    var query = 'SELECT * FROM `matches`;';
    sql_db.Sq.query(query, send_matches, res);
})

var server = app.listen(8080);