FROM python:2.7.12-alpine

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY dockerpuller .

ENTRYPOINT ["python", "app.py"]
