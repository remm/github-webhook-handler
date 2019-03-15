#!/usr/bin/env sh

set -a

cp /configs/token_config.py /app/hooks/token_config.py

python index.py
