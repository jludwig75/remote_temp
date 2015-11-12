from temp_server.TemperatureServer import Server


s = Server(7000, 'temps.txt', log=True)
print 'Starting server...'
s.startServer()
print 'Press enter to stop server'
raw_input()
print 'Stopping server'
s.stopServer()
