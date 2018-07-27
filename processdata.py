import os
import math

def calcMocapBasic(subjnums):
	# Read 4 mocap files (two good and two poor) then calculate the vertical angle change. At the end, calculate confidence interval.
	
	filenames = ["good1.csv", "good2.csv", "poor1.csv", "poor2.csv"]
	
	delta_theta = []
	delta_gamma = []
	
	for subjnum in subjnums:
		thetag1 = []
		thetag2 = []
		thetap1 = []
		thetap2 = []
		
		gammag1 = []
		gammag2 = []
		gammap1 = []
		gammap2 = []
	
		for name in filenames:
			realfilename = "subject" + subjnum + "\\" + name
			#print("Now processing" + realfilename)
			fileobj = open(realfilename, "r")
			
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
			
		# print("thetag1, thetag2")
		# print(sum(thetag1)/float(len(thetag1)))
		# print(sum(thetag2)/float(len(thetag2)))
		# print("thetap1, thetap2")
		# print(sum(thetap1)/float(len(thetap1)))
		# print(sum(thetap2)/float(len(thetap2)))
		# print("gammag1, gammag2")
		# print(sum(gammag1)/float(len(gammag1)))
		# print(sum(gammag2)/float(len(gammag2)))
		# print("gammap1, gammap2")
		# print(sum(gammap1)/float(len(gammap1)))
		# print(sum(gammap2)/float(len(gammap2)))
		
		goodavgtheta = (sum(thetag1) + sum(thetag2)) / (float(len(thetag1) + len(thetag2)))
		goodavggamma = (sum(gammag1) + sum(gammag2)) / (float(len(gammag1) + len(gammag2)))
		
		pooravgtheta = (sum(thetap1) + sum(thetap2)) / (float(len(thetap1) + len(thetap2)))
		pooravggamma = (sum(gammap1) + sum(gammap2)) / (float(len(gammap1) + len(gammap2)))
		
		delta_theta.append(goodavgtheta - pooravgtheta)
		delta_gamma.append(goodavggamma - pooravggamma)
	
	n_theta = len(delta_theta)
	n_gamma = len(delta_gamma)
	avg_theta = sum(delta_theta)/n_theta
	avg_gamma = sum(delta_gamma)/n_gamma
	
	print("The confidence intervals using two tailed prob of 5%")
	
	sum_angle = 0
	for theta in delta_theta:
		sum_angle = sum_angle + (theta - avg_theta)**2
	theta_s = math.sqrt(float((1/n_theta)*sum_angle))
	
	sum_angle = 0
	for gamma in delta_gamma:
		sum_angle = sum_angle + (gamma - avg_gamma)**2
	gamma_s = math.sqrt(float((1/n_gamma)*sum_angle))
	
	# n-1 degrees of freedom here is 6, for a 0.025....
	dict_t = {}
	dict_t[6] = 2.447
	dict_t[5] = 2.571
	dict_t[4] = 2.776
	
	t = dict_t[n_theta-1]
	halfrange_theta = t * theta_s/math.sqrt(float(n_theta))
	t = dict_t[n_gamma-1]
	halfrange_gamma = t * gamma_s/math.sqrt(float(n_gamma))
	
	print("change in theta, confidence range in degrees")
	print(str(avg_theta) + " +/- " + str(halfrange_theta))
	print(str(avg_theta - halfrange_theta) + " to " + str(avg_theta + halfrange_theta))
	
	print("change in gamma, confidence range in degrees")
	print(str(avg_gamma) + " +/- " + str(halfrange_gamma))
	print(str(avg_gamma - halfrange_gamma) + " to " + str(avg_gamma + halfrange_gamma))
	
	return
	
def calcMocapNat(subjnums):
	# Read the natp and natg and see if any noticeable diff.
	
	filenames = ["natp.csv", "natg.csv"]
	
	delta_theta = []
	delta_gamma = []
	
	for subjnum in subjnums:
		thetag = []
		thetap = []
		
		gammag = []
		gammap = []
	
		for name in filenames:
			realfilename = "subject" + subjnum + "\\" + name
			#print("Now processing" + realfilename)
			fileobj = open(realfilename, "r")
			
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
					
					
					if "leftx" in perlinedict and "topx" in perlinedict and "rightx" in perlinedict:
						findtheta = True
					else:
						findtheta = False
					if "topx" in perlinedict and "centrex" in perlinedict and "bottomx" in perlinedict:
						findgamma = True
					else:
						findgamma = False
					
					# Now time to calculate theta and gamma
					if findtheta:
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
					
					if findgamma:
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
					if name == "natp.csv":
						if findtheta: thetap.append(theta)
						if findgamma: gammap.append(gamma)
					elif name == "natg.csv":
						if findtheta: thetag.append(theta)
						if findgamma: gammag.append(gamma)
					
					perlinedict.clear()
					
		# print("thetap, thetag")
		# print(sum(thetap)/float(len(thetap)))
		# print(sum(thetag)/float(len(thetag)))
		goodavgtheta = sum(thetag) / float(len(thetag))
		pooravgtheta = sum(thetap) / float(len(thetap))
		delta_theta.append(goodavgtheta - pooravgtheta)

		# print("gammap, gammag")
		# print(sum(gammap)/float(len(gammap)))
		# print(sum(gammag)/float(len(gammag)))
		goodavggamma = sum(gammag) / float(len(gammag))
		pooravggamma = sum(gammap) / float(len(gammap))
		delta_gamma.append(goodavggamma - pooravggamma)
	
	print(delta_gamma)
	
	n_theta = float(len(delta_theta))
	n_gamma = float(len(delta_gamma))
	
	if n_theta == 0 or n_gamma == 0:
		print("ERROR!")
	else:
		avg_theta = sum(delta_theta)/n_theta
		avg_gamma = sum(delta_gamma)/n_gamma
	
	print("The confidence intervals")
	
	sum_angle = 0
	for theta in delta_theta:
		sum_angle = sum_angle + (theta - avg_theta)**2
	theta_s = math.sqrt(float((1/n_theta)*sum_angle))
	
	sum_angle = 0
	for gamma in delta_gamma:
		sum_angle = sum_angle + (gamma - avg_gamma)**2
	gamma_s = math.sqrt(float((1/n_gamma)*sum_angle))
	
	print("The confidence intervals using two-tailed prob of 5%")

	# n-1 degrees of freedom here is 6, for a 0.05....
	dict_t = {}
	dict_t[9] = 2.262
	dict_t[6] = 2.447
	dict_t[5] = 2.571
	dict_t[4] = 2.776
	dict_t[3] = 3.182
	
	t = dict_t[n_theta-1]
	halfrange_theta = t * theta_s/math.sqrt(float(n_theta))
	t = dict_t[n_gamma-1]
	halfrange_gamma = t * gamma_s/math.sqrt(float(n_gamma))
	
	print("change in theta, confidence range in degrees")
	print(str(avg_theta) + " +/- " + str(halfrange_theta))
	print(str(avg_theta - halfrange_theta) + " to " + str(avg_theta + halfrange_theta))
	
	print("change in gamma, confidence range in degrees")
	print(str(avg_gamma) + " +/- " + str(halfrange_gamma))
	print(str(avg_gamma - halfrange_gamma) + " to " + str(avg_gamma + halfrange_gamma))
	
	return
	
		
if __name__ == "__main__":

	subjnums = ["01", "03", "04", "05", "06", "07", "08"]
	print("Comparing the GOOD vs POOR 10second clips.")
	calcMocapBasic(subjnums)
	
	print("")
	
	subjnums2 = ["01", "03", "04", "05", "07"]
	print("Comparing the NATP vs NATG trials")
	calcMocapNat(subjnums2)
	
	print("")
	print("SECOND ROUND")
	
	subjnums = ["09", "10", "11", "12", "13"]
	print("Comparing the GOOD vs POOR 10second clips.")
	calcMocapBasic(subjnums)

	subjnums2 = ["09", "10", "11", "12", "13"]
	print("Comparing the NATP vs NATG trials")
	calcMocapNat(subjnums2)
	
	justforfun = ["01", "03", "04", "05", "07", "09", "10", "11", "12", "13"]
	print("The total:")
	calcMocapNat(justforfun)