import tornado.ioloop
import tornado.web
import os
import csv

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

class MainHandler(tornado.web.RequestHandler):
    loader = tornado.template.Loader("templates")
    def get(self):
        os.system('cp temps.csv data.csv')
        os.system('gnuplot gplot2.txt')
        data = get_last_report()
        if data:
            print 'Last Reported Temperature: %s at %s' % (data[1], data[0])
        self.render('templates/index.html', temperature = data[1], time_stamp = data[0])

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
         (r"/images/(.*)", NoncachingStaticFileHandler, {"path": "images"}),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()
