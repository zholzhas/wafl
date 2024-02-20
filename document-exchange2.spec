
(
service oldSystemA {
    persistent agreements = {};
    persistent retracted = [] ;

    persistent correspondents = {
        companyA : "oldSystemA",
        companyB : "oldSystemB",
        newCompany : "newCompany"
    };

    routes {
        "/ext/create" -> extCreate
        "/ext/receipt" -> extReceipt
    }

    code {
        function extCreate(request) {
            lock(request . id);
            agreements = getPersistent("agreements") ;
            agreement = request ;
            correspondents = [] ;
            i = 0 ;
            
            ret = getPersistent("retracted") ;
            while (i < len(ret)) {
                if (ret [ i ] == agreement . id) {
                    agreement . state = "retracted" ;
                }
                i = i + 1 ;
            }

            agreements[ agreement . id ] = agreement ;
            setPersistent("agreements", agreements) ;
            unlock(request . id);
            respond(agreement) ;
        }

        function extReceipt(request) {
            lock(request . id);
            agreements = getPersistent("agreements") ;
            id = request . id ;

            if (keyExists(agreements, id)) {
                agreement = agreements[id] ;

                agreement . state = "retracted" ;
                agreements[agreement . id] = agreement ;
                setPersistent("agreements", agreements) ;
            } else {
                ret = getPersistent("retracted");
                ret = append(ret, id);
                setPersistent("retracted", ret);
            }
            unlock(request . id);
            respond("ok");
        }
    }
}

service center {
    persistent correspondents = {
        companyA : "oldSystemA",
        companyB : "oldSystemB",
        newCompany : "newCompany"
    };

    listen {
        "newDocument" -> newDocument
        "receipt" -> receipt
    }

    code {
        function newDocument(request) {
            systems = getPersistent("correspondents");
            i = 0 ;
            while ( i < len(request . correspondents) ) {
                request ( systems [ request . correspondents [ i ] ], "/ext/create", request ) ;
                i = i + 1 ;
            }
        }

        function receipt(request) {
            systems = getPersistent("correspondents");
            i = 0 ;
            while ( i < len(request . correspondents) ) {
                request ( systems [ request . correspondents [ i ] ], "/ext/receipt", request ) ;
                i = i + 1 ;
            }
        }
    }
}

service newSystem {
    persistent agreements = {};

    routes {
        "/create" -> create
        "/send" -> send
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

            agreement = agreements[id] ;

            
            agreement . state = "sent" ;
            agreements[agreement . id] = agreement ;
            setPersistent("agreements", agreements) ;
            
            agreement . sender = "newCompany" ;
            message("newDocument", agreement);

            respond("ok");
        }

        function retract(request) {
            agreements = getPersistent("agreements") ;
            id = request . id ;
            agreement = agreements[id] ;

            agreement . state = "retracted" ;
            agreements[agreement . id] = agreement ;
            setPersistent("agreements", agreements) ;

            message("receipt", { type : "retract", id : id, correspondents : agreement . correspondents });

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
    
    
    request("newSystem", "/send", {
        id : "doc1"
    }) ;

    
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
            i = i + 1 ;
        }
        assert(retracted) ;
    }

    function retractedAll(id) {
        serviceNames = [ "newSystem", "oldSystemA" ];
        i = 0 ;
        retracted = true ;
        while (i < len(serviceNames)) {
            agreements = services[serviceNames[i]] . persistents . agreements ;
            agreement = agreements[id] ;
            retracted = retracted && agreement . state == "retracted" ;
            i = i + 1 ;
        }
        assert(retracted) ;
    }

}
)

