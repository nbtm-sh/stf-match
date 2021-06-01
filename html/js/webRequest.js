class WebRequest {
    static get(url, callback, ext_args, error_callback=null) {
        var xmlHttp;

        xmlHttp = new XMLHttpRequest();
        xmlHttp.onreadystatechange = function() { 
            if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
                callback(xmlHttp.responseText, ext_args);
            } else {
                error_callback(xmlHttp.status, ext_args);
            }
        }
        xmlHttp.open("GET", url, true); // true for asynchronous 
        xmlHttp.send(null);
    }
}