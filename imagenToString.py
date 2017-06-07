from PIL import Image
import sys
import ansi


def load_and_resize_image(imgname, antialias, maxLen, aspectRatio):
	if aspectRatio is None:
			aspectRatio = 1.0

	img = Image.open(imgname)

	# force image to RGBA - deals with palettized images (e.g. gif) etc.
	if img.mode != 'RGBA':
			img = img.convert('RGBA')

	# need to change the size of the image?
	if maxLen is not None or aspectRatio != 1.0:

			native_width, native_height = img.size

			new_width = native_width
			new_height = native_height

			# First apply aspect ratio change (if any) - just need to adjust one axis
			# so we'll do the height.
			if aspectRatio != 1.0:
					new_height = int(float(aspectRatio) * new_height)

			# Now isotropically resize up or down (preserving aspect ratio) such that 
			# longer side of image is maxLen 
			if maxLen is not None:
					rate = float(maxLen) / max(new_width, new_height)
					new_width = int(rate * new_width)  
					new_height = int(rate * new_height)

			if native_width != new_width or native_height != new_height:
					img = img.resize((new_width, new_height), Image.ANTIALIAS if antialias else Image.NEAREST)

	return img




def indent_image (img):
	for i in img:
		print((i),end="")
		#if img[i] == '\n':
		#	img[i] += "\t\t"
	
	#print(img)



def imgToStr (imgname, maxLen = 45, target_aspect_ratio = 0.5):

	antialias = False

	try:
			maxLen = float(maxLen)
	except:
			maxLen = 100.0   # default maxlen: 100px

	try:
			target_aspect_ratio = float(target_aspect_ratio)
	except:
			target_aspect_ratio = 1.0   # default target_aspect_ratio: 1.0

	try:
			img = load_and_resize_image(imgname, antialias, maxLen, target_aspect_ratio)
	except IOError:
			exit("File not found: " + imgname)


	# get pixels
	pixel = img.load()
	width, height = img.size
	bgcolor = None

	# MAKE MAGIC
	imagenFinal = ansi.generate_ANSI_from_pixels(pixel, width, height, bgcolor)[0]

	# Undo residual color changes, output newline because
	# generate_ANSI_from_pixels does not do so
	# removes all attributes (formatting and colors)
	imagenFinal += "\x1b[0m\n"

	return imagenFinal

#imagenCopia = imagenFinal
#print(imagenCopia)
#print(imagenFinal.replace("\n", "\n\t"))
#print(imagenFinal)

#sys.stdout.flush()