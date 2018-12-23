#!/bin/bash
set -euo pipefail

curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"post data example":"test"}' \
  "http://localhost:5000/users/register?username=topher&description=sillycat"


curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"post data example":"test"}' \
  "http://localhost:5000/users/remove?username=topher"
