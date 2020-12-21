# =====================
# ==step to do
# =====================

# --------deploy cmd
#  aws apigateway create-deployment --rest-api-id 77ue66yk77 --region us-east-2 --stage-name dev
import json
import time
from pprint import pprint

import boto3
import requests

# =====================
# ==set up
# =====================
# --------aws setup
apigateway = boto3.client('apigateway')
apis = apigateway.get_rest_apis()
api_id = apis['items'][0]['id']  # 77ue66yk77

apigateway.get_gateway_responses(restApiId=api_id)

apigateway.get_resources(restApiId=api_id)

# note: "https://77ue66yk77.execute-api.us-east-2.amazonaws.com/dev"
region = 'us-east-2'
stage = 'dev'

# --------api gateway path and params setup

stream_path = '/streams'
# stream_name_path =  '/faucovidstreamsentiment'
stream_name_path = '/faucovidstream_input'
sharditerator_path = '/sharditerator'
record_path = '/record'
records_path = '/records'
sharditerator_param = '?shard-id=shardId-000000000000'
sharditerator_api = \
    stream_path + stream_name_path + sharditerator_path + sharditerator_param
records_api = \
    stream_path + stream_name_path + records_path
base_api = f"https://{api_id}.execute-api.{region}.amazonaws.com/{stage}"

# =====================
# ==get shardID
# =====================


requests.get('https://77ue66yk77.execute-api.us-east-2.amazonaws.com/dev'
             '/streams/faucovidstreamsentiment/records',
             headers={"Shard-Iterator":
                          "AAAAAAAAAAEa/ca/mBIt4GzihIIWQT4CyfJsHvIlU780cmHiP4vRuXUg63ST3kf1Bo+a2qH2Kj2wXtYk4axDua/63o2D7WLso7DcmB3ietxHR0Y/6fg6i5dxrukXOlGdlgH3JzTeG9+Ir36WAi95i/6nbvEiQgESCpE3y5HJKOn9gs88j4wio+SHVbQ893KkKGHvIa/GpT4Of8X5/1jzg/nU5O2lDSDQ3j/Z1mRrr7Gc7A3nz7gfWQ=="
                      }
             )

full_api = base_api + sharditerator_api
my_shard_iterator = json.loads(requests.get(full_api).text)['ShardIterator']

# =====================
# ==request kinesis stream data from shardID
# =====================

full_api = base_api + records_api
headers = {'Shard-Iterator': my_shard_iterator}
record_response = requests.get(full_api, headers=headers)

print('-----------------\n\n\n\n')

next_shard_iterator = 'NextShardIterator'

while next_shard_iterator in json.loads(record_response.text):
    record_response = requests.get(full_api, headers=headers)
    headers = \
        {'Shard-Iterator':
             json.loads(record_response.text)[next_shard_iterator]
         }

    # pprint(f"text: {record_response.text}")
    # pprint(record_response.text)
    pprint(record_response.content)
    print('==============\n\n')

    time.sleep(1)
