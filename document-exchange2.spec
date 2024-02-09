
(
service oldSystemA {
    persistent agreements = {};

    persistent correspondents = {
        companyA : "oldSystemA",
        companyB : "oldSystemB",
        newCompany : "newCompany"
    };

    routes {
        "/ext/create" -> extCreate
        "/ext/sign" -> extSign
        "/ext/retract" -> extRetract
        "/list" -> list
    }

    code {
        function extCreate(request) {
            agreements = getPersistent("agreements") ;
            agreement = request . agreement ;
            correspondents = [] ;
            i = 0 ;
            while (i < len(agreement . correspondents)) {
                if (agreement . correspondents [ i ] != "companyA") {
                    correspondents = append(correspondents, agreement . correspondents [ i ]);
                }
                i = i + 1 ;
            }
            agreement . correspondents = correspondents ;

            agreements[ agreement . id ] = agreement ;
            setPersistent("agreements", agreements) ;
            respond(agreement) ;
        }

        function sign(request) {
            agreements = getPersistent("agreements") ;
            id = request . id ;
            if (! keyExists(agreements, id)) {
                respond("fail");
                return 0 ;
            }
            agreement = agreements[id] ;

            agreement . state = "signed" ;
            agreements[agreement . id] = agreement ;
            setPersistent("agreements", agreements) ;

            systems = getPersistent("correspondents");
            i = 0 ;
            while ( i < len(agreement . correspondents) ) {
                request ( systems [ agreement . correspondents [ i ] ], "/ext/sign", { id : id } ) ;
                i = i + 1 ;
            }
            respond("ok");
        }

        function extSign(request) {
            agreements = getPersistent("agreements") ;
            id = request . id ;
            if (! keyExists(agreements, id)) {
                respond("fail");
                return 0 ;
            }
            agreement = agreements[id] ;

            agreement . state = "signed" ;
            agreements[agreement . id] = agreement ;
            setPersistent("agreements", agreements) ;

            respond("ok");
        }

        function extRetract(request) {
            agreements = getPersistent("agreements") ;
            id = request . id ;
            if (! keyExists(agreements, id)) {
                respond("fail");
                return 0 ;
            }
            agreement = agreements[id] ;

            agreement . state = "retracted" ;
            agreements[agreement . id] = agreement ;
            setPersistent("agreements", agreements) ;

            respond("ok");
        }
    }
}

service newSystem {
    persistent agreements = {};

    persistent correspondents = {
        companyA : "oldSystemA",
        companyB : "oldSystemB",
        newCompany : "newCompany"
    };

    routes {
        "/create" -> create
        "/send" -> send
        "/sign" -> sign
        "/retract" -> retract
    }

    code {
        function create(request) {
            agreements = getPersistent("agreements") ;
            agreement = request . agreement ;
            agreement . state = "created" ;
            agreements[agreement . id] = agreement ;
            setPersistent("agreements", agreements) ;
            respond(agreement) ;
        }

        function send(request) {
            agreements = getPersistent("agreements") ;
            id = request . id ;
            if (! keyExists(agreements, id)) {
                respond("fail");
                return 0 ;
            }
            agreement = agreements[id] ;

            systems = getPersistent("correspondents");
            i = 0 ;
            while ( i < len(agreement . correspondents) ) {
                modified_agreement = agreement ;
                modified_agreement . correspondents = append(agreement . correspondents, "newCompany");
                request ( systems [ agreement . correspondents [ i ] ], "/ext/create", { agreement : modified_agreement } ) ;
                i = i + 1 ;
            }
            agreement . state = "sent" ;
            agreements[agreement . id] = agreement ;
            setPersistent("agreements", agreements) ;
            respond("ok");
        }

        function sign(request) {
            agreements = getPersistent("agreements") ;
            id = request . id ;
            if (! keyExists(agreements, id)) {
                respond("fail");
                return 0 ;
            }
            agreement = agreements[id] ;

            agreement . state = "signed" ;
            agreements[agreement . id] = agreement ;
            setPersistent("agreements", agreements) ;

            systems = getPersistent("correspondents");
            while ( i < len(agreement . correspondents) ) {
                request ( systems [ agreement . correspondents [ i ] ], "/ext/sign", { id : id } ) ;
                i = i + 1 ;
            }
            respond("ok");
        }

        function retract(request) {
            agreements = getPersistent("agreements") ;
            id = request . id ;
            if (! keyExists(agreements, id)) {
                respond("fail");
                return 0 ;
            }
            agreement = agreements[id] ;

            agreement . state = "retracted" ;
            agreements[agreement . id] = agreement ;
            setPersistent("agreements", agreements) ;

            systems = getPersistent("correspondents");
            i = 0 ;
            while ( i < len(agreement . correspondents) ) {
                request ( systems [ agreement . correspondents [ i ] ], "/ext/retract", { id : id } ) ;
                i = i + 1 ;
            }
            respond("ok");
        }
    }
}


init {
    request("newSystem", "/create", {
        agreement : {
            id : "doc1",
            correspondents : [ "companyA" ]
        }
    });
}

init {
    request("newSystem", "/send", {
        id : "doc1"
    }) ;
}

init {
    request("newSystem", "/retract", {
        id : "doc1"
    }) ;
}


props {
    function test() {
        assert(len(services . oldSystemA . persistents . agreements) < 1);
    }

    function retractedAny(id) {
        serviceNames = [ "newSystem", "oldSystemA" ];
        i = 0 ;
        retracted = false ;
        while (i < len(serviceNames)) {
            agreements = services[serviceNames[i]] . persistents . agreements ;
            if (keyExists(agreements, id)) {
                agreement = agreements[id] ;        
                retracted = retracted || agreement . state == "retracted" ;
            }
        }
        assert(retracted) ;
    }

    function retractedAll(id) {
        services = [ "newSystem", "oldSystemA" ];
        i = 0 ;
        retracted = true ;
        while (i < len(services)) {
            agreements = services[services[i]] . persistents . agreements ;
            agreement = agreements[id] ;
            retracted = retracted && agreement . state == "retracted" ;
        }
        assert(retracted) ;
    }

}
)

