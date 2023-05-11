# importing libraries
from airflow.operators.python_operator import PythonOperator
from airflow import DAG
from datetime import datetime, timedelta, date
import gspread
from pathlib import Path
import requests
import os
os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'

# defining python functions

# col_num_to_letter converts column index number to letter(i.e. column 1 is column A)
def col_num_to_letter(col_num):
    div = col_num
    column_label = ""
    while div > 0:
        (div, mod) = divmod(div - 1, 26)
        column_label = chr(mod + 65) + column_label
    return column_label

# function pul_gsheets() pull the data from test_pr spreadsheet as pandas DataFrame
def pull_gsheets():
    credentials_file = f"{Path(__file__).parent}/credentials.json"
    gc = gspread.service_account(filename=credentials_file)
    sh = gc.open_by_key("1gtEsbb4yPPZhqr6RT0bT9uVLhuJ9QOy3JcqAQn34PIk")
    worksheet = sh.worksheet("test")

    header_row = worksheet.row_values(1)  # Get the first row of the sheet as a list
    header_row = [x.lower() for x in header_row]
    error_column_index = header_row.index(
        "error") + 1 if "error" in header_row else None  # Find the index of the "error" column
    date_of_dead_link_column_index = header_row.index(
        "date-of-dead-url") + 1 if "date-of-dead-url" in header_row else None  # Find the index of the "date-of-dead-url" column

    # Error Column
    if error_column_index is not None:  # The "error" column is found
        error_column_letter = col_num_to_letter(error_column_index)
        print(f"The 'error' column is in column {error_column_letter}")
    else:  # The "error" column was not found, script will create it
        print("The 'error' column was not found")
        headers = worksheet.row_values(1)
        last_col_index = len(headers) + 1
        worksheet.update_cell(1, last_col_index, 'error')
        error_column_letter = col_num_to_letter(last_col_index)

    # Date of Dead URL Column
    if date_of_dead_link_column_index is not None:  # The "error" column is found
        date_of_dead_link_column_letter = col_num_to_letter(date_of_dead_link_column_index)
        print(f"The 'date_of_dead_link' column is in column {date_of_dead_link_column_letter}")
    else:  # The "date_of_dead_link" column was not found, script will create it
        print("The 'date-of-dead-url' column was not found")
        headers = worksheet.row_values(1)
        last_col_index = len(headers) + 1
        worksheet.update_cell(1, last_col_index, 'date-of-dead-url')
        date_of_dead_link_column_letter = col_num_to_letter(last_col_index)

    return error_column_letter,date_of_dead_link_column_letter

# function find_dead_placements() is using XCOM to error cell index and date cell index
# it pull worksheet and it checks all placements that are newer(last 90 days) and that do not have error cell marked as True
# it checks if URL status code is 404 and it returns list of indexes that needs to be updated
def find_dead_placements(**context):
    USER_AGENT = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/109.0.0.0 Safari/537.36")
    headers = {"user-agent": USER_AGENT}

    # pull error cell index and date of placement cell index from XCOM
    cells = context['ti'].xcom_pull(task_ids='pull_gsheets')
    ERROR_CELL = cells[0]
    DATE_CELL = cells[1]
    print(f"Error cell is {ERROR_CELL} and date cell is {DATE_CELL}")

    # loading worksheet
    credentials_file = f"{Path(__file__).parent}/credentials.json"
    gc = gspread.service_account(filename=credentials_file)
    sh = gc.open_by_key("1gtEsbb4yPPZhqr6RT0bT9uVLhuJ9QOy3JcqAQn34PIk")
    worksheet = sh.worksheet("test")
    res = worksheet.get_all_records()

    # find dead placements
    index = 1 # index counter
    cells_to_update = []  # here we'll keep track of cells that should be updated with errors

    for placement in res:
        index += 1
        print(placement)
        print(f'Date of placement: {placement["Date of Placement"]}')

        try:  # getting date of placement
            placement_dt = datetime.strptime(placement["Date of Placement"], "%d-%m-%Y")
        except:
            placement_dt = datetime(1000, 1, 1)

        # selecting last 90 days placements
        last_90_days_date = datetime.now() - timedelta(days=90)
        current_error_cell_value = placement["error"].lower()
        if ((placement_dt > last_90_days_date) & (
                current_error_cell_value != "true")):  # if placement is from last 90 days, and does not contain True in error cell, we will check it
            print("placement is new. we're checking it")
            try:  # checking if url is alive
                req = requests.get(placement["Link to article"], timeout=5, headers=headers,
                                   verify=False)  # load current link to article
                print(req.status_code)
                status_code = req.status_code
            except:
                status_code = 404
            if (status_code == 404):  # dead urls
                cells_to_update.append(
                    f"{ERROR_CELL}{index}-{DATE_CELL}{index}")  # marking index of cell that needs to be updated
            print(index)
            print(status_code)
        else:
            print("placement is old or already contains error marked. we're not checking it")
    return cells_to_update

# update_gsheets takes dataframe as input and it updates test_pr_edit sheet with provided dataframe
def update_gsheets(**context):
    gc = gspread.service_account(filename="credentials.json")
    sh = gc.open_by_key("1gtEsbb4yPPZhqr6RT0bT9uVLhuJ9QOy3JcqAQn34PIk")
    cells_to_update = context['ti'].xcom_pull(task_ids='find_dead_placements') # XCOM tuple from find_dead_placements function
    today_date = str(date.today())
    worksheet_to_update = sh.worksheet("test")

    for cell in cells_to_update:
        error_cell = cell.split("-")[0]
        date_of_dead_placement_cell = cell.split("-")[1]
        worksheet_to_update.update(error_cell, True)
        worksheet_to_update.update(date_of_dead_placement_cell, today_date)
        print(f"updated index:{cell} with value True")
    print("worksheet updated with new data")

# Apache Airflow Setup
default_args = {
    "owner" : "mvasiljevic",
    "start_date" : datetime(2023,3,15),
    "catchup" : False,
    "retries" : 1,
    "retry_delay" : timedelta(minutes=5)
}

# Defining DAG for gsheets_pipeline
dag = DAG(
    dag_id = "sheets_pipeline",
    default_args=default_args,
    schedule_interval="@daily"
)

# task pull_gsheets is calling pul_gsheets() function via PythonOperator
pull_gsheets_task = PythonOperator(
    task_id = "pull_gsheets",
    python_callable=pull_gsheets,
    dag = dag
)

# task find_dead_placements is looking for dead urls from gsheets worksheet
find_dead_placements_task = PythonOperator(
    task_id="find_dead_placements",
    python_callable=find_dead_placements,
    dag=dag,
    provide_context=True
)

# task push_gsheets_results is pulling indexes of dead placements from find_dead_placements via xcom and updating gsheets with Errors
push_gsheets_results_task = PythonOperator(
    task_id = "push_gsheets",
    python_callable=update_gsheets,
    dag=dag,
    provide_context=True
)

# task airflow
pull_gsheets_task >> find_dead_placements_task >> push_gsheets_results_task

