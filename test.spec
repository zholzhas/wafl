service a0 { 
    code {!
        function main() {
            a = 1 + 5 ;
            respond("123") ;
        }
    !}
    routes {
        "/main" -> "main"
    }
};

service a1 { 
    empty 
}; 

service a2 { 
    empty 
};