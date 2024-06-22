import sqlite3
from data_collection import get_elements, get_compounds
from data_processing import get_compound_components
import db_setup


def build_prompt(table, prompt_dict):
    sql = f"""SELECT * FROM {table}"""
    i = 0
    for key, value in prompt_dict.items():
        if i == 0:
            sql = sql + f" WHERE (component = '{key}' AND count = {value})"
        else:
            sql = sql + f""" AND name IN (SELECT name FROM {table} WHERE component = '{key}' AND count = {value}"""
        if i == len(prompt_dict) - 1:
            sql = sql + ");"
        i += 1
    return sql


class Database:

    def __init__(self):
        self.conn = sqlite3.connect("compounds.db")
        self.setup_tables()

    def setup_tables(self):
        db_setup.setup_compounds_table(self.conn)
        db_setup.setup_compound_component_tables(self.conn)
        db_setup.setup_elements_table(self.conn)

    def add_compounds(self):
        compounds_sql = """INSERT INTO compounds(name, equation) VALUES (?, ?)"""
        components_sql = """ INSERT INTO compoundsComponents(name,component,count)
                  VALUES(?,?,?) """
        cur = self.conn.cursor()
        compounds = get_compounds()
        for key, value in compounds.items():
            cur.execute(compounds_sql, (key, value))
            unique_id = cur.lastrowid
            components = get_compound_components(value)
            for name, number in components.items():
                cur.execute(components_sql, (unique_id, name, number,))
        self.conn.commit()
        return cur.lastrowid

    def add_elements(self):
        sql = """INSERT INTO elements(name, equation) VALUES (?, ?)"""
        cur = self.conn.cursor()
        elements = get_elements()
        for key, value in elements.items():
            cur.execute(sql, (value, key))
        self.conn.commit()
        return cur.lastrowid

    def get_name_from_id(self, table, unique_id):
        cur = self.conn.cursor()
        cur.execute(f"SELECT * FROM {table} WHERE id = ?", (unique_id,))
        return cur.fetchone()

    def find_prompt(self, input_dict):
        # TODO make work for other layers
        cur = self.conn.cursor()
        sql = build_prompt("compoundsComponents", input_dict)
        cur.execute(sql)
        sample = cur.fetchall()
        if sample is None:
            return None
        for row in sample:
            if len(input_dict) == self.find_number_for_id(row[1])[0]:
                return self.get_name_from_id("compounds", row[1])
        return None

    def find_number_for_id(self, unique_id):
        cur = self.conn.cursor()
        sql = f"""SELECT COUNT(*) AS row_count FROM compoundsComponents WHERE name = {unique_id};"""
        cur.execute(sql)
        sample = cur.fetchone()
        if sample is None:
            return None
        return sample
