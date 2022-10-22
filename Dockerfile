FROM python:3.9
WORKDIR /root
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY blessing .
EXPOSE 8000
ENTRYPOINT bash run.sh
