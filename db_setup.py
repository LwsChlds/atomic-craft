from sqlite3 import Error


def setup_compound_component_tables(conn):
    compounds_table = """ CREATE TABLE IF NOT EXISTS compoundsComponents (
                                        id integer PRIMARY KEY,      
                                        name integer,
                                        component text,
                                        count integer,
                                        FOREIGN KEY (name) REFERENCES compounds(id)
                                    ); """
    try:
        c = conn.cursor()
        c.execute(compounds_table)
    except Error as e:
        print(e)


def setup_compounds_table(conn):
    compounds_table = """ CREATE TABLE IF NOT EXISTS compounds (
                                        id integer PRIMARY KEY,
                                        name text,
                                        equation text
                                    ); """
    try:
        c = conn.cursor()
        c.execute(compounds_table)
    except Error as e:
        print(e)


def setup_elements_table(conn):
    compounds_table = """ CREATE TABLE IF NOT EXISTS elements (
                                        id integer PRIMARY KEY,
                                        name text,
                                        equation text
                                    ); """
    try:
        c = conn.cursor()
        c.execute(compounds_table)
    except Error as e:
        print(e)