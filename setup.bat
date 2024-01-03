docker rm --force testneo4j
docker run --name testneo4j -p7474:7474 -p7687:7687 -d --env NEO4J_AUTH=neo4j/password neo4j:latest

:: gerar base de dados
python .\02_create.py 50 > .\02_create.cypher
cat .\02_create.cypher | python .\neo4j_console.py