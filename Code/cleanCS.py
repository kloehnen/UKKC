from happyfuntokenizing import *

def main():
	f = open(path,"r")
	fOut = open('UKKC', "w")
	for line in f:
		newInfo = "twitter.com\t"
		info = line.split("\t")
		if len(info) > 4:
			date = info[1].split(" ")[0].replace("-","/")
			newInfo += date + "\t"
			coor1, coor2 = info[3].split("]")[0][1:].split(", ")
			newInfo += coor1 + "\t"
			newInfo += coor2 + "\t"
			cleanedTweet = " ".join(tok.replace(tok.tokenize(info[0])))
			newInfo += cleanedTweet
			fOut.write(newInfo)
			fOut.write("\n")


if __name__ == '__main__':
	path = "/Users/pokea/Documents/Work/UofA/Current/Dissertation/Productivity/CS_Corpus/PAST/IMM_Data/CodeSwitch_IMM17.txt"
	main()
