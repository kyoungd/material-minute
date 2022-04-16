#!/usr/bin/python
import os
from configparser import ConfigParser


def configWithEnvironmentVariables(db):
    if 'DATABASE_HOST' in os.environ:
        db['host'] = os.environ['DATABASE_HOST']
    if 'DATABASE_NAME' in os.environ:
        db['database'] = os.environ['DATABASE_NAME']
    if 'DATABASE_PORT' in os.environ:
        db['port'] = os.environ['DATABASE_PORT']
    if 'DATABASE_USERNAME' in os.environ:
        db['user'] = os.environ['DATABASE_USERNAME']
    if 'DATABASE_PASSWORD' in os.environ:
        db['password'] = os.environ['DATABASE_PASSWORD']
    return db


def config(filename='./app/dbase/database.ini', section='postgresql'):
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

    db1 = configWithEnvironmentVariables(db)
    return db1
