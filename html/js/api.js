class API {
    users = [];

    constructor() {

    }

    getAllUserData() {
        WebRequest.get("http://stf.nbti.net:8080/players", this.cb_getAllUserData, this, error_callback=ecb_getAllUserData);
    }

    cb_getAllUserData(t, st) {
        t.users = JSON.parse(st);
    }
    ecb_getAllUserData(t, st) {
        console.log(st);
    }
}

const api = new API();

api.getAllUserData();