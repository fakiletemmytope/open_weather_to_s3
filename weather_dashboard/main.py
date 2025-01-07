#!/bin/env python3
from .function import (
    get_weather_details,
    bucket_exist,
    create_bucket,
    save_to_s3,
)

import os
import dotenv

dotenv.load_dotenv()


def retrieve_and_save():
    bucket_name = os.getenv("BUCKETNAME")
    folder = os.getenv("FOLDERNAME")
    url = os.getenv("APIURL")
    key = os.getenv("APIKEY")
    region = os.getenv("REGION")

    cities = ["Abuja", "Cairo", "Ankara"]

    if not bucket_exist(bucket_name):
        create_bucket(bucket_name, region)

    for city in cities:
        detail = get_weather_details(city, url, key)
        if detail is None:
            print(f"weather details for {city} not available")
        else:
            if bucket_exist(bucket_name):
                if save_to_s3(detail, folder, city, bucket_name):
                    print("Data saved successfully")
                else:
                    print("Data not saved")


if __name__ == "__main__":
    retrieve_and_save()
