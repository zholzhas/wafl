service a0 { 
    persistent total = 1 ;
    code {
        function main(request) {
            b = {
                type : "response",
                in : request . out,
                out : request . in
            } ;
            respond(b) ;
        }
    }
    routes {
        "/main" -> main
    }
}

init {
    a = request("a0", "/main", { in : "out", out : "in" });
}