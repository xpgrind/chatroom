curl -H "Content-Type: application/json" --request POST --data '{"token":"valid"}'  http://127.0.0.1:5000/secure
{
  "success": true
}

curl -H "Content-Type: application/json" --request POST --data '{"username":"xyz","password":"xyz"}'  http://127.0.0.1:5000/secure
# {
#   "reason": "no token in POST data",
#   "success": false
# }
curl -H "Content-Type: application/json" --request POST --data '{"token":"xyz"}'  http://127.0.0.1:5000/secure
# {
#   "reason": "invalid token",
#   "success": false
# }
DizhudeMBP:server dizhu$ curl  --request POST --data '{"token":"valid"}'  http://127.0.0.1:5000/secure
# {
#   "reason": "no POST json data",
#   "success": false
# }
DizhudeMBP:server dizhu$ curl  --request POST  http://127.0.0.1:5000/secure
# {
#   "reason": "no POST json data",
#   "success": false
# }
DizhudeMBP:server dizhu$ curl http://127.0.0.1:5000/secure
# {
#   "reason": "no POST json data",
#   "success": false
# }
