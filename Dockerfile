FROM python:3.7-alpine
MAINTAINER "Roman Stepanchuk" <romanst@wix.com>
ENV REPOS_JSON_PATH=/app/repos.json
ENV VALIDATE_SOURCEIP=false
WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

ADD templates /templates

COPY . /app


EXPOSE 8080
CMD ["python", "index.py"]