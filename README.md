# ETL-Pipeline-Orchestration-Using-Airflow-Postgres-Docker

## ETL Pipeline
This repository contains code for an ETL (Extract, Transform, Load) pipeline orchestration using Apache Airflow. The pipeline reads data with pandas, performs data cleaning by dropping null values, extracts time and dates using pd.to_datetime, and loads the data into a CSV file and a Postgres database.

Prerequisites
To run this project, you need to have the following dependencies installed:

* Python
* Apache Airflow
* pandas

## Screeshot 
picture of the workflow:
![Alt Workflow](./success.png) 

## Installation
1. Clone the repository to your local machine:
```
git clone https://github.com/your-username/etl-pipeline.git
```
2. Install the required Python packages:
```
pip install -r requirements.txt
```
3. Configure Apache Airflow by following the official documentation: Airflow Installation Guide

## Usage
To use this ETL pipeline, follow the steps below:

1. Start Apache Airflow:
```
airflow webserver -p 8080
airflow scheduler
```
2. Access the Airflow UI by opening http://localhost:8080 in your browser.
3. Set up the required connections in Airflow:
    Create a connection named postgres_conn to connect to your Postgres database.
    Create a connection named csv_conn to specify the directory for the CSV file.
4. Enable the DAG (Directed Acyclic Graph) named etl_pipeline in the Airflow UI.
5. Monitor the progress of the ETL pipeline in the Airflow UI. You can view the logs, check the status of each task, and troubleshoot any issues that may arise.

## Functions 
The ETL consists of five steps:
1. Loading the dataset from a csv file downloaded by the command below
2. Dropping all the null values in the dataset.
3. Extracting all periodic attributes of the tpep_pickup_datetime and tpep_dropoff_datetime, periodic attributes like
    * pickupdays and dropoff days
    * pickup and dropoff days of the week
    * pickup and dropoff hours
    * pickup and dropoff months
    * and last trip duration by subtracting the dropoff period by the pickup period and divided by 60
4. Load the data to a csv file cleansed
5. load the data Postgres DB

## Getting the data 
To obtain the data required for this ETL pipeline, you can use the following wget command:
```
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz
```
This command will download the "yellow_tripdata_2021-01.csv.gz" file to your current directory.
