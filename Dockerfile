# Comment these out if deploy via Openshift web
# FROM python:3.8-slim
# LABEL version="1.0"
# LABEL app="cidrtools"
# LABEL maintaner="https://github.com/ja3600/cidrtools.git"

RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app
RUN pip3 install --no-cache-dir -r requirements.txt
ADD . /app
EXPOSE 5000
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["sh", "entrypoint.sh"]


# Use for development
# COPY . /app
# WORKDIR /app
# RUN pip3 install --no-cache-dir -r requirements.txt
# EXPOSE 5000
# ENTRYPOINT [ "python", "app/app.py" ]
