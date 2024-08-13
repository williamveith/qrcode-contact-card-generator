# Use Python 3.12 Alpine as the base image to keep the image small and efficient
FROM python:3.12-alpine

# Set the working directory inside the container to /app
WORKDIR /app

# Set the Flask environment variable to production to optimize Flask's internal settings
ENV FLASK_ENV=production

# Copy the requirements.txt file into the container at /app/requirements.txt
COPY requirements.txt ./

# Install dependencies from requirements.txt, disable caching to keep the image small,
# and clean up the cache to ensure no unnecessary data is stored in the image
RUN pip3 install --no-cache-dir -r requirements.txt && \
    rm -rf /var/cache/apk/* /tmp/* /var/tmp/*

# Copy the entire current directory into the container's working directory
# This includes all files and subdirectories from the build context into /app
COPY . .

# Command to run the application
# Runs 'python app.py', which should be configured to start your Flask application
CMD ["python", "app.py"]
