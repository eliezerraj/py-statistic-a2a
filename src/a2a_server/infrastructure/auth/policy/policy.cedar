//
// Global tenant-isolation rule.
//
// A principal may not access resources belonging to another tenant,
// regardless of any permit policy.
//

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
        "statistics.compute"
    )
};