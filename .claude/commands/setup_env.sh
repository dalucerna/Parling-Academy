#!/usr/bin/env bash
# Serve Parling-Academy landing page
set -e

cd "$(dirname "$0")/../../.."

PORT=3000
echo "==> Serving Parling-Academy on port $PORT..."
echo "==> Public URL: https://code.kenitech.io/preview/$PORT/"
npx serve . -l $PORT
