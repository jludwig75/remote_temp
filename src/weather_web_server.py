import tornado.ioloop
import tornado.web
import os
import csv
import time
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

def get_minutes_since_report(report):
    t = time.strptime(report[0], TIME_FORMAT_STRING)
    t = int(time.time() - time.mktime(t))
    return (t + 59) / 60
    
class MainHandler(tornado.web.RequestHandler):
    loader = tornado.template.Loader("templates")
    def get(self):
        os.system('cp temps.csv data.csv')
        os.system('gnuplot gplot2.txt')
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
    time.tzset()
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()
