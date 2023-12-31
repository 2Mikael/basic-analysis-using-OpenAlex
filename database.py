import mariadb

connection_parameters = {
    "user": "root", 
    "password": "password",
    "database": "openalex_database",
    "host": "localhost"
}

tables = ["dataset1", "dataset2", "dataset3"]

"""
Requirements:
- MariaDB installed and running (as a service in the background)
- Database "openalex_database" and tables "dataset1", "dataset2", and "dataset3" must exist

Setup commands (you can use MariaDB(MySQL) client terminal):
- CREATE DATABASE openalex_database;
- USE openalex_database;
- CREATE TABLE dataset1 (
    title VARCHAR(2000) NOT NULL,
    authors VARCHAR(2000) NOT NULL,
    abstract TEXT NOT NULL
);

Notes:
- Repeat CREATE TABLE for dataset2 and dataset3
- To empty a table, use "TRUNCATE TABLE table_name;"
- To destroy a table/database, use "DROP TABLE/DATABASE table_or_database_name;"
"""

#----------------------------------------------------------------
#- Data Handling ------------------------------------------------
#----------------------------------------------------------------
def run_command(command: str, data: tuple):
    # with-clauses automatically close the connection and cursor after returning
    with mariadb.connect(**connection_parameters) as connection:
        with connection.cursor() as cursor:
            cursor.execute(command, data)
            connection.commit()
            if cursor.rowcount > 1:
                return cursor.fetchall()

def add_work(title: str, authors: str, abstract: str, table: str):
    if not table in tables:
        return
    command = "INSERT INTO " + table + "(title, authors, abstract) VALUES(%s, %s, %s);"
    data = (title, authors, abstract)
    run_command(command, data)

def get_works(table: str) -> dict:
    """
    Returns data in form of [(title, authors, abstract)]
    """
    if not table in tables:
        return
    command = "SELECT * FROM " + table + ";"
    data = ()
    return run_command(command, data)