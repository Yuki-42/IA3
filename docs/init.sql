/*
Initialise logs database. More detailed database layout can be found in [docs/database.md](docs/database.md)

LANG=SQLITE
*/

/* Create tables */
CREATE TABLE program_logs (
    id VARCHAR(36) NOT NULL PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    level INT NOT NULL,
    filename TEXT NOT NULL,
    funcname TEXT NOT NULL,
    lineno INT NOT NULL,
    message TEXT NOT NULL,
    module TEXT NOT NULL,
    name TEXT NOT NULL,
    pathname TEXT NOT NULL,
    process INT NOT NULL,
    process_name TEXT NOT NULL,
    thread INT,
    thread_name TEXT,
    task_name TEXT
);

CREATE TABLE requests (
    id VARCHAR(36) NOT NULL PRIMARY KEY,
    log_id VARCHAR(36) NOT NULL,
    view_args TEXT,
    routing_exception TEXT,
    endpoint TEXT,
    blueprint TEXT,
    blueprints TEXT,
    accept_languages TEXT,
    accept_mimetypes TEXT,
    access_route TEXT,
    args TEXT,
    authorization TEXT,
    base_url TEXT,
    cookies TEXT,
    full_path TEXT,
    host TEXT,
    host_url TEXT,
    url TEXT,
    method TEXT,
    headers TEXT,
    remote_addr TEXT
);

CREATE TABLE responses (
    id VARCHAR(36) NOT NULL PRIMARY KEY,
    request_id VARCHAR(36) NOT NULL,
    expires TIMESTAMP,
    location TEXT,
    status TEXT,
    status_code INT,
    headers TEXT,
    response TEXT
);

/* Create indexes that don't exist */
CREATE INDEX program_logs_timestamp ON program_logs (timestamp);
CREATE INDEX program_logs_level ON program_logs (level);
CREATE INDEX program_logs_funcname ON program_logs (funcname);
CREATE INDEX program_logs_module ON program_logs (module);
CREATE INDEX program_logs_name ON program_logs (name);

CREATE INDEX requests_log_id ON requests (log_id);
CREATE INDEX requests_endpoint ON requests (endpoint);
CREATE INDEX requests_blueprint ON requests (blueprint);
CREATE INDEX requests_method ON requests (method);
CREATE INDEX requests_remote_addr ON requests (remote_addr);

CREATE INDEX responses_request_id ON responses (request_id);
CREATE INDEX responses_status_code ON responses (status_code);
