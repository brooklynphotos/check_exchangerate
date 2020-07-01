import json

def get_user(username):
  return {
    "username": username
  }

def get_users() -> list:
  return [
    {
      "username": "hi@bye.com"
    }
  ]

user_handlers = {
  "GET": get_user
}

def lambda_handler(event, context):
  body = user_handlers[event["method"].upper()](event["username"]) if "username" in event else get_users()
  return {
    "status": 200,
    "body": body
  }