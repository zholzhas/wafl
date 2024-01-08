
(
service oldSystemA {
    persistent agreements = [];

    persistent correspondents = {
        companyA : "oldSystemA",
        companyB : "oldSystemB",
        newCompany : "newCompany"
    };

    routes {
        "/ext/create" -> extCreate
        "/list" -> list
    }

    code {
        function extCreate(request) {
            agreements = getPersistent("agreements") ;
            agreement = request . agreement ;
            agreement . id = len(agreements) ;
            agreements = append(agreements, agreement) ;
            setPersistent("agreements", agreements) ;
            respond(agreement) ;
        }

        function list(request) {
            agreements = getPersistent("agreements") ;
            respond(agreements) ;
        }
    }
}

service newSystem {
    persistent agreements = [];

    persistent correspondents = {
        companyA : "oldSystemA",
        companyB : "oldSystemB",
        newCompany : "newCompany"
    };

    routes {
        "/create" -> create
        "/send" -> send
        "/sign" -> sign
    }

    code {
        function create(request) {
            agreements = getPersistent("agreements") ;
            agreement = request . agreement ;
            agreement . id = len(agreements) ;
            agreements = append(agreements, agreement) ;
            setPersistent("agreements", agreements) ;
            respond(agreement) ;
        }

        function send(request) {
            agreements = getPersistent("agreements") ;
            id = request . id ;
            i = 0 ;
            agreement = { } ;
            while (i < len(agreements)) {
                if (id == agreements [ i ] . id) {
                    agreement = agreements [ i ] ;
                }
                i = i + 1 ;
            }
            systems = getPersistent("correspondents");
            i = 0 ;
            while ( i < len(agreement . correspondents) ) {
                request ( systems [ agreement . correspondents [ i ] ], "/ext/create", { agreement : agreement } ) ;
                i = i + 1 ;
            }
            respond("ok");
        }
    }
}

init {
    user = { 
        name : "newCompanyEmployee"
    } ;
    response = request("newSystem", "/create", { 
        user : user,
        agreement : {
            correspondents : [ "companyA", "companyB" ]
        }
    });
    id = response . id ;
    request("newSystem", "/send", {
        user : user,
        id : id
    }) ;
}


props {
    function test() {
        assert(len(services . oldSystemA . persistents . agreements) < 1);
    }
}
)

