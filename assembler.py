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

# OPCODE CATEGORIES
category1 = {"CLA":"0000", "STP":"1100"}
category2 = {"LAC":"0001", "SAC":"0010", "ADD":"0011", "SUB":"0100", "MUL":"1010", "DIV":"1011", "INP":"1000", "DSP":"1001"}
category3 = {"BRN":"0110", "BRZ":"0101", "BRP":"0111"}

# Adds literal in table
def addLiteralInTable(literal, locationCounter):
	for x in range(len(literalTable)):
		if(literalTable[x] == literal):
			return
	literalTable.append([literal, locationCounter, literal[2:-1]])

# Adds opcode in table
def addOpcodeInTable(opcode, operand, locationCounter, category):
	mainCategory = category3
	if(category == 1):
		mainCategory = category1
	elif(category == 2):
		mainCategory = category2

	opcodeTable.append([opcode, mainCategory[opcode], operand, locationCounter])

# Checks if operand literal
def isLiteral(literal):
	if(len(literal) < 4):
		return False
	elif(literal[1] == "=" and literal[0] == literal[-1] and (literal[0] == "\'" or literal[0] == "\"")):
		return True
	return False

# Categorizes opcode
def opcodeCategorizer(opcode):
	if(opcode in category1.keys()):
		return 1
	elif(opcode in category2.keys()):
		return 2
	elif(opcode in category3.keys()):
		return 3
	else:
		return -1

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
					print("ERROR! LABEL ALREADY DEFINED AT " + locationCounter)
				elif(labelPos == -2):
					labelTable.append([line[0], locationCounter])
				else:
					labelTable[labelPos][1] = locationCounter
			
				opcodeCategory = opcodeCategorizer(line[1])
				if(opcodeCategory == 1):
					pass
				elif(opcodeCategory == 2):
					
					addOpcodeInTable(line[1], line[2], locationCounter, 2)

					if(isLiteral(line[2])):
						addLiteralInTable(line[2], locationCounter)
					else:
						variablePos = searchVariableTable(line[2])
						if(variablePos == -2):
							variableTable.append([line[2], "", ""])
						else:
							pass

				elif(opcodeCategory == 3):

					addOpcodeInTable(line[1], line[2], locationCounter, 3)

					labelPos = searchLabelTable(line[2])
					if(labelPos == -2):
						labelTable.append([line[2], ""])
					else:
						pass

				else:
					print("ERROR! OPCODE DOESN'T EXIST AT " + locationCounter)
					
			else:
				variablePos = searchVariableTable(line[0])
				if(variablePos == -1):
					print("ERROR! VARIABLE MULTIPLE DEFINATION AT " + locationCounter)
				elif(variablePos == -2):
					variableTable.append([line[0], locationCounter, line[2]])
				else:
					variableTable[variablePos][1] = locationCounter
					variableTable[variablePos][2] = line[2]

		else:
			opcodeCategory = opcodeCategorizer(line[1])
			if(opcodeCategory == 1):
				pass
			elif(opcodeCategory == 2):
				
				addOpcodeInTable(line[1], line[2], locationCounter, 2)

				if(isLiteral(line[2])):
					addLiteralInTable(line[2], locationCounter)
				else:
					variablePos = searchVariableTable(line[2])
					if(variablePos == -2):
						variableTable.append([line[2], "", ""])
					else:
						pass

			elif(opcodeCategory == 3):

				addOpcodeInTable(line[1], line[2], locationCounter, 3)

				labelPos = searchLabelTable(line[2])
				if(labelPos == -2):
					labelTable.append([line[2], ""])
				else:
					pass

			else:
				print("ERROR! OPCODE DOESN'T EXIST AT " + locationCounter)


	print(labelTable)
	print("__________________")
	print(variableTable)
	print("__________________")
	print(literalTable)
	print("__________________")
	print(opcodeTable)
if __name__ == '__main__':
	main()

