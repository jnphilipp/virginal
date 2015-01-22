#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

if len(sys.argv) != 3:
	print('usage: TEIToHTML.py <PATH TO TEI> <OUTPUT DIRECTORY>')
	sys.exit(1)

tei = open(sys.argv[1], 'r')
text = tei.read()
tei.close()

for match in re.finditer(r'<div type="textpart" subtype="chapter" n="(\d+)">.+?</div>', text, re.DOTALL):
	div = match.group()
	chapter = ''
	number = match.group(1)

	m = re.search(r'<h1>.+</h1>', div, re.DOTALL)
	title = ''
	if m:
		title = re.sub(r'\s*\n\s*', ' ', re.sub(r'<[^>]+>', '', m.group()))

	for ab in re.finditer(r'<ab n="\d+">.+?</ab>', div, re.DOTALL):
		chapter += '<p>%s</p>\n' % ''.join('%s<br/>' % line for line in re.compile(r'\s*\n\s*').split(re.sub(r'<[^>]+>', '', ab.group())) if line )
	
	chapter = "<?xml version='1.0' encoding='utf-8'?>\n<html xmlns=\"http://www.w3.org/1999/xhtml\">\n\t<head>\n\t\t<title>Kapitel %s</title>\n\t</head>\n\t<body><h1>%s</h1>\n%s\t</body>\n</html>" % (number, title if title else 'Kapitel %s' % number, chapter)

	f = open(os.path.join(sys.argv[2], 'chapter%s.html' % number), 'w')
	f.write(chapter)
	f.close()