#!/usr/bin/python
import psycopg2
import pandas as pd
import json
import datetime
import logging

#!/usr/bin/python
import os
from configparser import ConfigParser

def config(filename='./db.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} not found in the {1} file'.format(section, filename))

    return db

class DB:
    def __init__(self):
        self.conn = self.db_connection()

    def db_connection(self):
        conn = None
        try:
            # read connection parameters
            params = config()
            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**params)
            return conn
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None

    def SelectQuery(self, sql, params):
        try:
            cur = self.conn.cursor()
            cur.execute(sql, params)
            result = cur.fetchall()
            if (result == None):
                return False, None
            else:
                return True, result
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(f'DB.SelectQuery() - {error}')
            print(error)
            return False, None

    def ExecuteQuery(self, sql, params):
        try:
            cur = self.conn.cursor()
            cur.execute(sql, params)
            self.conn.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(f'DB.ExecuteQuery() - {error}')
            print(error)
            return False

