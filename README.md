# Install All Required Package
- pip install requirements.txt

# Run Application Locally
- python3 app.py

# Run Application with Docker
## Build Docker
- docker build --no-cache -t flask-backend .
## Run Docker
- docker run -it -d -p 5001:5001 flask-backend
## View logs
- docker ps: get container Id
- docker logs - f {container_id}


# Check Application is Running
## Dev
- https://hackathon-355107-ejimfcjqnq-uc.a.run.app/user/api/v1/healthCheck

## Local
- http://127.0.0.1:5001/user/api/v1/healthCheck should return success status
