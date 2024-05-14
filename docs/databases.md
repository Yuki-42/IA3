# Databases

## Table of Contents

- [Logs](#logs)

## Logs

The logging for this project makes use of an SQLite database. The database is created in the `logs` directory and
is named `logs.db`.

### Schema

The database has 4 tables, `program_logs`, `web`, `requests`, and `responses`.

#### `program_logs`

The `program_logs` table is used to store logs from the program unrelated to web requests. The table has the following
columns:

| Column Name  | Data Type   | Description                                                                      | Nullable | PK  | FK | Gen | 
|--------------|-------------|----------------------------------------------------------------------------------|----------|-----|----|-----|
| id           | VARCHAR(36) | Primary key of the log record. This is a UUID generated when the log is created. | No       | Yes | No | No  |
| timestamp    | TIMESTAMP   | The time the log was created.                                                    | No       | No  | No | No  |
| level        | INT         | The log level. This is an integer value.                                         | No       | No  | No | No  |
| filename     | TEXT        | The name of the file that the log was created in.                                | No       | No  | No | No  |
| funcname     | TEXT        | The name of the function that the log was created in.                            | No       | No  | No | No  |
| lineno       | INT         | The line number that the log was created on.                                     | No       | No  | No | No  |
| message      | TEXT        | The log message.                                                                 | No       | No  | No | No  |
| module       | TEXT        | The module that the log was created in.                                          | No       | No  | No | No  |
| name         | TEXT        | The name of the logger that created the log.                                     | No       | No  | No | No  |
| pathname     | TEXT        | The full path to the file that the log was created in.                           | No       | No  | No | No  |
| process      | INT         | The process ID of the program that created the log.                              | No       | No  | No | No  |
| process_name | TEXT        | The name of the process that created the log.                                    | No       | No  | No | No  |
| thread       | INT         | The thread ID of the thread that created the log.                                | Yes      | No  | No | No  |
| thread_name  | TEXT        | The name of the thread that created the log.                                     | Yes      | No  | No | No  |
| task_name    | TEXT        | The name of the task that created the log.                                       | Yes      | No  | No | No  |

#### `requests`

The `requests` table is used to store logs from web requests. The table has the following columns:

| Column Name       | Data Type   | Description                                                                                                  | Nullable | PK  | FK  | Gen |
|-------------------|-------------|--------------------------------------------------------------------------------------------------------------|----------|-----|-----|-----|
| id                | VARCHAR(36) | Primary key of the log record. This is a UUID generated when the request is created.                         | No       | Yes | No  | No  |
| log_id            | VARCHAR(36) | The ID of the log record in the `program_logs` table that this request is related to.                        | No       | No  | Yes | No  |
| view_args         | TEXT        | The view arguments that were passed to the view function.                                                    | Yes      | No  | No  | No  |
| routing_exception | TEXT        | The routing exception that occurred during the request.                                                      | Yes      | No  | No  | No  |
| endpoint          | TEXT        | The endpoint that the request was made to.                                                                   | Yes      | No  | No  | No  |
| blueprint         | TEXT        | The blueprint that the endpoint is in.                                                                       | Yes      | No  | No  | No  |
| blueprints        | TEXT        | The blueprints that the endpoint is in.                                                                      | Yes      | No  | No  | No  |
| accept_languages  | TEXT        | The accept languages that were passed in the request.                                                        | Yes      | No  | No  | No  |
| accept_mimetypes  | TEXT        | The accept mimetypes that were passed in the request.                                                        | Yes      | No  | No  | No  |
| access_route      | TEXT        | If a forwarded header exists this is a list of all ip addresses from the client ip to the last proxy server. | Yes      | No  | No  | No  |
| args              | TEXT        | The url parameters.                                                                                          | Yes      | No  | No  | No  |
| authorization     | TEXT        | The authorization header.                                                                                    | Yes      | No  | No  | No  |
| base_url          | TEXT        | The base url of the request.                                                                                 | Yes      | No  | No  | No  |
| cookies           | TEXT        | The cookies that were passed in the request.                                                                 | Yes      | No  | No  | No  |
| full_path         | TEXT        | The full path of the request.                                                                                | Yes      | No  | No  | No  |
| host              | TEXT        | The host the request was made to.                                                                            | Yes      | No  | No  | No  |
| host_url          | TEXT        | The host url of the request.                                                                                 | Yes      | No  | No  | No  |
| url               | TEXT        | The full url of the request.                                                                                 | Yes      | No  | No  | No  |
| method            | TEXT        | The request method.                                                                                          | Yes      | No  | No  | No  |
| headers           | TEXT        | The headers that were passed in the request.                                                                 | Yes      | No  | No  | No  |
| remote_addr       | TEXT        | The remote address of the request.                                                                           | Yes      | No  | No  | No  |

#### `responses`

The `responses` table is used to store logs from web responses. The table has the following columns:

| Column Name | Data Type   | Description                                                                                                                                                                      | Nullable | PK  | FK  | Gen |
|-------------|-------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|-----|-----|-----|
| id          | VARCHAR(36) | Primary key of the log record. This is a UUID generated when the response is created.                                                                                            | No       | Yes | No  | No  |
| request_id  | VARCHAR(36) | The id of the request that this response is for.                                                                                                                                 | No       | No  | Yes | No  |
| expires     | TIMESTAMP   | The time the response expires.                                                                                                                                                   | Yes      | No  | No  | No  |
| location    | TEXT        | The Location response-header field is used to redirect the recipient to a location other than the Request-URI for completion of the request or identification of a new resource. | Yes      | No  | No  | No  |
| status      | TEXT        | The status code of the response.                                                                                                                                                 | Yes      | No  | No  | No  |
| status_code | INT         | The status code of the response.                                                                                                                                                 | Yes      | No  | No  | No  |
| headers     | TEXT        | The headers that were passed in the response.                                                                                                                                    | Yes      | No  | No  | No  |
| response    | TEXT        | The response data.                                                                                                                                                               | Yes      | No  | No  | No  |
