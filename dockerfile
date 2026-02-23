##define airflow and python versions as arguments
ARG AIRFLOW_VERSION=2.9.2
ARG PYTHON_VERSION=3.10

FROM apache/airflow:${AIRFLOW_VERSION}-python${PYTHON_VERSION}

## define airflow environment variable
ENV AIRFLOW_HOME=/opt/airflow

##copy the requirements.txt file from our local directory to the root directory of the
##docker images file system 
COPY requirements.txt / 

##install specified version of airflow and packages in requirements.txt file
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt
