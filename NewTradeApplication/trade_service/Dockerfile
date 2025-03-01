FROM python:3.9
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install psycopg2
COPY . .
CMD ["python", "app.py"]