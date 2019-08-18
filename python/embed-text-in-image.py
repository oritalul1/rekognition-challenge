from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import matplotlib.image as mpimg
import boto3
from io import BytesIO
import random
import string

textColor = (0,0,255)
font_size = 40
font = ImageFont.truetype('/Library/Fonts/Arial.ttf', font_size)


s3BucketName = "aws-summits-eu-west-1"
image_s3_prefix = "easter-egg-challenge/celebs/{}.jpg"

numImagesToEmbedText = 200
maxCelebsIndex = 980

s3 = boto3.resource('s3')
bucket = s3.Bucket(s3BucketName)

def random_string(stringLength=3):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def embed_random_text(image):
    string_len = random.randint(3,5)
    txt = random_string(string_len)
    draw = ImageDraw.Draw(img)
    width, height = image.size
    x = random.randint(0, width - font_size)
    y = random.randint(0, height - font_size)
    draw.text((x, y),txt,textColor,font=font)
    return image


# Choose random images to embed text
image_indexes = []
for r in range (numImagesToEmbedText):
    image_indexes.append(random.randint(1,maxCelebsIndex))
    
image_indexes.sort()
print(image_indexes)

for i in image_indexes:
    print("Embedding text in {}.jpg".format(i))
    image_object = bucket.Object(image_s3_prefix.format(i)) 
    img = Image.open(image_object.get()['Body'])
    img = embed_random_text(img)
    try:
        img.save('random-text-images/{}.jpg'.format(i))
    except Exception as e:
        pass
