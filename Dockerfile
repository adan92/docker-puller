FROM python:2.7
ADD dockerpuller /root/dockerpuller
ADD requirements.txt /root/requirements.txt
WORKDIR /root/
RUN pip install -r requirements.txt
WORKDIR /root/dockerpuller
ENTRYPOINT ["python", "app.py"]
