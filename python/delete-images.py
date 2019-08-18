import boto3

s3BucketName = "aws-summits-eu-west-1"
s3Prefix = "easter-egg-challenge/celebs/{}.jpg"

s3 = boto3.client('s3')

for i in range(1001, 5467):
    key = s3Prefix.format(i)
    print("deleting: {}".format(key))
    s3.delete_object(Bucket=s3BucketName, Key=key)