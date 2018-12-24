#!/bin/bash
set -euo pipefail

curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"username":"topher"}' \
  "http://localhost:5000/users/register"


curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"username":"topher"}' \
  "http://localhost:5000/users/remove"
