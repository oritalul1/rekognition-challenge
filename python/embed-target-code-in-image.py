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
directory = "target-images"
passcode = "rekognitionnoitingoker"


def embed_text(image, txt):
    draw = ImageDraw.Draw(img)
    width, height = image.size
    x = random.randint(0, width - font_size)
    y = random.randint(0, height - font_size)
    draw.text((x, y),txt,textColor,font=font)
    return image

num_images = len([name for name in os.listdir(directory)])
print("num images: {}".format(num_images))

#get random indexes for the images
image_indexes = []
for r in range (num_images):
    image_indexes.append(random.randint(1,maxCelebsIndex))
    
image_indexes.sort()
print(image_indexes)

# iterate over non-celeb images
i = 0
start = 0
step = len(passcode)/num_images
end = step
print ("start: {}, step: {} end: {}".format(start, step, end))

for filename in os.listdir(directory):
    print(filename)
    img = Image.open("{}/{}".format(directory,filename))
    txt = passcode[start:end]
    start += step
    img = embed_text(img, txt)
    img.save('target-images-with-code/{}.jpg'.format(image_indexes[i]))
    i += 1
    if i == (num_images-1):
        end = len(passcode)
    else:
        end += step
