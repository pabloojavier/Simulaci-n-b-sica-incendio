import matplotlib.pyplot as plt
from matplotlib import colors
import time
import random

def reemplazar(datos,x,y):
    """
    Reemplaza x por y
    """
    if type(datos[0]=="list"):
        for i in range(len(datos)):
            for j in range(len(datos)):
                if datos[i][j] == x: datos[i][j] =  y
    else:
        for i in range(len(datos)):
            if datos[i] == x : datos[i] = y

def utext(s):
    return '\033[4m'+s+'\033[0m'

def btext(s):
    return '\033[1m'+s+'\033[0m'

class Bosque:
    def __init__(self,archivo):
        archivo = open(archivo,mode="r")
        lineas = [linea.split() for linea in archivo]
        self.instante = 0
        self.n = int(lineas[0][0])
        self.inicioX = int(lineas[1][0])
        self.inicioY = int(lineas[1][1])
        self.viento = Viento([(i[0],i[1]) for i in lineas[2]])
        self.datos = lineas[3:]

        if len(self.datos)!= self.n:
            print("n no coincide con el orden de la matriz.")
            print("Se continuará con el orden de la matriz dada.")
            self.n = len(self.datos)

        if sum(list(map(lambda x: len(x),self.datos))) != self.n**2:
            print("Faltan datos en la matriz bosque.")
            print("FIN")
            exit(0)

        if self.inicioX <0 or self.inicioX>=self.n:
            print("Coordenada X de inicio del fuego mal ingresada")
            print(f"Tiene que ser un valor en el intervalo [0,{self.n-1}]")
            print("Fin")
            exit(0)
        
        if self.inicioY <0 or self.inicioY>=self.n:
            print("Coordenada Y de inicio del fuego mal ingresada")
            print(f"Tiene que ser un valor en el intervalo [0,{self.n-1}]")
            print("Fin")
            exit(0)

        reemplazar(self.datos,"x",0)
        reemplazar(self.datos,"+",1)
        reemplazar(self.datos,"*",2)
        reemplazar(self.datos,"-",3)
        reemplazar(self.datos,"o",4)
        self.quemandoseX = [self.inicioX]
        self.quemandoseY = [self.inicioY]
        self.proximos = []
        archivo.close()

    def mostrar(self,instante,boolean=True):
        direccion = self.viento.direccion(instante)
        magnitud = self.viento.magnitud(instante)
        c_quemado = (191/256,127/256,64/256) #0
        #Gris 1 
        c_arbol = (2/256,255/256,0) #2
        c_fuego = (255/256,0,0) #3
        c_nada = (233/256,210/256,188/256) #4
        cmap = colors.ListedColormap([c_quemado,"gray",c_arbol,c_fuego,c_nada])
        bounds=[-0.5, 0.5, 1.5, 2.5, 3.5,4.5]
        norm = colors.BoundaryNorm(bounds, cmap.N)
        plt.pcolor(self.datos[::-1], cmap=cmap, norm=norm)
        plt.title(f"Tarea 1 PAII\nInstante {self.instante}")
        plt.xticks([])
        plt.yticks([])
        plt.suptitle(f"Magnitud: {magnitud}\nDirección: {direccion}",x=0.5,y=0.1)
        if boolean == True:
            plt.show()
        else:
            if len(self.quemandoseX)!=0:
                plt.show(block=False)
                plt.pause(0.001)
                plt.close()
            else:
                plt.show()

    def empezar_fuego(self):
        try:
            if self.inicioY>=0 and self.inicioY<self.n and self.inicioX>=0 and self.inicioX<self.n:
                self.datos[self.inicioY][self.inicioX] = 3

        except IndexError:
            print("Fuera de la matriz")
        except:
            raise

    def actualizar_viento(self,instante):    

        x = self.quemandoseX
        y = self.quemandoseY
        direccion = self.viento.direccion(instante)
        magnitud = self.viento.magnitud(instante)
        try:
            for i in range(len(x)):
                if direccion in ["n","s","o","e"] and magnitud==0:
                    for j in range(9):
                        if (x[i]-j//3+1,y[i]+j%3-1) != (x[i],y[i]) and x[i]-j//3+1>=0 and x[i]-j//3+1< self.n and y[i]+j%3-1 >=0 and y[i]+j%3-1<self.n:
                            if x[i]>=0 and x[i]<self.n and y[i]>=0 and y[i]<self.n:
                                if self.datos[y[i]+j%3-1][x[i]-j//3+1] == 2:
                                    self.datos[y[i]+j%3-1][x[i]-j//3+1] = 1
                                    self.proximos.append((y[i]+j%3-1,x[i]-j//3+1))
                                    #Todos los if pudieron estar en una linea pero me queda más comodo verlo así.

                elif (direccion =="n" or direccion =="s") and magnitud in [1,2]:
                    a = 1 if direccion =="n" else -1
                    if x[i]>=0 and x[i]< self.n and y[i]>=0 and y[i]<self.n:
                        self.__comprobar_viento(x[i]+1,y[i])
                        self.__comprobar_viento(x[i]-1,y[i])
                        for j in range(1,magnitud+1):
                            self.__comprobar_viento(x[i]+1,y[i]-a*j)
                            self.__comprobar_viento(x[i],y[i]-a*j)
                            self.__comprobar_viento(x[i]-1,y[i]-a*j)

                elif (direccion =="e" or direccion=="o") and magnitud in [1,2]:
                    a = 1 if direccion =="o" else -1
                    if x[i]>=0 and x[i]< self.n and y[i]>=0 and y[i]<self.n:
                        self.__comprobar_viento(x[i],y[i]+1)
                        self.__comprobar_viento(x[i],y[i]-1)
                        for j in range(1,magnitud+1):
                            self.__comprobar_viento(x[i]-a*j,y[i]+1)
                            self.__comprobar_viento(x[i]-a*j,y[i])
                            self.__comprobar_viento(x[i]-a*j,y[i]-1)
                else:
                    raise ValueError

            for i in range(len(x)):
                self.datos[y[i]][x[i]] == 3
            
        except ValueError:
            print(f"Dirección o magnitud mal ingresada en instante {instante}")
        except:
            pass

        self.instante+=1

    def __comprobar_viento(self,x,y):
        #Comprueba los limites, si estan bien, quema el arbol
        if x>=0 and x<self.n and y>=0 and y<self.n:
            if self.datos[y][x]==2:
                self.datos[y][x]= 1
                self.proximos.append((y,x))

    def actualizar_fuego(self):
        #quemando pasan a estar quemados
        for i in range(len(self.quemandoseX)):
            self.datos[self.quemandoseY[i]][self.quemandoseX[i]] = 0

        self.quemandoseX = []
        self.quemandoseY = []

        #proximos a quemar pasan a quemando
        for i in range(len(self.proximos)):
            if random.uniform(0,1)<0.4:
                self.datos[self.proximos[i][0]][self.proximos[i][1]] = 3
                self.quemandoseY.append(self.proximos[i][0])
                self.quemandoseX.append(self.proximos[i][1])
            else:
                self.datos[self.proximos[i][0]][self.proximos[i][1]] = 2
        self.proximos = []
        self.instante+=1

class Viento:
    def __init__(self,cambios):
        self.cambios = cambios

    def magnitud(self,t):
        try:
            return int(self.cambios[t][0])
        except IndexError:
            try:
                return self.magnitud(-1) #Intenta devolver el ultimo
            except:
                print("Faltan datos para el viento, se usará magnitud 0")
                return 0 #En caso de que no hayan datos, devuelve 0 para que continúe el programa
        except ValueError:
            #Si no se ingresa un numero correcto, prueba el siguiente
            return self.magnitud(t+1)
            
    def direccion(self,t):
        try:
            return self.cambios[t][1]
        except IndexError:
            try:
                return self.direccion(-1) 
            except:
                print("Faltan datos para la dirección del viento, se usará norte")
                return "n"

print("\nSi quiere generar un archivo aleatorio ingrese 0.")
print("Para iniciar bosque.dat, ingrese 1")
tipo_archivo = (input("Ingrese tipo de archivo (0/1): "))
while True:
    try:
        tipo_archivo = int(tipo_archivo)
        if tipo_archivo not in [0,1]:
            raise
        break
    except:
        print("\nValor mal ingresado, intentelo denuevo")
        tipo_archivo = (input("Ingrese tipo de archivo (0/1): "))
#tipo_archivo = 0

if tipo_archivo==0:
    from generador import *
    print("\nGenerando archivo aleatorio")
    print("...")
    crear_archivo()
    bosque = Bosque("aleatorio.txt")
    print("Finalizado\n")
else:
    print("\nCargando archivo bosque")
    print("...")
    bosque = Bosque("/Users/pablogutierrezaguirre/OneDrive - Universidad de Concepción/Material UdeC/Cuarto año/Octavo semestre/Programación aplicada a la ingeniería industrial/Tarea 1/Gutierrez_Aguirre_P/bosque.dat")
    print("Finalizado\n")

print(utext("Modos de visualización"))
print("-Para ver el ultimo instante, ingresar -2")
print("-Para ver como evoluciona el fuego ingrese -1 ")
print("-Para ver un instante dado, ingrese el instante")
modo = input("Ingrese: ")
while True:
    try:
        modo = int(modo)
        if modo <-2:
            raise
        else:
            break
    except:
        print("Por favor ingrese una opción valida")
        modo = input("Ingrese:")


print("\nEmpezando simulación\n")
inicio = time.time()
if modo ==-1:
    i = 0
    bosque.empezar_fuego()
    bosque.mostrar(i,False)
    while True:
        if len(bosque.quemandoseX) !=0:
            bosque.actualizar_viento(i)
            i+=1
            bosque.mostrar(i,False)
            bosque.actualizar_fuego()
            final = time.time()
            bosque.mostrar(i,False)
        else:
            break

else:
    i = 0
    bosque.empezar_fuego()
    while True:
        if modo != 0:
            bosque.actualizar_viento(i)
            if bosque.instante==modo:
                final = time.time()
                bosque.mostrar(bosque.instante)
                break
            i+=1
            bosque.actualizar_fuego()
            if bosque.instante==modo:
                final = time.time()
                bosque.mostrar(bosque.instante)
                break

            if len(bosque.quemandoseX)==0 and modo == -2:
                #bosque.instante = modo
                final = time.time()
                bosque.mostrar(bosque.instante)
                break
            
            elif len(bosque.quemandoseX)==0:
                bosque.instante = modo
                final = time.time()
                bosque.mostrar(bosque.instante)
                break
        else:
            final = time.time()
            bosque.mostrar(modo)
            break

# try:
#     import os
#     os.remove("aleatorio.txt")
# except:
#     pass

print("Simulación terminada")
print(f"Tiempo: {final-inicio}")
if modo != -1:
    print("El tiempo que se demora en graficar no está incluido")
