// query 4 : Reclamacoes efetuadas pelo user_12
MATCH (:User {username:"user_12"})-[:RESERVE_IN]->(n)-[:REVIEW_IN]-(a:Review {positiva:false})
RETURN n.name,a.name