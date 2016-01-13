#!/bin/bash
pushd /root/dockerpuller

pip install -r ../requirements.txt
python app.py
