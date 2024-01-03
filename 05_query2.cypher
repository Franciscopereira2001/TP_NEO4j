// query 2 : Reservas do utilizador 12
MATCH (:User {username:"user_12"})-[:RESERVE_IN]->(n)
RETURN n