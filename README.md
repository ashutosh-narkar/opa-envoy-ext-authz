# WIP: opa-envoy-ext-authz

This document is a WIP.

OPA-Envoy(v1.10.0) External Authorization Example.

## Overview

Example of using Envoy's [External authorization filter](https://www.envoyproxy.io/docs/envoy/v1.10.0/intro/arch_overview/ext_authz_filter.html) with OPA as an authorization service.

## Example

WIP

## Running the Example

### Step 1: Install Docker

Ensure that you have recent versions of `docker` and `docker-compose` installed.

### Step 2: Start containers

```bash
$ docker-compose up --build -d
$ docker-compose ps

                Name                               Command               State                            Ports
----------------------------------------------------------------------------------------------------------------------------------------
opa-envoy-ext-authz_api-server-1_1      flask run --host=0.0.0.0         Up      0.0.0.0:5000->5000/tcp
opa-envoy-ext-authz_api-server-2_1      flask run --host=0.0.0.0         Up      0.0.0.0:5001->5000/tcp, 5001/tcp
opa-envoy-ext-authz_backend-service_1   /bin/sh -c /usr/local/bin/ ...   Up      10000/tcp, 80/tcp
opa-envoy-ext-authz_db-service_1        /bin/sh -c /usr/local/bin/ ...   Up      10000/tcp, 80/tcp
opa-envoy-ext-authz_front-envoy_1       /docker-entrypoint.sh /bin ...   Up      10000/tcp, 0.0.0.0:8000->80/tcp, 0.0.0.0:8001->8001/tcp
opa-envoy-ext-authz_opa_1               ./opa_istio_linux_amd64 -- ...   Up      0.0.0.0:9191->9191/tcp
opa-envoy-ext-authz_web-service_1       /bin/sh -c /usr/local/bin/ ...   Up      10000/tcp, 80/tcp
```

### Step 3: Test Ingress Policy

```bash
$ curl -i localhost:5000/hello

HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 29
Server: Werkzeug/0.15.2 Python/2.7.15
Date: Fri, 19 Apr 2019 09:44:46 GMT

Hello from the WEB service !
```

```bash
$ curl -i localhost:5001/hello

HTTP/1.0 403 FORBIDDEN
Content-Type: text/html; charset=utf-8
Content-Length: 40
Server: Werkzeug/0.15.2 Python/2.7.15
Date: Fri, 19 Apr 2019 09:45:19 GMT

Access to the Web service is forbidden.
```

### Step 4: Test Service-To-Service Policy

```bash
$ curl -i localhost:5000/the/good/path

HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 35
Server: Werkzeug/0.15.2 Python/2.7.15
Date: Fri, 19 Apr 2019 09:48:29 GMT

Allowed path: WEB -> BACKEND -> DB
```

```bash
$ curl -i localhost:5000/the/bad/path

HTTP/1.0 403 FORBIDDEN
Content-Type: text/html; charset=utf-8
Content-Length: 26
Server: Werkzeug/0.15.2 Python/2.7.15
Date: Fri, 19 Apr 2019 09:48:46 GMT

Forbidden path: WEB -> DB
```
