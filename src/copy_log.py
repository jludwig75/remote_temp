import sys
import csv
import datetime
from temp_server.remotetempcommon import *

def copy_log_last_n_days(source_log_file_name, destination_file_name, number_of_days):
    now = datetime.datetime.now()
    print 'It is now %s' % now
    threshold_time = now - datetime.timedelta(days=1)
    print '24 hours ago it was %s' % threshold_time
    with open(source_log_file_name, 'rt') as file:
        reader = csv.reader(file)
        for row in reader:
            time_stamp = datetime.datetime.strptime(row[0], TIME_FORMAT_STRING)
            if time_stamp >= threshold_time:
                print ','.join(row)

copy_log_last_n_days(sys.argv[1], sys.argv[2], int(sys.argv[3]))