import json
import urllib.request
import boto3
from datetime import datetime
from decimal import Decimal
import uuid

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('weather_data')

def lambda_handler(event, context):
    try:
        print("Lambda started")

        url = f"https://api.openweathermap.org/data/2.5/weather?lat=9.9312&lon=76.2673&appid=f40feac5a85ab481b4eeb7f2222997ca&units=metric"
        print("Calling Weather API...")
        response = urllib.request.urlopen(url, timeout=10)
        data = json.loads(response.read())
        print("API response received:", data["name"])

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        result = {
            "city": data["name"],
            "temperature": float(data["main"]["temp"]),
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["main"],
            "time": str(datetime.now())
        }

        # Save to S3
        try:
            s3.put_object(
                Bucket="weather-data-121",
                Key=f"weather_{timestamp}.json",
                Body=json.dumps(result)
            )
            print("S3 upload success:", f"weather_{timestamp}.json")
        except Exception as s3_error:
            print("S3 ERROR:", str(s3_error))

        # Save to DynamoDB with id (partition key) + timestamp (sort key)
        try:
            table.put_item(Item={
                "id": str(uuid.uuid4()),           # ✅ partition key
                "timestamp": timestamp,             # ✅ sort key
                "city": data["name"],
                "temperature": Decimal(str(data["main"]["temp"])),
                "humidity": Decimal(str(data["main"]["humidity"])),
                "weather": data["weather"][0]["main"],
                "time": str(datetime.now())
            })
            print("DynamoDB insert success")
        except Exception as db_error:
            print("DynamoDB ERROR:", str(db_error))

        return {
            "statusCode": 200,
            "body": json.dumps(result)
        }

    except Exception as e:
        print("GENERAL ERROR:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }