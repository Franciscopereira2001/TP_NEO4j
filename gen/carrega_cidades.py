import json, os, chardet, random
from unidecode import unidecode

def normaliza_str(s):
    return unidecode(s).replace("-","_").replace(" ","_")

class Cidades:
    
    def __init__(self, file):
        self.enc = chardet.detect(open(os.path.dirname(__file__) + "/" + file, "rb").read())["encoding"]
        with open(os.path.dirname(__file__) + "/" + file, "r", encoding = self.enc) as f:
            self.raw = json.load(f)
             
    def get_distritos(self):
        distritos = []
        for i in self.raw:
            if i["level"] == 1:
                i["name"] = normaliza_str(i["name"])
                distritos.append(i)
        return distritos
    
    def get_cidades(self, distrito):
        cidades = []
        for i in self.raw:
            if i["level"] == 2 and str(i["code"]).startswith(str(distrito["code"])) and len(str(i["code"])) == 2 + len(str(distrito["code"])):
                i["name"] = normaliza_str(i["name"])
                cidades.append(i)
        return cidades

    def get_cidade_random(self):
        d = random.choice(self.get_distritos())
        c = random.choice(self.get_cidades(d))
        return c
        
        
def main():
    c = Cidades("cidades.json")
    print(c.get_distritos()[3])
    print(c.get_cidades(c.get_distritos()[0]))

if __name__ == "__main__":
    main()