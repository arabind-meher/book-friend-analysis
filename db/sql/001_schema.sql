-- db/sql/001_schema.sql

CREATE SCHEMA IF NOT EXISTS library;
SET search_path TO library, public;

-- users: [id, username]
CREATE TABLE IF NOT EXISTS users
(
    id       UUID PRIMARY KEY,
    username TEXT NOT NULL UNIQUE
);

-- books (summary at the end)
CREATE TABLE IF NOT EXISTS books
(
    id              UUID PRIMARY KEY,
    title           TEXT NOT NULL,
    author          TEXT,
    "year"          INTEGER,
    description     TEXT,
    image_url       TEXT,
    reviews_count   INTEGER,
    rating          NUMERIC(3, 2) CHECK (rating BETWEEN 0 AND 5),
    featured_rating NUMERIC(3, 2) CHECK (featured_rating BETWEEN 0 AND 5),
    sentiment_score NUMERIC(3, 2) CHECK (sentiment_score BETWEEN 0 AND 5),
    summary         TEXT
);

-- rating: [user_id, book_id, rating]
CREATE TABLE IF NOT EXISTS rating
(
    user_id UUID     NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    book_id UUID     NOT NULL REFERENCES books (id) ON DELETE CASCADE,
    rating  SMALLINT NOT NULL CHECK (rating BETWEEN 0 AND 5),
    PRIMARY KEY (user_id, book_id)
);

-- genres
CREATE TABLE IF NOT EXISTS genres
(
    id   UUID PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

-- book_genres (M:N)
CREATE TABLE IF NOT EXISTS book_genres
(
    book_id  UUID NOT NULL REFERENCES books (id) ON DELETE CASCADE,
    genre_id UUID NOT NULL REFERENCES genres (id) ON DELETE CASCADE,
    PRIMARY KEY (book_id, genre_id)
);

-- media types (Paper / Audiobook / Ebook, etc.)
CREATE TABLE IF NOT EXISTS media_types
(
    id   UUID PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

-- book_media_types (M:N)
CREATE TABLE IF NOT EXISTS book_media_types
(
    book_id       UUID NOT NULL REFERENCES books (id) ON DELETE CASCADE,
    media_type_id UUID NOT NULL REFERENCES media_types (id) ON DELETE CASCADE,
    PRIMARY KEY (book_id, media_type_id)
);

-- Essential indexes
CREATE INDEX IF NOT EXISTS idx_rating_user ON rating (user_id);
CREATE INDEX IF NOT EXISTS idx_rating_book ON rating (book_id);

------------------------------------------------------------------
-- Hybrid recommendation table: top 5 recs per base book
------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS book_recs
(
    base_book_id UUID        NOT NULL REFERENCES books (id) ON DELETE CASCADE,
    rec_book_id  UUID        NOT NULL REFERENCES books (id) ON DELETE CASCADE,
    rank         SMALLINT    NOT NULL CHECK (rank BETWEEN 1 AND 5),
    score        REAL        NOT NULL, -- blended hybrid score
    reason       TEXT,                 -- optional explanation for debugging/explainability
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (base_book_id, rec_book_id)
);

CREATE INDEX IF NOT EXISTS idx_book_recs_base_rank
    ON book_recs (base_book_id, rank);
