import sys
import string

with open(sys.argv[1], 'r') as file:
    for line in file:
        parts = line.split('-')
        new_line = (parts[1] + '/' + parts[0] + '/' + parts[2]).strip()
        print new_line