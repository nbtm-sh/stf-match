class API {
    users = [];

    constructor() {

    }

    getAllUserData() {
        WebRequest.get("http://stf.nbti.net:8080/players", this.cb_getAllUserData, this);
    }

    cb_getAllUserData(t, st) {
        t.users = JSON.parse(st);
    }
}

const api = new API();

api.getAllUserData();