# Databases

## Table of Contents

- [Logs](#logs)

## Logs

The logging for this project makes use of an SQLite database. The database is created in the `logs` directory and 
is named `logs.db`. 

### Schema

The database has 4 tables, `program_logs`, `web`, `requests`, and `responses`.

#### `program_logs`

The `program_logs` table is used to store logs from the program unrelated to web requests. The table has the following columns:

| Column Name | Data Type   | Description                    | Nullable | PK  | FK |
|-------------|-------------|--------------------------------|----------|-----|----|
| id          | VARCHAR(36) | Primary key of the log record. | No       | Yes | No |
