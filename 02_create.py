from importlib import reload
import sys, random, datetime
from lib.carrega_cidades import *

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

def main():
    n = 500
    if len(sys.argv) == 2:
        n = int(sys.argv[1])
    
    enderecos = gen_elemento("addr_", n)
    users = gen_elemento("user_",n)
    parks = gen_elemento("park_",n)
    orders = gen_elemento("order_", n*4)
    roles = ["Administrator", "Utilizador", "Convidado"]
    paises = ["Portugal"]

    for pais in paises:
        print(f"CREATE({pais}:Country {{name:'{pais}'}})")

    c = Cidades("cidades.json")  

    for distrito in c.get_distritos():
        print(f"CREATE({distrito['name']}:Cities {{name:'{distrito['name']}'}})")
        for cidade in c.get_cidades(distrito):
            if cidade['name'] != distrito['name']:
                print(f"CREATE({cidade['name']}:Cities {{name:'{cidade['name']}'}})")
            print(f"CREATE({cidade['name']})-[:CITY_IN]->({distrito['name']})")

        print(f"CREATE({distrito['name']})-[:DISTRICT_IN]->(Portugal) ")
        
    # Enderecos
    for addr in enderecos:
        cidade = c.get_cidade_random()
        print(f'CREATE({addr}:Address {{name:"{addr}", rua:"{addr}", nr:"{addr}"}})')
        print(f'CREATE({addr})-[:ADDR_IN]->({cidade["name"]})')
    
    # roles
    for role in roles:
        print(f'CREATE({role}:Role {{name:"{role}"}})')
        
    # Utilizadores
    for user in users:
        print(f'CREATE({user}:User {{name:"{user}", email:"{user}@user.com", username:"{user}", password:"{user}", enabled:true}})')
        role = random.choices(roles)[0]
        print(f'CREATE ({user})-[:ROLE_IN]->({role})')
        
    # Parks
    enderecos_tmp = enderecos
    saved_parks = []
    for park in parks:
        lat = random.choices(range(n*1000))[0]
        long = random.choices(range(n*1000))[0]
        print(f'CREATE({park}:Parkings {{name:"{park}",latitude:{lat}, longitude:{long}, enabled:true}})')
        addr = random.choices(enderecos_tmp)[0]
        enderecos_tmp.remove(addr)
        print(f'CREATE ({park})-[:LOCATED_IN]->({addr})')
        print(f'CREATE({park}_occupation:Occupation {{name:"{park}_o",percentage: {random.choices(range(100))}, last_updated_min:0}})')
        print(f'CREATE ({park})-[:OCCUPATION_IN]->({park}_occupation)')
        saved_parks.append({
            "park": park,
            "addr": addr
        })
    
    order_per_user = {}
    for order in orders:
        print(f'CREATE({order}:Order {{name:"{order}",time:timestamp(), arrival:datetime("{gen_data()}")}})')
        saved_park = random.choices(saved_parks)[0]
        print(f'CREATE ({order})-[:SEARCH_IN]->({saved_park["addr"]})')
        user = random.choices(users)[0]
        print(f'CREATE ({user})-[:RESERVE_IN]->({order})')
        print(f'CREATE ({order})-[:RESERVE_IN]->({saved_park["park"]})')
        print(f'CREATE(Response_{order}:Response {{name:"Response_{order}", time:timestamp(), response:{random.choice(["true", "false"])}}})')
        print(f'CREATE (Response_{order})-[:RESPONSE_IN]->({order})')
        print(f'Create(Review_{order}:Review {{name:"Review_{order}", positiva: {random.choice(["true", "false"])}, descricao: "ok"}})')
        print(f'CREATE (Review_{order})-[:REVIEW_IN]->({order})')
        if user in order_per_user:
            order_per_user[user].append(order)
        else:
            order_per_user[user] = [order]
    
    last = None
    for _, orders in order_per_user.items():
        for order in orders:
            if last != None:
                print(f'CREATE ({last})-[:PREVIOUS_IN]->({order})')
            last = order
                
            
        
        
if __name__ == "__main__":
    main()