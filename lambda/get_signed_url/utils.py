import decimal
import json
from datetime import datetime


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 == 0:
                return int(o)
            else:
                return round(float(o), 12)
        return super(DecimalEncoder, self).default(o)


def get_month_year():
    now = datetime.now()
    return f'{now.year:04d}/{now.month:02d}'


def jsonify(obj, statusCode=200):
    return {
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'statusCode': statusCode,
        'body': json.dumps(obj, cls=DecimalEncoder)
    }
