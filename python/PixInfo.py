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
			width, height = im.size

			# Get histogram bins for each method.
			CcBins, InBins = self.encode(im, width, height)
   
			self.colorCode.append(CcBins)
			self.intenCode.append(InBins)
						

	# Bin function returns an array of bins for each 
	# image, both Intensity and Color-Code methods.
	def encode(self, im, width, height):
			
		# 2D array initilazation for bins, initialized
		# to zero.
		CcBins = [0]*65  # 64 bins. index 0 -> total number of pixels in picture, index 1 -> bin 1, index 2 -> bin 2 ...
		InBins = [0]*26  # 25 bins. Again, first index stores total pixels.
		
		InBins = self.intensity_method(im, width, height, InBins)
		CcBins = self.color_code_method(im, width, height, CcBins)            
		
		return CcBins, InBins
		

	# Intensity method 
	# Formula: I = 0.299R + 0.587G + 0.114B 
	# 24-bit of RGB (8 bits for each color channel) color 
	# intensities are transformed into a single 8-bit value. 
	# There are 24 histogram bins.
	def intensity_method(self, im, width, height, InBins):
		total_pixels = width * height
		InBins[0] = total_pixels
  
		for y in range(height): # reads pixels left to right, top down (by each row).
			for x in range(width): # This example code reads the RGB (red, green, blue) values 
       
				r, g, b = im.getpixel((x, y))  # in every pixel of a 'x' pixel wide 'y' pixel tall image.	
				intensity = (0.299*r) + (0.587*g) + (0.114*b)
				bin = (intensity + 10) // 10  # Division rounds down to bin number.. in this case bins will range 0-24 (25 bins).
    
				if bin == 26:  # last bin is 240 to 255, so bin of 24 and 25 will 
					bin = 25   # correspond to bin 24, BUT +1 since first index stores total pixels.
				InBins[bin] += 1  # allocate pixel to corresponding bin
    
		return InBins
		
	
	# Color-Code Method 
	# 24-bit of RGB color intensities transformed into 6-bit color
	# code from the first 2 bits of each of the three colors. 
	# There are 64 histogram bins. 
	def color_code_method(self, im, width, height, CcBins):
		total_pixels = width * height
		CcBins[0] = total_pixels 
  
		for y in range(height): 
			for x in range(width):  
       
				r, g, b = im.getpixel((x, y))	
				r = self.first_two_nums( self.decimal_to_binary(r) )  # get binary representation, then 
				g = self.first_two_nums( self.decimal_to_binary(g) )  # get the first two significant numbers
				b = self.first_two_nums( self.decimal_to_binary(b) )
    
				color_code = r + g + b
				bin = self.binary_to_decimal(color_code)
				CcBins[bin + 1] += 1  # allocate pixel to corresponding bin, +1 since first index stores total pixels
    
		return CcBins


	# Function to convert decimal number to binary using recursion
	def decimal_to_binary(self, num):
		if num >= 1:
			self.decimal_to_binary(num // 2)
		return num % 2

	
	# Turns a binary number to a decimal
	def binary_to_decimal(binary):
		decimal, i = 0, 0
		while binary != 0:
			result = binary % 10
			decimal = decimal + result * pow(2, i)
			binary = binary // 10
			i += 1
		return decimal


	# Gets the first two significant digits of the binary. 
	# If the two digits are less than 10, makes sure that 
	# the 0 is retained to get the correct 6 bit color code.
	def first_two_nums(self, num):
		first_two = num // 1000000
		if first_two == 0:
			first_two = "00"
		elif first_two < 10:
			first_two = "0" + str(first_two)
		return str(first_two)

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