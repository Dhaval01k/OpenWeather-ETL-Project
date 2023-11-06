import pandas as pd
import json
from datetime import datetime,timedelta
import requests
import config as config
from airflow import DAG
from airflow.operators.python import PythonOperator
import boto3

#storing filtered city
filtered_cities = []

#base url
base_url=config.base
now=datetime.now()
dt_date=now.strftime("%d_%m_%Y_%H_%M")

file_name="City_Weather_Report_"+dt_date+".csv"
aws_access_key=config.aws_access_key
aws_secret_key=config.aws_access_secret_key
bucket_name = 'openweathercityreport'
Local_path=config.EC_base_path




#insert into list
def city_list(filtered_cities):
    with open(config.EC_cities_path,mode="r",encoding="utf8") as cities:
        filtered_cities=cities.read().splitlines()
        return filtered_cities

api_key = config.credentials()
#print("credentials verified")

transformed_data=config.transformed_data

def api_call(filter_city):
    
    for city in filter_city:
        city_name=str(city)
        if city_name=='city':
            continue
        full_url=base_url+city_name+"&APPID="+api_key
        data=requests.get(full_url).json()

        city = data["name"]
        weather_description = data["weather"][0]['description']
        temp_celsius = kelvin_to_celsius(data["main"]["temp"])
        feels_like_celsius= kelvin_to_celsius(data["main"]["feels_like"])
        min_temp_celsius = kelvin_to_celsius(data["main"]["temp_min"])
        max_temp_celsius = kelvin_to_celsius(data["main"]["temp_max"])
        pressure = data["main"]["pressure"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        time_of_record = datetime.utcfromtimestamp(data['dt'] + data['timezone'])
        sunrise_time = datetime.utcfromtimestamp(data['sys']['sunrise'] + data['timezone'])
        sunset_time = datetime.utcfromtimestamp(data['sys']['sunset'] + data['timezone'])
        insert_records(city,weather_description,temp_celsius,feels_like_celsius,min_temp_celsius,max_temp_celsius,pressure,humidity,wind_speed,time_of_record,sunrise_time,sunset_time)
    print("Data inserted")
    return transformed_data

def kelvin_to_celsius(kelvin):
    celsius = kelvin - 273.15
    return round(celsius,2)

def insert_records(city,weather_description,temp_celsius,feels_like_celsius,min_temp_celsius,max_temp_celsius,pressure,humidity,wind_speed,time_of_record,sunrise_time,sunset_time):
    transformed_data["City"].append(city)
    transformed_data["Description"].append(weather_description)
    transformed_data["Temperature (C)"].append(temp_celsius)
    transformed_data["Feels Like (C)"].append(feels_like_celsius)
    transformed_data["Minimun Temp (C)"].append(min_temp_celsius)
    transformed_data["Maximum Temp (C)"].append(max_temp_celsius)
    transformed_data["Pressure"].append(pressure)
    transformed_data["Humidty"].append(humidity)
    transformed_data["Wind Speed"].append(wind_speed)
    transformed_data["Time of Record"].append(time_of_record)
    transformed_data["Sunrise (Local Time)"].append(sunrise_time)
    transformed_data["Sunset (Local Time)"].append(sunset_time)
    return transformed_data

def transformed(transformed_data):
    df = pd.DataFrame(transformed_data)
    print("Dataframe created")
    return df



def write_csv(df):
    #Local_path = config.EC_base_path+file_name
    df.to_csv(file_name,index=False,header=True,mode='w')
    print("File name : ",file_name)
    return file_name
    



try:
    def Filter_city(**context):
        print("Retriving data from csv file")
        filter=[]
        filter = city_list(filter)
        context['ti'].xcom_push(key="filter",value=filter)
        print("sucessfully reterived.")
        


    def Insert_city(**context):
        print("calling api this might take time..........")
        filtered_cities = context.get("ti").xcom_pull(key='filter')
        context['ti'].xcom_push(key='local_dct',value=api_call(filtered_cities))
        print("called api sucessfully and data inserted to dictonary.")


    def Transform_write(**context):
        print("transforming data to dataframe.")
        trans=context.get("ti").xcom_pull(key='local_dct')
        dataframe=transformed(trans)
        print("transformed data sucessfully.")
        print("writing data to csv_file")
        context['ti'].xcom_push(key='Local',value=write_csv(dataframe))
    
    def upload_S3(**context):
        s3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
        dat=str(context.get("ti").xcom_pull(key='Local'))
        Local=config.EC_base_path+dat
        print("Uploading......")
        print(Local)
        s3.upload_file(Local, bucket_name,dat)
        print(f"File {Local} successfully uploaded to S3 bucket {bucket_name} as {dat}")
    

except Exception as e:
    print(e)



with DAG(
        dag_id='OpenWeather_airflow',
        schedule_interval='@daily',
        default_args={
            "owner" : "Dhaval",
            "retries" : 1,
            "start_date" : datetime(2023,10,30),
            "retry_delay" : timedelta(minutes=1)
        }) as d:
    Filter_city_1 = PythonOperator(
        task_id="Filter_city_1",
        python_callable=Filter_city,
        provide_context=True
    )

    Insert_city_execute = PythonOperator(
        task_id='Insert_city_execute',
        python_callable=Insert_city,
        provide_context=True
    )

    Transform_write_execute = PythonOperator(
        task_id='Transform_write_execute',
        python_callable=Transform_write,
        provide_context=True
    )

    upload_s3_execute = PythonOperator(
        task_id='upload_s3_execute',
        python_callable=upload_S3,
        provide_context=True
    )
    

Filter_city_1 >> Insert_city_execute >> Transform_write_execute >>upload_s3_execute

print("All executed.....")



