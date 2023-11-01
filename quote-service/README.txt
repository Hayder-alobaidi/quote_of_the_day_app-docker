Remember to add the env varibiles when create K8s , these two are needed: 
ENV DATABASE_URI=replace_with_actual_database_uri
ENV RABBITMQ_URL=replace_with_actual_rabbitmq_url




docker login

docker build -t quote-service:latest .

docker tag quote-service:latest hayder89/quote-service:latest

docker push hayder89/quote-service:latest



docker-compose up -d

