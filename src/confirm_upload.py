import json
import boto3
import uuid
from datetime import datetime
import os

dynamodb = boto3.resource('dynamodb')
token_table = dynamodb.Table('SecureUploadTokens')
log_table = dynamodb.Table('SecureUploadLogs')

S3_BUCKET = os.environ.get('S3_BUCKET')

def lambda_handler(event, context):
    try:
        token = event['pathParameters']['token']
        body = json.loads(event['body'])

        filename = body.get('filename')
        content_type = body.get('content_type')

        if not filename or not content_type:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing filename or content_type'})
            }

        # Validate token
        res = token_table.get_item(Key={'token': token})
        if 'Item' not in res:
            return {'statusCode': 403, 'body': json.dumps({'error': 'Invalid token'})}

        client_id = res['Item']['client_id']
        file_url = f"s3://{S3_BUCKET}/uploads/{filename}"

        # Save metadata
        log_table.put_item(Item={
            'id': uuid.uuid4().hex,
            'token': token,
            'client_id': client_id,
            'filename': filename,
            'mimetype': content_type,
            'file_url': file_url,
            'timestamp': datetime.utcnow().isoformat()
        })

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Upload confirmed'})
        }

    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}
