#!/usr/bin/python3

import argparse
import csv
from textwrap import TextWrapper
import xml.etree.ElementTree as ET
import subprocess

# Handle the CLI arguments

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--infile", help="The input file to read.  Must be in Zefania XML format.")
parser.parse_args()

## TODO ask for a CSV names list
correctNamesFile = 'names.csv'

## TODO get file names from args
inFileName = 'src.xml'
outDir = 'out/'

# If the dir name doesn't have a trailing slash, add it
if outDir[-1] != '/':
	outDir = outdir + '/'

# Create the text wrapper
# TODO- add option to change line width
wrapper = TextWrapper(width=79)

tree = ET.parse(inFileName)
root = tree.getroot()

# Create a dict of the names from the CSV
correctNamesDict = dict()
correctNamesReader = csv.DictReader(open(correctNamesFile))
for row in correctNamesReader:
	correctNamesDict[row['XMLName']] = row['RealName']

for book in root:
	# Iterating over the root's tags, most of which are books
	if book.tag == "BIBLEBOOK":
		# Now we know that it's actually a book
		bookName = book.get('bname')
		if bookName in correctNamesDict:
			bookName = correctNamesDict[bookName]

		# Open the output file, which is the lowercase and underscored version
		# of the book name
		outFileName = outDir + bookName.lower().replace(' ', '_')
		outFile = open(outFileName, 'w')

		for chapter in book:
			if chapter.tag == "CHAPTER":
				chapterNum = chapter.get('cnumber')
				for verse in chapter:
					if verse.tag == "VERS":
						verseNum = verse.get('vnumber')
						verseContent = verse.text
						# TODO write out the verse to the output file,
						# wrapped to 80 lines
						#wrappedText = wrapper.fill(verseContent)
						#print(wrappedText)
						outFile.write(wrapper.fill(verseContent) + "\n")
						#citeLine = "        --" + bookName + " " + chapterNum + ":" + verseNum
						#print(citeLine)
						outFile.write("        --" + bookName + " " + chapterNum + ":" + verseNum + "\n")
						outFile.write("%\n")
		outFile.flush()
		outFile.close()
		# call strfile on the output to create the .db files for Fortune
		subprocess.run(['strfile', outFileName, '-s'])
		print("Completed", bookName)
