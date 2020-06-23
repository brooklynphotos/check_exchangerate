mock_data = [
    {
        'id': 1,
        'previousId': 0,
        'timestamp': 'June 12, 2020 14:40:23.123',
        'timestamp': 'June 22, 2020 14:40:23.123'
    },
    {
        'id': 2,
        'previousId': 1,
        'timestamp': 'June 12, 2020 14:40:23.123',
        'timestamp': 'June 22, 2020 14:40:23.123'
    }
]


def lambda_handler(event, context):
    if "id" in event:
        id = event['id']
        return {
            'statusCode': 200,
            'data': next(d for d in mock_data if d["id"] == id)
        }
    return {
        'statusCode': 200,
        'data': mock_data
    }
