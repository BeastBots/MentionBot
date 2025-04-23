# Use a more secure base image
FROM python:3.11.8-slim-bookworm

# Update system packages to fix vulnerabilities and remove unnecessary files
RUN apt-get update && \
	apt-get upgrade -y && \
	apt-get dist-upgrade -y && \
	apt-get autoremove -y && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/*

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

# Expose port 8080 for the webserver
EXPOSE 8080

# Copy the startup script into the container
COPY startup /app/startup

# Ensure the startup script is executable
RUN chmod +x /app/startup

# Start both the bot and the webserver
CMD ["bash", "/app/startup"]
