import tornado.ioloop
import tornado.web
import os

class NoncachingStaticFileHandler(tornado.web.StaticFileHandler):
    def set_extra_headers(self, path):
        print 'Adding Cache-control=no-cache'
        self.set_header("Cache-control", "no-store, no-cache, must-revalidate, max-age=0")

class MainHandler(tornado.web.RequestHandler):
    loader = tornado.template.Loader("templates")
    def get(self):
        os.system('cp temps.csv data.csv')
        os.system('gnuplot gplot2.txt')
        self.write(self.loader.load("index.html").generate())

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
         (r"/images/(.*)", NoncachingStaticFileHandler, {"path": "images"}),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()
