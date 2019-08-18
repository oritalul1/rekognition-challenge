import boto3
import json
import time
import sys

# Document
s3BucketName = "aws-summits-eu-west-1"
s3Prefix = "easter-egg-challenge/celebs/"

auditFileIndex = 1
auditFileName = "logs/celebs-rekognition-sol{}.json"
auditFile = open(auditFileName.format(auditFileIndex), "w")
nonCelebsFile = open("non-celebs.txt", "w")

nonCelebsIndexs = []

#Rekognition client
rekognition=boto3.client('rekognition')
s3 = boto3.client('s3')

def recognize_celeb(bucketName, imageName):
    try:
        response = rekognition.recognize_celebrities(
                        Image={
                            'S3Object':{
                                'Bucket': bucketName,
                                'Name': imageName
                            }
                        })

        if not response['CelebrityFaces']:
            celeb = 'No celebrity identified'
            image_index = imageName.split("/")[-1]
            image_index = image_index.split(".")[0]
            print("image index: {}".format(image_index))
            nonCelebsFile.write(image_index)
            nonCelebsFile.write("\n")
            nonCelebsIndexs.append(image_index)
        else:
            celeb = response['CelebrityFaces'][0]['Name']

        data = {'image' : imageName, 'celeb' : celeb}
        print(json.dumps(data))
        auditFile.write(json.dumps(data))
        auditFile.write("\n")
    except Exception as e:
        pass
        

if len(sys.argv) > 1:
    print("Got {} arguments".format(len(sys.argv)))
    s3BucketName = sys.argv[1]
    s3Prefix = sys.argv[2]


# 1. identify teh non-celeb images
paginator = s3.get_paginator('list_objects_v2')
operation_parameters = {'Bucket': s3BucketName,
                        'Prefix': s3Prefix}
page_iterator = paginator.paginate(**operation_parameters)

count = 0
for page in page_iterator:
    if page['KeyCount'] > 0:
        for item in page['Contents']:
            print(item['Key'])
            recognize_celeb(s3BucketName, item['Key'])
            count += 1
            if (count%50) == 0: #avoid trottling by API calls to rekognition
                time.sleep(1)

            if (count%500) == 0: #start new audit file
                auditFile.close()
                auditFileIndex += 1
                auditFile = open(auditFileName.format(auditFileIndex), "w")


# 2. sort the images indexes in ascending order
nonCelebsIndexs.sort(key=int)
print(nonCelebsIndexs)

# 3. extract the text from the non celebs images to get the passcode
passcode = ""
for index in nonCelebsIndexs:
    imageName = s3Prefix + index + ".jpg"
    print(imageName)

    response = rekognition.detect_text(
                        Image={
                            'S3Object':{
                                'Bucket': s3BucketName,
                                'Name': imageName
                            }
                        })
                        
    textDetections=response['TextDetections']
    text = textDetections[0]['DetectedText']
    print(text)
    passcode += text


print("The passcode is: " + passcode)



auditFile.close()
nonCelebsFile.close()
    