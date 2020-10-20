import sqlite3


def create_connection(db_file):
    conn = None
    conn = sqlite3.connect(db_file)

    return conn


def insert_row(conn, timestamp, location, table):
    sql = f'INSERT INTO {table} (timestamp, location) values (?,?)'
    params = (timestamp, location)
    cur = conn.cursor()
    cur.execute(sql, params)

    conn.commit()


def clear_table(conn, table):
    sql = f'DELETE FROM {table}'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


def read_rows(conn, table):
    sql = f"SELECT * FROM {table}"
    cur = conn.cursor()
    cur.execute(sql)

    rows = cur.fetchall()

    conn.commit()

    return rows[0]

# create poopietable (
#     keupoopie (INT) PRIMARY KEY,
#     foreinkeymuziek = foreign key,
#     genrer

# )
