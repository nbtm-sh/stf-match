var express = require("express");
var creds = require("./mysql-creds.json");
var mysql = require("mysql");

var mysql_connection = mysql.createConnection({
    "host": "localhost",
    "user": creds.username,
    "password": creds.password,
    "database": "stf"
});

function query_db(sql_query, callback, ext_args) {
    console.log("Query: " + sql_query);
    mysql.query(sql_query, (err, result, fields, cb=callback, ext=ext_args) => {
        console.log("Complete. Callback!");
        cb((result, fields), ext_args);
    });
}

mysql_connection.connect();

var app = express();

function send_matches(results, client_res) {
    var res_json = [];
    console.log(results);
    console.log("Reached send matches function");

    client_res.json({
        result: results.toString()
    })
}

app.get('/matches', (req, res) => {
    var player1 = req.query.u1;
    var player2 = req.query.u2;

    var query = `SELECT * FROM \`matches\` WHERE (uPlayer1=${player1} OR uPlayer2=${player1}) AND (uPlayer1=${player2} OR uPlayer2=${player2});`;
    sql_db.query(query, send_matches, res);
});

app.get('/all', (req, res, query_callback=query_db, msql=mysql_connection) => {
    msql.query("SELECT * FROM `matches`;", (err, result, fields, cb=send_matches, ext=res) => {
        console.log("Complete. Callback!");
        cb((result, fields), ext_args);
    });
})

var server = app.listen(8080);