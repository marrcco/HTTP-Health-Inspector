# HTTP-Health-Inspector

HTTP Health Inspector is an Airflow DAG (Directed Acyclic Graph) designed to monitor the health of a list of URLs. This project pulls a list of URLs from Google Sheets from the last 3 months, sends a GET request to each URL, and checks if it's healthy or not based on the status code returned. If the status code is 200, it is considered healthy; otherwise, it is considered not healthy. The health information about all URLs is then updated in the Google Sheets.
