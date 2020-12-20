import boto3
import json
import time
import sys
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# Variables that contains the user credentials to access Twitter API
consumer_key = 'M2dcKnRZGqBWTrPBXeefFHHjZ'
consumer_secret = 'ktTB1WAJNsZBnKTddPqHMpzczj7ehZigXtN77YIFUdSlZ1EW7v'
access_token = '1140239819127365632-gnWnwYZmb6IxKCzOBdXcTWBEc0v1GU'
access_token_secret = '25wy0DsyD7yfzdKkRdvKTY3ILHbR4fF8t7vnVfRvkknym'

class TweetStreamListener(StreamListener):
    print('runing...')

    # on success
    def on_data(self, data):
        print('streaming...')
        tweet = json.loads(data)
        try:
            if 'text' in tweet.keys():
                # print (tweet['text'])
                # message = str(tweet)+',\n'
                message = json.dumps(tweet)
                message = message + ",\n"
                print(message)

                timestamp_ms = tweet['timestamp_ms']
                # print(timestamp_ms)
                # print(type(timestamp_ms))

                kinesis_input_data = bytes(message, 'utf-8')

                response = kinesis_client.put_record(
                    StreamName=stream_name,
                    Data=kinesis_input_data,
                    PartitionKey=timestamp_ms,
                )
                print(response)

                # kinesis_client.put_record(
                #     DeliveryStreamName=stream_name,
                #     Record={
                #         'Data': message
                #     }
                # )

        except (AttributeError, Exception) as e:
            print(e)

        print('--------')
        print('work fine')
        return True

    # on failure
    def on_error(self, status):
        print(status)


stream_name = 'faucovidstream_input'  # fill the name of Kinesis data stream you created
# stream_name = 'transforminputtoS3'  # fill the name of Kinesis data stream you created

if __name__ == '__main__':

    # # # create kinesis client connection
    # # kinesis_client = boto3.client('firehose',
    # #                               region_name='us-east-2',  # enter the region
    # #                               aws_access_key_id='AKIAIET5BC65M6AQN23Q',
    # #                               # fill your AWS access key id
    # #                               aws_secret_access_key='sC4FP3Q61k43Lk9tks4TRyidSCk3H5PtdFbvEh7q')  # fill you aws secret access key
    #
    # # create kinesis client connection
    # kinesis_client = boto3.client('kinesis',
    #                               region_name='us-east-2',  # enter the region
    #                               aws_access_key_id='AKIAIET5BC65M6AQN23Q',
    #                               # fill your AWS access key id
    #                               aws_secret_access_key='sC4FP3Q61k43Lk9tks4TRyidSCk3H5PtdFbvEh7q')  # fill you aws secret access key
    #
    # # create instance of the tweepy tweet stream listener
    # listener = TweetStreamListener()
    # # set twitter keys/tokens
    # auth = OAuthHandler(consumer_key, consumer_secret)
    # auth.set_access_token(access_token, access_token_secret)
    # # create instance of the tweepy stream
    # stream = Stream(auth, listener)
    # # search twitter for tags or keywords from cli parameters
    # query = sys.argv[1:]  # list of CLI arguments
    # query_fname = ' '.join(query)  # string
    # stream.filter(track=query)

    sleep_time = 3600

    while True:
        try:
            # # create kinesis client connection
            # kinesis_client = boto3.client('firehose',
            #                               region_name='us-east-2',  # enter the region
            #                               aws_access_key_id='AKIAIET5BC65M6AQN23Q',
            #                               # fill your AWS access key id
            #                               aws_secret_access_key='sC4FP3Q61k43Lk9tks4TRyidSCk3H5PtdFbvEh7q')  # fill you aws secret access key

            # create kinesis client connection
            kinesis_client = boto3.client('kinesis',
                                          region_name='us-east-2',  # enter the region
                                          aws_access_key_id='AKIAIET5BC65M6AQN23Q',
                                          # fill your AWS access key id
                                          aws_secret_access_key='sC4FP3Q61k43Lk9tks4TRyidSCk3H5PtdFbvEh7q')  # fill you aws secret access key

            # create instance of the tweepy tweet stream listener
            listener = TweetStreamListener()
            # set twitter keys/tokens
            auth = OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            # create instance of the tweepy stream
            stream = Stream(auth, listener)
            # search twitter for tags or keywords from cli parameters
            query = sys.argv[1:]  # list of CLI arguments
            query_fname = ' '.join(query)  # string
            stream.filter(track=query)

        except Exception as e:

            print(f'the following exception is foud:{e}')
            time.sleep(sleep_time)
            print(f'sleeping for {sleep_time} section')
