# HTTP-Health-Inspector

HTTP Health Inspector is an Airflow DAG (Directed Acyclic Graph) designed to monitor the health of a list of URLs. This project pulls a list of URLs from Google Sheets from the last 3 months, sends a GET request to each URL, and checks if it's healthy or not based on the status code returned. If the status code is 200, it is considered healthy; otherwise, it is considered not healthy. The health information about all URLs is then updated in the Google Sheets.

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
