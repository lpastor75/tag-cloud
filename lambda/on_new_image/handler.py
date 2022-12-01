import boto3
import botocore

from datetime import datetime
from decimal import Decimal

session = boto3.session.Session(region_name='us-east-1')

rekognition_client = session.client("rekognition")
s3_client = session.client("s3")
dynamo_resource = boto3.resource('dynamodb', region_name='us-east-1')
tags_table = dynamo_resource.Table('Tags')

def move_object(orig_key, dst_key):
    copy_source = {
        'Bucket': 'lpastor.cognitive.aws.input',
        'Key': orig_key
    }
    s3_client.copy(CopySource=copy_source, Bucket='lpastor.cognitive.aws.images', Key=dst_key)
    s3_client.delete_object(Bucket='lpastor.cognitive.aws.input', Key=orig_key)

def get_month_year():
    now = datetime.now()
    return f'{now.year:04d}/{now.month:02d}'

def get_image_label(file_key):
   
    return rekognition_client.detect_labels(
    Image={
        "S3Object": {
            "Bucket": 'lpastor.cognitive.aws.input', 
            "Name": file_key
        }
    },
    MaxLabels=1,
    )
     
def lambda_handler(event, context):
    
    file_key = event['Records'][0]['s3']['object']['key']
    rekognition = get_image_label(file_key)
    
    category = rekognition['Labels'][0]['Name']
    score = Decimal(str(round(rekognition['Labels'][0]['Confidence'],1)))
        
    new_key = get_month_year()+'/'+category+'/'+file_key
    move_object(file_key, new_key)
    
    try:
        tags_table.update_item(
            Key={'upload_date': get_month_year(),'category': category},
            UpdateExpression="ADD #counter :increment",
            ExpressionAttributeNames={'#counter': 'score'},
            ExpressionAttributeValues={':increment':score},
            ReturnValues="UPDATED_NEW"           
        ) 

    except botocore.exceptions.ClientError as e:
        
        if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
            raise