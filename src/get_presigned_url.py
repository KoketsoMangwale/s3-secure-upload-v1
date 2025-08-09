import json
import uuid
import boto3
import os
import mimetypes
from datetime import datetime

# AWS Resources
dynamodb = boto3.resource('dynamodb')
token_table = dynamodb.Table('SecureUploadTokens')

s3 = boto3.client(
    's3',
    region_name=os.environ.get('AWS_REGION', 'us-west-2'),
    endpoint_url=os.environ.get('S3_ENDPOINT', 'https://s3.us-west-2.amazonaws.com')
)
S3_BUCKET = os.environ.get('S3_BUCKET')

# Allowed file types (from env or defaults)
ALLOWED_EXTENSIONS = set(os.environ.get('ALLOWED_EXTENSIONS', 'pdf,png,jpg,jpeg,txt').split(','))
ALLOWED_CONTENT_TYPES = set(os.environ.get(
    'ALLOWED_CONTENT_TYPES',
    'application/pdf,image/png,image/jpeg,text/plain'
).split(','))

def lambda_handler(event, context):
    try:
        token = event['pathParameters']['token']
        query_params = event.get('queryStringParameters') or {}
        ext = query_params.get('ext')
        content_type = query_params.get('contentType')

        # Validate token
        res = token_table.get_item(Key={'token': token})
        if 'Item' not in res:
            return {
                'statusCode': 403,
                'body': json.dumps({'error': 'Invalid or expired token'})
            }

        # If extension not provided, derive from content type
        if not ext and content_type:
            guessed_ext = mimetypes.guess_extension(content_type)
            ext = guessed_ext.lstrip('.') if guessed_ext else 'bin'

        # If content type not provided, derive from extension
        if not content_type and ext:
            guessed_type, _ = mimetypes.guess_type(f"file.{ext}")
            content_type = guessed_type or 'application/octet-stream'

        # Defaults if both missing
        if not ext:
            ext = 'bin'
        if not content_type:
            content_type = 'application/octet-stream'

        # Whitelist check
        if ext.lower() not in ALLOWED_EXTENSIONS or content_type not in ALLOWED_CONTENT_TYPES:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Unsupported file type',
                    'allowed_extensions': list(ALLOWED_EXTENSIONS),
                    'allowed_content_types': list(ALLOWED_CONTENT_TYPES)
                })
            }

        # Create file name and S3 key
        file_id = uuid.uuid4().hex
        filename = f"{file_id}.{ext}"
        key = f"uploads/{filename}"

        # Generate presigned URL
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

        # Success response
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'upload_url': presigned_url,
                'filename': filename,
                'key': key,
                'content_type': content_type,
                'expires_in_seconds': 300,
                'timestamp': datetime.utcnow().isoformat()
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
