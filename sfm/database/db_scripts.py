create_table_statement = """CREATE TABLE IF NOT EXISTS ImageInfo(
        imgid    TEXT     PRIMARY KEY,
        file     TEXT     NOT NULL UNIQUE,
        height   INTEGER  NOT NULL,
        width    INTEGER  NOT NULL,
        channel  INTEGER  NOT NULL DEFAULT 0,
    );"""
