# syntax=docker/dockerfile:1

FROM python:3.11.6-bookworm
WORKDIR /app
COPY requirements.txt requirements.txt
RUN apt update
RUN apt install -y curl build-essential chrpath libssl-dev libxft-dev libfreetype6 libfreetype6-dev libfontconfig1 libfontconfig1-dev firefox-esr
RUN pip3 install -r requirements.txt
COPY . .
CMD ["python3", "main.py"]
