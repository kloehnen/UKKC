import re

def main():
	fl = list(l for l in open(path,"r"))
	fiter = iter(fl)
	fOut = open('UKKC_Clean', "w")
	i = 0
	N = len(fl)
	current = ''

	while True:
		try:
			i += 1
			current = next(fiter)
			text = re.split(r"\t",current)[4]
			previous = text
			val = input("%d of %d:\t %s" % (i,N,text))
			if val == "l":
				fOut.write(current)
			elif val =="a":
				continue
			else:
				print("Wrong button")
				val = input("%d of %d:\t %s" % (i,N,text))
		except:
			StopIteration()
			break

#twitter.com	2015/10/03	35.3194331	0.2970387	winning bpl trophy has consequences . look whats happening to chelsea . what happened to man u .. sisi kama arsenali wacha tubakie top 4
#@USER @USER , mornig team #thehotbreakfast . , am up to build up my nation . , amkeni maze . , play them anything done by gloria muliro .







if __name__ == '__main__':
	path = "UKKC"
	main()
