/*
Initialise logs database. More detailed database layout can be found in [docs/database.md](docs/database.md)

LANG=PGSQL
*/

/* Check what database is currently selected */
SELECT CURRENT_DATABASE();

/* Activate the UUID Extension if it is not already active */
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

/* Create tables */
CREATE TABLE IF NOT EXISTS ia3.program_logs
(
    id           uuid      NOT NULL PRIMARY KEY DEFAULT ia3.uuid_generate_v4(),
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
    id                uuid NOT NULL PRIMARY KEY,
    log_id            uuid NOT NULL,
    view_args         jsonb,
    routing_exception TEXT,
    endpoint          TEXT,
    blueprint         TEXT,
    blueprints        TEXT[],
    accept_languages  TEXT,
    accept_mimetypes  TEXT,
    access_route      TEXT[],
    args              jsonb,
    "authorization"   TEXT,
    base_url          TEXT,
    cookies           jsonb,
    full_path         TEXT,
    host              TEXT,
    host_url          TEXT,
    url               TEXT,
    method            TEXT,
    headers           TEXT,
    remote_addr       TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ia3.responses
(
    id          uuid NOT NULL PRIMARY KEY DEFAULT ia3.uuid_generate_v4(),
    request_id  uuid NOT NULL,
    expires     TIMESTAMP,
    location    TEXT,
    status      TEXT,
    status_code INT,
    headers     TEXT,
    response    TEXT
);

/* Create indexes that don't exist */
CREATE INDEX IF NOT EXISTS program_logs_timestamp ON ia3.program_logs (timestamp);
CREATE INDEX IF NOT EXISTS program_logs_level ON ia3.program_logs (level);
CREATE INDEX IF NOT EXISTS program_logs_funcname ON ia3.program_logs (funcname);
CREATE INDEX IF NOT EXISTS program_logs_module ON ia3.program_logs (module);
CREATE INDEX IF NOT EXISTS program_logs_name ON ia3.program_logs (name);

CREATE INDEX IF NOT EXISTS requests_log_id ON ia3.requests (log_id);
CREATE INDEX IF NOT EXISTS requests_endpoint ON ia3.requests (endpoint);
CREATE INDEX IF NOT EXISTS requests_blueprint ON ia3.requests (blueprint);
CREATE INDEX IF NOT EXISTS requests_method ON ia3.requests (method);
CREATE INDEX IF NOT EXISTS requests_remote_addr ON ia3.requests (remote_addr);

CREATE INDEX IF NOT EXISTS responses_request_id ON ia3.responses (request_id);
CREATE INDEX IF NOT EXISTS responses_status_code ON ia3.responses (status_code);

/* Create foreign keys */
ALTER TABLE ia3.requests
    ADD FOREIGN KEY (log_id) REFERENCES ia3.program_logs (id);
ALTER TABLE ia3.responses
    ADD FOREIGN KEY (request_id) REFERENCES ia3.requests (id);

/* Give all permissions to the loghandler user */
GRANT ALL ON ALL TABLES IN SCHEMA ia3 TO loghandler;

/* Create views */
DROP VIEW IF EXISTS ia3.web_logs;
DROP VIEW IF EXISTS ia3.simple_requests;
DROP VIEW IF EXISTS ia3.simple_responses;

/* View joins program_logs, requests, and responses. More columns will be manually added */
CREATE VIEW ia3.web_logs(timestamp, method, remote_addr, path, status) AS
SELECT program_logs.timestamp,
       requests.method,
       requests.remote_addr,
       requests.full_path,
       responses.status_code
FROM ia3.program_logs
         JOIN
     ia3.requests ON program_logs.id = requests.log_id
         JOIN
     ia3.responses ON requests.id = responses.request_id;

COMMENT ON VIEW ia3.web_logs IS 'Used for viewing unified web logs.';

ALTER VIEW ia3.web_logs
    OWNER TO loghandler;

CREATE VIEW ia3.simple_requests(method, remote_addr, full_path, cookies, args, view_args, id, log_id) AS
SELECT requests.method,
       requests.remote_addr,
       requests.full_path,
       requests.cookies,
       requests.args,
       requests.view_args,
       requests.id,
       requests.log_id
FROM ia3.requests;

COMMENT ON VIEW ia3.simple_requests IS 'Used to view requests in a more logical order and format.';

ALTER TABLE ia3.simple_requests
    OWNER TO loghandler;


CREATE VIEW ia3.simple_responses(status, status_code, request_id, headers, response) AS
SELECT response.status,
       response.status_code,
       response.request_id,
       response.headers,
       response.response
FROM ia3.responses response;

COMMENT ON VIEW ia3.simple_responses IS 'Used to view responses in a more logical order and format.';

ALTER TABLE ia3.simple_responses
    OWNER TO loghandler;


