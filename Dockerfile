FROM python:3.7-alpine
MAINTAINER "Roman Stepanchuk" <romanst@wix.com>
ENV REPOS_JSON_PATH=/app/repos.json
ENV VALIDATE_SOURCEIP=false
WORKDIR /app

COPY requirements.txt /app
RUN apk add --no-cache git openssh-client bash && \
    pip install -r requirements.txt

RUN mkdir -p ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts

COPY . /app

COPY ./ssh_keys/* /root/.ssh/

EXPOSE 80
CMD ["python", "index.py"]