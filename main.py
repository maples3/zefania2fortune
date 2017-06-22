#!/usr/bin/python3

import argparse
import xml.etree.ElementTree as ET

# Handle the CLI arguments

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--infile", help="The input file to read.  Must be in Zefania XML format.")
parser.parse_args()

## TODO get file names from args
inFileName = 'src.xml'
outFileName = 'out.txt'

tree = ET.parse(inFileName)
root = tree.getroot()

for book in root:
	# Iterating over the root's tags, most of which are books
	if book.tag == "BIBLEBOOK":
		# Now we know that it's actually a book
		bookName = book.get('bname')
		# TODO have a dictionary of the Zefania name to the real name
		for chapter in book:
			if chapter.tag == "CHAPTER":
				chapterNum = chapter.get('cnumber')
				for verse in chapter:
					if verse.tag = "VERS":
						verseNum = verse.get('vnumber')
						verseContent = verse.text
						# TODO write out the verse to the output file,
						# wrapped to 80 lines
		print("Completed " + bookName)
