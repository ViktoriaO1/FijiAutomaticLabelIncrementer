"""
Labeling Extension for ImageJ Fiji 

The purpose of this script is to enable multi-object keypoint labeling for an imagestack in ImageJ.
With each click the counter/label of the point is incremented in order to be able to distinguish a set of chosen labels more easily
also already when labeling in ImageJ.

Instructions:
	You must open the Imagestack or the image and select e.g. the Hand Tool (just not the MultiPointTool directly, as we activate it at first click).
	You can then start labeling the desired keypoints and the counter will start at 0 again when you have reached the end of your labeling list.
	E.g. I want to label 14 keypoints, so I configure the counter number to be 14.
	If you want to move or delete a keypoint that you might have misplaced, you should first press 'F3', in order to disable the 
	counter from automatically incrementing. Once you have finished repositioning your label, press 'F4' to resume the automatic label incrementer.
	
	Once you have labeled all your images and objects, click 'Analyze' and 'Measure' and then save your measurement results.
	In the Section 'Counter' of the measured results you will now find the identification label for the respective X and Y coordinate.

Known bugs: 
	1. The delete function at the moment just lets you delete a label, but does not let you add one at its place.
	2. The dragging and deleting of points without freezing the automatic incrementer is possible, but leads to the whole counting scheme being muddled.
	

Author: V de La Rochefoucauld
Date: 04-2019
"""


from ij import IJ
from ij import WindowManager
from java.awt.event import MouseAdapter, MouseEvent, KeyAdapter
 
def changePointer(imp, counter, colors):
	#IJ.log("point selected for bodypart: " +str(counter))
	curr_color = colors[counter%7]
	#print("curr color :" +str(curr_color))
	IJ.setTool('multipoint')
	IJ.run("Point Tool...", "type=Hybrid color=" +curr_color +"size=Small label counter=" + str(counter))
	if counter %13 ==0 and counter > 0:
 		counter = 0
 	else: 
 		counter +=1
 	return counter

 
class ML(MouseAdapter):

	class KL(KeyAdapter):
		def __init__(self, mouse):
			KeyAdapter.__init__(self)
			self.mouse = mouse
			self.enabled = True
			
		def keyPressed(self, keyevent):
			if (keyevent.getKeyCode() == 114): # If you press F4 you can drag and delete points, as it behaves like the multipoint module 
				print("Disabled Mouse")
				self.enabled = False
			elif (keyevent.getKeyCode() == 115):  # If you press F5
				self.enabled = True
				print("Enabled Mouse")
 
 	def __init__(self, counter):
	   self.counter = counter
	   #print("counter: " + str(self.counter))
	   self.bodycolors = ['Red','Green','Blue','Magenta','Yellow','Orange','Cyan']
	   self.enabled = True
	   MouseAdapter.__init__(self)
	   self.keys = self.KL(self)

 	def mousePressed(self, event):
		canvas = event.getSource()
		imp = canvas.getImage()
		if self.keys.enabled:
			#print("counter: " + str(self.counter))
			self.counter = changePointer(imp, self.counter, self.bodycolors)
	
listener = ML(counter=0)

for imp in map(WindowManager.getImage, WindowManager.getIDList()):
	win = imp.getWindow()
	if win is None:
   		continue
	win.getCanvas().addMouseListener(listener)
	win.getCanvas().addKeyListener(listener.keys)