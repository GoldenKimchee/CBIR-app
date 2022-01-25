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
		self.imageSizes = []
		self.xmax = 0
		self.ymax = 0
		self.colorCode = []
		self.intenCode = []
		self.fileList = []
		self.binary_cache = dict()

		# Add each image (for evaluation) into a list,
		# and a Photo from the image (for the GUI) in a list.
		for infile in glob.glob('images/*.jpg'):

			file, ext = os.path.splitext(infile)
			self.fileList.append(file + ".jpg")
			im = Image.open(infile)

			# Resize the image for thumbnails.
			imSize = im.size
			x = int(imSize[0]/4)
			y = int(imSize[1]/4)
			self.imageSizes.append(x * y)
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
		for image in self.imageList[:]:
			width, height = image.size

			# Get histogram bins for each method.
			CcBins, InBins = self.encode(image, width, height)
			self.colorCode.append(CcBins)
			self.intenCode.append(InBins)


	# Bin function returns an array of bins for the image(given as an argument),
	# both Intensity and Color-Code methods.
	def encode(self, image, width, height):

		# 2D array initilazation for bins, initialized
		# to zero.
		CcBins = [0]*65  # 64 bins. index 0 -> total number of pixels in picture, index 1 -> bin 1, index 2 -> bin 2 ...
		InBins = [0]*26  # 25 bins. Again, first index stores total pixels.

		InBins = self.intensity_method(image, width, height, InBins)
		CcBins = self.color_code_method(image, width, height, CcBins)

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
				bin = int((intensity + 10) // 10)  # Division rounds down to bin number.. in this case bins will range 0-24 (25 bins).

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
				eight_r = self.convert_to_eight_bit( str( self.decimal_to_binary(r) ) )
				eight_g = self.convert_to_eight_bit( str( self.decimal_to_binary(g) ) )
				eight_b = self.convert_to_eight_bit( str( self.decimal_to_binary(b) ) )
				r = self.first_two_nums( eight_r )  # get binary representation, then
				g = self.first_two_nums( eight_g )  # get the first two significant numbers
				b = self.first_two_nums( eight_b )

				color_code = r + g + b
				bin = self.binary_to_decimal(color_code)
				CcBins[bin + 1] += 1  # allocate pixel to corresponding bin, +1 since first index stores total pixels

		return CcBins


	# Convert binary to 8-bit form
	def convert_to_eight_bit(self, num):
		zeroes = 8 - len(num)
		return ("0" * zeroes) + num


	# Function to convert decimal number to binary using recursion
	def decimal_to_binary(self, num):
		return bin(num).replace("0b", "")


	# Turns a binary string to a decimal int
	def binary_to_decimal(self, binary):
		if binary in self.binary_cache.keys():
			return self.binary_cache[binary]
		else:
			decimal = int(binary, 2)
			self.binary_cache[binary] = decimal
		return decimal

	# Gets the first two significant digits of the binary.
	def first_two_nums(self, num):
		first_two = num[:2]
		return first_two

	# Accessor functions:
	def get_imageList(self):
		return self.imageList

	def get_photoList(self):
		return self.photoList

	def get_xmax(self):
		return self.xmax

	def get_ymax(self):
		return self.ymax
	# get the list of color code bins for the images
	def get_colorCode(self):
		return self.colorCode

	# get the list of intensity code bins for the images
	def get_intenCode(self):
		return self.intenCode

	# get the list of image sizes
	def get_image_sizes(self):
		return self.imageSizes

	# get the list of file names of the images
	def get_file_list(self):
		return self.fileList