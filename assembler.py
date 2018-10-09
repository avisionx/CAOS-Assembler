# Imports
import re

# Variable/Table Name Setup
input_file_name = "sample-input.txt"
label_table_name = 'labelTable.txt'
variable_table_name = 'variableTable.txt'
literal_table_name = 'literalTable.txt'
opcode_table_name = 'opcodeTable.txt'

labelTable = []
variableTable = []
literalTable = []
opcodeTable = []

# Search for label in table if already exist return position 0 base
def searchLabelTable(label):
	for x in range(len(labelTable)):
		if(label == labelTable[x][0]):
			if(labelTable[x][1] == ""):
				return x # Present without defination
			else:
				return -1 # Present with defination
	else:
		return -2 # Not present already
		
# Search for variable in table if already exist return position 0 base
def searchVariableTable(variable):
	for x in range(len(variableTable)):
		if(variable == variableTable[x][0]):
			if(variableTable[x][1] == ""):
				return x # Present without defination
			else:
				return -1 # Present with defination
	return -2 # Not present already

# Checks if variable assignment opcode
def variableAssignment(opcode):
	
	if(opcode == 'DW' or opcode == 'DS' or opcode == 'DC'):
		return True
	
	return False

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
	locationCounter = -1

	for line in procList:
		
		locationCounter+=1 	
		
		if(line[0] != ''):
			if(not variableAssignment(line[1])):
				labelPos = searchLabelTable(line[0])
				if(labelPos == -1):
					# TODO: REPORT ERROR LABEL ALREADY DEFINED
					pass
				elif(labelPos == -2):
					labelTable.append([line[0], locationCounter])
				else:
					labelTable[labelPos][1] = locationCounter

			else:
				variablePos = searchVariableTable(line[0])
				if(variablePos == -1):
					# TODO: REPORT ERROR VARIABLE MULTIPLE VALUE ASSIGNMENT
					pass
				elif(variablePos == -2):
					variableTable.append([line[0], locationCounter, line[2]])
				else:
					variableTable[variablePos][1] = locationCounter
					variableTable[variablePos][2] = line[2]

			# MANAGE OPCODE AND OPERAND EXCEPT ASSIGNMENT ONCE
		
		else:
			# MANAGE OPCODE AND OPERNAD
			

if __name__ == '__main__':
	main()

