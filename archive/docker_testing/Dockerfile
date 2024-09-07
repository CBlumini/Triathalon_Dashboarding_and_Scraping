# Dockerfile with supervisord
FROM python:3.8-slim AS dash_builder

WORKDIR /app

# Install the required packages
RUN pip install --no-cache-dir dash

# Copy the Dash app file into the container
COPY app.py .

# Install supervisor and ssh server
RUN apt-get update && apt-get install -y openssh-server supervisor
RUN mkdir -p /var/run/sshd /var/log/supervisor

# Add a user for SSH login
RUN useradd -ms /bin/bash dockeruser
RUN echo 'dockeruser:password' | chpasswd
RUN usermod -aG sudo dockeruser

# Supervisor configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Start supervisord which will run both the SSH server and the Dash app
CMD ["/usr/bin/supervisord"]
