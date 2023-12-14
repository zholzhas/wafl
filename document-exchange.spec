
service newSystem {
    persistent agreements = [];

    persistent correspondents = {
        companyA : "oldSystemA",
        comapnyB : "oldSystemB"
    };

    routes {
        "/create" -> create
    }

    code {
        function create(request) {
            agreements = getPersistent("agreements") ;
            
            setPersistent("agreements", agreements) ;
            respond(agreement) ;
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
        assert(len(services . newSystem . persistents . agreements) < 1);
    }
}

