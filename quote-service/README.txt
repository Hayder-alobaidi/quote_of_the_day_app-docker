Remember to add the env varibiles when create K8s , these two are needed: 
ENV DATABASE_URI=replace_with_actual_database_uri
ENV RABBITMQ_URL=replace_with_actual_rabbitmq_url




docker login

docker build -t analytics-service:1 .

docker tag analytics-service:1 hayder89/analytics-service:1

docker push hayder89/analytics-service:1



docker-compose up -d

