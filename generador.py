import random
def crear_archivo():
    opciones = "***oo"
    direccion = "nseo"
    magnitud = "012"
    n = random.randint(15,200)
    #n=2000
    archivo = open("aleatorio.txt","w")
    archivo.write(str(n)+"\n")
    archivo.write(str(random.randint(0,n))+" "+str(random.randint(0,n))+"\n")
    palabra=""
    for i in range(0,random.randint(2,int(n*0.4))):
        palabra += (random.choice(magnitud)+random.choice(direccion)+" ")
    archivo.write(palabra+"\n")

    for i in range(n):
        palabra = ""
        for j in range(n):
            palabra+= random.choice(opciones)+" "
        archivo.write(palabra+"\n")
    archivo.close()
