service backend {
    code {
        function addFavorite(request) {
            user = request . user ;
            if (user . type == "guest") {
                request("db", "insert-favorite", { type : "guest", guest_id : user . session }) ;
                response = request("db", "get-favorites", { type : "guest", field : "guest_id", value : user . session }) ;
                request("cache", "set", { key : "fav:guest:" + user . session , value : len(response) }) ;
            } else {
                if (user . type == "user") {
                    request("db", "insert-favorite", { type : "user", user_id : user . id }) ;
                    response = request("db", "get-favorites", { type : "user", field : "user_id", value : user . id }) ;
                    request("cache", "set", { key : "fav:user:" + user . id , value : len(response) }) ;
                }
            }
            respond("ok");
        }
        function getFavoriteCount(request) {
            user = request . user ;
            if (user . type == "guest") {
                r = request("cache", "get", { key : "fav:guest:" + user . session, default : 0 });
                respond(r) ;
            } else {
                if (user . type == "user") {
                    r = request("cache", "get", { key : "fav:user:" + user . id, default : 0 });
                    respond(r) ;
                }
            }
            respond("ok");
        }

        function login(request) {
            guest = request . user ;
            user_id = request . user_id ;
            fav = request("db", "get-favorites", { type : "guest", field : "guest_id", value : guest . session }) ;
            
            userCount = request("cache", "get", { key : "fav:user:" + user_id, default : 0 });
            request("cache", "set", { key : "fav:user:" + user_id, value : userCount + len(fav) });
            
        }
    }
    routes {
        "/add-favorite" -> addFavorite
        "/favorite-count" -> getFavoriteCount
        "/login" -> login
    }
}

service cache {
    persistent keys = {} ;
    routes {
        "set" -> set
        "get" -> get
        "flush" -> flush
    }
    code {
        function set(request) {
            k = getPersistent("keys") ;
            k [ request . key ] = request . value ;
            setPersistent("keys", k) ;
            respond("ok") ;
        }
        function get(request) {
            k = getPersistent("keys") ;
            if (keyExists(k, request . key)) {
                respond(k [ request . key ]) ;
            } else {
                respond(request . default);
            }
        }
        function flush(request) {
            setPersistent("keys", { }) ;
            respond("ok") ;
        }
    }
}

service db {
    persistent favorites = [ ] ;

    routes {
        "insert-favorite" -> insertFavorite
        "get-favorites" -> getFavorites
    }

    code {
        function insertFavorite(request) {
            fav = getPersistent("favorites") ;
            setPersistent("favorites", append(fav, request)) ;
            respond("ok") ;
        }
        function getFavorites(query) {
            fav = getPersistent("favorites") ;
            i = 0 ;
            resp = [] ;
            while (i < len(fav)) {
                if (fav [ i ] . type == query . type && fav [ i ] [ query . field ] == query . value) {
                    resp = append(resp, fav[i]) ;
                }
                i = i + 1 ;
            }
            respond(resp) ;
        }
    }
}

init {
    user = {
        type : "guest",
        session : "session-0"
    };
    request("backend", "/add-favorite", { user : user });
    request("backend", "/add-favorite", { user : { type : "user", id : "0" } });
    request("backend", "/login", { user : user, user_id : "0" });
    request("backend", "favorite-count", { user : user });
}

init {
    request("cache", "flush", {}) ;
}