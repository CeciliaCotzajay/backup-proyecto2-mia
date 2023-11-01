import time
import random
from estructuras import MBR
import os
import singleton

class mkdisk:

    def __init__(self):
        self.size = 0 #int
        self.path = "" #string
        self.fit = ""   #string 2
        self.unit = '' #char

    def make_mkdisk(self):
        #SI LOS PARAMETROS OBLIGATORIOS NO ESTAN VACIOS
        if(self.size != 0 and self.path != ""):
            #SI EL TAMAÑO DEL DISCO ES MAYOR A 0
            if(self.size > 0):
                # VALIDACION DE FIT
                if(self.fit == ""):
                    self.fit = "ff"#FF
                if(self.fit == "bf" or self.fit == "ff" or self.fit == "wf"):
                    #VALIDACION DE UNIT
                    kb = 0
                    if(self.unit == "k"):
                        kb = 1024
                    elif(self.unit == "m"):
                        kb = 1024 * 1024
                    elif(self.unit == ""):
                        kb = 1024 * 1024 #m
                        self.unit = "m"
                    else:
                        singleton.objL.respuesta['mensaje']+= ">>>>Error: unit debe ser 'K' o 'M'..>>>>\n"
                        print("*****************************************************************************")
                    if(kb != 0):
                        # EXTRAIGO DIRECTORIO PARA VER SI EXISTE
                        self.verificarDirectorio()
                        # CREA DIRECTORIO EN CASO NO EXISTA
                        directorio = os.path.split(self.path)
                        os.makedirs(directorio[0], mode=0o777, exist_ok=True)
                        # CREO EL DISCO CON TODAS LAS VALIDACIONES
                        with open(self.path, "wb") as file:
                            for i in range(0,self.size):
                                file.write(b'\x00' * kb)
                            file.close()
                        self.inicializar_MBR(kb)
                        singleton.objL.respuesta['mensaje']+= ">>>>Disco creado exitosamente!>>>>\n"
                        print("*****************************************************************************")
                else:
                    singleton.objL.respuesta['mensaje']+= ">>>>Error: fit debe ser 'BF' o 'FF' o 'WF'..>>>>\n"
                    print("*****************************************************************************")
            else:
                singleton.objL.respuesta['mensaje']+= ">>>>Error: El disco no puede tener tamaño: " + self.size + ">>>>\n"
                print("*****************************************************************************")
        
        else:
            singleton.objL.respuesta['mensaje']+= ">>>>Error: parámetros obligatorios: size y path>>>>\n"
            print("*****************************************************************************")
            
    def verificarDirectorio(self):
        palabra = ""
        directorio = self.path.replace("\"","")
        self.path = directorio
        list_dir = directorio.split('/')
        if(list_dir[1]  != "home"):
            list_dir.insert(1,"home")
            list_dir.remove(list_dir[0])
            for l in list_dir:
                palabra = palabra +"/"+ l
            self.path = palabra
            palabra = ""
        if(list_dir[1]  == "home"):
            if(list_dir[2] == "user"):
                list_dir[2] = "cecic"
                list_dir.remove(list_dir[0])
                for l in list_dir:
                    palabra = palabra +"/"+ l
                self.path = palabra
                palabra = ""
        list_dir = self.path.split('/')
        if(list_dir[1]  == "home"):
            if(list_dir[2] != "cecic"):
                singleton.objL.respuesta['mensaje']+= ">Creando directorios\n"
                list_dir.insert(2,"cecic")
                #print("insertado, corregido")
                list_dir.remove(list_dir[0])
                for l in list_dir:
                    palabra = palabra +"/"+ l
                self.path = palabra
        #print(self.path)


    def inicializar_MBR(self,kb):
        date = self.obtener_time()
        sign = random.randint(0,100)
        nuevofit = self.fit[0]
        nuevo_size = self.size*kb
        with open(self.path, "rb+") as file:
            mbr = MBR(nuevo_size,date,sign,nuevofit)
            bytes = mbr.get_bytes()
            #print(bytes)
            #print(len(bytes))
            file.write(bytes)
        singleton.objL.respuesta['mensaje']+= "MBR inicializado correctamente!\n"
    
    def obtener_time(self):
        timeA = int(time.time())
        return timeA

    