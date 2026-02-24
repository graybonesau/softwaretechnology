def reverseString(inputString):
	reversedString = str(inputString)[::-1]
	print(reversedString)

def separateString(inputString):
	separatedString = [*str(inputString).strip().replace(" ", "")]
	print(separatedString)

def checkEvenness(inputInteger):
	if inputInteger & 1 == 0:
		print(inputInteger, "is even.")
	else:
		print(inputInteger, "is odd.")

def runBirthdayParadox(inputInteger):
	inputInteger = int(inputInteger)
	noShareProbability = 1.0
	for i in range(inputInteger):
		noShareProbability *= (365 - i) / 365
	shareProbability = 1.0 - noShareProbability
	print("There is a {:.2f}% chance that at least two people share a birthday in a group of {} people.".format(shareProbability * 100, inputInteger))