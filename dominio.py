###ALEJANDRO GARCIA GIL 77042008N
# Un objeto de esta clase está formado por un número (tamaño) y
# una lista de palabras que tienen un número de caracteres igual al tamaño
class Dominio:
    def __init__(self, tam):
        self.tam=tam
        self.lista=[]
    def copy(self):
        dom=Dominio(self.tam)
        dom.lista=list(self.lista)
        return dom
    def addPal(self, pal):
        self.lista.append(pal)
    
    def delete(self, val):
        self.lista.remove(val)
        
    def getTam(self):
        return self.tam
    
    def getLista(self):
        return self.lista
    
    

