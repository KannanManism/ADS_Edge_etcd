# syntax=docker/dockerfile:1

FROM apache/spark
WORKDIR /spark_job
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD ["python3", "spark_job.py"]
