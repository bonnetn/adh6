from src.entity.api_definition import EndpointDefinition, APIDefinition, Policy

adh6_endpoints = (
    EndpointDefinition(
        path_regex=r'^api/health/$',
        authz=Policy.ADMIN_ONLY,
    ),
    EndpointDefinition(
        path_regex=r'^api/',
        authz=Policy.DENY_ALL,
    ),
)
ENDPOINTS = {APIDefinition(
    host='https://api_server',
    cert='/run/secrets/api_server.crt',
    endpoints=adh6_endpoints,
)}
