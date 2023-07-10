service a0 { 
    code {!
        function main(request) {
            a = 1 + 5 ;
            respond("123") ;
        }
    !}
    routes {
        "/main" -> "main"
    }
}