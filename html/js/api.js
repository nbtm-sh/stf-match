class API {
    users = [];
    matches = [];
    domain = "stf.nbti.net:8080"
    wait = false;

    constructor() {

    }

    //#region   API method calls
    getAllMatches() {
        WebRequest.get(`http://${this.domain}/all`, this.cb_getAllMatches, this, this.ecb_getAllMatches);
        this.wait = true;
    }

    getMatchup(u1, u2) {
        WebRequest.get(`http://${this.domain}/matches?u1=${u1}&u2=${u2}`, this.cb_getAllMatches, this, this.ecb_getAllMatches);
        this.wait = true;
    }
    //#endregion

    //#region Non-API functions
    
    getUserById(id) {
        for (var i = 0; i < this.users.length; i += 1) {
            if (this.users[i].id == Number(id)) {
                return this.users[i];
            }
        }

        return null;
    }

    getUserByUsername(username) {
        for (var i = 0; i < this.users.length; i += 1) {
            if (this.users[i].uName == username) {
                return this.users[i];
            }
        }

        return null;
    }

    getTableData(htmlElement) {
        var htmlData = `
            <tbody><tr>
                <th>Player 1</th>
                <th>Fighter</th>
                <th>Winner</th>
                <th>Round</th>
                <th>Fighter</th>
                <th>Player 2</th>
            </tr>
        `;

        for (var i = 0; i < this.matches.length; i += 1) {
            htmlData += `
                <tr>
                    <td data="player1" country="${this.matches[i].uPlayer1.uCountry}">${this.matches[i].uPlayer1.uName}</td>
                    <td data="player1Figher">${this.matches[i].uPlayer1Fighter}</td>
                    <td data="winner"><a href="match?m=${this.matches[i].id}$">${this.matches[i].tResult.uName}</a></td>
                    <td data="winner">${this.matches[i].tRound}</td>
                    <td data="player1Figher">${this.matches[i].uPlayer2Fighter}</td>
                    <td data="player1" country="${this.matches[i].uPlayer2.uCountry}">${this.matches[i].uPlayer2.uName}</td>
                </tr>
            `;
        }

        htmlData += "</tbody>"

        htmlElement.innerHTML = htmlData;
    }

    //#endregion

    //#region Correct response callback functions

    cb_getAllMatches(st, t) {
        t.matches = JSON.parse(st);

        t.wait = false;
    }
    //#endregion

    //#region Errornous response callbacks
    ecb_getAllUserData(st, t) {
        console.log(st);
        t.wait = false;
    }

    ecb_getAllMatches(st, t) {
        console.log(st);
        t.wait = false;
    }
    //#endregion
}

const api = new API();

function updateTableAll() {
    console.log("Update table");
    if (api.wait) {
        window.setTimeout(updateTableAll, 200);
    } else {
        try {
            api.getTableData(document.getElementById("resulttable"));
        } catch (e) {
            console.log("Failed getting data from server. Retrying...");
            api.getAllMatches();
            window.setTimeout(updateTableAll, 1000);
        }
    }
}

function updateTableSelect(u1, u2) {
    console.log("Update table");
    if (api.wait) {
        window.setTimeout(updateTableSelect, 200);
    } else {
        try {
            api.getTableData(document.getElementById("resulttable"));
        } catch (e) {
            console.log("Failed getting data from server. Retrying...");
            api.getMatchup(u1, u2);
            window.setTimeout(updateTableSelect, 1000);
        }
    }
}

function updateTableSelectAsync() {
    if (api.wait) {
        window.setTimeout(updateTableSelectAsync, 200);
    } else {
        try {
            console.log(api.users);
            console.log(api.matches);

            var u1 = urlParams.get("u1");
            var u2 = urlParams.get("u2");

            api.getMatchup(u1, u2);
            api.getAllUserData();

            updateTableSelect(u1, u2);
        } catch (e) {
            console.log("Failed getting data from server. Retrying...");
            api.getAllUserData();
            window.setTimeout(updateTableSelectAsync, 200);
        }
    }
}

const urlParams = new URLSearchParams(window.location.search);

if (urlParams.get("u1") == null) {
    api.getAllMatches();

    console.log(api.matches);

    updateTableAll();
} else {

    updateTableSelectAsync();
}