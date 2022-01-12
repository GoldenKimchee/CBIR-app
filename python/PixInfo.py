# PixInfo.py
# Program to start evaluating an image in python

from PIL import Image, ImageTk
import glob, os, math


# Pixel Info class.
class PixInfo:
			
	# Constructor.
	def __init__(self, master):

		self.master = master
		self.imageList = []
		self.photoList = []
		self.xmax = 0
		self.ymax = 0
		self.colorCode = []
		self.intenCode = []
			
		# Add each image (for evaluation) into a list, 
		# and a Photo from the image (for the GUI) in a list.
		for infile in glob.glob('images/*.jpg'):
				
			file, ext = os.path.splitext(infile)
			im = Image.open(infile)
			
			# Resize the image for thumbnails.
			imSize = im.size
			x = imSize[0]/4
			y = imSize[1]/4
			imResize = im.resize((x, y), Image.ANTIALIAS)
			photo = ImageTk.PhotoImage(imResize)
					
			# Find the max height and width of the set of pics.
			if x > self.xmax:
				self.xmax = x
			if y > self.ymax:
				self.ymax = y
			
			# Add the images to the lists.
			self.imageList.append(im)
			self.photoList.append(photo)

		# Create a list of pixel data for each image and add it
		# to a list.
		for im in self.imageList[:]:
				
			#pixList = list(im.getdata())  # Rachel: not sure how the representation works with 
			pixList = im.load()  					 # getdata() even after testing, so im using load()
			CcBins, InBins = self.encode(pixList)
			self.colorCode.append(CcBins)
			self.intenCode.append(InBins)
						

	# Bin function returns an array of bins for each 
	# image, both Intensity and Color-Code methods.
	def encode(self, pixlist):
			
		# 2D array initilazation for bins, initialized
		# to zero.
		CcBins = [0]*64
		InBins = [0]*25
		
		self.intensity_method(pixlist, CcBins)
		self.color_code_method(pixlist, InBins)            
		#your code
		
		# Return the list of binary digits, one digit for each
		# pixel.
		return CcBins, InBins
		

	# Intensity method 
	# Formula: I = 0.299R + 0.587G + 0.114B 
	# 24-bit of RGB (8 bits for each color channel) color 
	# intensities are transformed into a single 8-bit value. 
	# There are 24 histogram bins.
	def intensity_method(self, pix, CcBins):
		width, height = pix.size
		for y in range(height): # reads pixels left to right, top down (by each row).
			for x in range(width): # This example code reads the RGB (red, green, blue) values 
				r, g, b = pix[x, y]  # in every pixel of a 'x' pixel wide 'y' pixel tall image.	
				intensity = (0.299*r) + (0.587*g) + (0.114*b)
		
	
	# Color-Code Method 
	# 24-bit of RGB color intensities transformed into 6-bit color
	# code from the first 2 bits of each of the three colors. 
	# There are 64 histogram bins. 
	def color_code_method(self, InBins):
		pass


	# Function to convert decimal number to binary using recursion
	def decimal_to_binary(self, num):
		if num >= 1:
			self.decimal_to_binary(num // 2)
		return num % 2

	# Accessor functions:
	def get_imageList(self):
		return self.imageList

	def get_photoList(self):
		return self.photoList

	def get_xmax(self):
		return self.xmax

	def get_ymax(self):
		return self.ymax

	def get_colorCode(self):
		return self.colorCode
		
	def get_intenCode(self):
		return self.intenCode