# HTTP-Health-Inspector

HTTP Health Inspector is an Airflow DAG (Directed Acyclic Graph) designed to monitor the health of a list of URLs. This project pulls a list of URLs from Google Sheets from the last 3 months, sends a GET request to each URL, and checks if it's healthy or not based on the status code returned. If the status code is 200, it is considered healthy; otherwise, it is considered not healthy. The health information about all URLs is then updated in the Google Sheets.

# Configuration
Before running the HTTP Health Inspector DAG, you need to set up the necessary configuration. Follow the steps below:

Create a Google Cloud project and enable the Google Sheets API.

Create a service account key and download the JSON file containing the credentials.

Rename the downloaded JSON file to service_account.json and place it in the project directory.

Open the config.json file and update the following fields:

* google_sheets_url: The URL of the Google Sheets document containing the list of URLs.
* google_sheets_range: The range of cells in the Google Sheets document where the URLs are located.
* project_id: The ID of your Google Cloud project.
* bucket_name: The name of the Google Cloud Storage bucket where the DAG files will be stored.
* dag_name: The name of the DAG file.

# Usage
To use HTTP Health Inspector, follow these steps:

Make sure you have completed the configuration steps mentioned above.

Start the Airflow web server by running the following command:

`airflow webserver`
Start the Airflow scheduler by running the following command in a separate terminal:

`airflow scheduler`
Access the Airflow web interface by opening http://localhost:8080 in your web browser.

In the Airflow web interface, enable the http_health_inspector DAG.

Trigger the DAG manually or let it run according to the schedule defined in the DAG.

Check the Google Sheets document to view the health information about all URLs.

# Contributing
Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request on the GitHub repository.

# License
This project is licensed under the MIT License.

# Acknowledgments
HTTP Health Inspector was inspired by the need to monitor the health of URLs and provide an automated solution for updating the status in a Google Sheets document.
