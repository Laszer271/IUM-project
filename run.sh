echo '> about us'
curl http://localhost:5000/about --request GET

# set base model

# uzycie base modelu
echo '> using base model'
curl http://localhost:5000/model/predict --header "Content-Type: application/json" --request GET --data '{"last_browsed_product": id}'

echo '> load the complex model'
curl http://localhost:5000/model --header "Content-Type: application/json" --request POST --data '{"path": "some_model.h5"}'

# set model

echo '> using complex model'
curl http://localhost:5000/model/predict --header "Content-Type: application/json" --request GET --data '{"last_browsed_product": id}'

echo '> check model used'
curl http://localhost:5000/model --request GET

echo '> check AB status'
curl http://localhost:5000/model/ab/status --request GET

echo '> set AB status'
curl http://localhost:5000/model/ab/status --header "Content-Type: application/json" --request POST --data '{"status": True}'

echo '> check AB status'
curl http://localhost:5000/model/ab/status --request GET

# uzycie ab (kilka razy?)
curl http://localhost:5000/model/predict --header "Content-Type: application/json" --request GET --data '{"last_browsed_product": id}'
curl http://localhost:5000/model/predict --header "Content-Type: application/json" --request GET --data '{"last_browsed_product": id}'
curl http://localhost:5000/model/predict --header "Content-Type: application/json" --request GET --data '{"last_browsed_product": id}'
curl http://localhost:5000/model/predict --header "Content-Type: application/json" --request GET --data '{"last_browsed_product": id}'

# sprawdzenie historii
curl http://localhost:5000/model --request GET