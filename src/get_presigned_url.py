import json
import uuid
import boto3
import os

dynamodb = boto3.resource('dynamodb')
token_table = dynamodb.Table('SecureUploadTokens')

s3 = boto3.client('s3')
S3_BUCKET = os.environ.get('S3_BUCKET')

def lambda_handler(event, context):
    try:
        token = event['pathParameters']['token']
        query_params = event.get('queryStringParameters') or {}
        ext = query_params.get('ext', 'bin')
        content_type = query_params.get('contentType', 'application/octet-stream')

        # Validate token
        res = token_table.get_item(Key={'token': token})
        if 'Item' not in res:
            return {
                'statusCode': 403,
                'body': json.dumps({'error': 'Invalid or expired token'})
            }

        file_id = uuid.uuid4().hex
        filename = f"{file_id}.{ext}"
        key = f"uploads/{filename}"

        presigned_url = s3.generate_presigned_url(
            ClientMethod='put_object',
            Params={
                'Bucket': S3_BUCKET,
                'Key': key,
                'ContentType': content_type,
                'ACL': 'private',
                'ServerSideEncryption': 'AES256'
            },
            ExpiresIn=300  # 5 minutes
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'upload_url': presigned_url,
                'filename': filename,
                'key': key,
                'content_type': content_type
            })
        }

    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}
