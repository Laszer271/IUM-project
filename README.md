# IUM-project

Treść zadania:
Są osoby, które wchodzą na naszą stronę i nie mogą się zdecydować który produkt obejrzeć. Może dało by się im coś polecić?

Wiktor Michalski, Wojciech Maciejewski

## Uruchomienie

Uruchomienie samego api:
```
python3 api.py
```

Uruchomienie skryptu testowego (wymagane uruchomione api do działania):
```
./run.sh
```

## Moduły

### api.py
Api we Flasku, umożliwiające wybieranie i ładowanie modeli, uzyskanie predykcji, przeprowadzenie eksperymentu A/B oraz pobranie historii sesji.

### models.py
Moduł zawierający oba rodzaje modeli (prosty i docelowy) oraz "kontener". Kontener przechowuje modele i wykonuje na nich operacje na podstawie żądań z API.

## API

### /about
#### GET
```
curl http://localhost:5000/about --request GET
```
Informacje o autorach :)
```
"IUM 20Z Project. Wojciech Maciejewski, Wiktor Michalski"
```

### /model
#### GET
```
curl http://localhost:5000/model --request GET
```
Sprawdzenie aktywnego modelu.
```
 {
    "model_name": "simple"
 }
```
```
{
  "model_name": "complex", 
  "path": "parametrized_model.csv"
}
```

#### POST
```
curl http://localhost:5000/model --header "Content-Type: application/json" --request POST --data '{"type": "complex", "path": "parametrized_model.csv"}'
```
Umożliwia wybranie modelu ("simple" lub "complex") i wag do niego. 
```
    {
        "info": "Request successfully sent"
    }
```

### /model/predict
#### GET
```
curl http://localhost:5000/model/predict --header "Content-Type: application/json" --request GET --data '{"last_browsed_product": 1279}'
```
Przewidywanie produktów na podstawie ostatnio przejrzanego.
```
    [
    1011, 
    1130, 
    1021, 
    1008, 
    1022
    ]
```

### /model/history
#### GET
```
curl http://localhost:5000/model/history --request GET
```
Pobranie historii sesji.
```
    [
    {
        "CurrentSession": [
        1279
        ], 
        "Model": "simple", 
        "Predictions": [
        1012, 
        1009, 
        1314, 
        1128, 
        1016
        ]
    }, 
    {
        "CurrentSession": [
        1279, 
        1278
        ], 
        "Model": "simple", 
        "Predictions": [
        1281
        ]
    }
    ]
```

### /model/ab
#### GET
```
curl http://localhost:5000/model/ab --request GET
```
Sprawdzenie, czy eksperyment A/B jest uruchomiony.
```
    {
    "AB_status": false
    }
```

#### POST
```
curl http://localhost:5000/model/ab --header "Content-Type: application/json" --request POST --data '{"status": true}'
```
Uruchomienie lub wyłączenie eksperymentu A/B (tylko jeśli model docelowy jest załadowany).
```
{
    "info": "AB status successfully set."
}
```

## AB
W ramach eksperymentu A/B, do predykcji używany jest losowo model prosty lub załadowany model skomplikowany. Do poprawnego przeprowadzenia eksperymentu każda nowa sesja powinna mieć losowany jeden z modeli, który byłby konsekwentnie używany przez całość trwania sesji - ale dla uproszczenia prezentacji (i w związku z tym, że oba modele są do siebie zbliżone koncepcyjnie), przyjmiemy uproszczenie, że każde zapytanie zwraca odpowiedź na podstawie losowego modelu.

## Notebooki
### model_comparison.ipynb 
Porównanie modelu prostego i docelowego.

### EDA.ipynb
Analiza danych na podstawie pierwszego etapu, ale z zaktualizowaną ścieżką do nowych danych i kilkoma nowymi wykresami.