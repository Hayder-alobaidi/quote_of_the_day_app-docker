docker build -t end-user-service:latest .
docker tag end-user-service:latest hayder89/end-user-service:latest
docker push hayder89/end-user-service:latest

docker run -p 5002:5002 end-user-service -d