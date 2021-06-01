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
        result = [];
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
        this.sql_connection.query(sql_query, (err, result, fields, t=this) => {
            if (result == null) {
                // No results
                t.temp_response = [];
                t.wait = false;
            } else {
                t.temp_response = this.constructUserObjects(result);
                t.wait = false;
            }
        });

        while (this.wait) {
            // Do nothing
        }
        return this.constructUserObjects(this.temp_response);
    }
    //#endregion
}

module.exports = SQL;