# This module is a JSMinimizer
# It will take any file and strip away all
# comments, and whitespace characters.
# This has only been tested for JS scripts,
# all other file types have not been verified
# to work as expected.
# Author: MikeWest

from string import whitespace
from sys import *;

# Given a string remove all whitespace from it and
# return the whitespace-stripped version
# Current algorithm builds a list of all the non-whitespace
# runs then returns the join of that list. There is probably
# a more efficient algorithm, but this way will work for now
def removewhitespace(sLine):
	iLineBeg = 0
	stripped = []
	for iCurr in range(0,len(sLine)):
		if whitespace.find(sLine[iCurr]) >= 0:
			if iCurr > iLineBeg:
				stripped.append(sLine[iLineBeg:(iCurr)])
			iLineBeg = iCurr+1
			
	# If no whitespace appears on the line then return input line
	if iLineBeg == 0:
		return sLine
	else:
		return "".join(stripped)

# Make sure the user gave us an input and output file
if len(argv) < 3:
	print "Usage: minimizer infile outfile\n"
	exit(1)

# Remember the first element of argv is the scripts name
inFile = argv[1]
outFile = argv[2]

inHandle = open(inFile, "r")

# Lets strip away all JS comments, single, and multi-line
# Only type of comment left to purge is the multi-line comment block
# that appears only on one line
SINGLE_COMMENT = "//"
MULTILINE_COMMENT_START = "/*"
MULTILINE_COMMENT_END = "*/"

minimizedLns = []
bMultiCommentBlock = False	# True, if were in a multi-line comment block, False otherwise
lines = inHandle.readlines()
for line in lines:
	processed = line
	
	if bMultiCommentBlock:
		iMultiEnd = processed.find(MULTILINE_COMMENT_END)
		if iMultiEnd >= 0:
			processed = processed[(iMultiEnd+2):-1]
			bMultiCommentBlock = False
		else:
			continue
	
	iSingle = processed.find(SINGLE_COMMENT)
	if iSingle > 0:
		processed = processed[0:(iSingle)]
	elif iSingle == 0:
		continue

	iMultiStart = processed.find(MULTILINE_COMMENT_START)
	if iMultiStart > 0:
		processed = processed[0:(iMultiStart)]
		bMultiCommentBlock = True
	elif iMultiStart == 0:
		bMultiCommentBlock = True
		continue
	
	# Now strip all whitespace
	processed = removewhitespace(processed)
	
	# If no empty then dont bother adding to our list
	if processed != "":
		minimizedLns.append(processed)

inHandle.close()

newcontents = ''.join(minimizedLns)

outHandle = open(outFile, "w");
outHandle.write(newcontents);
outHandle.close()

