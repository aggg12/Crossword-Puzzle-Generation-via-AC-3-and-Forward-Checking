###ALEJANDRO GARCIA GIL 77042008N
import variable
class Reestriciones:
    def __init__(self, v1, v2, fil, col):
        self.v1=v1
        self.v2=v2
        self.fil=fil
        self.col=col

    def printRest(self):
        print(str(self.v1.getNombre())+', '+str(self.v2.getNombre())+', '+str(self.fil)+', '+str(self.col))
    def getV1(self):
        return self.v1
    def getV2(self):
        return self.v2
    def getPosRestV1(self):
        if self.v1.getOrientation() == 'h':
            return self.col - self.v1.getPos()[1]
        else:
            return self.fil - self.v1.getPos()[0]
    def getPosRestV2(self):
        if self.v2.getOrientation()=='h':
            return self.col-self.v2.getPos()[1]
        else:
            return self.fil - self.v2.getPos()[0]

    def getFil(self):
        return self.fil
    def getCol(self):
        return self.col
    def getPos(self):
        return (self.fil, self.col)
    
