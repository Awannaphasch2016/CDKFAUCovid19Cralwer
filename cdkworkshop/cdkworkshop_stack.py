from aws_cdk import aws_apigateway as _apigateway
from aws_cdk import aws_dynamodb as _dynamodb
from aws_cdk import aws_kinesis as _kinesis
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_s3 as _s3
from aws_cdk import aws_kinesisfirehose as _firehose
from aws_cdk import core


class CdkworkshopStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) \
            -> None:
        super().__init__(scope, construct_id, **kwargs)

        my_table = \
            _dynamodb.Table(
                self,
                id='dynamoTable',
                table_name='cdk_faucovidstream_twitter_with_sentiment',
                partition_key=_dynamodb.Attribute(
                    name='platform',
                    type=_dynamodb.AttributeType.STRING,
                )
            )

        my_bucket = \
            _s3.Bucket(
                self,
                id='s3bucket',
                bucket_name='cdkfaucovidstream',
            )

        my_stream = \
            _kinesis.Stream(
                self,
                id='kinesisStream',
                stream_name='cdk_faucovidstream_input',
            )

        # my_firehose = \
        #     _firehose.CfnDeliveryStream(
        #         self,
        #         id='kinesisFirehose',
        #         delivery_stream_name='cdk_faucovidstream_input',
        #     )

        my_lambda = \
            _lambda.Function(
                self,
                id='lambdaFunction',
                runtime=_lambda.Runtime.PYTHON_3_8,
                handler='hello.handler',
                code=_lambda.Code.asset('cdk_faucovidstream')
            )

        my_api = \
            _apigateway.RestApi(
                self,
                id = 'api',
                rest_api_name='cdk_kinesisproxy',
            )

        music = my_api.root.add_resource('dynamodb')
        music.add_method('GET')
