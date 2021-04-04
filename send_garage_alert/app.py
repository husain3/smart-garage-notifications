import json
import boto3
import os


def lambda_handler(event, context):    
    ses_client = boto3.client("ses", region_name="us-west-2")
    CHARSET = "UTF-8"

    sns_client = boto3.client('sns')

    if(event['queryStringParameters'] is None):
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": json.dumps({"status": "Bad Request Error", "message": "Malformed client request. No params specified. Please provide one door_status, and one open_duration (if applicable) in params"}),
            }),
        }

    try:
        sns_client = boto3.client('sns')

        if('door_status' in event['queryStringParameters'].keys() and event['queryStringParameters']['door_status'] == 'opened'):
            response = ses_client.send_email(
                Destination={
                    "ToAddresses": [
                        os.environ["SESEmail"],
                    ],
                },
                Message={
                    "Body": {
                        "Text": {
                            "Charset": CHARSET,
                            "Data": "Garage door has been opened",
                        }
                    },
                    "Subject": {
                        "Charset": CHARSET,
                        "Data": "GARAGE DOOR OPENED",
                    },
                },
                Source=os.environ["SESEmail"],
            )
        elif('door_status' in event['queryStringParameters'].keys() and event['queryStringParameters']['door_status'] == 'closed'):
            response = ses_client.send_email(
                Destination={
                    "ToAddresses": [
                        os.environ["SESEmail"],
                    ],
                },
                Message={
                    "Body": {
                        "Text": {
                            "Charset": CHARSET,
                            "Data": "Garage door has been closed",
                        }
                    },
                    "Subject": {
                        "Charset": CHARSET,
                        "Data": "GARAGE DOOR CLOSED",
                    },
                },
                Source=os.environ["SESEmail"],
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
                }),
            }

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Message sent successfully",
            }),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": json.dumps({"status": "Lambda Error", "message": f"Lambda error message - {str(e)}"}),
            }),
        }
