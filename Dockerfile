FROM python:3.12.3
RUN apt-get update

WORKDIR /app

COPY requirements.txt requirements.txt

RUN --mount=type=cache,target=C:/Windows/Temp \
    pip install -r requirements.txt

COPY . .

EXPOSE 81
CMD [ "python", "app.py"]