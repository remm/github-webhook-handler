#!/usr/bin/env bash

REPO="github-webhook-handler-test"

if [[ -d "/tmp/${REPO}" ]]; then
  cd /tmp/${REPO} && git pull origin master
else
  cd /tmp/${REPO} && git clone git@github.com:remm/github-webhook-handler-test.git
fi

python3 /app/hooks/bi-repo-webhook.py
cd /tmp/${REPO}
git commit -m "Update modules list" || echo "No changes to commit"
git push