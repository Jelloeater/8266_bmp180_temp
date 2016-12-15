import argparse
import logging
import socketserver
import json
import sqlalchemy

__author__ = 'Jesse'

logging.basicConfig(format="[%(asctime)s] [%(levelname)8s] --- %(message)s (%(filename)s:%(lineno)s)",
                    level=logging.DEBUG)


# from sqlalchemy.dialects.sqlite import \
#     BLOB, BOOLEAN, CHAR, DATE, DATETIME, DECIMAL, FLOAT, \
#     INTEGER, NUMERIC, SMALLINT, TEXT, TIME, TIMESTAMP, \
#     VARCHAR

# Global ORM BASE, used by module
BASE = sqlalchemy.ext.declarative.declarative_base()


def get_engine():
    return sqlalchemy.create_engine('sqlite:///TemperatureData.db')


def get_session():
    engine = get_engine()
    BASE.metadata.bind = engine
    DBSession = sqlalchemy.orm.sessionmaker(bind=engine)
    return DBSession()


# Classes are directly mapped to tables, without the need for a mapper binding (ex mapper(Class, table_definition))
class Email(BASE):
    from sqlalchemy import Column, Integer, String
    """Defines Device object relational model, is used for both table creation and object interaction"""
    __tablename__ = 'Email'
    device_id = Column('device_id', Integer, primary_key=True)
    username = Column('username', String, nullable=False)

    # Helper methods
    @staticmethod
    def get_all_rows():
        session = get_session()
        return session.query(Email).all()


class DatabaseSetup:
    def __init__(self):
        pass

    @staticmethod
    def setup_sql_environment():
        logging.debug('Creating table if not already present')
        DatabaseSetup.create_tables()


    @staticmethod
    def create_tables():
        engine = get_engine()
        print('Are you sure to want to DROP ALL TABLES, this cannot be undone!')
        if input('({0})>'.format('Type YES to continue')) == 'YES':
            BASE.metadata.drop_all(engine)
            BASE.metadata.create_all(engine)
            print('DATABASE RE-INITIALIZED')
        else:
            print('Skipping database re-initialization')


class TableOutput(object):
    @staticmethod
    def create_table(header_list_in, data_list_in):
        from prettytable import PrettyTable
        t = PrettyTable(header_list_in)
        for i in data_list_in:
            t.add_row(i)
        return str(t)


class SocketServer(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        logging.debug("{} wrote:".format(self.client_address[0]))
        logging.debug(self.data)

        data_string = self.data.decode("utf-8")
        data_obj = json.loads(data_string)

        logging.debug(data_obj)

        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())


class main(object):
    @staticmethod
    def run():
        parser = argparse.ArgumentParser()
        parser.add_argument("-s", "--setup", action="store_true", help="Setup Environment")
        args = parser.parse_args()

        if args.setup:
            DatabaseSetup.setup_sql_environment()

    HOST, PORT = "", 1337

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), SocketServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()


if __name__ == "__main__":
    main.run()