import json
import boto3
import urllib.request
from datetime import datetime, timezone

s3 = boto3.client('s3')

API_KEY = "f40feac5a85ab481b4eeb7f2222997ca"
CITY = "Kochi"

def lambda_handler(event, context):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
        
        with urllib.request.urlopen(url, timeout=10) as response:
            weather_data = json.loads(response.read().decode())

        item = {
            "city": weather_data["name"],
            "temperature": weather_data["main"]["temp"],   # ✅ FIXED
            "humidity": weather_data["main"]["humidity"],
            "weather": weather_data["weather"][0]["description"],
            "time": datetime.now(timezone.utc).isoformat() # ✅ FIXED
        }

        s3.put_object(
            Bucket='weather-data-121',
            Key=f"weather/{context.aws_request_id}.json",
            Body=json.dumps(item)
        )

        print("Saved to S3:", item)
        return {"status": "success", "data": item}

    except Exception as e:
        print("ERROR:", str(e))
        return {"status": "error", "message": str(e)}