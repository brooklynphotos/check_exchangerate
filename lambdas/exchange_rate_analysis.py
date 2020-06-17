import boto3
import json
from boto3.dynamodb.conditions import Key, Attr

session = boto3.Session(profile_name="dbadmin")
dynamodb = session.resource('dynamodb')
table = dynamodb.Table('exchange_rates')

def lambda_handler(event, context):
  print("event:",event)
  msg = event["Records"][0]["Sns"]["Message"]
  msg = msg.replace('\n','')
  print("message:", msg)
  data = json.loads(msg)
  latest_id = data["responsePayload"]["id"]
  difference = find_difference(latest_id)
  difference = "{:.3%}".format(difference) if difference else None
  print("difference", difference)
  return {
    'statusCode': 200,
    'difference': difference
  }

def find_difference(id):
  if id==0:
    return None
  item = find_by_id(id)
  if not item:
    return None
  prev_id = item['previousId']
  if prev_id==0:
    return None
  prev_item = find_by_id(prev_id)
  if not prev_item:
    return None
  return (item['rate'] - prev_item['rate'])/prev_item['rate']

def find_by_id(id):
  res = table.query(KeyConditionExpression=Key('id').eq(id))
  items = res["Items"]
  if not items:
    return None
  return items[0]


if __name__ == '__main__':
    event = {'Records': [{'EventSource': 'aws:sns', 'EventVersion': '1.0', 'EventSubscriptionArn': 'arn:aws:sns:eu-west-1:575798484766:checkExchangeRate:7d4b3c50-4e32-431d-b2ab-527b3bfb69df', 'Sns': {'Type': 'Notification', 'MessageId': '24ba716c-411c-5c78-870f-260ff9823053', 'TopicArn': 'arn:aws:sns:eu-west-1:575798484766:checkExchangeRate', 'Subject': None, 'Message': '{"version":"1.0","timestamp":"2020-06-17T06:21:18.700Z","requestContext":{"requestId":"6ee29b0a-9d7d-405f-96cb-a190518aea23","functionArn":"arn:aws:lambda:eu-west-1:575798484766:function:checkExchangeRate:$LATEST","condition":"Success","approximateInvokeCount":1},"requestPayload":{"exchange_url": "http://gzmockendpoints.s3-website-eu-west-1.amazonaws.com/exchange_rate.json"},"responseContext":{"statusCode":200,"executedVersion":"$LATEST"},"responsePayload":{"statusCode": 200, "rate": 0.961715, "id": 31}}','Timestamp': '2020-06-17T06:21:18.717Z', 'SignatureVersion': '1', 'Signature': 'XrtUjVhmZwSUCRF7kYBQvoV8IpkWp5lcktDGFLya7dzuUb9fB01hRJkSLMHPMeNEgkkZ8Ymwj18CejfcJPSQcuipkwr4CpDQ3vgRPjbLYarP6Jc6p55zvJkRlwi8eJ/Vf1IePEAeluXAKxF/qgN0Nk6x3sFqziAuAXWbW/xcRFw8UfxhpKRQiUGA6bYv/Wz+tmw1QfL2Aw4z+3iBs+W8rFFwrybS7pRf80Mj2LwWwiUxZjKm4gM1r4wKeLUIVxSHugordTdsweSkTLunJor0hRH98auBFODR2ih+cFSdg11MvtCi76rUvMiS/nGNf5cz0YF5VwM2vw0T1DdJgirlmw==', 'SigningCertUrl': 'https://sns.eu-west-1.amazonaws.com/SimpleNotificationService-a86cb10b4e1f29c941702d737128f7b6.pem', 'UnsubscribeUrl': 'https://sns.eu-west-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:eu-west-1:575798484766:checkExchangeRate:7d4b3c50-4e32-431d-b2ab-527b3bfb69df', 'MessageAttributes': {}}}]}
    print(lambda_handler(event, None))
