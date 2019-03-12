#!/usr/bin/env sh

set -a

cp /configs/token.py /app/hooks/token.py

python index.py
