forbid(
    principal,
    action == Action::"send_message",
    resource == MessageType::"statistics.compute"
)
when {
    principal.client_id == "blocked-client"
};

permit(
    principal,
    action == Action::"send_message",
    resource == MessageType::"statistics.compute"
)
when {
    principal.scopes.contains(
        "statistics:compute"
    )
};
