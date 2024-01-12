from importlib import reload
import sys, random, datetime
from lib.carrega_cidades import *
from py2neo import Graph

from timeit import default_timer as timer

def gen_elemento(prefix, n):
    r = []
    for i in range(n):
        r.append(prefix + str(i))
    return r

def gen_data():
    start_date = datetime.datetime(2022, 10, 1, 1, 1, 1)
    end_date   = datetime.datetime(2030, 11, 30, 1, 1, 1)
    num_days   = (end_date - start_date).days
    rand_days   = random.randint(1, num_days)
    rand_hours  = random.randint(1, 24)
    rand_min  = random.randint(1, 60)
    random_date = start_date + datetime.timedelta(days=rand_days, hours=rand_hours, minutes=rand_min)
    return random_date.strftime("20%y-%m-%dT%H:%M:%S")

def medir_tempo_start(msg):
    print("==============================")
    print("comecar medicao : " +msg)
    return timer()

def medir_tempo_stop(msg, start, n_entries):
    end = timer() - start
    print("Medido : " + msg + " " + str(end) + " s" + " (" + str(n_entries) + ")")
    print("==============================")

    
def main():
    n = 500
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))
    
    if len(sys.argv) == 2:
        n = int(sys.argv[1])
    
    enderecos = gen_elemento("addr_", n)
    users = gen_elemento("user_",n)
    parks = gen_elemento("park_",n)
    orders = gen_elemento("order_", n*4)
    roles = ["Administrator", "Utilizador", "Convidado"]
    paises = ["Portugal"]

    step = "apagar base de dados"
    t = medir_tempo_start(step)
    graph.run("MATCH (n) DETACH DELETE n")
    medir_tempo_stop(step, t, 1)
    
    step = "criar paises"
    n_e = 0
    t = medir_tempo_start(step)
    
    for pais in paises:
        graph.run(f"CREATE({pais}:Country {{name:'{pais}'}})")
        n_e += 1

    c = Cidades("cidades.json")  

    for distrito in c.get_distritos():
        graph.run(f"CREATE({distrito['name']}:Cities {{name:'{distrito['name']}'}})")
        n_e += 1
        for cidade in c.get_cidades(distrito):
            if cidade['name'] != distrito['name']:
                n_e += 1
                graph.run(f"CREATE({cidade['name']}:Cities {{name:'{cidade['name']}'}})")
            n_e += 1
            graph.run(f"MATCH (a:Cities {{name: '{cidade['name']}'}}),(b:Cities {{name: '{distrito['name']}'}}) CREATE(a)-[:CITY_IN]->(b)")
        n_e += 1
        graph.run(f"MATCH (a:Cities {{name: '{distrito['name']}'}}),(b:Country {{name: 'Portugal'}}) CREATE(a)-[:DISTRICT_IN]->(b)")
        
    medir_tempo_stop(step, t, n_e)
    
    # Enderecos
    step = "enderecos"
    t = medir_tempo_start(step)
    n_e = 0
    
    for addr in enderecos:
        cidade = c.get_cidade_random()
        n_e += 1
        graph.run(f'CREATE({addr}:Address {{name:"{addr}", rua:"{addr}", nr:"{addr}"}})')
        n_e += 1
        graph.run(f"MATCH (a:Address {{name:'{addr}', rua:'{addr}', nr:'{addr}'}}),(b:Cities {{name: '{cidade['name']}'}}) CREATE(a)-[:ADDR_IN]->(b)")
    medir_tempo_stop(step, t, n_e)
    
    
    # roles
    step = "roles"
    t = medir_tempo_start(step)
    n_e = 0
    for role in roles:
        n_e += 1
        graph.run(f'CREATE({role}:Role {{name:"{role}"}})')
    medir_tempo_stop(step, t, n_e)
        
    # Utilizadores
    step = "Utilizadores"
    t = medir_tempo_start(step)
    n_e = 0
    for user in users:
        n_e += 1
        graph.run(f'CREATE({user}:User {{name:"{user}", email:"{user}@user.com", username:"{user}", password:"{user}", enabled:true}})')
        role = random.choices(roles)[0]
        n_e += 1
        graph.run(f"MATCH (a:User {{username: '{user}'}}),(b:Role {{name: '{role}'}}) CREATE(a)-[:ROLE_IN]->(b)")
    medir_tempo_stop(step, t, n_e)
    
    return
    # Parks
    step = "Parks"
    t = medir_tempo_start(step)
    n_e = 0
    enderecos_tmp = enderecos
    saved_parks = []
    for park in parks:
        lat = random.choices(range(n*1000))[0]
        long = random.choices(range(n*1000))[0]
        n_e += 1
        graph.run(f'CREATE({park}:Parkings {{name:"{park}",latitude:{lat}, longitude:{long}, enabled:true}})')
        addr = random.choices(enderecos_tmp)[0]
        enderecos_tmp.remove(addr)
        n_e += 1
        graph.run(f"MATCH (a:Parkings {{name: '{park}'}}),(b:Address {{name: '{addr}'}}) CREATE(a)-[:LOCATED_IN]->(b)")
        n_e += 1
        graph.run(f'CREATE({park}_occupation:Occupation {{name:"{park}_o",percentage: {random.choices(range(100))}, last_updated_min:0}})')
        n_e += 1
        graph.run(f"MATCH (a:Parkings {{name: '{park}'}}),(b:Occupation {{name: '{park}_o'}}) CREATE(a)-[:OCCUPATION_IN]->(b)")
        
        saved_parks.append({
            "park": park,
            "addr": addr
        })
    medir_tempo_stop(step, t, n_e)
     
    step = "Order"
    t = medir_tempo_start(step)
    n_e = 0
    
    order_per_user = {}
    for order in orders:
        n_e += 1
        graph.run(f'CREATE({order}:Order {{name:"{order}",time:timestamp(), arrival:datetime("{gen_data()}")}})')
        saved_park = random.choices(saved_parks)[0]
        n_e += 1
        graph.run(f"MATCH (a:Order {{name: '{order}'}}),(b:Address {{name: '{saved_park['addr']}'}}) CREATE(a)-[:SEARCH_IN]->(b)")
        
        user = random.choices(users)[0]
        n_e += 1
        graph.run(f"MATCH (a:User {{name: '{user}'}}),(b:Order {{name: '{order}'}}) CREATE(a)-[:RESERVE_IN]->(b)")
        
        n_e += 1
        graph.run(f"MATCH (a:Order {{name: '{order}'}}),(b:Occupation {{name: '{saved_park['park']}_o'}}) CREATE(a)-[:RESERVE_IN]->(b)")
                
        n_e += 1
        graph.run(f'CREATE(Response_{order}:Response {{name:"Response_{order}", time:timestamp(), response:{random.choice(["true", "false"])}}})')
        
        n_e += 1
        graph.run(f"MATCH (a:Response {{name:'Response_{order}'}}),(b:Order {{name: '{order}'}}) CREATE(a)-[:RESPONSE_IN]->(b)")
        
        n_e += 1
        graph.run(f'Create(Review_{order}:Review {{name:"Review_{order}", positiva: {random.choice(["true", "false"])}, descricao: "ok"}})')
        n_e += 1
        graph.run(f"MATCH (a:Review {{name:'Review_{order}'}}),(b:Order {{name: '{order}'}}) CREATE(a)-[:REVIEW_IN]->(b)")
        if user in order_per_user:
            order_per_user[user].append(order)
        else:
            order_per_user[user] = [order]
    
    last = None
    for _, orders in order_per_user.items():
        for order in orders:
            if last != None:
                n_e += 1
                graph.run(f"MATCH (a:Order {{name: '{last}'}}),(b:Order {{name: '{order}'}}) CREATE(a)-[:PREVIOUS_IN]->(b)")
            last = order
    medir_tempo_stop(step, t, n_e)
                
            
        
        
if __name__ == "__main__":
    main()