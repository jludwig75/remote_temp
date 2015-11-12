import unittest

from temp_server.TemperatureServer import Server

class TestTemperatureServer(unittest.TestCase):
    
    def test_processInputBuffer(self):
        server = Server(1, 'temp.txt', True)
        server.inputBuffer = 'sgfdhg{fdghghgd}{fgfdgf}fgfsd'
        server.processInputBuffer()
        self.assertEqual(server.inputBuffer, '{fgfdgf}fgfsd')
        server.processInputBuffer()
        self.assertEqual(server.inputBuffer, 'fgfsd')        