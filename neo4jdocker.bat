docker rm --force testneo4j
docker run --name testneo4j -p7474:7474 -p7687:7687 -d --env NEO4J_AUTH=neo4j/password neo4j:latest