import os
import io
import boto3
import logging
import logging.handlers

from pathlib import Path

LOG_FILENAME = 'logs/upload-to-s3.log'
INPUT_FILENAME = 'source-dirs.txt'

# Set up a specific logger with our desired output level
# logger = logging.getLogger('MyLogger')
# logger.setLevel(logging.INFO)
# # Add the log message handler to the logger
# handler = logging.handlers.RotatingFileHandler(
#               LOG_FILENAME, maxBytes=5242880, backupCount=100)
# logger.addHandler(handler)

logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)
logger = logging.getLogger('MyLogger')

s3BucketName = "aws-summits-eu-west-1"
keyName = "easter-egg-challenge/tests/{}.jpg"
# keyName = "easter-egg-challenge/original-images/{}.jpg"


#root_dir = Path('/Users/oritalul/WorkDocs/AI/Rekognition-Celebrity/')

client=boto3.client('s3')

i=1
file = open(INPUT_FILENAME, 'r') 
for line in file:
    root_dir = Path(line.strip()) 
    logger.info('Uploading directory: ' + str(root_dir))
    logger.info('Index ' + str(i))
    # root_dir = Path("\"/Users/oritalul/WorkDocs/AI/Rekognition Demo Images\"")
    for f in root_dir.glob('**/*.jpg'):
        logger.info('found images to upload')
        file_path = str(f)      
        # logger.info('uploading file: \t' + file_path)
        client.upload_file(file_path, s3BucketName, keyName.format(i))
        i += 1
