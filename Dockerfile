FROM python:3.7-alpine
MAINTAINER "Roman Stepanchuk" <romanst@wix.com>
ENV REPOS_JSON_PATH=/app/repos.json
WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

ADD templates /templates
ADD docker-entrypoint.sh /usr/local/bin/

COPY . /app


EXPOSE 8080
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
