# HTTP-Health-Inspector

HTTP Health Inspector is an Airflow DAG (Directed Acyclic Graph) designed to monitor the health of a list of URLs. This project pulls a list of URLs from Google Sheets from the last 3 months, sends a GET request to each URL, and checks if it's healthy or not based on the status code returned. If the status code is 200, it is considered healthy; otherwise, it is considered not healthy. The health information about all URLs is then updated in the Google Sheets.

# Contributing
Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request on the GitHub repository.

# License
This project is licensed under the MIT License.

# Acknowledgments
HTTP Health Inspector was inspired by the need to monitor the health of URLs and provide an automated solution for updating the status in a Google Sheets document.
