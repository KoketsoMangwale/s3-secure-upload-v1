import json
import uuid
from datetime import datetime, timedelta
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SecureUploadTokens')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        client_id = body.get('client_id')

        if not client_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'client_id is required'})
            }

        token = uuid.uuid4().hex[:8].upper()
        now = datetime.utcnow()
        expires_at = now + timedelta(days=3)

        table.put_item(Item={
            'token': token,
            'client_id': client_id,
            'created_at': now.isoformat(),
            'expires_at': expires_at.isoformat()
        })

        return {
            'statusCode': 200,
            'body': json.dumps({
                'token': token,
                'upload_url': f'/upload-url/{token}',
                'expires_at': expires_at.isoformat()
            })
        }

    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}
