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

global_temp = [];
intent_global_length = 0;

function send_players(client_res, gt) {
    var res_json = [];

    console.log(gt);

    for (var i = 0; i < gt.length; i += 1) {
        res_json.push({
            id: gt[i][0].id,
            uName: gt[i][0].uName,
            uCountry: gt[i][0].uCountry
        });
    }

    console.log(res_json);

    client_res.json(res_json);
}

function send_matches(results, client_res) {
    var res_json = [];
    console.log("Reached send matches function");

    console.log(results[0]);
    console.log(results[0].length);

    for (var i = 0; i < results[0].length; i += 1) {
        res_json.push({
            id: results[0][i].id,
            uPlayer1: results[0][i].uPlayer1,
            uPlayer2: results[0][i].uPlayer2,
            uPlayer1Fighter: results[0][i].uPlayer1Fighter,
            uPlayer2Fighter: results[0][i].uPlayer2Fighter,
            tRound: results[0][i].tRound,
            tResult: results[0][i].tResult
        });
    }

    console.log(res_json[0]);

    client_res.json(res_json)
}

app.get('/matches', (req, res, query_callback=null, msql=mysql_connection, cb=send_matches) => {
    res.setHeader("Access-Control-Allow-Origin", "*");
    var player1 = req.query.u1;
    var player2 = req.query.u2;

    var query = `SELECT * FROM \`matches\` WHERE (\`uPlayer1\`=${player1} OR \`uPlayer2\`=${player1}) AND (\`uPlayer1\`=${player2} or \`uPlayer2\`=${player2});`;
    msql.query(query, (err, result, fields, cb=send_matches, ext=res) => {
        console.log("Complete. Callback!");
        console.log(result);
        console.log(fields);
        console.log(query);
        cb([result, fields], ext);
    });
});

app.get('/player', (req, res, query_callback=null, msql=mysql_connection) => {
    res.setHeader("Access-Control-Allow-Origin", "*");
    console.log("Player request: " + req.query.p);
    var ids = req.query.p.split(",");
    intent_global_length = ids.length;

    global_temp = [];

    for (var i = 0; i < ids.length; i += 1) {
        msql.query(`SELECT * FROM \`players\` WHERE id=${ids[i]};`, (err, result, fields, cb=send_players, ext=res, send_results=(i==ids.length-1), gt=global_temp, len=i, intent=intent_global_length) => {
            console.log("GT LENGTH: " + gt.length.toString() + ", INTENT: " + intent.toString());
            gt.push(result);
            if (gt.length == intent) {
                console.log("Callback");
                cb(ext, gt);
            }
        });
    }
});

app.get('/players', (req, res, query_callback=null, msql=mysql_connection) => {
    res.setHeader("Access-Control-Allow-Origin", "*");

    msql.query(`SELECT * FROM \`players\`;`, (err, result, fields, ret=res) => {
        ret_json = [];

        for (var i = 0; i < result.length; i += 1) {
            ret_json.push({
                id: result[i].id,
                uName: result[i].uName,
                uCountry: result[i].uCountry
            });
        }

        res.json(ret_json);
    });
});

app.get('/all', (req, res, query_callback=query_db, msql=mysql_connection) => {
    res.setHeader("Access-Control-Allow-Origin", "*");
    msql.query("SELECT * FROM `matches`;", (err, result, fields, cb=send_matches, ext=res) => {
        console.log("Complete. Callback!");
        cb([result, fields], ext);
    });
})

var server = app.listen(8080);