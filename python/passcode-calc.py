import boto3


s3BucketName = "aws-summits-eu-west-1"
imagePrefix = "easter-egg-challenge/celebs/{}.jpg"

nonCelebsIndexs = ['1474', '2574', '317', '441', '4740', '5108', '2811']

rekognition = boto3.client('rekognition')


nonCelebsIndexs.sort(key=int)

passcode = ""
for index in nonCelebsIndexs:
    imageName = imagePrefix.format(index)
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


print(passcode)