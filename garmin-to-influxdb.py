import csv
from datetime import datetime, timedelta
from influxdb_client import InfluxDBClient, Point, WriteOptions, WritePrecision
from datetime import datetime, timedelta
from garminconnect import Garmin

# Define your Garmin Connect credentials
USERNAME = '{GARMIN_USER_NAME}'  # Replace with your Garmin Connect username (email)
PASSWORD = '{GARMIN_PASSWORD}'  # Replace with your Garmin Connect password
# InfluxDB configuration
INFLUXDB_URL = "{INFLUXDB_URL}"  # URL of your InfluxDB instance default: http://localhost:8086
INFLUXDB_TOKEN = "{INFLUXDB_TOKEN}"  # Replace with your InfluxDB token
INFLUXDB_ORG = "{INFLUXDB_ORG}"  # Replace with your InfluxDB organization name
INFLUXDB_BUCKET = "{INFLUXDB_BUCKET}"  # Replace with your InfluxDB bucket name

def authenticate_garmin(username, password):
    """Authenticate to Garmin Connect and return the Garmin instance."""
    try:
        client = Garmin(username, password)
        client.login()
        print("Authentication successful.")
        return client
    except Exception as e:
        print(f"Failed to authenticate: {e}")
        return None

def get_health_data(client, days=7):
    """Retrieve detailed health data for the past 'days', including steps, heart rate, sleep, and stress metrics."""
    health_data = []
    
    try:
        for day in range(days):
            date = (datetime.today() - timedelta(days=day)).strftime("%Y-%m-%d")
            # Fetch raw data for each category
            steps_data = client.get_steps_data(date)
            heart_rate_data = client.get_heart_rates(date)
            sleep_data = client.get_sleep_data(date)
            stress_data = client.get_stress_data(date)
            # Debugging output to review raw data
            print(f"Raw Data for {date}:")
            print(f"Steps Data: {steps_data}")
            print(f"Heart Rate Data: {heart_rate_data}")
            print(f"Sleep Data: {sleep_data}")
            print(f"Stress Data: {stress_data}")
            # Process and extract relevant information from raw data
            total_steps = sum(entry.get('steps', 0) for entry in steps_data) if isinstance(steps_data, list) else None
            heart_rate_max = heart_rate_data.get('maxHeartRate')
            heart_rate_resting = heart_rate_data.get('restingHeartRate')
            seven_day_avg_resting = heart_rate_data.get('lastSevenDaysAvgRestingHeartRate')
            sleep_info = sleep_data.get('dailySleepDTO', {})
            sleep = {
                "sleep_time_seconds": sleep_info.get('sleepTimeSeconds'),
                "sleep_start_timestamp_gmt": sleep_info.get('sleepStartTimestampGMT'),
                "sleep_end_timestamp_gmt": sleep_info.get('sleepEndTimestampGMT'),
                "deep_sleep_seconds": sleep_info.get('deepSleepSeconds'),
                "light_sleep_seconds": sleep_info.get('lightSleepSeconds'),
                "rem_sleep_seconds": sleep_info.get('remSleepSeconds'),
                "awake_sleep_seconds": sleep_info.get('awakeSleepSeconds'),
                "average_respiration": sleep_info.get('averageRespirationValue'),
                "lowest_respiration": sleep_info.get('lowestRespirationValue'),
                "highest_respiration": sleep_info.get('highestRespirationValue'),
                "average_sleep_stress": sleep_info.get('avgSleepStress')
            }
            stress = {
                "max_stress_level": stress_data.get('maxStressLevel'),
                "average_stress_level": stress_data.get('avgStressLevel')
            }
            # Append extracted and processed data to the list
            health_data.append({
                "date": date,
                "total_steps": total_steps,
                "heart_rate_max": heart_rate_max,
                "heart_rate_resting": heart_rate_resting,
                "seven_day_avg_resting": seven_day_avg_resting,
                "sleep_time_seconds": sleep["sleep_time_seconds"],
                "sleep_start_timestamp_gmt": sleep["sleep_start_timestamp_gmt"],
                "sleep_end_timestamp_gmt": sleep["sleep_end_timestamp_gmt"],
                "deep_sleep_seconds": sleep["deep_sleep_seconds"],
                "light_sleep_seconds": sleep["light_sleep_seconds"],
                "rem_sleep_seconds": sleep["rem_sleep_seconds"],
                "awake_sleep_seconds": sleep["awake_sleep_seconds"],
                "average_respiration": sleep["average_respiration"],
                "lowest_respiration": sleep["lowest_respiration"],
                "highest_respiration": sleep["highest_respiration"],
                "average_sleep_stress": sleep["average_sleep_stress"],
                "max_stress_level": stress["max_stress_level"],
                "average_stress_level": stress["average_stress_level"]
            })
            print(f"Processed data for {date} - Total Steps: {total_steps}, "
                  f"Heart Rate Max: {heart_rate_max}, Heart Rate Resting: {heart_rate_resting}, "
                  f"Seven Day Avg Resting: {seven_day_avg_resting}, Sleep: {sleep}, Stress: {stress}")
            # Store data in InfluxDB
            write_data_to_influxdb(date, total_steps, heart_rate_max, heart_rate_resting,
                                   seven_day_avg_resting, sleep, stress)
    except Exception as e:
        print(f"Failed to retrieve health data: {e}")
    
    return health_data

def write_data_to_influxdb(date, total_steps, heart_rate_max, heart_rate_resting,
                            seven_day_avg_resting, sleep, stress):
    """Writes health data to InfluxDB"""
    try:
        # Create the Point object with tags and fields
        point = Point("health_data") \
            .tag("date", date) \
            .field("total_steps", total_steps) \
            .field("heart_rate_max", heart_rate_max) \
            .field("heart_rate_resting", heart_rate_resting) \
            .field("seven_day_avg_resting", seven_day_avg_resting) \
            .field("sleep_time_seconds", sleep["sleep_time_seconds"]) \
            .field("sleep_start_timestamp_gmt", sleep["sleep_start_timestamp_gmt"]) \
            .field("sleep_end_timestamp_gmt", sleep["sleep_end_timestamp_gmt"]) \
            .field("deep_sleep_seconds", sleep["deep_sleep_seconds"]) \
            .field("light_sleep_seconds", sleep["light_sleep_seconds"]) \
            .field("rem_sleep_seconds", sleep["rem_sleep_seconds"]) \
            .field("awake_sleep_seconds", sleep["awake_sleep_seconds"]) \
            .field("average_respiration", sleep["average_respiration"]) \
            .field("lowest_respiration", sleep["lowest_respiration"]) \
            .field("highest_respiration", sleep["highest_respiration"]) \
            .field("average_sleep_stress", sleep["average_sleep_stress"]) \
            .field("max_stress_level", stress["max_stress_level"]) \
            .field("average_stress_level", stress["average_stress_level"])

        # Debugging output to ensure it's a Point object
        print(f"Created Point object: {point}")

        # Use the correct InfluxDB client setup with WritePrecision
        with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN) as client:
            # Use the write_api context manager
            with client.write_api(write_options=WriteOptions(batch_size=1, flush_interval=10_000)) as write_api:
                write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point, write_precision=WritePrecision.NS)
                print(f"Data written to InfluxDB for {date}")
    
    except Exception as e:
        print(f"Failed to write data to InfluxDB: {e}")

# Example Client Class with Mocked Methods for Testing
class MockClient:
    def get_steps_data(self, date):
        return [{'steps': 12000}, {'steps': 8000}]
    
    def get_heart_rates(self, date):
        return {
            'maxHeartRate': 175,
            'restingHeartRate': 65,
            'lastSevenDaysAvgRestingHeartRate': 68
        }
    
    def get_sleep_data(self, date):
        return {
            'dailySleepDTO': {
                'sleepTimeSeconds': 28800,
                'sleepStartTimestampGMT': 1672345600,
                'sleepEndTimestampGMT': 1672353600,
                'deepSleepSeconds': 7200,
                'lightSleepSeconds': 14400,
                'remSleepSeconds': 3600,
                'awakeSleepSeconds': 3600,
                'averageRespirationValue': 14,
                'lowestRespirationValue': 12,
                'highestRespirationValue': 16,
                'avgSleepStress': 2.5
            }
        }
    
    def get_stress_data(self, date):
        return {
            'maxStressLevel': 3,
            'avgStressLevel': 2
        }

# Example usage
if __name__ == "__main__":
    client = MockClient()
    health_data = get_health_data(client, days=5)
    print(f"Collected Health Data: {health_data}")