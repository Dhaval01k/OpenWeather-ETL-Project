# OpenWeather-ETL-Project
# Open Weather ETL Pipeline Readme

## Project Overview
This Open Weather ETL (Extract, Transform, Load) Pipeline is a data engineering project that collects, transforms, and stores weather data from the OpenWeather API for a list of cities specified in a CSV file. The project employs various technologies and tools to automate the data processing and make the data readily accessible for further analysis and reporting.

## Project Highlights
- **Data Collection**: The project gathers weather data from the OpenWeather API for a predefined list of cities. This data includes information such as temperature, humidity, wind speed, and more.

- **Data Transformation**: The collected raw data is processed and transformed into a structured format using Pandas. It is converted into a DataFrame, which facilitates further analysis and visualization.

- **Pipeline Orchestration**: Apache Airflow is used to orchestrate the entire data pipeline. It handles automation, scheduling, and monitoring of the ETL process, ensuring that data is processed consistently and reliably.

- **Data Storage**: The processed data is transferred and stored in an AWS S3 bucket. This cloud-based storage solution makes the data easily accessible for subsequent analysis and reporting.

- **Development Environment**: Visual Studio and an Ubuntu operating system are utilized to develop and maintain the project. These tools provide a robust environment for coding, testing, and managing the ETL pipeline.

## Getting Started
To get started with the Open Weather ETL Pipeline, follow these steps:

1. **Prerequisites**: Ensure that you have Python, Pandas, Apache Airflow, and the necessary AWS credentials set up on your system.

2. **Project Setup**: Clone this project repository to your local machine.

3. **Configuration**: Configure the project by specifying the list of cities in a CSV file, API keys, and AWS S3 bucket details.

4. **Run the Pipeline**: Execute the ETL pipeline by triggering the Airflow DAG. This will initiate data collection, transformation, and storage.

5. **Access Data**: Once the pipeline is complete, you can access the processed data in the configured AWS S3 bucket for analysis and reporting.

## Directory Structure
- `/data`: Contains sample data files and CSV templates.
- `/src`: Houses the source code for the ETL pipeline, including Airflow DAGs and Python scripts.
- `/config`: Stores configuration files for API keys, city lists, and AWS S3 bucket details.
- `/notebooks`: Optionally, you can use Jupyter notebooks for data analysis and visualization.

## Contributions
Contributions to this project are welcome. If you have suggestions, improvements, or bug fixes, feel free to open an issue or submit a pull request.


## Author
This Open Weather ETL Pipeline was created and is maintained by Dhaval Kacha.

For any questions or inquiries, please contact dhavalkacha.01@gmail.com.

Happy data processing! 🌦️📊🛠️
