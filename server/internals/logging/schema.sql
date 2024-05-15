/*
Initialise logs database. More detailed database layout can be found in [docs/database.md](docs/database.md)

LANG=PGSQL
*/

/* Create tables */
CREATE TABLE IF NOT EXISTS ia3.program_logs
(
    id           VARCHAR(36) NOT NULL PRIMARY KEY,
    timestamp    TIMESTAMP   NOT NULL,
    level        INT         NOT NULL,
    filename     TEXT        NOT NULL,
    funcname     TEXT        NOT NULL,
    lineno       INT         NOT NULL,
    message      TEXT        NOT NULL,
    module       TEXT        NOT NULL,
    name         TEXT        NOT NULL,
    pathname     TEXT        NOT NULL,
    process      INT         NOT NULL,
    process_name TEXT        NOT NULL,
    thread       INT,
    thread_name  TEXT
);

CREATE TABLE IF NOT EXISTS ia3.requests
(
    id                VARCHAR(36) NOT NULL PRIMARY KEY,
    log_id            VARCHAR(36) NOT NULL,
    view_args         TEXT,
    routing_exception TEXT,
    endpoint          TEXT,
    blueprint         TEXT,
    blueprints        TEXT,
    accept_languages  TEXT,
    accept_mimetypes  TEXT,
    access_route      TEXT,
    args              TEXT,
    "authorization"   TEXT,
    base_url          TEXT,
    cookies           TEXT,
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
ALTER TABLE ia3.requests ADD CONSTRAINT fk_requests_log_id FOREIGN KEY (log_id) REFERENCES ia3.program_logs (id);
ALTER TABLE ia3.responses ADD CONSTRAINT fk_responses_request_id FOREIGN KEY (request_id) REFERENCES ia3.requests (id);

/* Give all permissions to the loghandler user */
GRANT ALL ON ALL TABLES IN SCHEMA ia3 TO loghandler;