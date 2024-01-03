from py2neo import Graph
import sys 

def main():
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))
    i = 0
    for line in sys.stdin:
        try:
            graph.run(line)
            i = i + 1
            print(f"{str(i)} Ok")
        except Exception as error:
            print(f"error: {error}")
    

if __name__ == "__main__":
    main()