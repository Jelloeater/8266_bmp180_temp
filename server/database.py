import datetime
import logging
import platform
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

BASE = declarative_base()  # Needs to be module level w/ database

__author__ = 'Jesse'


# Classes are directly mapped to tables, without the need for a mapper binding (ex mapper(Class, table_definition))

class DatabaseHelper:
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

    @classmethod
    def get_engine(cls):

        if platform.system() == 'Windows':
            DB_PATH = 'EnvData.db'
        else:
            DB_PATH = '/data/EnvData.db'

        return create_engine('sqlite:///' + DB_PATH)

    def get_session(self):
        engine = self.get_engine()
        BASE.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        return DBSession()

    def get_all_rows(self):
        session = self.get_session()
        return session.query(EnvData).all()

    def get_last_x_rows(self, x):
        session = self.get_session()
        return session.query(EnvData).order_by(EnvData.row_id.desc()).limit(x).all()

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
