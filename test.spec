
init {
    user = {
        type : "guest",
        session : "session-0"
    };
    request("backend", "/login", { user : user, user_id : "0" });
}