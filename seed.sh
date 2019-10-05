#!/bin/bash

HOST=

echo -e "\n +++ Creating merchants"
curl -X POST -H 'Content-Type: application/json' -i http://localhost:5000/merchants --data '{"name": "merchant1", "vat_number": "12343", "ateco": "1", "address": "Via delle ghiaie, Trento"}'
curl -X POST -H 'Content-Type: application/json' -i http://localhost:5000/merchants --data '{"name": "merchant2", "vat_number": "13121", "ateco": "2", "address": "Viale Antonio Gramsci,Trento"}'
curl -X POST -H 'Content-Type: application/json' -i http://localhost:5000/merchants --data '{"name": "merchant3", "vat_number": "13125", "ateco": "3", "address": "Via Alcide de gasperi, Trento"}'
curl -X POST -H 'Content-Type: application/json' -i http://localhost:5000/merchants --data '{"name": "merchant4", "vat_number": "41232", "ateco": "4", "address": "Via Riccardo Zandonai, Trento"}'
curl -X POST -H 'Content-Type: application/json' -i http://localhost:5000/merchants --data '{"name": "merchant5", "vat_number": "12314", "ateco": "5", "address": "Via Fratelli perini, Trento"}'
curl -X POST -H 'Content-Type: application/json' -i http://localhost:5000/merchants --data '{"name": "merchant6", "vat_number": "51232", "ateco": "6", "address": "Via Fabio Filzi, Trento"}'
curl -X POST -H 'Content-Type: application/json' -i http://localhost:5000/merchants --data '{"name": "merchant7", "vat_number": "54321", "ateco": "7", "address": "Via Milano, Trento"}'
curl -X POST -H 'Content-Type: application/json' -i http://localhost:5000/merchants --data '{"name": "merchant8", "vat_number": "12372", "ateco": "8", "address": "Via Tofane, Trento"}'
curl -X POST -H 'Content-Type: application/json' -i http://localhost:5000/merchants --data '{"name": "merchant9", "vat_number": "23461", "ateco": "9", "address": "Via Coni Zugna, Trento"}'
curl -X POST -H 'Content-Type: application/json' -i http://localhost:5000/merchants --data '{"name": "merchant10", "vat_number": "25367", "ateco": "10", "address": "Via Pecori Giraldi, Trento"}'
curl -X POST -H 'Content-Type: application/json' -i http://localhost:5000/merchants --data '{"name": "merchant11", "vat_number": "24671", "ateco": "11", "address": "Corso Verona, Rovereto"}'
curl -X POST -H 'Content-Type: application/json' -i http://localhost:5000/merchants --data '{"name": "merchant12", "vat_number": "27326", "ateco": "12", "address": "Via Alessandro Manzoni, Rovereto"}'
curl -X POST -H 'Content-Type: application/json' -i http://localhost:5000/merchants --data '{"name": "merchant13", "vat_number": "13663", "ateco": "13", "address": "Borgo Santa Caterina, Rovereto"}'
curl -X POST -H 'Content-Type: application/json' -i http://localhost:5000/merchants --data '{"name": "merchant14", "vat_number": "61311", "ateco": "14", "address": "Via Unione, Rovereto"}'

echo -e "\n +++ Creating coupons"
curl -X POST -H 'Content-Type: application/json' -i http://localhost:5000/coupons --data '{"merchant": "merchant1", "description": "deal1", "count":2}'
curl -X POST -H 'Content-Type: application/json' -i http://localhost:5000/coupons --data '{"merchant": "merchant2", "description": "deal2", "count":2}'
curl -X POST -H 'Content-Type: application/json' -i http://localhost:5000/coupons --data '{"merchant": "merchant3", "description": "deal3", "count":2}'
curl -X POST -H 'Content-Type: application/json' -i http://localhost:5000/coupons --data '{"merchant": "merchant4", "description": "deal4", "count":2}'
curl -X POST -H 'Content-Type: application/json' -i http://localhost:5000/coupons --data '{"merchant": "merchant11", "description": "deal5", "count":2}'
curl -X POST -H 'Content-Type: application/json' -i http://localhost:5000/coupons --data '{"merchant": "merchant12", "description": "deal6", "count":2}'

