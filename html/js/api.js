class API {
    users = [];
    matches = [];
    domain = "stf.nbti.net:8080"
    wait = false;

    constructor() {

    }

    //#region   API method calls
    getAllUserData() {
        WebRequest.get(`http://${this.domain}/players`, this.cb_getAllUserData, this, this.ecb_getAllUserData);
        this.wait = true;
    }

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
            <tr>
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
                    <td data="player1" >${this.matches[i].uPlayer1.uName}</td>
                    <td data="player1Figher">${this.matches[i].uPlayer1Fighter}</td>
                    <td data="winner">${this.matches[i].tResult.uName}</td>
                    <td data="winner">${this.matches[i].tRound}</td>
                    <td data="player1Figher">${this.matches[i].uPlayer2Fighter}</td>
                    <td data="player1" >${this.matches[i].uPlayer2.uName}</td>
                </tr>
            `;
        }

        htmlElement.innerHTML = htmlData;
    }

    //#endregion

    //#region Correct response callback functions
    cb_getAllUserData(st, t) {
        t.users = JSON.parse(st);
        t.wait = false;
    }

    cb_getAllMatches(st, t) {
        t.matches = JSON.parse(st);

        // Replace the user IDs with user objects
        for (var i = 0; i < t.matches.length; i += 1) {
            t.matches[i].uPlayer1 = t.getUserById(t.matches[i].uPlayer1);
            t.matches[i].uPlayer2 = t.getUserById(t.matches[i].uPlayer2);
            t.matches[i].tResult = t.getUserById(t.matches[i].tResult);
        }

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

api.getAllUserData();
api.getAllMatches();

console.log(api.users);
console.log(api.matches);

function updateTableAll() {
    console.log("Update table");
    if (api.wait) {
        window.setTimeout(updateTableAll, 200);
    } else {
        try {
            api.getTableData(document.getElementById("resulttable"));
        } catch (e) {
            console.log("Failed getting data from server. Retrying...");
            api.getAllUserData();
            api.getAllMatches();
            window.setTimeout(updateTableAll, 1000);
        }
    }
}

updateTableAll();