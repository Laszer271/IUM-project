echo '> about us'
curl http://localhost:5000/about --request GET

echo '> using base model'
curl http://localhost:5000/model/predict --header "Content-Type: application/json" --request GET --data '{"last_browsed_product": 1021}'

echo '> load the complex model'
curl http://localhost:5000/model --header "Content-Type: application/json" --request POST --data '{"type": "complex", "path": "parametrized_model.csv"}'

echo '> using complex model'
curl http://localhost:5000/model/predict --header "Content-Type: application/json" --request GET --data '{"last_browsed_product": 1279}'

echo '> check model used'
curl http://localhost:5000/model --request GET

echo '> check AB status'
curl http://localhost:5000/model/ab --request GET

echo '> set AB status'
curl http://localhost:5000/model/ab --header "Content-Type: application/json" --request POST --data '{"status": true}'

echo '> check AB status'
curl http://localhost:5000/model/ab --request GET

echo '> runinng A/B multiple times'
curl http://localhost:5000/model/predict --header "Content-Type: application/json" --request GET --data '{"last_browsed_product": 1130}'
curl http://localhost:5000/model/predict --header "Content-Type: application/json" --request GET --data '{"last_browsed_product": 1022}'
curl http://localhost:5000/model/predict --header "Content-Type: application/json" --request GET --data '{"last_browsed_product": 1008}'
curl http://localhost:5000/model/predict --header "Content-Type: application/json" --request GET --data '{"last_browsed_product": 1011}'

echo '> checking history'
curl http://localhost:5000/model/history --request GET