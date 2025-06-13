###ALEJANDRO GARCIA GIL 77042008N
import pygame
import tkinter
import cProfile
import queue
from tkinter import *
from tkinter.simpledialog import *
from tkinter import messagebox as MessageBox
from tablero import *
from dominio import *
from variable import *
from restricciones import *
from pygame.locals import *

GREY=(190, 190, 190)
NEGRO=(100,100, 100)
BLANCO=(255, 255, 255)

MARGEN=5 #ancho del borde entre celdas
MARGEN_INFERIOR=60 #altura del margen inferior entre la cuadrícula y la ventana
TAM=60  #tamaño de la celda
FILS=5 # número de filas del crucigrama
COLS=6 # número de columnas del crucigrama

LLENA='*' 
VACIA='-'

#########################################################################
# Detecta si se pulsa el botón de fc
######################################################################### 
def pulsaBotonfc(pos, anchoVentana, altoVentana):
    if pos[0]>=anchoVentana//4-25 and pos[0]<=anchoVentana//4+25 and pos[1]>=altoVentana-45 and pos[1]<=altoVentana-19:
        return True
    else:
        return False
    
######################################################################### 
# Detecta si se pulsa el botón de AC3
######################################################################### 
def pulsaBotonAC3(pos, anchoVentana, altoVentana):
    if pos[0]>=3*(anchoVentana//4)-25 and pos[0]<=3*(anchoVentana//4)+25 and pos[1]>=altoVentana-45 and pos[1]<=altoVentana-19:
        return True
    else:
        return False
    
######################################################################### 
# Detecta si se pulsa el botón de reset
######################################################################### 
def pulsaBotonReset(pos, anchoVentana, altoVentana):
    if pos[0]>=(anchoVentana//2)-25 and pos[0]<=(anchoVentana//2)+25 and pos[1]>=altoVentana-45 and pos[1]<=altoVentana-19:
        return True
    else:
        return False
##########################################################################
# realizo aqui forward
##########################################################################
def forchecking(variables,guia):
    for i in range(guia+1,len(variables)):
        vacio=True
        for fact in variables[i].getDominio().copy():
            if restr(variables[i].getRestricciones(),fact):
                vacio=False
            else:
                variables[i].borrarDom(fact,variables[guia].getNombre())
        if vacio:
            return False
    return True
    
######################################################################### 
# Detecta si el ratón se pulsa en la cuadrícula
######################################################################### 
def inTablero(pos):
    if pos[0]>=MARGEN and pos[0]<=(TAM+MARGEN)*COLS+MARGEN and pos[1]>=MARGEN and pos[1]<=(TAM+MARGEN)*FILS+MARGEN:        
        return True
    else:
        return False
    
######################################################################### 
# Busca posición de palabras de longitud tam en el almacen
######################################################################### 
def busca(almacen, tam):
    enc=False
    pos=-1
    i=0
    while i<len(almacen) and enc==False:
        if almacen[i].tam==tam: 
            pos=i
            enc=True
        i=i+1
    return pos
    
######################################################################### 
# Crea un almacen de palabras
######################################################################### 
def creaAlmacen():
    muestra= open('20k.txt','r',encoding="utf-8")
    lista=muestra.read()
    muestra.close()
    listaPal=lista.split()
    almacen=[]
    for pal in listaPal:        
        pos=busca(almacen, len(pal)) 
        if pos==-1:
            control=Dominio(len(pal))
            control.addPal(pal.upper())            
            almacen.append(control)
        elif pal.upper() not in almacen[pos].lista:       
            almacen[pos].addPal(pal.upper())           
    return almacen
######################################################################### 
# Imprime todo el contenido del almacen
######################################################################### 
def impAlm(almacen):
    for control in almacen:
        print (control.tam)
        all=control.getLista()
        for pal in all:
            print(pal,end=" ")
        print()
##########################################################################
# fc
##########################################################################
def fc(variables,guia):
    if guia==len(variables):
            return True
    for i in variables[guia].getDominio().copy():
        variables[guia].setValorActual(i)
        if forchecking(variables, guia):
            if fc(variables, guia + 1):
                return True
        change(variables, guia)
        variables[guia].setValorActual(None)
    return False   
#########################################################################
# Imprimir por pantalla
#########################################################################
def impPan(tablero,variables):
    for i in variables:
        if i.getOrientation()=='h':
            pos=i.primeraPos()[1]
            while pos<=i.ultimaPos()[1]:
                tablero.setCelda(i.primeraPos()[0],pos,i.getValorActual()[pos-i.primeraPos()[1]])
                pos=pos+1
        else:
            pos=i.primeraPos()[0]
            while pos<=i.ultimaPos()[0]:
                tablero.setCelda(pos,i.primeraPos()[1],i.getValorActual()[pos-i.primeraPos()[0]])
                pos=pos+1


##########################################################################
# FORWARD RESTRICCIONES
##########################################################################
def restr(restricciones,palabra):
    for rest in restricciones:
        if rest.getV2().getValorActual()==None:
            continue
        if letPosition(rest.getPos(),rest.getV2())!=palPosition(rest.getPos(),palabra,rest.getV1()):
            return False
    return True

##########################################################################
# AC3
##########################################################################
def AC3(restricciones):
    
    while restricciones!=[]:
        rest=restricciones.pop(0)
        cambio=False
        for i in rest.getV1().getDominio().copy():
            if not fixed(i,rest.getV2().getDominio(),rest.getPos(),rest.getV1(),rest.getV2()):
                rest.getV1().borrarDom(i,rest.getV2().getNombre())
                cambio=True
        if rest.getV1().getDominio()==[]:
            return False
        if cambio:
            for i in rest.getV1().getRestricciones():
                if i.getV1()==rest.getV1():
                    restricciones.append(i)
    return True

##########################################################################
# consistencia posicion palabra
##########################################################################
def fixed(palabra,dominio,posicion,v1,v2):
    for i in dominio:
        if palPosition(posicion,palabra,v1)==palPosition(posicion,i,v2):
            return True
    return False
##########################################################################
# CREAR VARIABLES
##########################################################################
def crearVariables(tablero, almacen):
    aux=0
    nume=0
    variables=[]
    reestricciones=[]
    for fil in range(tablero.getAlto()):
        for col in range(tablero.getAncho()):
            listaLetras=[]
            if aux!=0:
                aux=aux-1
                continue
            if tablero.getCelda(fil,col)!=LLENA:
                colAux=col
                while col!=tablero.getAncho() and tablero.getCelda(fil,col)!=LLENA:
                    col=col+1
                    aux=col-colAux
                    if tablero.getCelda(fil,col-1)!=VACIA:
                        listaLetras.append((aux-1,tablero.getCelda(fil,col-1).upper()))
                for i in almacen:
                    if i.getTam()==aux: control=i
                if listaLetras!=[]:
                    domAux=[palabra for palabra in control.getLista() if all(len(palabra) > pos and palabra[pos]==letra for pos,letra in listaLetras)]
                    domActualizado=Dominio(len(domAux))
                    for palabra in domAux:
                        domActualizado.addPal(palabra)
                else:domActualizado=control.copy()
                if aux == 1:
                    
                    val=checkAlo(variables,domActualizado,tablero,fil,colAux,nume)
                    if val: nume=nume+1
                    continue
                nume=nume+1
                variables.append(Variable(aux,(fil,colAux),(fil,col-1),domActualizado,'h',nume))
        if aux != 0: aux = 0
    for col in range(tablero.getAncho()):
        for fil in range(tablero.getAlto()):
            listaLetras = []
            if aux != 0:
                aux = aux - 1
                continue
            if tablero.getCelda(fil,col)!=LLENA:
                filAux = fil
                while fil != tablero.getAlto() and tablero.getCelda(fil,col)!=LLENA:
                    fil = fil + 1
                    aux = fil - filAux
                    if tablero.getCelda(fil-1,col)!=VACIA:
                        listaLetras.append((aux-1,tablero.getCelda(fil-1,col).upper()))
                if aux == 1:
                    continue
                for i in almacen:
                    if i.getTam()==aux: control=i
                if listaLetras!=[]:
                    domAux=[palabra for palabra in control.getLista() if all(len(palabra) > pos and palabra[pos]==letra for pos,letra in listaLetras)]
                    domActualizado=Dominio(len(domAux))
                    for palabra in domAux:
                        domActualizado.addPal(palabra)
                else:
                    domActualizado = control.copy()
                    nume=nume+1
                    varVertical=Variable(aux,(filAux,col),(fil-1,col),domActualizado,'v',nume)
                    addRestr(variables,reestricciones,col,varVertical)
                    variables.append(varVertical)
                if aux!=0: aux=0
                
        return variables,reestricciones
##########################################################################
# change
##########################################################################
def change(variables,guia):
    for j in range(guia+1,len(variables)):
        for b in variables[j].getPodas().copy():
            if b[1]==variables[guia].getNombre():
                variables[j].addDominio(b[0])
                variables[j].deletePoda(b[0])


##########################################################################
# Añadir crear restricciones
##########################################################################
def addRestr(variables,reestricciones,col,vertical):
    for var in variables:
        if var.getOrientation()=='h':
            posIni=(var.primeraPos()[0],var.primeraPos()[1])
            posFin=(var.ultimaPos()[0],var.ultimaPos()[1]+1)
            while posIni!=posFin:
                if posIni[1]==col and posIni[0]>=vertical.primeraPos()[0] and posIni[0]<=vertical.ultimaPos()[0]:
                    restriccion1=Reestriciones(var,vertical,var.primeraPos()[0],col)
                    restriccion2=Reestriciones(vertical,var,var.primeraPos()[0],col)
                    var.addRestriccion(restriccion1)
                    vertical.addRestriccion(restriccion2)
                    reestricciones.append(restriccion1)
                    reestricciones.append(restriccion2)
                    break
                posIni=(posIni[0],posIni[1]+1)




##########################################################################
# LETRA SEGUN POSICION (VARIABLE)
##########################################################################
def letPosition(posicion, palabra):
    if palabra.getOrientation() == 'h':
        return palabra.getValorActual()[posicion[1]-palabra.primeraPos()[1]]
    else:
        return palabra.getValorActual()[posicion[0]-palabra.primeraPos()[0]]

##########################################################################
# LETRA SEGUN POSICION (PALABRA)
##########################################################################
def palPosition(posicion,palabra,variable):
    if variable.getOrientation()=='h':
        pos=posicion[1]-variable.primeraPos()[1]
    else:
        pos=posicion[0]-variable.primeraPos()[0]
    return palabra[pos]

##########################################################################
# Palabras en los dominios guiado segun la letra
##########################################################################
def letInDom(letra, palabra, posicion):
    if 0 <= posicion < len(palabra) and palabra[posicion]==letra:
        return palabra


                    
    

##########################################################################
# Comprobar las aisladas (arriba tambien se usa)
##########################################################################
def checkAlo(variables,i,tablero,fil,col,nume):
    val=False
    if fil==0 and tablero.getCelda(fil+1,col)==LLENA:    
        val=True
    elif fil==tablero.getAlto()-1 and tablero.getCelda(fil-1,col)==LLENA:
        val=True
    elif tablero.getCelda(fil-1,col)==LLENA and tablero.getCelda(fil+1,col)==LLENA:
        val=True
    if val:
        nume=nume+1
        variables.append(Variable(1,(fil,col),(fil,col),i,'a',nume))
    return val

##########################################################################
# Imprimir ac3
##########################################################################
def AC3Print(variables, restricciones):
    for i in variables:
        i.impVariable()
    if AC3(restricciones):
        for i in variables:
            i.impVariable()
        return True

def AC3Aux(variables,guia):
    for rest in variables[guia].getRestricciones():
        vacio=True
        j=rest.getV2().getNombre()-1
        letraV1=letPosition(rest.getPos(),variables[guia])
        for i in variables[j].getDominio().copy():
            letraV2=palPosition(rest.getPos(),i,variables[j])
            if letraV1==letraV2:
                vacio=False
            else:
                variables[j].borrarDom(i,variables[guia].getNombre())
        if vacio:
            return False
    return True
#########################################################################  
# Principal
#########################################################################
def main():
    root= tkinter.Tk() #para eliminar la ventana de Tkinter
    root.withdraw() #se cierra
    pygame.init()
    
    reloj=pygame.time.Clock()
    
    anchoVentana=COLS*(TAM+MARGEN)+MARGEN
    altoVentana= MARGEN_INFERIOR+FILS*(TAM+MARGEN)+MARGEN
    
    dimension=[anchoVentana,altoVentana]
    screen=pygame.display.set_mode(dimension) 
    pygame.display.set_caption("Practica 1: Crucigrama")
    
    botonfc=pygame.image.load("botonfc.png").convert()
    botonfc=pygame.transform.scale(botonfc,[50, 30])
    
    botonAC3=pygame.image.load("botonAC3.png").convert()
    botonAC3=pygame.transform.scale(botonAC3,[50, 30])
    
    botonReset=pygame.image.load("botonReset.png").convert()
    botonReset=pygame.transform.scale(botonReset,[50,30])
    almacen=creaAlmacen()
    game_over=False
    tablero=Tablero(FILS, COLS)
    AC3_activo=False    
    while not game_over:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:               
                game_over=True
            if event.type==pygame.MOUSEBUTTONUP:                                               
                pos=pygame.mouse.get_pos()                
                if pulsaBotonfc(pos, anchoVentana, altoVentana):
                    if not AC3_activo:
                        variables, restricciones=crearVariables(tablero, almacen)
                    print("fc")
                    profiler = cProfile.Profile()
                    profiler.enable()
                    res=fc(variables, 0)
                    profiler.disable()
                    profiler.print_stats()
                    if res==False:
                        MessageBox.showwarning("Alerta","No hay solución")     
                    if res==True:
                        impPan(tablero,variables)
                        MessageBox.showwarning("Correcto","Excelente") 
                        print("Variables: ")
                        for i in variables:
                            i.impVariable()
                            i.printRestriccion()                  
                elif pulsaBotonAC3(pos, anchoVentana, altoVentana):
                    AC3_activo=True                    
                    print("AC3")
                    variables, restricciones=crearVariables(tablero, almacen)
                    res=AC3Print(variables, restricciones)
                elif pulsaBotonReset(pos, anchoVentana, altoVentana):                   
                    tablero.reset()
                elif inTablero(pos):
                    colDestino=pos[0]//(TAM+MARGEN)
                    filDestino=pos[1]//(TAM+MARGEN)                    
                    if event.button==1:
                        if tablero.getCelda(filDestino, colDestino)==VACIA:
                            tablero.setCelda(filDestino, colDestino, LLENA)
                        else:
                            tablero.setCelda(filDestino, colDestino, VACIA)
                    elif event.button==3:
                        c=askstring('Entrada', 'Introduce carácter')
                        tablero.setCelda(filDestino, colDestino, c.upper())   
            
        ##código de dibujo        
        #limpiar pantalla
        screen.fill(NEGRO)
        pygame.draw.rect(screen, GREY, [0, 0, COLS*(TAM+MARGEN)+MARGEN, altoVentana],0)
        for fil in range(tablero.getAlto()):
            for col in range(tablero.getAncho()):
                if tablero.getCelda(fil, col)==VACIA: 
                    pygame.draw.rect(screen, BLANCO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                elif tablero.getCelda(fil, col)==LLENA: 
                    pygame.draw.rect(screen, NEGRO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                else: #dibujar letra                    
                    pygame.draw.rect(screen, BLANCO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                    fuente= pygame.font.Font(None, 70)
                    texto= fuente.render(tablero.getCelda(fil, col), True, NEGRO)            
                    screen.blit(texto, [(TAM+MARGEN)*col+MARGEN+15, (TAM+MARGEN)*fil+MARGEN+5])                     
        screen.blit(botonfc, [anchoVentana//4-25, altoVentana-45])
        screen.blit(botonAC3, [3*(anchoVentana//4)-25, altoVentana-45])
        screen.blit(botonReset, [anchoVentana//2-25, altoVentana-45])
        #actualizar pantalla
        pygame.display.flip()
        reloj.tick(40)
        if game_over==True:
            pygame.time.delay(500)
    
    pygame.quit()
 
if __name__=="__main__":
    main()
