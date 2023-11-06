from datetime import datetime
base="https://api.openweathermap.org/data/2.5/weather?q="
local_base_path="/home/admin1/airflow/dags/"
local_citites_path="/home/admin1/airflow/dags/cities.csv"
EC_base_path="/home/admin1/airflow/dags/"
EC_cities_path="/home/admin1/airflow/dags/cities.csv"


aws_access_key=''
aws_access_secret_key=''
aws_bucket_name = 'openweathercityreport'

now=datetime.now()
dt_date=now.strftime("%d-%m-%Y(%H:%M)")

file_name="City_Weather_Report_"+dt_date+".csv"

def credentials():
    with open("credentials.txt",mode="r") as credentials:
        return credentials.read()

#for storing the weather details of every country
transformed_data={      "City": [],
                        "Description": [],
                        "Temperature (C)": [],
                        "Feels Like (C)": [],
                        "Minimun Temp (C)": [],
                        "Maximum Temp (C)": [],
                        "Pressure": [],
                        "Humidty": [],
                        "Wind Speed": [],
                        "Time of Record": [],
                        "Sunrise (Local Time)": [],
                        "Sunset (Local Time)": []}
