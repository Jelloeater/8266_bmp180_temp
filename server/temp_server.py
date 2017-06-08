#!python
import argparse
import logging
import json
import datetime
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import bottle
import sys
import jsonpickle as jsonpickle

__author__ = 'Jesse'

logging.basicConfig(format="[%(asctime)s] [%(levelname)8s] --- %(message)s (%(filename)s:%(lineno)s)",
                    level=logging.DEBUG)

BASE = declarative_base()  # Needs to be module level w/ database


class DatabaseHelper():
    # from sqlalchemy.dialects.sqlite import \
    # BLOB, BOOLEAN, CHAR, DATE, DATETIME, DECIMAL, FLOAT, \
    # INTEGER, NUMERIC, SMALLINT, TEXT, TIME, TIMESTAMP, \
    # VARCHAR

    def create_tables(self):
        logging.debug('Creating table if not already present')
        engine = self.get_engine()
        print('Are you sure to want to DROP ALL TABLES, this cannot be undone!')
        if input('({0})>'.format('Type YES to continue')) == 'YES':
            BASE.metadata.drop_all(engine)
            BASE.metadata.create_all(engine)
            print('DATABASE RE-INITIALIZED')
        else:
            print('Skipping database re-initialization')

    @staticmethod
    def get_engine():
        return sqlalchemy.create_engine('sqlite:///EnvData.db')

    def get_session(self):
        engine = DatabaseHelper.get_engine()
        BASE.metadata.bind = engine
        DBSession = sqlalchemy.orm.sessionmaker(bind=engine)
        return DBSession()

    def get_all_rows(self):
        session = self.get_session()
        return session.query(EnvData).all()

    def get_last_row(self):
        session = self.get_session()
        return session.query(EnvData).order_by(EnvData.row_id.desc()).first()

    def add_data(self, data_obj, client_ip):

        # Create DB obj class instance
        db_entry = EnvData()
        db_entry.client_ip = client_ip
        db_entry.timestamp = datetime.datetime.now().isoformat()
        db_entry.altitude = data_obj['altitude']
        db_entry.p = data_obj['p']
        db_entry.temp = data_obj['temp']

        # Write DB obj to disk
        s = self.get_session()
        s.add(db_entry)
        s.commit()


# Classes are directly mapped to tables, without the need for a mapper binding (ex mapper(Class, table_definition))
class EnvData(BASE):
    from sqlalchemy import Column, Integer, String
    """Defines Device object relational model, is used for both table creation and object interaction"""
    __tablename__ = 'EnvData'
    row_id = Column('row_id', Integer, primary_key=True)
    timestamp = Column('timestamp', String)
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


class WebServer(object):
    @staticmethod
    def start_server():
        @bottle.post('/')
        def index():
            logging.debug(bottle.request.headers.__dict__)
            logging.debug(bottle.request.body.read())
            header_ip = bottle.request.headers.environ['REMOTE_ADDR']
            data_post = json.loads(bottle.request.body.read().decode())
            DatabaseHelper().add_data(client_ip=header_ip, data_obj=data_post)

        @bottle.get('/')
        def index():
            # TODO Add nice HTML Table Output of last 24 temps, maybe even a graph
            d = DatabaseHelper()
            dataobj = d.get_all_rows()
            data_rows = []
            for i in dataobj:
                data_rows.append([i.timestamp, i.temp])
            return TableOutput.create_table(['timestamp', 'temp'], data_rows)

        @bottle.get('/last')
        def index():
            dataobj = DatabaseHelper().get_last_row()

            class DummyObj:
                def toJSON(self):
                    return json.dumps(self, default=lambda o: o.__dict__,
                                      sort_keys=True, indent=4)

            d = DummyObj()
            d.client_ip = dataobj.client_ip
            d.timestamp = dataobj.timestamp
            d.altitude = dataobj.altitude
            d.p = dataobj.p
            d.temp = dataobj.temp
            return d.toJSON()


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
            d = DatabaseHelper()
            dataobj = d.get_all_rows()
            data_rows = []
            for i in dataobj:
                data_rows.append([i.row_id, i.timestamp, i.client_ip, i.temp, i.p, i.altitude])
            table = TableOutput.create_table(['row_id', 'timestamp', 'client_ip', 'temp', 'p', 'altitude'], data_rows)

            logging.debug(table)
            sys.exit(0)
        # Create the server
        logging.debug("Starting socket server")
        WebServer.start_server()


if __name__ == "__main__":
    main.run()
    bottle.run(host='', port=8080, debug=True)
