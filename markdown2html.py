#!/usr/bin/python3
""" script that takes an argument 2 strings """
import sys
import os
import markdown


if len(sys.argv) < 3:
    sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
    sys.exit(1)

md_file = sys.argv[1]
output_file = sys.argv[2]

if not os.path.isfile(md_file):
    sys.stderr.write(f"Missing {md_file}\n")
    sys.exit(1)

with open(md_file, 'r') as mdfile:
    md_text = mdfile.read()
    html = markdown.markdown(md_text)

with open(output_file, 'w') as htmlfile:
    htmlfile.write(html)

sys.exit(0)
