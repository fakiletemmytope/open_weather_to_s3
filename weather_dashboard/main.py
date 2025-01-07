#!/bin/env python3
from function import (
    get_weather_details,
    bucket_exist,
    create_bucket,
    save_to_s3,
)

import os
import dotenv
import sys

dotenv.load_dotenv()


def retrieve_and_save(citiies=[]):
    bucket_name = os.getenv("BUCKETNAME")
    folder = os.getenv("FOLDERNAME")
    url = os.getenv("APIURL")
    key = os.getenv("APIKEY")
    region = os.getenv("REGION")
    # cities = ["accra", "tunis", "algiers"]

    if not bucket_exist(bucket_name):
        create_bucket(bucket_name, region)

    for city in cities:
        detail = get_weather_details(city, url, key)
        if detail is None:
            print(f"weather details for {city} not available")
        else:
            if save_to_s3(detail, folder, city, bucket_name):
                print(f"Weather details for {city} successfully retrieved and saved")
            else:
                print("Data not saved")


if __name__ == "__main__":
    while len(sys.argv) == 1:
        print(
            "The cities are not included, run the command again including the cities."
        )
    cities = []
    for i in range(1, len(sys.argv)):
        cities.append(sys.argv[i])

    retrieve_and_save(citiies=cities)
