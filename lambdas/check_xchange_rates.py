import urllib.request, json 
import boto3
import datetime
from decimal import Decimal

session = boto3.Session(profile_name="dbadmin")
appName = "exchange_rate"
dynamodb = session.resource('dynamodb')
def get_rate(exchange_url):
  with urllib.request.urlopen(exchange_url) as url:
    data = json.loads(url.read().decode())
    return data['rates']['CHF']

def write_rate(rate):
  previousId = get_last_id()
  table = dynamodb.Table('exchange_rates')
  this_id = previousId + 1
  timestamp = int(datetime.datetime.now().timestamp())
  table.put_item(Item={
    "id": this_id,
    "rate": Decimal(str(rate)),
    "timestamp": timestamp,
    "previousId": previousId
  })
  write_last_id(this_id)
  return this_id, rate

def write_last_id(new_id):
  table = dynamodb.Table('constants')
  return table.update_item(
    Key={
      'appName': appName
    },
    UpdateExpression='set appValue=:v',
    ExpressionAttributeValues={
      ':v': new_id
    }
  )

def get_last_id():
  table = dynamodb.Table('constants')
  response = table.get_item(Key={"appName":appName})
  return response["Item"]["appValue"] if "Item" in response else 0

def main():
  # print(get_last_id().value)
  import sys
  id, r = write_rate(get_rate(sys.argv[1]))
  print("id:", id, "rate:", r)

if __name__=='__main__':
  main()