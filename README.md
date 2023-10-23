# ETL-Pipeline-Orchestration-Using-Airflow-Postgres-Docker

## ETL Pipeline
This repository contains code for an ETL (Extract, Transform, Load) pipeline orchestration using Apache Airflow. The pipeline reads data with pandas, performs data cleaning by dropping null values, extracts time and dates using pd.to_datetime, and loads the data into a CSV file and a Postgres database.

Prerequisites
To run this project, you need to have the following dependencies installed:

* Python
* Apache Airflow
* pandas
## Installation
1. Clone the repository to your local machine:
```
git clone https://github.com/your-username/etl-pipeline.git
```
2. Install the required Python packages:
```
pip install -r requirements.txt
```
