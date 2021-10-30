from os import write
from PIL import Image, ImageDraw, ImageFont
from calculateBrightness import getCharList


def resize(image,resizing_factor):
	width,height = image.size
	resized_image = image.resize((int(width/resizing_factor/1), int(height/resizing_factor/1)))
	return resized_image

def grayify(image):
	grayscale_image = image.convert("L")
	return grayscale_image

def convertToAscii(image,charlist):
	pixels = image.getdata()
	ascii_chars = "".join(charlist[int(pixel/2.8)]['char'] for pixel in pixels)
	return ascii_chars

def writeToImage(ascii_chars,width,height,resizing_factor,font_size):
	txt = Image.new("RGBA", (width,height), (0,0,0))
	fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", font_size)
	d = ImageDraw.Draw(txt)

	rowStart = 0
	resized_width = int(1920/resizing_factor)
	for i in range(0,len(ascii_chars), resized_width):
		arr = ascii_chars[i:(i+resized_width)]
		j=0
		print("row number: ", rowStart)
		for char in arr:
			d.text((j*resizing_factor,rowStart), char, font=fnt, fill=(255,255,255))
			j += 1
		
		rowStart += resizing_factor

	txt.save('./output/asciiImage.png')
	return


def convert_to_ascii_image():
	try:
		image = Image.open('./input/image.png')

	except:
		print("image could not be accessed")

	#this times itself defines the number of pixels which will be replaced by each character
	resizing_factor = 4

	#font size of the ascii characters
	font_size = 6
	width,height = image.size	
	
	#get the list of characters. we will draw our image with these characters. 
	charlist = getCharList()

	resizedImage = resize(image,resizing_factor)
	grayscaleImage = grayify(resizedImage)
	ascii_chars = convertToAscii(grayscaleImage,charlist)
	writeToImage(ascii_chars,width,height,resizing_factor,font_size)
	

	pixel_count = len(ascii_chars)
	ascii_image = "\n".join(ascii_chars[i:(i+int(width/resizing_factor))] for i in range(0, pixel_count, int(width/resizing_factor))) #this is for writing to a text file
	with open("./output/ascii_image.txt", "w") as f:
		f.write(ascii_image)
convert_to_ascii_image()

