# Imports
import re

# Variable/Table Name Setup
input_file_name = "input.txt"
label_table_name = 'Label_Table.txt'
variable_table_name = 'Variable_Table.txt'
literal_table_name = 'Literal_Table.txt'
opcode_table_name = 'Opcode_Table.txt'
output_table_name = 'MachineCodeConverted.txt'

labelTable = []
variableTable = []
literalTable = []
opcodeTable = []

assemblyCode = []

# OPCODE CATEGORIES
category1 = {"CLA":"0000", "STP":"1100"}
category2 = {"LAC":"0001", "SAC":"0010", "ADD":"0011", "SUB":"0100", "MUL":"1010", "DIV":"1011", "INP":"1000", "DSP":"1001"}
category3 = {"BRN":"0110", "BRZ":"0101", "BRP":"0111"}
category4 = {"DS": "1101", "DW": "1101", "DC": "1101"}

# Output Saver
def saveOutputTable(table, tableName):
	file = open(tableName, 'w')
	for line in table:
		file.write(line + "\n")

# Save tables
def saveTable(table, tableName):
	file = open(tableName, 'w')
	if(tableName == "Label_Table.txt"):
		file.write("LABEL	OFFSET\n")
	elif(tableName == "Variable_Table.txt"):
		file.write("VAR	OFFSET	VALUE\n")
	elif(tableName == "Literal_Table.txt"):
		file.write("LITERAL	OFFSET	VALUE\n")
	elif(tableName == "Opcode_Table.txt"):
		file.write("OPCODE	BITCODE	OPERAND	OFFSET\n")
	for line in table:
		lineMaker = ""
		for x in range(len(line)):
			lineMaker += str(line[x]) + "	"
		file.write(lineMaker + "\n")

# Returns bin code for a branching address
def getLineBinCode(operand):
	for i in range(len(labelTable)):
		if(labelTable[i][0] == operand):
			labelDefAt = labelTable[i][1]
			binary = bin(assemblyCode[labelDefAt][3])[2:]
			return "0"*(12 - len(binary))  + binary

	return ""

# Returns bin code for operand in literal and variable table
def getBinOperandCode(operand):
	
	for i in range(len(literalTable)):
		if(literalTable[i][0] == operand):
			binary = bin(literalTable[i][3])[2:]
			return "0"*(12 - len(binary))  + binary

	for i in range(len(variableTable)):
		if(variableTable[i][0] == operand):
			binary = bin(variableTable[i][3])[2:]
			return "0"*(12 - len(binary))  + binary

	return ""

# Gives 4bit binary opcode
def getBinOpCode(opcode):
	if opcode in category1:
		return category1[opcode]
	elif opcode in category2:
		return category2[opcode]
	elif opcode in category3:
		return category3[opcode]
	else:
		return category4[opcode]

# Adds literal in table
def addLiteralInTable(literal, locationCounter):
	for x in range(len(literalTable)):
		if(literalTable[x][0] == literal):
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
		if(toSingleSpace != "\n" and toSingleSpace != " "):
			if(toSingleSpace.find("//") != -1):
				toSingleSpace = toSingleSpace[:toSingleSpace.find("//")] 
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
					print("ERROR! LABEL ALREADY DEFINED AT " + str(locationCounter))
					exit()
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
					print("ERROR! OPCODE DOESN'T EXIST AT " + str(locationCounter))
					exit()
			else:
				variablePos = searchVariableTable(line[0])
				if(variablePos == -1):
					print("ERROR! VARIABLE MULTIPLE DEFINATION AT " + str(locationCounter))
					exit()
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
				print("ERROR! OPCODE DOESN'T EXIST AT " + str(locationCounter))
				exit()

	for x in range(len(labelTable)):
		if(labelTable[x][1] == ""):
			print("ERROR! LABEL: " + str(labelTable[x][0]) + " NOT DEFINED")
			exit()

	for x in range(len(variableTable)):
		if(variableTable[x][1] == ""):
			print("ERROR! VARIABLE: " + str(variableTable[x][0]) + " NOT DEFINED")
			exit()
	
	saveTable(labelTable, label_table_name)
	saveTable(variableTable, variable_table_name)
	saveTable(literalTable, literal_table_name)
	saveTable(opcodeTable, opcode_table_name)

	global assemblyCode
	assemblyCode = procList
	machineCode = []
	
	memoryAdrress = 0

	numberOfLiterals = len(literalTable)

	if(locationCounter <= 255 - numberOfLiterals):

		for i in range(len(literalTable)):
			literalTable[i].append(memoryAdrress)
			memoryAdrress += 1		

		for i in range(len(variableTable)):
			variableTable[i].append(memoryAdrress)
			memoryAdrress += 1

		for i in range(len(assemblyCode)):
			assemblyCode[i].append(memoryAdrress)
			memoryAdrress += 1

		for i in range(len(assemblyCode)):
			line = assemblyCode[i]
			machineLine = ""
			if(line[0] != ""):
				if(not variableAssignment(line[1])):
					literalCode = getBinOperandCode(line[2])
					machineLine =  getBinOpCode(line[1]) + " " + literalCode
			else:
				opcodeCategory = opcodeCategorizer(line[1])
				if(opcodeCategory == 1):
					machineLine = getBinOpCode(line[1])

				elif(opcodeCategory == 2):
					machineLine = getBinOpCode(line[1]) + " " + getBinOperandCode(line[2])

				elif(opcodeCategory == 3):
					machineLine = getBinOpCode(line[1]) + " " + getLineBinCode(line[2])

			if(machineLine != ""):
				machineCode.append(machineLine)

	else:
		print("ERROR! NOT ENOUGH MEMORY TO STORE SO MANY INSTRUCTION AND ADDRESSES")
		exit()	

	for line in machineCode:
		print(line)

	saveOutputTable(machineCode, output_table_name)

if __name__ == '__main__':
	main()

