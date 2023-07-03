# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port that the Django app will listen on
EXPOSE 8000

# Run tests and fail the build if they don't pass
RUN python manage.py test

# Copy the settings config
RUN cp fileoperations/settings/select_sample.py fileoperations/settings/select.py
RUN cp fileoperations/settings/secrets_sample.json fileoperations/settings/secrets.json

# Run the initial migration
RUN python manage.py migrate

# Define the command to run your Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
