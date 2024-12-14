import requests
from influxdb_client import InfluxDBClient
from influxdb_client.client.query_api import QueryApi
import json
from datetime import datetime

# InfluxDB configuration
INFLUXDB_URL = "{INFLUXDB_URL}"  # InfluxDB URL default: http://localhost:8086
INFLUXDB_TOKEN = "{INFLUXDB_TOKEN}"  # Your InfluxDB token
INFLUXDB_ORG = "{INFLUXDB_ORG}"  # Your InfluxDB organization
INFLUXDB_BUCKET = "{INFLUXDB_BUCKET}"  # The InfluxDB bucket containing Garmin health data

# LM Studio configuration
LM_STUDIO_URL = "{LM_STUDIO_URL}"  # URL to LM Studio's local endpoint default: http://localhost:1234/v1/completions

# Function to query Garmin health data from InfluxDB
def query_garmin_data():
    # Create InfluxDB client
    client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
    # Define query to get Garmin health data for the last 7 days
    query = '''
    from(bucket: "garmin")
        |> range(start: -7d)
        |> filter(fn: (r) => r["_field"] == "average_respiration" or r["_field"] == "average_sleep_stress" or r["_field"] == "total_steps" or r["_field"] == "seven_day_avg_resting" or r["_field"] == "rem_sleep_seconds" or r["_field"] == "max_stress_level" or r["_field"] == "lowest_respiration" or r["_field"] == "light_sleep_seconds" or r["_field"] == "highest_respiration" or r["_field"] == "heart_rate_resting" or r["_field"] == "heart_rate_max" or r["_field"] == "deep_sleep_seconds" or r["_field"] == "awake_sleep_seconds" or r["_field"] == "average_stress_level" or r["_field"] == "sleep_time_seconds" or r["_field"] == "sleep_start_timestamp_gmt" or r["_field"] == "sleep_end_timestamp_gmt")
    '''
    # Execute query
    result = client.query_api().query(query)
    # Process the result into a dictionary with all fields for a given time
    health_data = {}
    for table in result:
        for record in table.records:
            time = record.get_time().strftime('%Y-%m-%dT%H:%M:%SZ')  # Convert datetime to string
            field = record.get_field()
            value = record.get_value()
            if time not in health_data:
                health_data[time] = {}
            # Add the field value to the dictionary
            health_data[time][field] = value
    # Generate prompt for each time entry
    formatted_data = []
    for time, fields in health_data.items():
        prompt = create_prompt(fields, time)
        formatted_data.append({
            'time': time,
            'fields': fields,
            'prompt': prompt
        })
    return formatted_data

def create_prompt(fields, time):
    """Create a single prompt with all health metrics for a specific time."""
    prompt = (
        f"Please evaluate my health data for {time}, "
        f"Average Respiration: {fields.get('average_respiration', 'N/A')}, "
        f"Average Sleep Stress: {fields.get('average_sleep_stress', 'N/A')}, "
        f"Total Steps: {fields.get('total_steps', 'N/A')}, "
        f"Seven Day Avg Resting: {fields.get('seven_day_avg_resting', 'N/A')}, "
        f"REM Sleep Seconds: {fields.get('rem_sleep_seconds', 'N/A')}, "
        f"Max Stress Level: {fields.get('max_stress_level', 'N/A')}, "
        f"Lowest Respiration: {fields.get('lowest_respiration', 'N/A')}, "
        f"Light Sleep Seconds: {fields.get('light_sleep_seconds', 'N/A')}, "
        f"Highest Respiration: {fields.get('highest_respiration', 'N/A')}, "
        f"Heart Rate Resting: {fields.get('heart_rate_resting', 'N/A')}, "
        f"Heart Rate Max: {fields.get('heart_rate_max', 'N/A')}, "
        f"Deep Sleep Seconds: {fields.get('deep_sleep_seconds', 'N/A')}, "
        f"Awake Sleep Seconds: {fields.get('awake_sleep_seconds', 'N/A')}, "
        f"Average Stress Level: {fields.get('average_stress_level', 'N/A')}, "
        f"Sleep Time Seconds: {fields.get('sleep_time_seconds', 'N/A')}, "
        f"Sleep Start: {fields.get('sleep_start_timestamp_gmt', 'N/A')}, "
        f"Sleep End: {fields.get('sleep_end_timestamp_gmt', 'N/A')} and provide recommendations for improving my health."
    )
    return prompt

def serialize_datetime(obj):
    """Recursively convert datetime objects to strings."""
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%dT%H:%M:%SZ')
    if isinstance(obj, dict):
        return {k: serialize_datetime(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [serialize_datetime(item) for item in obj]
    return obj

def send_to_lm_studio(data):
    # Serialize datetime objects to strings
    data = serialize_datetime(data)
    # Flatten the data and extract the prompt field for sending to LM Studio
    prompts = [entry['prompt'] for entry in data]
    # Send the health data to LM Studio server via a POST request
    response = requests.post(LM_STUDIO_URL, json={"prompt": prompts})
    # Handle response
    if response.status_code == 200:
        print("Data sent successfully to LM Studio")
    else:
        print(f"Failed to send data. Status code: {response.status_code}")
        print(f"Response: {response.text}")

# Main script execution
if __name__ == "__main__":
    # Query Garmin health data
    health_data = query_garmin_data()
    # Send health data to LM Studio if there is data
    if health_data:
        send_to_lm_studio(health_data)
    else:
        print("No Garmin health data to send.")