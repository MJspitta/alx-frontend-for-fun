#!/usr/bin/python3
""" script that takes an argument 2 strings """

import sys
import os
import re
import hashlib

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: ./markdown2html.py README.md README.html',
              file=sys.stderr)
        exit(1)

    md_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(md_file):
        print('Missing {}'.format(md_file), file=sys.stderr)
        exit(1)

    with open(md_file) as mdfile:
        with open(output_file, 'w') as html:
            u_start, o_start, para = False, False, False
            for line in mdfile:
                line = line.replace('**', '<b>', 1)
                line = line.replace('**', '</b>', 1)
                line = line.replace('__', '<em>', 1)
                line = line.replace('__', '</em>', 1)

                md5 = re.findall(r'\[\[.+?\]\]', line)
                md5_inside = re.findall(r'\[\[(.+?)\]\]', line)
                if md5:
                    line = line.replace(md5[0], hashlib.md5(
                        md5_inside[0].encode()).hexdigest())

                rm_letter_c = re.findall(r'\(\(.+?\)\)', line)
                rm_more_c = re.findall(r'\(\((.+?)\)\)', line)
                if rm_letter_c:
                    rm_more_c = ''.join(
                            c for c in rm_more_c[0] if c not in 'Cc')
                    line = line.replace(rm_letter_c[0], rm_more_c)

                length = len(line)
                heading = line.lstrip('#')
                heading_no = length - len(heading)
                unorder = line.lstrip('-')
                unorder_no = length - len(unorder)
                order = line.lstrip('*')
                order_no = length - len(order)
                if 1 <= heading_no <= 6:
                    line = '<h{}>'.format(
                        heading_no) + heading.strip() + '</h{}>\n'.format(
                        heading_no)

                if unorder_no:
                    if not u_start:
                        html.write('<ul>\n')
                        u_start = True
                    line = '<li>' + unorder.strip() + '</li>\n'
                if u_start and not unorder_no:
                    html.write('</ul>\n')
                    u_start = False

                if order_no:
                    if not o_start:
                        html.write('<ol>\n')
                        o_start = True
                    line = '<li>' + order.strip() + '</li>\n'
                if o_start and not order_no:
                    html.write('</ol>\n')
                    o_start = False

                if not (heading_no or u_start or o_start):
                    if not para and length > 1:
                        html.write('<p>\n')
                        para = True
                    elif length > 1:
                        html.write('<br/>\n')
                    elif para:
                        html.write('</p>\n')
                        para = False

                if length > 1:
                    html.write(line)

            if u_start:
                html.write('</ul>\n')
            if o_start:
                html.write('</ol>\n')
            if para:
                html.write('</p>\n')
    exit (0)
