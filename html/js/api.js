class API {
    users = [];

    constructor() {

    }

    getAllUserData(this) {
        WebRequest.get("http://stf.nbti.net:8080/players", this.cb_getAllUserData, this);
    }

    cb_getAllUserData(this, st) {
        this.users = JSON.parse(st);
    }
}