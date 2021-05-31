var creds = require("./mysql-creds.json");
var mysql = require("mysql");

var mysql_connection = mysql.createConnection({
    "host": "localhost",
    "user": creds.username,
    "password": creds.password,
    "database": "stf"
});

function query(sql_query, callback, ext_args) {
    mysql.query(sql_query, (err, result, fields, cb=callback, ext=ext_args) => {
        if (!err) {
            cb(result, ext_args);
        }
    })
}

mysql_connection.connect();