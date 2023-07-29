FROM python:3.9.2
WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

EXPOSE 8000

COPY . /app/

CMD ["./start.sh"]
