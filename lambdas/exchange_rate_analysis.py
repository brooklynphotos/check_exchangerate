import boto3
import json
from boto3.dynamodb.conditions import Key, Attr

session = boto3.Session(profile_name="dbadmin")
dynamodb = session.resource('dynamodb')
table = dynamodb.Table('exchange_rates')

def lambda_handler(event, context):
  msg = event["Records"][0]["Sns"]["Message"]
  msg = msg.replace('\n','')
  print(msg)
  data = json.loads(msg)
  latest_id = data["id"]
  difference = find_difference(latest_id)
  difference = float(difference) if difference else None
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
  return item['rate'] - prev_item['rate']

def find_by_id(id):
  res = table.query(KeyConditionExpression=Key('id').eq(id))
  items = res["Items"]
  if not items:
    return None
  return items[0]

if __name__=='__main__':
  event = {'Records': [{'EventSource': 'aws:sns', 'EventVersion': '1.0', 'EventSubscriptionArn': 'arn:aws:sns:eu-west-1:575798484766:checkExchangeRate:7d4b3c50-4e32-431d-b2ab-527b3bfb69df', 'Sns': {'Type': 'Notification', 'MessageId': '7c429aa0-6cad-535a-bcfb-cdc3491c2fe6', 'TopicArn': 'arn:aws:sns:eu-west-1:575798484766:checkExchangeRate', 'Subject': None, 'Message': '{\n        "statusCode": 200,\n        "rate": 0.948138,\n        "id": 10\n    }', 'Timestamp': '2020-06-16T19:54:25.330Z', 'SignatureVersion': '1', 'Signature': 'fBPc5e+pzMgGIQZqNk5XTHw1etdmy6NC1fO17YL4/c/Goab84UQdxWDPSdPUGFOfjZVku02hzbJDfcesqJLxgYOVJJRu78MhkZDzPrXYCYeNlLwi5KaFybaXavwAJpn8kKwGCHHkF/XTe4pFvjeixDw2wASx5y2MWIHc8mPmlnSy+w32DjuIQdZkX12dbOTanAMMluxNrK4qsK39VXxY3pvdtHBnX2zKgwQYZ52AxpbjrKROBI+hgC6+5SrfxOkwixrj28sVEBfLC9xXvT8hI9QD1QriytS+OvP5B4eUSlV7aNhX1Q7qX4+CHpqop4MO7JMgNAHIoAQtD93n6ZuxrQ==', 'SigningCertUrl': 'https://sns.eu-west-1.amazonaws.com/SimpleNotificationService-a86cb10b4e1f29c941702d737128f7b6.pem', 'UnsubscribeUrl': 'https://sns.eu-west-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:eu-west-1:575798484766:checkExchangeRate:7d4b3c50-4e32-431d-b2ab-527b3bfb69df', 'MessageAttributes': {}}}]}
  print(lambda_handler(event, None))