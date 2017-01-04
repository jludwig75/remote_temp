import tornado.ioloop
import tornado.web
import os
import csv
import time
import datetime
from temp_server.remotetempcommon import *

class NoncachingStaticFileHandler(tornado.web.StaticFileHandler):
    def set_extra_headers(self, path):
        self.set_header("Cache-control", "no-store, no-cache, must-revalidate, max-age=0")

def get_last_report():
    with open('data.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            last_row = row
        return last_row
    return None

def copy_log_last_n_days(source_log_file_name, destination_file_name, number_of_days):
    now = datetime.datetime.now()
    print 'Keeping data from last %d days' % number_of_days
    threshold_time = now - datetime.timedelta(days=number_of_days)
    with open(source_log_file_name, 'rt') as file:
        with open(destination_file_name, 'wt') as output:
            reader = csv.reader(file)
            for row in reader:
                time_stamp = datetime.datetime.strptime(row[0], TIME_FORMAT_STRING)
                if time_stamp >= threshold_time:
                    output.write(','.join(row) + '\n')
    
def get_minutes_since_report(report):
    t = time.strptime(report[0], TIME_FORMAT_STRING)
    t = int(time.time() - time.mktime(t))
    return (t + 59) / 60
    
class MainHandler(tornado.web.RequestHandler):
    loader = tornado.template.Loader("templates")
    def get(self):
        days = self.get_argument('days', True)
        if days:
            days = int(days)
        else:
            days = 1
        if days == 1:
            plot_file_name = 'gplot2_1day.txt'
        elif days > 180:
            print 'Plotting at month interval'
            plot_file_name = 'gplot2_months.txt'
        elif days > 14:
            plot_file_name = 'gplot2_weeks.txt'
        else:
            plot_file_name = 'gplot2.txt'
        print 'Using plot script file %s' % plot_file_name
        copy_log_last_n_days('temps.csv', 'data.csv', days)
        os.system('gnuplot %s' % plot_file_name)
        data = get_last_report()
        if data:
            print 'Last Reported Temperature: %s at %s' % (data[1], data[0])
            report_age_in_minutes = get_minutes_since_report(data)
            self.render('templates/index.html', temperature = data[1], time_stamp = data[0], age_minutes = report_age_in_minutes)
        else:
            self.render('templates/index.html', temperature = 'none reported', time_stamp = '', age_minutes='')

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
         (r"/images/(.*)", NoncachingStaticFileHandler, {"path": "images"}),
    ])

if __name__ == "__main__":
    os.environ['TZ'] = 'US/Mountain'
    try:
        time.tzset()
    except:
        pass
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()
