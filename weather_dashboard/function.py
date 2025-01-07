import datetime
import boto3
import requests
import json


# Create an S3 client instead of a resource
s3_client = boto3.client('s3')


def bucket_exist(bucket_name):
    bucket_names = [
        bucket['Name'] for bucket in s3_client.list_buckets()['Buckets']
    ] if s3_client.list_buckets() else []

    return bucket_name in bucket_names


def create_bucket(bucket_name, bucket_region):
    try:
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': bucket_region
            }
        )
        print(f'Bucket {bucket_name} created successfully.')
    except Exception as e:
        print(f'Error: {e}')


def get_weather_details(city, base_url, api_key):
    """Fetch weather data from OpenWeather API"""
    params = {
        "q": city,
        "appid": api_key,
        "units": "imperial",
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None


def save_to_s3(data, path, city, bucket_name):
    json_data = json.dumps(data)
    try:
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        s3_client.put_object(
            Bucket=bucket_name,
            Key=f'{path}/{city}-{timestamp}.json',
            Body=json_data,
            ContentType='application/json',
        )
        return True
    except Exception as e:
        print("Error:", str(e))
        return False
