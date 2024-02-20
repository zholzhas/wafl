(service backend {
    listen {
        "a" -> login
        "b" -> login
    }

    code {
        function login(request) {
            lock("a");
            unlock("a");
        }
    }
}


init {
    message("a", "1");
    message("b", "2");
})