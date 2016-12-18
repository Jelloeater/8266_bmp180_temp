#!python
import argparse
import logging
import socketserver
import json
import datetime
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sys

__author__ = 'Jesse'

logging.basicConfig(format="[%(asctime)s] [%(levelname)8s] --- %(message)s (%(filename)s:%(lineno)s)",
                    level=logging.DEBUG)


class DatabaseHelper():
    # from sqlalchemy.dialects.sqlite import \
    # BLOB, BOOLEAN, CHAR, DATE, DATETIME, DECIMAL, FLOAT, \
    # INTEGER, NUMERIC, SMALLINT, TEXT, TIME, TIMESTAMP, \
    # VARCHAR

    def __init__(self):
        # Global ORM BASE, used by module
        self.BASE = declarative_base()

    def create_tables(self):
        logging.debug('Creating table if not already present')
        engine = self.get_engine()
        print('Are you sure to want to DROP ALL TABLES, this cannot be undone!')
        if input('({0})>'.format('Type YES to continue')) == 'YES':
            self.BASE.metadata.drop_all(engine)
            self.BASE.metadata.create_all(engine)
            print('DATABASE RE-INITIALIZED')
        else:
            print('Skipping database re-initialization')


    @staticmethod
    def get_engine():
        return sqlalchemy.create_engine('sqlite:///EnvData.db')

    def get_session(self):
        engine = DatabaseHelper.get_engine()
        self.BASE.metadata.bind = engine
        DBSession = sqlalchemy.orm.sessionmaker(bind=engine)
        return DBSession()

    def get_all_rows(self):
        session = self.get_session()
        return session.query(EnvData).all()

    def add_data(self,data_obj,client_ip):

        # Create DB obj class instance
        db_entry = EnvData()
        db_entry.client_ip = client_ip
        db_entry.timestamp = datetime.datetime.now().isoformat()
        db_entry.altitude = data_obj.altitude
        db_entry.p = data_obj.p
        db_entry.temp = data_obj.temp

        #Write DB obj to disk
        s = self.get_session()
        s.add(db_entry)
        s.commit()


# Classes are directly mapped to tables, without the need for a mapper binding (ex mapper(Class, table_definition))
class EnvData(DatabaseHelper().BASE):
    from sqlalchemy import Column, Integer, String
    """Defines Device object relational model, is used for both table creation and object interaction"""
    __tablename__ = 'EnvData'
    row_id = Column('row_id', Integer, primary_key=True)
    timestamp = Column('timestamp, String')
    client_ip = Column('client_ip', String, nullable=False)
    temp = Column('temp', String, nullable=False)
    p = Column('p', String, nullable=False)
    altitude = Column('altitude', String, nullable=False)


class TableOutput(object):
    @staticmethod
    def create_table(header_list_in, data_list_in):
        from prettytable import PrettyTable
        t = PrettyTable(header_list_in)
        for i in data_list_in:
            t.add_row(i)
        return str(t)


class SocketCatcher(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        while True:
            self.data = self.request.recv(1024).strip()

            if not self.data: break

            client_ip = self.client_address[0]
            data_string = self.data.decode("utf-8")
            data_obj = json.loads(data_string)

            logging.debug("{} wrote:".format(client_ip))
            logging.debug(self.data)
            logging.debug(data_obj)

            DatabaseHelper().add_data(client_ip=client_ip, data_obj=data_obj)



class main(object):
    @staticmethod
    def run():
        parser = argparse.ArgumentParser()
        parser.add_argument("-s", "--setup", action="store_true", help="Setup Environment")
        parser.add_argument("-g", "--getrows", action="store_true", help="Get All Rows")
        args = parser.parse_args()

        if args.setup:
            DatabaseHelper().create_tables()
            sys.exit(0)

        if args.getrows:
            d=DatabaseHelper()
            logging.debug(d.get_all_rows())
            sys.exit(0)

        HOST, PORT = "", 1337

        # Create the server
        logging.debug("Starting socket server")
        server = socketserver.TCPServer((HOST, PORT), SocketCatcher)

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()


if __name__ == "__main__":
    main.run()