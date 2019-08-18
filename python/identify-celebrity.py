import boto3
import json

# Document
s3BucketName = "aws-summits-eu-west-1"
s3Prefix = "easter-egg-challenge/celebs-original"
destPrefix = "easter-egg-challenge/celebs"
destIndex = 1 

auditFileIndex = 1
auditFile = open("celebs-original-rekognition{}.json".format(auditFileIndex), "w")


#Rekognition client
rekognition=boto3.client('rekognition')
s3 = boto3.client('s3')

def recognize_celeb(bucketName, imageName, destIndex):
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
        else:
            celeb = response['CelebrityFaces'][0]['Name']
            copy_source = {'Bucket': bucketName, 'Key': imageName} 
            destKey = '{}/{}.jpg'.format(destPrefix, destIndex)     
            print(destKey) 
            s3.copy_object(CopySource=copy_source, Bucket=bucketName,
                        Key=destKey)
            destIndex += 1  
            print('index = {}'.format(destIndex))

        data = {'image' : imageName, 'celeb' : celeb}
        print(json.dumps(data))
        auditFile.write(json.dumps(data))
        auditFile.write("\n")
    except Exception as e:
        return destIndex
        
    return destIndex

paginator = s3.get_paginator('list_objects_v2')
operation_parameters = {'Bucket': s3BucketName,
                        'Prefix': s3Prefix}
page_iterator = paginator.paginate(**operation_parameters)

count = 0
for page in page_iterator:
    if page['KeyCount'] > 0:
        for item in page['Contents']:
            print(item['Key'])
            destIndex = recognize_celeb(s3BucketName, item['Key'], destIndex)
            count += 1

            if (count%1000) == 0: #start new audit file
                auditFile.close()
                auditFileIndex += 1
                auditFile = open("celebs-original-rekognition{}.json".format(auditFileIndex), "w")


auditFile.close()
    