import serial
import os
import io
import sys

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
import matplotlib.pyplot as plt

import tkinter as tk
from tkinter import *

# Use Tk class to create the main window of application
root = tk.Tk()

## ----- CONSTANTS AND VARIABLES
hb_ymax = 3500
hb_ymin = 3400
vb_ymax = 3450
vb_ymin = 3350
windowsize = 100

t = []
hbrecord = []
vbrecord = []
high_hb_thresh_record = []
low_hb_thresh_record = []
high_vb_thresh_record = []
low_vb_thresh_record = []

#global high_hb_thresh, low_hb_thresh, high_vb_thresh, low_vb_thresh
high_hb_thresh = 3470
low_hb_thresh = 3465
high_vb_thresh = 3425
low_vb_thresh = 3420

hb_currentgood = True
vb_currentgood = True
event_id = 0

## ----- FUNCTIONS
def update_labels():
	global hb_currentgood, vb_currentgood
	global event_id
	
	if hb_currentgood:
		label_hb.config(bg="green")
	else:
		label_hb.config(bg="red")
		
	if vb_currentgood:
		label_vb.config(bg="green")
	else:
		label_vb.config(bg="red")
		
	if hb_currentgood and vb_currentgood:
		label_overall.config(bg="green", text="GOOD")
	else:
		label_overall.config(bg="red", text="POOR")
		
	event_id = root.after(50, update_labels)

def set_hhb():
	global high_hb_thresh
	high_hb_thresh = int(entry_high_hb.get())
	
def set_lhb():
	global low_hb_thresh
	low_hb_thresh = int(entry_low_hb.get())
	
def set_hvb():
	global high_vb_thresh
	high_vb_thresh = int(entry_high_vb.get())
	
def set_lvb():
	global low_vb_thresh
	low_vb_thresh = int(entry_low_vb.get())
	
def quit_program():
	root.after_cancel(event_id)
	root.destroy()

def update_fhb(i):
	global hb_currentgood, vb_currentgood
	# Read serial input and parse it
	newline = ""
	while "\n" not in newline:
		newline = sio.readline()
		sio.flush()
	
	line = newline.strip("\n")
	splitvals = line.split(",")
	hbval = int(splitvals[0].strip())
	vbval = int(splitvals[1].strip())
	#print("hbval, vbval: " + str(hbval) + "," + str(vbval))
	
	# Update the values of all the lists
	if len(t) == 0:
		counter = 0
	else:
		counter = t[len(t)-1]
	t.append(counter+1)
	hbrecord.append(hbval)
	high_hb_thresh_record.append(high_hb_thresh)
	low_hb_thresh_record.append(low_hb_thresh)
	
	# Similar stuff for vbval
	vbrecord.append(vbval)
	high_vb_thresh_record.append(high_vb_thresh)
	low_vb_thresh_record.append(low_vb_thresh)
	
	# Is it good posture
	if hb_currentgood and hbval < low_hb_thresh:
		hb_currentgood = False
	elif not hb_currentgood and hbval > high_hb_thresh:
		hb_currentgood = True
	if vb_currentgood and vbval < low_vb_thresh:
		vb_currentgood = False
	elif not vb_currentgood and vbval > high_vb_thresh:
		vb_currentgood = True
	
	# Let the x-axis scroll
	current_time = max(len(t), windowsize)
	window_begin = max(1, current_time-windowsize)
	hb_axes.set_xlim(window_begin, current_time)
	hb_axes.set_ylim(hb_ymin, hb_ymax)
	
	# Plot the sensor line and both thresholds
	hb_sensorline, = hb_axes.plot(t[window_begin:current_time], hbrecord[window_begin:current_time], "black")	
	hb_high_line, = hb_axes.plot(t[window_begin:current_time], high_hb_thresh_record[window_begin:current_time], "blue")
	hb_low_line, = hb_axes.plot(t[window_begin:current_time], low_hb_thresh_record[window_begin:current_time], "red")

	return hb_sensorline, hb_high_line, hb_low_line

def update_fvb(i):	
	# With luck the serial is read from other function update_fhb(), and the record is made...
		
	# Let the x-axis scroll
	current_time2 = max(len(t), windowsize)
	window_begin2 = max(1, current_time2-windowsize)
	vb_axes.set_xlim(window_begin2, current_time2)
	vb_axes.set_ylim(vb_ymin, vb_ymax)
	
	# Plot the sensor line and both thresholds
	vb_sensorline, = vb_axes.plot(t[window_begin2:current_time2], vbrecord[window_begin2:current_time2], "black")	
	vb_high_line, = vb_axes.plot(t[window_begin2:current_time2], high_vb_thresh_record[window_begin2:current_time2], "blue")
	vb_low_line, = vb_axes.plot(t[window_begin2:current_time2], low_vb_thresh_record[window_begin2:current_time2], "red")

	return vb_sensorline, vb_high_line, vb_low_line
	
## ----- TITLE BAR
root.title("Stitched Sensors")


## ----- CENTRE TOP DESCRIPTION
label_instr = tk.Label(root, text="Observe graphs for sensor readings and set appropriate thresholds below.")
label_instr.pack()


## ----- TOP BLOCK FOR HB
hb_section = Frame(root)
hb_section.pack()

hb_graph = Frame(hb_section)
hb_graph.grid(rowspan=3, column=0)

figure_hb, hb_axes = plt.subplots(figsize=(6,2.5))
hb_axes.set_title("Horizontal Sensor")
hb_axes.get_xaxis().set_visible(False)
hb_axes.set_ylim(hb_ymin, hb_ymax)
hb_axes.minorticks_on()
hb_axes.grid(b=True, which='major', linestyle='-')
hb_axes.grid(b=True, which='minor', linestyle=':')

canvas = FigureCanvasTkAgg(figure_hb, hb_graph)
canvas.draw()
canvas.get_tk_widget().pack() 

# Horizontal sensor indicator
label_hb = tk.Label(hb_section, text="Horizontal Sensor", font="13", fg="white", bg="green")
label_hb.grid(row=0, column=1, columnspan=3)

# High threshold for horizontal back sensor
label_high_hb = tk.Label(hb_section, text="High threshold (HB):", fg="Blue")
label_high_hb.grid(row=1, column=1)
entry_high_hb = tk.Entry(hb_section)
entry_high_hb.insert(0, str(high_hb_thresh))
entry_high_hb.grid(row=1, column=2)
button_high_hb = tk.Button(hb_section, text = "Set Value", command=set_hhb)
button_high_hb.grid(row=1, column=3)

# Low threshold for horizontal back sensor
label_low_hb = tk.Label(hb_section, text="Low threshold (HB):", fg="Red")
label_low_hb.grid(row=2, column=1)
entry_low_hb = tk.Entry(hb_section)
entry_low_hb.insert(0, str(low_hb_thresh))
entry_low_hb.grid(row=2, column=2)
button_low_hb = tk.Button(hb_section, text = "Set Value", command=set_lhb)
button_low_hb.grid(row=2, column=3)


## ----- BOTTOM BLOCK FOR VB
vb_section = Frame(root)
vb_section.pack()

vb_graph = Frame(vb_section)
vb_graph.grid(rowspan=3, column=0)

figure_vb, vb_axes = plt.subplots(figsize=(6,2.5))
vb_axes.set_title("Vertical Sensor")
vb_axes.get_xaxis().set_visible(False)
vb_axes.set_ylim(vb_ymin, vb_ymax)
vb_axes.minorticks_on()
vb_axes.grid(b=True, which='major', linestyle='-')
vb_axes.grid(b=True, which='minor', linestyle=':')

canvas = FigureCanvasTkAgg(figure_vb, vb_graph)
canvas.draw()
canvas.get_tk_widget().pack() 

# Vertical Sensor label
label_vb = tk.Label(vb_section, text="Vertical Sensor", font="13", fg="white", bg="green")
label_vb.grid(row=0, column=1, columnspan=3)

# High threshold for vertical back sensor
label_high_vb = tk.Label(vb_section, text="High threshold (VB):", fg="Blue")
label_high_vb.grid(row=1, column=1)
entry_high_vb = tk.Entry(vb_section)
entry_high_vb.insert(0, str(high_vb_thresh))
entry_high_vb.grid(row=1, column=2)
button_high_vb = tk.Button(vb_section, text = "Set Value", command=set_hvb)
button_high_vb.grid(row=1, column=3)

# Low threshold for vertical back sensor
label_low_vb = tk.Label(vb_section, text="Low threshold (VB):", fg="Red")
label_low_vb.grid(row=2, column=1)
entry_low_vb = tk.Entry(vb_section)
entry_low_vb.insert(0, str(low_vb_thresh))
entry_low_vb.grid(row=2, column=2)
button_low_vb = tk.Button(vb_section, text = "Set Value", command=set_lvb)
button_low_vb.grid(row=2, column=3)

## ----- FOOTER for total and exit button
footer_section = Frame(root)
footer_section.pack()
label_overall = tk.Label(footer_section, text="GOOD", fg="White", bg="Green")
label_overall.grid(row=0, column=0)
button_exit = tk.Button(footer_section, text = "Exit Window", command=quit_program)
button_exit.grid(row=0, column=1)

# Set up serial communication
portname = 'COM3'
ser = serial.Serial(port=portname, baudrate=9600, timeout=0.2) 
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

# Update label colours
root.after(1000, update_labels)

# Animate graph and enter main loop
ani_hb = animation.FuncAnimation(figure_hb,update_fhb,interval=1,blit=True)
ani_vb = animation.FuncAnimation(figure_vb,update_fvb,interval=1,blit=True)
root.mainloop()	