
service newSystem {
    persistent agreements = [];

    persistent correspondents = {
        companyA : "oldSystemA",
        comapnyB : "oldSystemB"
    };

    routes {
        "/create" -> create
        "/send" -> send 
        "/sign" -> sign
        "/decline" -> decline
        "/retract" -> retract

        "/ext/create" -> extCreate
        "/ext/sign" -> extSign
        "/ext/decline" -> extDecline
        "/ext/retract" -> extRetract
    }

    code {
        function create(request) {
            agreements = getPersistent("aggreements") ;
            
            aggreement = {
                id : len(agreements) ,
                correspondents : request . agreements . correspondents ,
                signs : [] 
            } ;
            aggreements = append(aggreements, aggreement) ;
            setPersistent("aggreements", aggreements) ;
            respond(aggreement) ;
        }
    }
}

init {
    user = { 
        "name" : "newCompanyEmployee"
    } ;
    response = request("newSystem", "/create", { 
        user : user,
        aggreement : {
            correspondents : [ "companyA", "companyB" ]
        }
    });
    id = response . id ;
    request("newSystem", "/send", {
        user : user,
        id : id
    }) ;
}
