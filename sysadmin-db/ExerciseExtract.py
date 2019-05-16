#!/usr/bin/env python3
import sys

def usage():
    print(sys.argv[0])
    print('    Read from stdin and extract to stdout')
    print(sys.argv[0] + ' -h')
    print('    Show usage')
    print(sys.argv[0] + ' <inputfile>')
    print('    Read from <inputfile> and extract to stdout')
    print(sys.argv[0] + ' <inputfile> <outputfile>')
    print('    Read from <inputfile> and extract to <outputfile>')


def extract(in_file, out_file):
    format_string = '"%s","%s","%s","%s"\n'
    out_file.write(format_string % ('UNIQUEID', 'AGE', 'SEX', 'RACE'))
    for line in in_file:
        # Only process P records.
        if line[0] != 'P':
            continue
        data_num_p = line[5:7]
        year_p = line[1:5]
        serial_p = line[7:15]
        pernum = line[15:19]
        unique_id = data_num_p + year_p + serial_p + pernum
        age = line[53:56]
        sex = line[56:57]
        race = line[57:60]
        out_file.write(format_string % (unique_id, age, sex, race))

if __name__ == '__main__':
    if len(sys.argv) > 3:
        usage()
    elif len(sys.argv) > 1 and sys.argv[1] == '-h':
        usage()
    elif len(sys.argv) == 3:
        in_file = open(sys.argv[1], 'r')
        out_file = open(sys.argv[2], 'w') 
        extract(in_file, out_file)
    elif len(sys.argv) == 2:
        in_file = open(sys.argv[1], 'r')
        extract(in_file, sys.stdout)
    elif len(sys.argv) == 1:
        extract(sys.stdin, sys.stdout)

