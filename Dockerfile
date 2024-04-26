FROM python:3.10-slim
WORKDIR /server
COPY ./requirements.txt /server
RUN pip3 install --upgrade pip -r requirements.txt
COPY ./server /server