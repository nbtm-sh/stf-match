class API {
    users = [];

    constructor() {

    }

    getAllUserData() {
        WebRequest.get("http://stf.nbti.net:8080/players", this.cb_getAllUserData, this, this.ecb_getAllUserData);
    }

    cb_getAllUserData(st, t) {
        console.log(st);
        t.users = JSON.parse(st);
    }
    ecb_getAllUserData(st, t) {
        console.log(st);
    }
}

const api = new API();

api.getAllUserData();