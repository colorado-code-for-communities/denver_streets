"""Unit testing for a CLI utility to initialize the local development database.

Unit testing for the command line based utility to initialize a local
development database. Requires pymox to run.

@author: A. Samuel Pottinger (samnsparky - Gleap LLC, 2013)
@author: Joanne Cheng (joannecheng - Colorado Code for Communities, 2013)
@license: Apache v2
"""

import subprocess
import unittest

import mox
import sqlalchemy

import database
import initalize_environment

DATABASE_TYPE = 'testtype'
DATABASE_NAME = 'testdb'
DATABASE_USER = 'user'
DATABASE_PASSWORD = 'pass'
ENGINE_URL = 'postgresql://user:pass@localhost/postgres'
EXPECTED_CREATE_COMMAND = 'CREATE DATABASE testdb WITH ENCODING=\'UNICODE\''
EXPECTED_ROLE_COMMAND = 'CREATE ROLE user LOGIN PASSWORD \'pass\';'

EXPECTED_CREATE_COMMANDS = [EXPECTED_CREATE_COMMAND, 'commit']
EXPECTED_ROLE_COMMANDS = [EXPECTED_ROLE_COMMAND, 'commit']

TEST_CONFIG_SETTINGS = {
    'database': {
        DATABASE_TYPE: {
            'user': DATABASE_USER,
            'pass': DATABASE_PASSWORD,
            'db': DATABASE_NAME
        }
    }
}


# TODO(samnsparky): These could ultimately be mocked using pymox.
class MockEngine:
    """Mock sqlalchemy engine."""

    def __init__(self, connection):
        """Create a new engine that returns the given connection.

        @param connection: The connection to return to the client when client
            code attempts to connect to the DB.
        @type connection: MockDBConnection
        """
        self.connection = connection

    def connect(self):
        """Stubbed out connect routine that returns a preloaded connection.

        @return: Mocked connection.
        @rtype: MockDBConnection
        """
        return self.connection


class MockDBInnerConnection:
    """Mock inner db-specific connection."""

    def __init__(self):
        """Create a new mocked PostgreSQL native connection."""
        self.isolation_levels = []

    def set_isolation_level(self, level):
        """Set the PostgreSQL-native isloation level."""
        self.isolation_levels.append(level)


class MockDBConnection:
    """Mock sqlalchemy wrapped DB connection."""

    def __init__(self):
        """Create a new Mock sqlalchemy wrapped DB connection.

        Create a new Mock sqlalchemy wrapped DB connection with an empty
        commands history.
        """
        self.last_commands = []
        self.connection = MockDBInnerConnection()

    def execute(self, command):
        """Simulate executing a command on this connection.

        @param command: The command to execute.
        @type command: str
        """
        self.last_commands.append(command)

    # TODO(samnsparky): Should check if connection is actually closed.
    def close(self):
        """Simulate closing the connection."""
        pass


class TestInitEnvironment(mox.MoxTestBase):
    """Test suite for initializing the local test environment."""

    def test_create_user(self):
        """Test creating a new user on the local PostgreSQL server."""
        expected_elements = ['psql', '-c', EXPECTED_ROLE_COMMAND]
        self.mox.StubOutWithMock(subprocess, 'call')

        subprocess.call(expected_elements).AndReturn(0)

        self.mox.ReplayAll()
        initalize_environment.create_user(DATABASE_USER, DATABASE_PASSWORD)

    def test_create_db_lang(self):
        """Test creating a database language on a local development database."""
        expected_elements = ['createlang', 'plpgsql', DATABASE_NAME]
        self.mox.StubOutWithMock(subprocess, 'call')

        subprocess.call(expected_elements).AndReturn(0)

        self.mox.ReplayAll()
        initalize_environment.create_db_lang(DATABASE_NAME)

    def test_install_postgis(self):
        """Test installing the PostGIS extension."""
        expected_elements = [
            'psql',
            '-d',
            DATABASE_NAME,
            '-c',
            'CREATE EXTENSION IF NOT EXISTS postgis'
        ]
        self.mox.StubOutWithMock(subprocess, 'call')

        subprocess.call(expected_elements).AndReturn(0)

        self.mox.ReplayAll()
        initalize_environment.install_postgis(DATABASE_NAME)

    def test_create_db_engine(self):
        """Test creating the sqlalchemy DB engine."""
        self.mox.StubOutWithMock(sqlalchemy, 'create_engine')
        sqlalchemy.create_engine(ENGINE_URL).AndReturn(True)

        self.mox.ReplayAll()
        engine = initalize_environment.create_db_engine(DATABASE_USER,
            DATABASE_PASSWORD)
        self.assertTrue(engine, True)

    def test_create_db(self):
        """Test creating a local development database through sqlalchemy."""
        mock_connection = MockDBConnection()
        initalize_environment.create_db(mock_connection, DATABASE_NAME)
        self.assertEqual(mock_connection.last_commands,
            EXPECTED_CREATE_COMMANDS)
        self.assertEqual(mock_connection.connection.isolation_levels, [0, 1])

    def test_main(self):
        """Test the high level environment initialization logic."""
        self.mox.StubOutWithMock(initalize_environment, 'create_user')
        self.mox.StubOutWithMock(initalize_environment, 'create_db_engine')
        self.mox.StubOutWithMock(initalize_environment, 'get_env_config')
        self.mox.StubOutWithMock(initalize_environment, 'create_db')
        self.mox.StubOutWithMock(initalize_environment, 'create_db_lang')
        self.mox.StubOutWithMock(initalize_environment, 'install_postgis')
        self.mox.StubOutWithMock(database, 'init_db')

        mock_connection = MockDBConnection()
        mock_engine = MockEngine(mock_connection)

        initalize_environment.create_user(DATABASE_USER,
            DATABASE_PASSWORD).AndReturn(None)
        initalize_environment.create_db_engine(DATABASE_USER,
            DATABASE_PASSWORD).AndReturn(mock_engine)
        initalize_environment.get_env_config().AndReturn(TEST_CONFIG_SETTINGS)
        initalize_environment.create_db(mock_connection,
            DATABASE_NAME).AndReturn(None)
        initalize_environment.create_db_lang(DATABASE_NAME).AndReturn(None)
        initalize_environment.install_postgis(DATABASE_NAME).AndReturn(None)
        database.init_db().AndReturn(mock_connection)

        self.mox.ReplayAll()
        initalize_environment.main(DATABASE_TYPE)


if __name__ == '__main__':
    unittest.main()
