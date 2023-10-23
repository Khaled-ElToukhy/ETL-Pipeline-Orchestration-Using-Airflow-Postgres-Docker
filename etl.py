from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator


import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import numpy as np 


def load_data(filename):
    df = pd.read_csv(filename)
    return df


def drop_null(data):
    data.dropna(inplace=True)
    data['tpep_pickup_datetime'] = pd.to_datetime(data['tpep_pickup_datetime'])
    data['tpep_dropoff_datetime'] = pd.to_datetime(data['tpep_dropoff_datetime'])
    return data


def extract_times(df1):
    df1['pickup_day']=df1['tpep_pickup_datetime'].dt.day_name()
    df1['dropoff_day']=df1['tpep_dropoff_datetime'].dt.day_name()
    df1['pickup_day_no']=df1['tpep_pickup_datetime'].dt.weekday
    df1['dropoff_day_no']=df1['tpep_dropoff_datetime'].dt.weekday
    df1['pickup_hour']=df1['tpep_pickup_datetime'].dt.hour
    df1['dropoff_hour']=df1['tpep_dropoff_datetime'].dt.hour
    df1['pickup_month']=df1['tpep_pickup_datetime'].dt.month
    df1['dropoff_month']=df1['tpep_dropoff_datetime'].dt.month
    df1["trip_duration"] = df1['tpep_dropoff_datetime'] - df1['tpep_pickup_datetime']
    df1['trip_duration'] = df1['trip_duration'].dt.total_seconds() / 60
    df1['trip_duration'] = df1['trip_duration'].round(2)
    return df1



def load_to_csv(df):
    return df.to_csv("D:/DE Projects/Project_4/airflow/dags/etl.py")
    
    
def load_to_postgres(filename): 
    df = pd.read_csv(filename)
    engine = create_engine('postgresql://user:user@pgdatabase:5432/taxi_data')
    if(engine.connect()):
        print('connected succesfully')
    else:
        print('failed to connect')
    return df.to_sql(name = 'taxi_data',con = engine,if_exists='replace')    
    
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    'start_date': days_ago(2),
    "retries": 1,
}


dag = DAG(
    'taxi_etl_pipeline',
    default_args=default_args,
    description='taxi etl pipeline',
)
with DAG(
    dag_id = 'taxi_etl_pipeline',
    schedule_interval = '@once',
    default_args = default_args,
    tags = ['taxi-pipeline'],
)as dag:
    load_data_taxi= PythonOperator(
        task_id = 'extract_dataset',
        python_callable = load_data,
        op_kwargs={
            "filename": '/opt/airflow/data/taxi_trips.csv'
        },
    )
    drop_null_taxi= PythonOperator(
        task_id = 'extract_dataset',
        python_callable = drop_null,
        op_kwargs={
            "filename": '/opt/airflow/data/taxi_noNull.csv'
        },
    )
    extract_times_taxi= PythonOperator(
        task_id = 'encoding',
        python_callable = encode_load,
        op_kwargs={
            "filename": "/opt/airflow/data/taxi_times.csv"
        },
    )
    load_to_csv_task= PythonOperator(
        task_id = 'load_to_postgres',
        python_callable = load_to_csv,
        op_kwargs={
            "filename": "/opt/airflow/data/taxi.csv"
        },
    )
    load_to_postgres_task = PythonOperator(
        task_id = 'create_dashboard_task',
        python_callable = load_to_postgres,
        op_kwargs={
            "filename": "/opt/airflow/data/taxi.csv"
        },
    )
    
    
    
load_data_taxi >> drop_null_taxi >> extract_times_taxi >> load_to_csv_task >> load_to_postgres_task