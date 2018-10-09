# Variable Setup
input_file = "sample-input.txt"


# Main Function
def main():
	file = open(input_file, "r")
	for line in file:
		a = line.split()
		print(a)

if __name__ == '__main__':
	main()