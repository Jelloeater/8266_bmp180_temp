#!python
import argparse
import logging
import json
import sys

import bottle
import dateparser
import pygal

import server.database as database

__author__ = 'Jesse'

logging.basicConfig(format="[%(asctime)s] [%(levelname)8s] --- %(message)s (%(filename)s:%(lineno)s)",
                    level=logging.DEBUG)


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
            database.DatabaseHelper().add_data(client_ip=header_ip, data_obj=data_post)

        @bottle.get('/')
        def index_root():
            return index_graph()

        @bottle.get('/last/<x>')
        def index_last_x(x):
            query_results = database.DatabaseHelper().get_last_x_rows(int(x))
            data_rows = []
            for i in query_results:
                d = {'client_ip': i.client_ip, 'timestamp': i.timestamp, 'altitude': i.altitude, 'p': i.p,
                     'temp': i.temp}
                data_rows.append(d)
            return json.dumps(data_rows, sort_keys=True, indent=4)

        @bottle.get('/graph/<last>')
        def index_graph_last(last):
            data = database.DatabaseHelper().get_last_x_rows(int(last))

            date_chart = pygal.DateTimeLine(x_label_rotation=-45, width=1200, height=600, explicit_size=True,
                                            dynamic_print_values=True, value_font_size=12, human_readable=True)
            date_chart.value_formatter = lambda x: "%.2f" % x

            temprature = []
            pressure = []

            for i in data:
                d = dateparser.parse(i.timestamp)
                # Do not remove, this is due to storing the time stamp as a STRING in the DDL vs as a TIMESTAMP
                temprature.append((d, float(i.temp)))
                pressure.append((d, float(i.altitude)))

            date_chart.add("temprature", temprature)
            date_chart.add("pressure", pressure, secondary=True)

            date_chart.render()

            html = """
                <html>
                      <body>
                         {}
                     </body>
                </html>
                """
            html = html.format(date_chart.render())

            return html

        @bottle.get('/last')
        def index_last():
            return index_last_x(1)

        @bottle.get('/graph')
        def index_graph():
            return index_graph_last(7)

        @bottle.get('/table')
        def table():
            d = database.DatabaseHelper()
            dataobj = d.get_all_rows()
            data_rows = []
            for i in dataobj:
                data_rows.append([i.timestamp, i.temp])
            return TableOutput.create_table(['timestamp', 'temp'], data_rows)

class main(object):
    @staticmethod
    def run():
        parser = argparse.ArgumentParser()
        parser.add_argument("-s", "--setup", action="store_true", help="Setup Environment")
        parser.add_argument("-g", "--getrows", action="store_true", help="Get All Rows")
        args = parser.parse_args()

        if args.setup:
            database.DatabaseHelper().create_tables()
            sys.exit(0)

        if args.getrows:
            d = database.DatabaseHelper()
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
