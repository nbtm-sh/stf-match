var creds = require("./mysql-creds.json");
var msql = require("mysql");

class SQL {
    constructor() {
        this.sql_connection = msql.createConnection({
            "host": "localhost",
            "user": creds.username,
            "password": creds.password,
            "database": "stf"
        });

        this.sql_connection.connect();
    }

    //#region Non-SQL functions
    constructUserObjects(sqlResult) {
        var result = [];
        for (var i = 0; i < sqlResult; i += 1) {
            result.push({
                id: sqlResult[i].id,
                uName: sqlResult[i].uName,
                uCountry: sqlResult[i].uCountry
            });
        }

        return result;
    }
    //#endregion

    //#region SQL Query functions
    getUsernameFromId(id) {
        var query = `SELECT * FROM \`players\` WHERE id=${id};`;
        this.wait = true;
        var result = this.sql_connection.query(query).result;

        return result;
    }
    //#endregion
}

module.exports = SQL;