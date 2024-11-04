FROM python:3.12

WORKDIR /fastapi-application

COPY ./requirements.txt .

RUN apt-get update && apt-get upgrade
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "FastAPI/main.py"]