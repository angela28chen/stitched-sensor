import os
import math

def calcMocapThreshold(subjID):
	# Read 4 mocap files (two good and two poor) then calculate the threshold for vertical and horizontal sensor.
	
	filenames = ["good1.csv", "good2.csv", "poor1.csv", "poor2.csv"]
	
	thetag1 = []
	thetag2 = []
	thetap1 = []
	thetap2 = []
	
	gammag1 = []
	gammag2 = []
	gammap1 = []
	gammap2 = []
	
	for name in filenames:
		fileobj = open("subject" + str(subjID) + "\\" + name, "r")
		
		lines = fileobj.readlines()
		
		for line in lines:
			line = line.strip("\n")
			perlinedict = {}
			splitvals = line.split(",")
			if splitvals[0] == "frame":
				end = len(splitvals)
				#print(splitvals)
				
				# Iterating one line and putting its values in dict perlinedict
				for i in range(end-1, 0, -1):
					key = splitvals[i]
					if key.isalpha():
						perlinedict[key + "x"] = splitvals[i-4]
						perlinedict[key + "y"] = splitvals[i-3]
						perlinedict[key + "z"] = splitvals[i-2]
				#print(perlinedict)
				
				# Now time to calculate theta and gamma
				TLx = float(perlinedict["leftx"]) - float(perlinedict["topx"])
				TLy = float(perlinedict["lefty"]) - float(perlinedict["topy"])
				TLz = float(perlinedict["leftz"]) - float(perlinedict["topz"])
				TLmag = math.sqrt(TLx**2 + TLy**2 + TLz**2)
				TRx = float(perlinedict["rightx"]) - float(perlinedict["topx"])
				TRy = float(perlinedict["righty"]) - float(perlinedict["topy"])
				TRz = float(perlinedict["rightz"]) - float(perlinedict["topz"])
				TRmag = math.sqrt(TRx**2 + TRy**2 + TRz**2)
				
				dotprod = TLx*TRx + TLy*TRy + TLz*TRz
				theta = math.degrees(math.acos(dotprod/(TLmag*TRmag)))
				
				CTx = float(perlinedict["topx"]) - float(perlinedict["centrex"])
				CTy = float(perlinedict["topy"]) - float(perlinedict["centrey"])
				CTz = float(perlinedict["topz"]) - float(perlinedict["centrez"])
				CTmag = math.sqrt(CTx**2 + CTy**2 + CTz**2)
				CBx = float(perlinedict["bottomx"]) - float(perlinedict["centrex"])
				CBy = float(perlinedict["bottomy"]) - float(perlinedict["centrey"])
				CBz = float(perlinedict["bottomz"]) - float(perlinedict["centrez"])
				CBmag = math.sqrt(CBx**2 + CBy**2 + CBz**2)
				
				dotprod = CTx*CBx + CTy*CBy + CTz*CBz
				gamma = math.degrees(math.acos(dotprod/(CTmag*CBmag)))
				
				
				# Store values and clear dictionary
				if name == "good1.csv":
					thetag1.append(theta)
					gammag1.append(gamma)
				elif name == "good2.csv":
					thetag2.append(theta)
					gammag2.append(gamma)
				elif name == "poor1.csv":
					thetap1.append(theta)
					gammap1.append(gamma)
				elif name == "poor2.csv":
					thetap2.append(theta)
					gammap2.append(gamma)
				
				perlinedict.clear()
		
	print("thetag1, thetag2")
	print(sum(thetag1)/float(len(thetag1)))
	print(sum(thetag2)/float(len(thetag2)))
	print("thetap1, thetap2")
	print(sum(thetap1)/float(len(thetap1)))
	print(sum(thetap2)/float(len(thetap2)))
	print("gammag1, gammag2")
	print(sum(gammag1)/float(len(gammag1)))
	print(sum(gammag2)/float(len(gammag2)))
	print("gammap1, gammap2")
	print(sum(gammap1)/float(len(gammap1)))
	print(sum(gammap2)/float(len(gammap2)))
	
	goodavgtheta = (sum(thetag1) + sum(thetag2)) / (float(len(thetag1) + len(thetag2)))
	goodavggamma = (sum(gammag1) + sum(gammag2)) / (float(len(gammag1) + len(gammag2)))
	
	pooravgtheta = (sum(thetap1) + sum(thetap2)) / (float(len(thetap1) + len(thetap2)))
	pooravggamma = (sum(gammap1) + sum(gammap2)) / (float(len(gammap1) + len(gammap2)))
	
	return [goodavgtheta, goodavggamma, pooravgtheta, pooravggamma]
	
		
def calcSSThreshold(subjID):
	# Read 4 stitched sensor files (two good and two poor) then calculate the threshold for vertical and horizontal sensor.
	
	filenames = ["good_0.csv", "good_1.csv", "poor_0.csv", "poor_1.csv"]
	
	hbgood1 = []
	hbpoor1 = []
	hbgood2 = []
	hbpoor2 = []
	
	vbgood1 = []
	vbpoor1 = []
	vbgood2 = []
	vbpoor2 = []
		
	for name in filenames:
		fileobj = open("subject" + str(subjID) + "\\" + "ESP32sub" + str(subjID) + "_" + name, "r")
		
		lines = fileobj.readlines()
		
		hb = []
		vb = []
		
		for line in lines:
			line = line.strip("\n")
			line = line.strip()
			splitvals = line.split(",")
			splitvals[0] = splitvals[0].strip()
			splitvals[1] = splitvals[1].strip()
			
			if splitvals[0].isnumeric():
				hb.append(float(splitvals[0]))
			else:
				print(splitvals[0])
			if splitvals[1].isnumeric():
				vb.append(float(splitvals[1]))
			else:
				print(splitvals[1])
			
		if name == "good_0.csv":
			hbgood1 = hb
			vbgood1 = vb
		elif name == "good_1.csv":
			hbgood2 = hb
			vbgood2 = vb
		elif name == "poor_0.csv":
			hbpoor1 = hb
			vbpoor1 = vb
		elif name == "poor_1.csv":
			hbpoor2 = hb
			vbpoor2 = vb
			
	print("hbgood1, hbgood2")
	hbgood1_sum = sum(hbgood1)/float(len(hbgood1))
	print(hbgood1_sum)
	hbgood2_sum = sum(hbgood2)/float(len(hbgood2))
	print(hbgood1_sum)
	
	print("hbpoor1, hbpoor2")
	hbpoor1_sum = sum(hbpoor1)/float(len(hbpoor1))
	print(hbpoor1_sum)
	hbpoor2_sum = sum(hbpoor2)/float(len(hbpoor2))
	print(hbpoor2_sum)
	print("vbgood1, vbgood2")
	print(sum(vbgood1)/float(len(vbgood1)))
	print(sum(vbgood2)/float(len(vbgood2)))
	print("vbpoor1, vbpoor2")
	print(sum(vbpoor1)/float(len(vbpoor1)))
	print(sum(vbpoor2)/float(len(vbpoor2)))
	
	print("JUST THE HB RANGE AND RECOMMENDED THRESHOLD BASED ON SECOND")
	print("hbgood2 -> hbpoor2")
	print(hbgood2_sum)
	print(hbpoor2_sum)
	print("we want it a lot more lenient; closer to the lower HBpoor")
	print((hbgood2_sum-hbpoor2_sum)*0.1+hbpoor2_sum)
	
	goodavghb = (sum(hbgood1) + sum(hbgood2)) / (float(len(hbgood1) + len(hbgood2)))
	goodavgvb = (sum(vbgood1) + sum(vbgood2)) / (float(len(vbgood1) + len(vbgood2)))
	
	pooravghb = (sum(hbpoor1) + sum(hbpoor2)) / (float(len(hbpoor1) + len(hbpoor2)))
	pooravgvb = (sum(vbpoor1) + sum(vbpoor2)) / (float(len(vbpoor1) + len(vbpoor2)))
	
	return [goodavghb, goodavgvb, pooravghb, pooravgvb]
		
if __name__ == "__main__":

	subjnum = input("What is subject number? Two digits: ")
	threshold_type = input("mocap or ss: ")

	if threshold_type == "mocap":
		print("Crunching mocap data now...")

		angles = calcMocapThreshold(subjnum)
		print("Good average theta/gamma, Poor average theta/gamma")
		print(angles)
		print("...")
	
	else:	
		print("Crunching ss data now...")
		ssvals = calcSSThreshold(subjnum)
		print("Good average hb/vb, Poor average hb/vb")
		print(ssvals)