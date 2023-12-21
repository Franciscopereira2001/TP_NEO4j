import sys
import random

def gen_elemento(prefix, n):
    r = []
    for i in range(n):
        r.append(prefix + str(i))
    return r

def main():
    n = int(sys.argv[1])
    print(n)
    
    distrios = gen_elemento("distrito_",int(n/4))
    cidades = gen_elemento("cidade_", n)
    enderecos = gen_elemento("addr_", n)
    users = gen_elemento("user_",n)
    roles = ["Administrator", "Utilizador", "Convidado"]
    paises = ["Portugal"]
    
    for pais in paises:
        print(f"CREATE({pais}:Country {{name:'{pais}'}})")
    
    for cidade in cidades:
        print(f"CREATE({cidade}:Cities {{name:'{cidade}'}})")
        
    
if __name__ == "__main__":
    main()