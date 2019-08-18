from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import boto3
from io import BytesIO
import random
import string
import os

textColor = (0,0,255)
font_size = 40
font = ImageFont.truetype('/Library/Fonts/Arial.ttf', font_size)

maxCelebsIndex = 5467
sourceImage = "target-images/2811.jpg"
targetImage = "fixed-2811.jpg"


def embed_text(image, txt):
    draw = ImageDraw.Draw(img)
    width, height = image.size
    x = random.randint(0, width - font_size)
    y = random.randint(0, height - font_size)
    draw.text((x, y),txt,textColor,font=font)
    return image



img = Image.open(sourceImage)
txt = "oit"
img = embed_text(img, txt)
img.save(targetImage)
