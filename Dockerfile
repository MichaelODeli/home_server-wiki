# syntax=docker/dockerfile:1

FROM python:3.10.8
RUN apt-get update

WORKDIR /app

COPY requirements.txt requirements.txt
# RUN pip3 install -r requirements.txt
RUN --mount=type=cache,target=C:/Windows/Temp \
    pip install -r requirements.txt

COPY . .

EXPOSE 8050
CMD [ "python", "app.py"]