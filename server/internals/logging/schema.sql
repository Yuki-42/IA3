/*
Initialise logs database. More detailed database layout can be found in [docs/database.md](docs/database.md)

LANG=PGSQL
*/

/* Activate the UUID Extension if it is not already active */
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

/* Create tables */
CREATE TABLE IF NOT EXISTS ia3.program_logs
(
    id           uuid      NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    timestamp    TIMESTAMP NOT NULL,
    level        INT       NOT NULL,
    filename     TEXT      NOT NULL,
    funcname     TEXT      NOT NULL,
    lineno       TEXT      NOT NULL,
    message      TEXT      NOT NULL,
    module       TEXT      NOT NULL,
    name         TEXT      NOT NULL,
    pathname     TEXT      NOT NULL,
    process      TEXT      NOT NULL,
    process_name TEXT      NOT NULL,
    thread       TEXT,
    thread_name  TEXT
);

CREATE TABLE IF NOT EXISTS ia3.requests
(
    id                VARCHAR(36) NOT NULL PRIMARY KEY,
    log_id            uuid NOT NULL,
    view_args         JSONB,
    routing_exception TEXT,
    endpoint          TEXT,
    blueprint         TEXT,
    blueprints        TEXT[],
    accept_languages  TEXT,
    accept_mimetypes  TEXT,
    access_route      TEXT[],
    args              JSONB,
    "authorization"   TEXT,
    base_url          TEXT,
    cookies           JSONB,
    full_path         TEXT,
    host              TEXT,
    host_url          TEXT,
    url               TEXT,
    method            TEXT,
    headers           TEXT,
    remote_addr       TEXT        NOT NULL
);

CREATE TABLE IF NOT EXISTS ia3.responses
(
    id          VARCHAR(36) NOT NULL PRIMARY KEY,
    request_id  VARCHAR(36) NOT NULL,
    expires     TIMESTAMP,
    location    TEXT,
    status      TEXT,
    status_code INT,
    headers     TEXT,
    response    TEXT
);

/* Create indexes that don't exist */
CREATE INDEX program_logs_timestamp ON ia3.program_logs (timestamp);
CREATE INDEX program_logs_level ON ia3.program_logs (level);
CREATE INDEX program_logs_funcname ON ia3.program_logs (funcname);
CREATE INDEX program_logs_module ON ia3.program_logs (module);
CREATE INDEX program_logs_name ON ia3.program_logs (name);

CREATE INDEX requests_log_id ON ia3.requests (log_id);
CREATE INDEX requests_endpoint ON ia3.requests (endpoint);
CREATE INDEX requests_blueprint ON ia3.requests (blueprint);
CREATE INDEX requests_method ON ia3.requests (method);
CREATE INDEX requests_remote_addr ON ia3.requests (remote_addr);

CREATE INDEX responses_request_id ON ia3.responses (request_id);
CREATE INDEX responses_status_code ON ia3.responses (status_code);

/* Create foreign keys */
/* YEAH NO. THIS FOR SOME REASON BREAKS THE DATABASE. */

/* Give all permissions to the loghandler user */
GRANT ALL ON ALL TABLES IN SCHEMA ia3 TO loghandler;