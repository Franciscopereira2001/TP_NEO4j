from create_db_02 import gen_data, medir_tempo_start, medir_tempo_stop, gen_elemento
import sys
from py2neo import Graph

def main():
    n = 500
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))
    
    if len(sys.argv) == 2:
        n = int(sys.argv[1])
    
    enderecos = gen_elemento("addr_", n)
    users = gen_elemento("user_",n)
    
    step = "enderecos"
    t = medir_tempo_start(step)
    n_e = 0
    for addr in enderecos:
        n_e += 1
        graph.run(f"MATCH (n: Address {{name: '{addr}'}}) SET n.nr='0' RETURN n")
    medir_tempo_stop(step, t, n_e)
    
    step = "utilizadores"
    t = medir_tempo_start(step)
    n_e = 0
    for user in users:
        n_e += 1
        graph.run(f"MATCH (n: User {{name: '{user}'}}) SET n.enabled=false RETURN n")
    
    medir_tempo_stop(step, t, n_e)

if __name__ == "__main__":
    main()