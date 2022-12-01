import boto3
import os
import random
import json
from urllib.parse import unquote_plus
from datetime import datetime

S3_BUCKET = os.environ['S3_IMAGES_BUCKET']
s3_client = boto3.client('s3', region_name='us-east-1')

def get_month_year():
    now = datetime.now()
    return f'{now.year:04d}/{now.month:02d}'

def lambda_handler(event, context):
  
    category = unquote_plus(event['pathParameters']['category'])
    
    prefix = get_month_year()+'/'+category+'/' 
    
    response = s3_client.list_objects_v2(
        Bucket = S3_BUCKET,
    )
    
    images_list = []
    
    for item in response.get('Contents', []):
        image = item['Key']
    
        if image.startswith(prefix):
            images_list.append(image)
    
    if not images_list:
        exception = "There is no such category in the saved images"
        return{
            "statusCode": 200,
            "body": json.dumps(exception),
            }
        
    key = random.choice(images_list)

    url_imagen = s3_client.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': S3_BUCKET,
            'Key': key
        }
    )
    
    response = {"url": url_imagen}
   
    return {
        "statusCode": 200,
        "body": json.dumps(response),
        "headers": { 'Access-Control-Allow-Origin': '*'}
     }