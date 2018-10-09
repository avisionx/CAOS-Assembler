# Imports
import re

# Variable Setup
input_file_name = "sample-input.txt"
processed_file_name = "processedFile.txt"

# Setting up file for processing
def setup_file():
	
	inputFile = open(input_file_name, "r")
	processedList = [] 
	
	for line in inputFile:	
		convertTabsToSpace = line.replace('	', ' ')
		toSingleSpace = re.sub("\s\s+" , " ", convertTabsToSpace)
		convertSpaceToCommas = toSingleSpace.replace(' ', ',')
		lineWithEndLine = convertSpaceToCommas.split(',')
		if(lineWithEndLine[-1] == ''):
			lineWithEndLine = lineWithEndLine[0:-1]
		else:
			lineWithEndLine[-1] = lineWithEndLine[-1].split()[0]
		finalLine = lineWithEndLine
		processedList.append(finalLine)

	inputFile.close()

	return processedList

# Main Function
def main():
	
	procList = setup_file()
	
	for line in procList:
		print(line)

if __name__ == '__main__':
	main()