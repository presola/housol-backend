# Application Details

### Housol
===================

Housol is an API-based application built using Django Rest Framework that provides valuable insights into the real estate market. It offers the following functionalities:

1. Get current house prices in different locations. The application comes prepopulated with various locations.
2. Predict future house prices in different locations. Note that predictions may stay on a straight line for a while due to the limited available data.

## Requirement
To run this application, install the required packages listed in the `requirements.txt` file using the following command:
```bash
pip install -r requirements.txt
```

## Run
After installing the requirements, follow the instructions below to run the Housol application.

### Local Deployment
1. Run `init.sh` to initialize the database and structures data.
   ```bash
   sh init.sh
   ```
2. Start the application using Gunicorn:
   ```bash
   gunicorn housol.wsgi:application --workers 2 --timeout 360
   ```
3. Load Prices data once the server is up and running:
   ```bash
   python3 loadPrices.py
   ```

### Docker Compose
If you prefer to deploy the application using Docker Compose, ensure you have Docker installed, and then follow these steps:

1. Build all containers:
   ```bash
   docker-compose build
   ```

2. Run all containers (Frontend on port 8000, Web API on port 10010, Data Science on port 8060):
   ```bash
   docker-compose up
   ```

After running the application:

1. Swagger UI can be accessed via [http://127.0.0.1:8000/v1/swagger/ui](http://127.0.0.1:8000/v1/swagger/ui).