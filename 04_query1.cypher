// query 1 : Retirar todas as cidades de aveiro
MATCH (n)-[:CITY_IN]->(:Cities {name:'Aveiro'})
RETURN n