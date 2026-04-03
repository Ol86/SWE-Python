SET default_tablespace = libraryspace;

CREATE TYPE gender AS ENUM ('MALE', 'FEMALE', 'DIVERS');
CREATE TYPE genre AS ENUM ('FANTASY', 'SCIENCE_FICTION', 'CRIME_NOVEL', 'THRILLER', 'NON_FICTION');

CREATE TABLE IF NOT EXISTS member (
    id              INTEGER GENERATED ALWAYS AS IDENTITY(START WITH 1000) PRIMARY KEY,
    username        TEXT NOT NULL UNIQUE,
    last_name       TEXT NOT NULL,
    first_name      TEXT NOT NULL,
    gender          gender,
    date_of_birth   DATE NOT NULL CHECK (date_of_birth < current_date),
    member_since    DATE CHECK (member_since <= current_date),
    is_student      BOOLEAN NOT NULL DEFAULT FALSE,
    email_address   TEXT NOT NULL UNIQUE,
    interests       JSONB,
    version         INTEGER NOT NULL DEFAULT 0,
    generated       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated         TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS member_last_name_idx ON member(last_name);

CREATE TABLE IF NOT EXISTS address (
    id              INTEGER GENERATED ALWAYS AS IDENTITY(START WITH 1000) PRIMARY KEY,
    postal_code     TEXT NOT NULL CHECK (postal_code ~ '\d{5}'),
    place           TEXT NOT NULL,
    member_id       INTEGER REFERENCES member ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS address_library_id_idx ON address(member_id);
CREATE INDEX IF NOT EXISTS address_postal_code_idx ON address(postal_code);

CREATE TABLE IF NOT EXISTS book (
    id              INTEGER GENERATED ALWAYS AS IDENTITY(START WITH 1000) PRIMARY KEY,
    name            TEXT NOT NULL,
    isbn            TEXT NOT NULL UNIQUE,
    author          TEXT,
    still_borrowed  BOOLEAN NOT NULL DEFAULT FALSE,
    genre           genre,
    member_id       INTEGER REFERENCES member ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS book_member_id_idx ON book(member_id);
