from importlib import reload
import sys
import random
from carrega_cidades import *

def gen_elemento(prefix, n):
    r = []
    for i in range(n):
        r.append(prefix + str(i))
    return r

def main():
    n = 500
    if len(sys.argv) == 2:
        n = int(sys.argv[1])
    
    enderecos = gen_elemento("addr_", n)
    users = gen_elemento("user_",n)
    parks = gen_elemento("park_",n)
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
    for park in parks:
        lat = random.choices(range(n*1000))[0]
        long = random.choices(range(n*1000))[0]
        print(f'{park}:Parkings {{name:"{park}",latitude:{lat}, longitude:{long}, enabled:true}}')
        addr = random.choices(enderecos)[0]
        enderecos.remove(addr)
        print(len(enderecos))
        print(f'CREATE ({park})-[:LOCATED_IN]->({addr}),')
        
if __name__ == "__main__":
    main()