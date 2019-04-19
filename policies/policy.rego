package envoy.authz

import input.attributes.request.http as http_request
import input.attributes.source.address as source_address

default allow = false

# allow access to Web service from the subnet 172.28.0.0/16
allow {
    http_request.path == "/hello"
    net.cidr_contains("172.28.0.0/16", source_address.Address.SocketAddress.address)
}

# allow access to Web service from the subnet 172.28.0.0/16
allow {
    http_request.path == "/the/good/path"
    net.cidr_contains("172.28.0.0/16", source_address.Address.SocketAddress.address)
}

# allow access to Web service from the subnet 172.28.0.0/16
allow {
    http_request.path == "/the/bad/path"
    net.cidr_contains("172.28.0.0/16", source_address.Address.SocketAddress.address)
}

# allow Web service to access Backend service
allow {
    http_request.path == "/good"
    svc_name == "web"
}

# allow Backend service to access DB service
allow {
    http_request.path == "/good/db"
    svc_name == "backend"
}

svc_name = parsed {
    [_, encoded] := split(http_request.headers.authorization, " ")
    [parsed, _] := split(base64url.decode(encoded), ":")
}
