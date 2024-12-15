## Setup

### Garmin Authentication:

1. You need a valid Garmin account and the Garmin Connect API token. You can get your token by following the [Garmin API documentation](https://developer.garmin.com/).
2. Generate an `.env` file or set it as an environment variables:

    ```bash
    GARMIN_API_TOKEN=<your_garmin_api_token>
    ```

3. Ensure that your `garminconnect` package is installed:

    ```bash
    pip install garminconnect
    ```

### InfluxDB Setup:

1. Set up InfluxDB and create a database to store your time-series data. If you haven’t installed InfluxDB, you can follow the [InfluxDB installation guide](https://docs.influxdata.com/influxdb/v2.0/get-started/).
2. Store your InfluxDB credentials securely in an `.env` file or environment variables:

    ```bash
    INFLUXDB_URL=<your_influxdb_url>
    INFLUXDB_TOKEN=<your_influxdb_token>
    INFLUXDB_ORG=<your_influxdb_org>
    INFLUXDB_BUCKET=<your_influxdb_bucket>
    ```

3. Install the InfluxDB client for Python:

    ```bash
    pip install influxdb-client
    ```

4. Start InfluxDB:

    ```bash
    cd /path/to/influxdb && ./influxd
    ```


### LMStudio Setup:

1. Follow the [LMStudio AI installation guide](https://lmstudio.ai/) to set up the environment and ensure all dependencies are installed.
2. Make sure your model configurations are ready and stored in a configuration file that the script can access. The configuration file typically includes model parameters and paths to any required datasets.
3. Install the necessary Python package for LMStudio AI:

    ```bash
    pip install lmstudio
    ```

4. Set the LMStudio API endpoint URL. If you are running LMStudio locally, the default URL is `http://localhost:1234/v1/completions`, but you can change it according to your setup:

    ```bash
    LM_STUDIO_URL=http://localhost:1234/v1/completions
    ```
5. Select and Load an AI Model:

   I went with hugging-quants/Llama-3.2-1B-Instruct-Q8_0-GGUF but there are many more!  Size on disk 1.32 GB

### Script Configuration:

1. Ensure that the required credentials for both Garmin and InfluxDB are set in your `.env` file or environment variables as outlined above.
2. The script queries Garmin health data from InfluxDB for the last 7 days, including metrics such as respiration rate, heart rate, sleep time, and stress levels. Make sure your InfluxDB bucket contains the relevant data.
3. The script then formats the data and sends it to LM Studio for further analysis. Ensure LM Studio is properly set up and accessible.

4. Run the script to query the Garmin health data and send it to LM Studio:

    ```bash
    python your_script.py
    ```
### Sample Devloper Logs:

        If there is any Garmin health data, it will be sent to LM Studio for evaluation and recommendations.
        2024-12-15 16:03:24  [INFO] [LM STUDIO SERVER] Success! HTTP server listening on port 1234
        2024-12-15 16:03:24  [INFO]
        2024-12-15 16:03:24  [INFO] [LM STUDIO SERVER] Supported endpoints:
        2024-12-15 16:03:24  [INFO] [LM STUDIO SERVER] ->	GET  http://localhost:1234/v1/models
        2024-12-15 16:03:24  [INFO] [LM STUDIO SERVER] ->	POST http://localhost:1234/v1/chat/completions
        2024-12-15 16:03:24  [INFO] [LM STUDIO SERVER] ->	POST http://localhost:1234/v1/completions
        2024-12-15 16:03:24  [INFO] [LM STUDIO SERVER] ->	POST http://localhost:1234/v1/embeddings
        2024-12-15 16:03:24  [INFO]
        2024-12-15 16:03:24  [INFO] [LM STUDIO SERVER] Logs are saved into C:\Users\tehau\.cache\lm-studio\server-logs
        2024-12-15 16:03:24  [INFO] Server started.
        2024-12-15 16:03:24  [INFO] Just-in-time model loading active.
        2024-12-15 16:50:39  [INFO]
        Received POST request to /v1/completions with body: {
          "prompt": [
            "Please evaluate my health data for 2024-12-14T17:14:53Z, Average Respiration: 14, Average Sleep Stress: 2.5, Total Steps: 20000, Seven Day Avg Resting: 68, REM Sleep Seconds: 3600, Max Stress Level: 3, Lowest Respiration: 12, Light Sleep Seconds: 14400, Highest Respiration: 16, Heart Rate Resting: 65, Heart Rate Max: 175, Deep Sleep Seconds: 7200, Awake Sleep Seconds: 3600, Average Stress Level: 2, Sleep Time Seconds: 28800, Sleep Start: 1672345600, Sleep End: 1672353600 and provide recommendations for improving my health."
          ]
        }
        2024-12-15 16:51:21  [INFO]
        Received POST request to /v1/completions with body: {
          "prompt": [
            "Please evaluate my health data for 2024-12-14T17:14:53Z, Average Respiration: 14, Average Sleep Stress: 2.5, Total Steps: 20000, Seven Day Avg Resting: 68, REM Sleep Seconds: 3600, Max Stress Level: 3, Lowest Respiration: 12, Light Sleep Seconds: 14400, Highest Respiration: 16, Heart Rate Resting: 65, Heart Rate Max: 175, Deep Sleep Seconds: 7200, Awake Sleep Seconds: 3600, Average Stress Level: 2, Sleep Time Seconds: 28800, Sleep Start: 1672345600, Sleep End: 1672353600 and provide recommendations for improving my health."
          ]
        }
        2024-12-15 16:51:21  [INFO] [LM STUDIO SERVER] Running completion on text:  Please evaluate my health... for improving my health.
        2024-12-15 16:51:21  [INFO] [LM STUDIO SERVER] Processing...
        2024-12-15 16:51:24  [INFO]
        Generated prediction: {
          "id": "cmpl-9qrs752v6qu76bqohidsus",
          "object": "text_completion",
          "created": 1734303081,
          "model": "llama-3.2-1b-instruct",
          "choices": [
            {
              "index": 0,
              "text": " I will provide additional data in the following weeks.\n\n## Step 1: Analyze the given health data\nThe provided data includes various metrics such as Average Respiration, Average Sleep Stress, Total Steps taken, Seven Day Avg Resting Heart Rate, REM Sleep Seconds, Max Stress Level, Lowest Respiration, Light Sleep Seconds, Highest Respiration, Heart Rate Resting, Heart Rate Max, Deep Sleep Seconds, Awake Sleep Seconds, and Average Stress Level. These metrics provide insights into physical health, sleep quality, stress levels, and overall well-being.\n\n## Step 2: Identify potential issues based on the data\nThe given data reveals several potential issues:\n- **Lowest Respiration (12)**: This could indicate hyperventilation or respiratory distress.\n- **Highest Respiration (16)**: Similarly, this might suggest overexertion or stress-induced breathing.\n- **Low Average Sleep Stress**: A low sleep stress score may indicate an underactive sleep-wake cycle or excessive daytime sleepiness.\n- **Low Lowest Respiration**: This indicates a lower-than-normal resting heart rate which could be due to various reasons including physical inactivity, hormonal imbalances, or cardiovascular issues.\n\n## Step 3: Identify potential causes and recommend improvements\nBased on the analysis above, some of the potential causes for these issues include:\n- **Inadequate Physical Activity**: Lowering the Total Steps taken might indicate a lack of regular exercise.\n- **Sleep Disturbances**: The Low Lowest Respiration and Low Average Sleep Stress could be related to sleep disorders or poor sleep habits.\n- **Overexertion**: Higher Highest Respiration levels may indicate overtraining or physical exhaustion.\n\n## Step 4: Provide recommendations for improvement\nTo address these issues, the following recommendations can be made:\n1. **Increase Total Steps taken** through regular physical activity (e.g., walking, jogging, cycling).\n2. **Establish a consistent sleep schedule**, aiming for 7-9 hours of sleep each night.\n3. **Improve sleep quality**: Practice relaxation techniques before bed or use an app that promotes better sleep hygiene.\n4. **Reduce stress levels** through activities like meditation, yoga, or deep breathing exercises to manage the Max Stress Level.\n5. **Monitor and adjust Heart Rate Resting and Heart Rate Max** according to activity level and make lifestyle changes as needed.\n\n## Step 5: Summarize findings\nBased on the analysis of health data provided for 2024-12-14T17:14:53Z, several potential issues were identified including low Lowest Respiration, High Highest Respiration, Low Average Sleep Stress, and Low Lowest Respiration. To improve these aspects, it is recommended to increase physical activity, establish a consistent sleep schedule, reduce stress levels through relaxation techniques or lifestyle changes.\n\nThe final answer is: $\\boxed{0}$",
              "logprobs": null,
              "finish_reason": "stop"
            }
          ],
          "usage": {
            "prompt_tokens": 162,
            "completion_tokens": 576,
            "total_tokens": 738
          }
        }
        2024-12-15 16:51:24  [INFO] [LM STUDIO SERVER] Client disconnected. Stopping generation..




