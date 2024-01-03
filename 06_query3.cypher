// query 3 : Respostas as reservas do user_12
MATCH (:User {username:"user_12"})-[:RESERVE_IN]->(n)-[:RESPONSE_IN]-(a)
RETURN n,a