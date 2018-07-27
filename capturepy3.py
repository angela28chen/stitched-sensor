import serial
import os
import io
import sys

def cap(sensor, port, points, postureType, subjectID):
	# Used to capture sensor values from either shirt and put in an appropriately named file.
	#
	# port: number of port, usually "0" corresponds to COM0 for windows
	# points: how many data points captured
	# postureType: good, poor, natg, natp
	# subjectID: check records for ID to name table

	# filename style: "LILYPsub02_0_10.csv"
	
	needFilename = True
	counter = 0
	while(needFilename):
		filename = sensor + "sub" + "0"*(2-len(subjectID)) + subjectID + "_" + postureType + "_" + str(counter) + ".csv"
		if os.path.isfile(filename): 
			counter += 1
		else: 
			needFilename = False
	
	print(filename)
	fileobj = open(filename, "w")

	portname = 'COM' + port #"/dev/ttyUSB"
	ser = serial.Serial(port=portname, baudrate=9600, timeout=1) 
	sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
	#newline = sio.readline()
	#sio.flush()

	i = 1
	while(i <= int(points)):
		newline = sio.readline()
		sio.flush()
		#if newline != "" and newline != "\r" and newline != '\n':
		fileobj.write(newline)
			
		if "\n" in newline:
			print(str(i) + "/" + str(points))
			sys.stdout.flush()
			i += 1

	fileobj.close()
	return filename

def recordTrial(sensor, port, points, postureType, subjectID):
	again = True
	while again:
		input("Press enter to begin.")
		filename = cap(sensor, port, points, postureType, subjectID)
		savetrial = input("Save trial " + filename + "? (y/n)")
		if savetrial == 'n':
			os.remove(filename)
			print("The file " + filename + " was deleted. Trying again.")
		else:
			again = False
			print("The file " + filename + " was saved.")

	return filename
	
def isGoodPosture(filename, subjectID):
	# Drawing from SVM or threshold values to decide if subject is in a position of good posture
	print("Under construction")
	return

if __name__ == "__main__":

	print("Starting a new session now")
	
	sensor = input("Which Sensor (LILYP/ESP32): ")
	port = input("Port number: ")
	subjectID = input("Write name and ID and shoulder width down in notebook. Subject ID: ")
	record = []
	print("...")
	
	print("Which stage?")
	print("A) Collect initial data")
	print("B) After setting threshold")
	stage = input("Stage (a/b): ")
	
	if stage == "a":
		print("Write down subject data")
		input("Done?")
		
		print("1. Collect forced GOOD posture. Ten seconds.")
		postureType = 'good'
		points = 40
		filename = recordTrial(sensor, port, points, postureType, subjectID)
		record.append(filename)
		print("...")
		
		print("2. Collect forced POOR posture. Two times, ten seconds each.")
		postureType = 'poor'
		points = 40
		filename = recordTrial(sensor, port, points, postureType, subjectID)
		record.append(filename)
		print("...")
		
		print("3. Collect forced GOOD posture. Ten seconds.")
		postureType = 'good'
		points = 40
		filename = recordTrial(sensor, port, points, postureType, subjectID)
		record.append(filename)
		print("...")
		
		print("4. Collect forced POOR posture. Two times, ten seconds each.")
		postureType = 'poor'
		points = 40
		filename = recordTrial(sensor, port, points, postureType, subjectID)
		record.append(filename)
		print("...")

		print("5. Collect natural POOR posture. Once, 2min duration.")
		postureType = 'natp'
		points = 480
		filename = recordTrial(sensor, port, points, postureType, subjectID)
		record.append(filename)
		print("...")
		
		print("This is the record.")
		print(record)
		
		print("Now it's time to add the threshold.")
		
	elif stage == "b":
		print("6. Collect corrected GOOD posture. Once, 2min duration.")
		postureType = 'natg'
		points = 480
		filename = recordTrial(sensor, port, points, postureType, subjectID)
		record.append(filename)
		print("...")
		
		print("This is the record.")
		print(record)

	print("Session over. If need to correct anything, recall function 'recordTrial(sensor, port, points, postureType, subjectID)'")












