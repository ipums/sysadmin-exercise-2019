# Recommended tag sysadmin-app

# Use customizable passenger base without ruby, etc, but add Python.
FROM phusion/passenger-customizable:1.0.5
RUN /pd_build/python.sh

# Upgrade OS at image build time.
# https://github.com/phusion/passenger-docker#upgrading_os
# May require docker build --no-cache to force OS upgrade.
RUN apt-get update \
 && apt-get upgrade -y -o Dpkg::Options::="--force-confold"

# Set base working directory.
WORKDIR /home/app

# Add Python packages Flask and Flask-MySQLdb.
# Note: The apt-get purge removes packages only needed for the pip installs,
# but not needed at runtime.  An exception is libmysqlclient-dev, which is
# not needed at runtime, but which is retained to keep its dependency
# libmysqlclient20 around, because that dependency IS needed at runtime.
# We could have just installed libmysqlclient20 separately and kept only it,
# but it looked so version-specific, we decided to keep the more generically
# versioned dev package instead.
COPY requirements.txt requirements.txt
RUN apt-get install -y --no-install-recommends python3-pip \
                                               python3-setuptools \
                                               python3-dev \
                                               libmysqlclient-dev \
 && pip3 install --trusted-host pypi.python.org -r requirements.txt \
 && apt-get purge -y --auto-remove python3-dev \
                                   python3-setuptools \
                                   python3-pip

# Configure and enable Nginx and Passenger.
COPY webapp.conf /etc/nginx/sites-enabled/webapp.conf
RUN rm /etc/nginx/sites-enabled/default \
 && rm -f /etc/service/nginx/down

# Copy in web app itself.
COPY --chown=app:app *.py webapp/

# Document what port the web app listens on.
EXPOSE 80/tcp

# Clean up.
RUN apt-get clean \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

