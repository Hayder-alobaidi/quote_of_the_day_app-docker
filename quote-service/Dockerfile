
# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variables with placeholder values
ENV DATABASE_URI=replace_with_actual_database_uri
ENV RABBITMQ_URL=replace_with_actual_rabbitmq_url

# Run app.py when the container launches
CMD ["python", "app.py"]