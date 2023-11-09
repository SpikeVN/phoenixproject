# syntax=docker/dockerfile:1

FROM python:3.11.6-bookworm
WORKDIR /app
COPY requirements_froze.txt requirements_froze.txt
RUN pip3 install -r requirements_froze.txt
COPY . .
CMD ["python3", "main.py"]
