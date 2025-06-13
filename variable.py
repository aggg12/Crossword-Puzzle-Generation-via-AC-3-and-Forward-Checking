###ALEJANDRO GARCIA GIL 77042008N
class Variable:
    def __init__(self,tamanyo,posi,posf,dom,ori,nume):
        self.tam=tamanyo
        self.posIni=posi
        self.posFin=posf
        self.dom=dom
        self.podas=[]
        self.orientation=ori
        self.valorActual=None
        self.nombre=nume
        self.restriccion=[]
    
    def impVariableAux(self):
        print('Nombre '+str(self.nombre)+' Posición '+str(self.valorActual)+', '+str(self.tam)+', ('+str(self.posIni)+','+str(self.posFin)+'), '+str(self.dom.getLista())+', '+str(self.orientation))
    
    def impVariable(self):
        if self.orientation == 'h':
            print('Nombre ' + str(self.nombre)+' Posición '+ str(self.posIni[0]) + ' ' + str(self.posIni[1]) + ' Tipo: horizontal Dominio: ' + str(self.dom.getLista()))
        else:
            print('Nombre ' + str(self.nombre)+' Posición '+ str(self.posIni[0]) + ' ' + str(self.posIni[1]) + ' Tipo: vertical Dominio: ' + str(self.dom.getLista()))

    def primeraPos(self):
        return self.posIni
    
    def ultimaPos(self):
        return self.posFin
    
    def getNombre(self):
        return self.nombre
    
    def setDom(self,dom):
        self.dom=dom
        
    def getDominio(self):
        return self.dom.getLista()
    
    def getRestricciones(self):
        return self.restriccion
    
    def getValorActual(self):
        return self.valorActual
    
    def getPodas(self):
        return self.podas
    
    def addDominio(self, dom):
        self.dom.addPal(dom)
    
    def borrarDom(self,val,causa):
        self.dom.delete(val)
        self.podas.append((val, causa))

    def addRestriccion(self, restriccion):
        self.restriccion.append(restriccion)
    
    def printRestriccion(self):
        for i in self.restriccion:
            i.printRest()
    
    def getTam(self):
        return self.tam

    def deletePoda(self, variable):
        for i in self.podas.copy():
            if i[0]==variable:
                self.podas.remove(i)
                break
        
    def setValorActual(self, val):
        self.valorActual=val

    def getOrientation(self):
        return self.orientation
    
    def setNewDominio(self, domi):
        nueva_lista = [palabra for palabra in self.dom.getLista() if palabra not in domi]
        for i in nueva_lista:
            self.deleteDominio(i)

    
