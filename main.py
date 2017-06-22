#!/usr/bin/python3

import argparse
import csv
from textwrap import TextWrapper
import xml.etree.ElementTree as ET
import subprocess
import os.path

# Handle the CLI arguments

parser = argparse.ArgumentParser(description="Convert Zefania XML to Fortune-readable files")
parser.add_argument("in_file",
	help="The input file to read.  Must be in Zefania XML format.",
	nargs=1)
parser.add_argument("-o", "--outdir",
	help="The directory to store the output files in.",
	dest="out_dir",
	default="bible/")
parser.add_argument("-n", "--names",
	help="The CSV file to read the name corrections from.  See the provided example.",
	dest="names_file")
parser.add_argument("-s", "--strfile",
	help="Automatically run strfile(1) to create the .db files for Fortune.",
	dest="strfile",
	default=False,
	action='store_true')
parser.add_argument("-w", "--width",
	help="The width to wrap the verses to.",
	type=int,
	dest='line_width',
	default=79)
results = parser.parse_args()

# Use the args to determine the files to use
correctNamesFile = results.names_file
inFileName = results.in_file[0]
outDir = results.out_dir
wrapper = TextWrapper(width=results.line_width)

print(correctNamesFile)
print(inFileName)
print(outDir)

# If the dir name doesn't have a trailing slash, add it
if outDir[-1] != '/':
	outDir = outDir + '/'
# Also make sure it exists
if not os.path.exists(outDir):
	subprocess.run(["mkdir", outDir])

tree = ET.parse(inFileName)
root = tree.getroot()

# Create a dict of the names from the CSV
correctNamesDict = dict()
if correctNamesFile != None:
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
		if results.strfile:
			# call strfile on the output to create the .db files for Fortune
			subprocess.run(['strfile', outFileName, '-s'])
		print("Completed", bookName)
