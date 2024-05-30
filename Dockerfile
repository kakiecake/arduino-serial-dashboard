# Use an official Python runtime as a parent image
FROM python:3.12-alpine

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./app /app/app
COPY ./templates /app/templates
COPY ./static /app/static

# Install Pipenv, then install dependencies
RUN pip install pipenv && \
  pipenv install --system --deploy

# Expose port 80 for the application
EXPOSE 80

# Run app.py when the container launches
CMD ["sh", "-c", "pipenv run uvicorn main:app --host 0.0.0.0 --port 80"]
