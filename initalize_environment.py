"""Convienence CLI utility to initialize the local development database.

Convienece command line utility to initialize a local development database,
taking a single argument for the database type. Acceptable values for that
single argument include "development" and "test" as strings.

@author: A. Samuel Pottinger (Gleap LLC, 2013)
@author: Joanne Cheng (Colorado Code for Communities, 2013)
@license: Apache v2
"""

import sys
import subprocess

import sqlalchemy
import yaml

import database

# TODO(samnsparky): These should not have %s. Unsafe in some contexts.
CONFIG_DATABASE_INFO_KEY = 'database'
ENGINE_TEMPLATE = 'postgresql://%s:%s@localhost/postgres'
CREATE_CMD_TEMPLATE = 'CREATE DATABASE %s WITH ENCODING=\'UNICODE\''
ROLE_CMD_TEMPLATE = 'CREATE ROLE %s LOGIN PASSWORD \'%s\';'
NUM_REG_ARGS = 2
USAGE_MESSAGE = 'usage: python initialize_environment.py database_type\n'
INVALID_TYPE_MESSAGE = '%s is not a valid database type. Valid types: %s.\n'
POSTGIS_EXTENSIONS_DIR_KEY = 'postgis_extensions_dir'


def get_env_config():
    """Load the config.yaml environment configuration settings.

    @return: Settings loaded from the local configuration YAML file.
    @rtype: dict
    """
    return yaml.load(open('config.yaml', 'r'))


def create_db_lang(database_name):
    """Creates a new programming langage for SQL Procedural Language

    Creates a new programming language in the given database for SQL Procedural
    Lanaguage.

    @param database_name: The name of the database to create the new langauge
        in.
    @type database_name: str
    """
    cmd_elements = ['createlang', 'plpgsql', database_name]
    subprocess.call(cmd_elements)


def install_postgis(database_name):
    """Install the PostGIS extension to the given database.

    @param database_name: The name of the database to install the extension in.
    @type database_name: str
    """
    cmd_elements = [
        'psql',
        '-d',
        database_name,
        '-c',
        'CREATE EXTENSION IF NOT EXISTS postgis'
    ]
    subprocess.call(cmd_elements)


def create_db_engine(database_user, database_password):
    """Create a sqlalchemy database engine with the given credentials.

    Create a sqlalchemy database engine for the local development database using
    the given database credentials.

    @param database_user: The name of the user to access the database with.
    @type database_user: str
    @param database_password: The password to use for that user.
    @type database_password: str
    """
    engine_url = ENGINE_TEMPLATE % (database_user, database_password)
    return sqlalchemy.create_engine(engine_url)


def create_db(conn, database_name):
    """Create a local development or test database.

    @param conn: Connection to the local running Postgres server.
    @type conn: DBAPI-valid connection
    @param database_name: The name of the database to create.
    @type database_name: str
    """
    create_cmd = CREATE_CMD_TEMPLATE % database_name
    conn.connection.set_isolation_level(0)
    conn.execute(create_cmd)
    conn.connection.set_isolation_level(1)
    conn.execute('commit')


def create_user(database_user, database_password):
    """Create a new user on the local Postgres server.

    @param database_user: The name of the user to create.
    @type database_user: str
    @param database_password: The password to give that new user.
    @type database_password: str
    """
    create_cmd = ROLE_CMD_TEMPLATE % (database_user, database_password)
    cmd_elements = [
        'psql',
        '-c',
        create_cmd
    ]
    subprocess.call(cmd_elements)


def is_valid_database_type(database_type, env_config):
    """Determine if the given database type can be initialized with this script.

    @param database_type: The name of the database type to check for.
    @type database_type: str
    @param env_config: Environment configuration settings, possibly loaded from
        the YAML configuration file.
    @type env_config: dict
    @return: True if the database type is recognized and can be initialized by
        this script and False otherwise.
    @rtype: bool
    """
    return database_type in env_config[CONFIG_DATABASE_INFO_KEY]


def display_invalid_type_message(database_type, env_config):
    """Display a message indicating that the user requested an invalid db type.

    Display a message indicating that ht user requested the initialization of an
    invalid or unrecognized database type. The message is written to stderr and
    includes valid options.

    @param database_type: The name of the database type the user requested.
    @type database_type: str
    @param env_config: Environment configuration settings, possibly loaded from
        the YAML configuration file.
    """
    valid_types = filter(lambda x: x != POSTGIS_EXTENSIONS_DIR_KEY,
        env_config[CONFIG_DATABASE_INFO_KEY])
    valid_types_str = ', '.join(valid_types)
    sys.stderr.write(INVALID_TYPE_MESSAGE % (database_type, valid_types_str))


def main(database_type):
    """Driver for this CLI utility.

    @param database_type: The name of the type of database to initialize.
        Typical values include development or test.
    @type database_type: str
    """
    env_config = get_env_config()

    if not is_valid_database_type(database_type, env_config):
        display_invalid_type_message(database_type, env_config)
        return

    db_init_config = env_config[CONFIG_DATABASE_INFO_KEY][database_type]
    
    user = db_init_config['user']
    password = db_init_config['pass']
    database_name = db_init_config['db']

    create_user(user, password)

    engine = create_db_engine(user, password)
    connection = engine.connect()

    create_db(connection, database_name)
    create_db_lang(database_name)
    install_postgis(database_name)
    database.init_db()

    connection.close()


if __name__ == '__main__':
    if len(sys.argv) != NUM_REG_ARGS:
        sys.stderr.write(USAGE_MESSAGE)
    else:
        main(sys.argv[1])

