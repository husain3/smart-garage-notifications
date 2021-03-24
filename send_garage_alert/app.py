import json
import boto3
import os
# import requests

def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e
    sns_client = boto3.client('sns')

    print("===========================")
    print("===========================")
    print(event)
    print("===========================")
    print("===========================")
    print(os.environ["SNSArn"])
    print("===========================")
    print("===========================")

    # if():

    # elif():

    # elif():

    # else:

    try:
        sns_client = boto3.client('sns')

        response = sns_client.publish(
            TopicArn=os.environ["SNSArn"],
            Message='Turkmenistan! Turkmenistan!',
            Subject='From the Dear Leader'
        )
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": f"SNS Arn =  {event}",
                # "location": ip.text.replace("\n", "")
            }),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": f"SNS Arn =  {response}",
                # "location": ip.text.replace("\n", "")
            }),
        }
