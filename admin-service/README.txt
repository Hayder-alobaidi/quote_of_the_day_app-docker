docker build -t admin-service:latest .
docker tag admin-service:latest hayder89/admin-service:latest
docker push hayder89/admin-service:latest

docker run -p 5003:5003 admin-service