import json
import boto3
import os


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
    sns_client = boto3.client('sns')

    if(event['queryStringParameters'] is None):
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": json.dumps({"status": "Bad Request Error", "message": "Malformed client request. No params specified. Please provide one door_status, and one open_duration (if applicable) in params"}),
                # "location": ip.text.replace("\n", "")
            }),
        }

    try:
        sns_client = boto3.client('sns')

        if('door_status' in event['queryStringParameters'].keys() and event['queryStringParameters']['door_status'] == 'opened'):
            response = sns_client.publish(
                TopicArn=os.environ["SNSArn"],
                Message='Garage door is now open',
                Subject='Door Activity'
            )
        elif('door_status' in event['queryStringParameters'].keys() and event['queryStringParameters']['door_status'] == 'closed'):
            response = sns_client.publish(
                TopicArn=os.environ["SNSArn"],
                Message='Garage door is now closed',
                Subject='Door Activity'
            )
        elif(event['queryStringParameters']['door_status'] == 'still_open' and ('open_duration' in event['queryStringParameters'].keys() and event['queryStringParameters']['open_duration'].isnumeric())):
            response = sns_client.publish(
                TopicArn=os.environ["SNSArn"],
                Message=f"Garage door has been open for {event['queryStringParameters']['open_duration']} minutes",
                Subject='Door Activity'
            )
        else:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": json.dumps({"status": "Bad Request Error", "message": "Malformed client request. Please provide one door_status, and one open_duration (if applicable) in params"}),
                    # "location": ip.text.replace("\n", "")
                }),
            }

        return {
            "statusCode": 200,
            "body": json.dumps({
                # "message": "SNS message published successfully",
                "message": "SNS message published successfully",
                # "location": ip.text.replace("\n", "")
            }),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": json.dumps({"status": "Lambda Error", "message": f"Lambda error message - {str(e)}"}),
            }),
        }
