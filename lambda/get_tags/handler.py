import boto3
from boto3.dynamodb.conditions import Key
import json
from datetime import datetime

dynamo_resource = boto3.resource('dynamodb', region_name='us-east-1')
tags_table = dynamo_resource.Table('Tags')

def get_month_year():
    now = datetime.now()
    return f'{now.year:04d}/{now.month:02d}'
    
def lambda_handler(event, context):
  
        response = tags_table.query(IndexName='score-index',
                            KeyConditionExpression=Key('upload_date').eq(get_month_year()),
                            ScanIndexForward=False, 
                            Limit=50
                    )
        
        tags=[]
        
        for item in response['Items']:
            tags.append({'tag':item['category'], 'score':str(item['score'])})
            
        return {
            "statusCode": 200,
            "body": json.dumps(tags),
            "headers": { 'Access-Control-Allow-Origin': '*'},
    }