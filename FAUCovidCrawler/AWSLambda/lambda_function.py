'''
Original code contributor: mentzera
Article link: https://aws.amazon.com/blogs/big-data/building-a-near-real-time-discovery-platform-with-aws/
'''
import boto3
import json

import twitter_to_es
# from Examples.Demo.AWS_Related.TwitterStreamWithAWS.LambdaWithS3Trigger import \
#     twitter_to_es

from tweet_utils import \
    get_tweet, id_field, get_tweet_mapping

headers = {"Content-Type": "application/json"}

s3 = boto3.client('s3')
kinesis_client = boto3.client('kinesis')
# dynamoDb_client = boto3.client('dynamodb')


# Lambda execution starts here
def handler(event, context):
    for record in event['Records']:

        # Get the bucket name and key for the new file
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        # Get s3 object, read, and split the file into lines
        try:
            obj = s3.get_object(Bucket=bucket, Key=key)

        except Exception as e:
            print(e)
            print(
                'Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(
                    key, bucket))
            raise e

            # Parse s3 object content (JSON)
        try:
            # https://stackoverflow.com/questions/31976273/open-s3-object-as-a-string-with-boto3
            s3_file_content = obj['Body'].read().decode('utf-8')

            # clean trailing comma
            if s3_file_content.endswith(',\n'):
                s3_file_content = s3_file_content[:-2]
            tweets_str = '[' + s3_file_content + ']'
            # print(tweets_str)
            tweets = json.loads(tweets_str)

        except Exception as e:
            print(e)
            print('Error loading json from object {} in bucket {}'.format(key,
                                                                          bucket))
            raise e

        for doc in tweets:
            tweet = get_tweet(doc)
            # print(tweet['sentiments'])
            print(tweet)

        print('===\n\n\n')

        #=====================
        #==send data to dynamoDB
        #=====================

        # Get the service resource.
        dynamodb = boto3.resource('dynamodb')

        # Instantiate a table resource object without actually
        # creating a DynamoDB table. Note that the attributes of this table
        # are lazy-loaded: a request is not made nor are the attribute
        # values populated until the attributes
        # on the table resource are accessed or its load() method is called.
        table = dynamodb.Table('faucovidstream_twitter_with_sentiment')

        # Print out some data about the table.
        # This will cause a request to be made to DynamoDB and its attribute
        # values will be set based on the response.
        print(table.creation_date_time)

        dynamodb.put_item(
            Item=tweet
        )
