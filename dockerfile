FROM apache/airflow:latest-python3.11

#change user to root and install Java
USER root
RUN apt update --fix-missing \
    && apt-get install -y wget gnupg unzip libgconf-2-4\
    && apt-get install -y openjdk-11-jdk

# Install ChromeDriver (replace 91 with the appropriate version)
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && wget -N https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/115.0.5790.102/linux64/chromedriver-linux64.zip -P /tmp/ \
    && unzip /tmp/chromedriver-linux64.zip -d /usr/local/bin/ \
    && rm /tmp/chromedriver-linux64.zip \
    && chmod +x /usr/local/bin/chromedriver-linux64


# Set Chrome options
ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROME_PATH=/usr/bin/google-chrome

#change user to airflow and install requirements
USER airflow
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt