import os
from estructuras import MBR
import singleton

class mountid:
    
    def __init__(self, idmount,path,name):
        self.idmount = idmount
        self.path = path
        self.name = name
    

class mount:

    def __init__(self):
        self.path = ""
        self.name = ""

    def make_mount(self):
        #SI EL PARAMETRO NO ESTA VACIO
        if(self.path != "" and self.name != ""):
            # VERIFICAR EXISTENCIA DE PATH
            if(self.verificarDirectorio()):
                mbr = self.obtener_mbr()
                # VERIFICAR EXISTENCIA DE NOMBRE DE PARTICION
                if(self.buscar_particion(self.name,mbr)):
                    position = self.obtener_position(mbr,self.name) + 1
                    directorio = os.path.split(self.path)
                    disklist = directorio[1].split('.')
                    disk = disklist[0]
                    #NUMERO DE CARNET 201602659
                    idM = "59"+str(position)+disk
                    new_mount = mountid(idM,self.path,self.name)
                    #METODO VERIFICA LA NO EXISTENCIA DE IDMOUNT Y LAS GUARDA
                    self.insertar_mount(new_mount)
                else:
                    singleton.objL.respuesta['mensaje']+= ">>>>Error: NO existe una partición con ese nombre>>>>"+"\n"
                    print("*****************************************************************************")
            else:
                singleton.objL.respuesta['mensaje']+= ">>>>Error: No se encontró el disco>>>>"+"\n"
                print("*****************************************************************************")
        else:
            singleton.objL.respuesta['mensaje']+= ">>>>Error: parámetros obligatorios: path y name>>>>"+"\n"
            print("*****************************************************************************")
    
    def insertar_mount(self, mountid):
        if(singleton.objL.list_Mounts):
            est = 0
            for m in singleton.objL.list_Mounts:
                #VALIDA QUE NO ESTE EN LA LISTA
                if(m.idmount == mountid.idmount):
                    est = 1
                    singleton.objL.respuesta['mensaje']+= ">>>>Error: Esta partición ya está Montada>>>>"+"\n"
                    print("*****************************************************************************")
                    break
            if(est == 0):
                #INSERTA
                singleton.objL.list_Mounts.append(mountid)
                self.recorrer()
                singleton.objL.respuesta['mensaje']+= ">>>>Partición Montada exitosamente!>>>>"+"\n"
                print("*****************************************************************************")
        else:
            #SOLO LO INSERTA
            singleton.objL.list_Mounts.append(mountid)
            self.recorrer()
            singleton.objL.respuesta['mensaje']+= ">>>>Partición Montada exitosamente!>>>>"+"\n"
            print("*****************************************************************************")
                
    def verificarDirectorio(self):
        self.arreglar_Directorio()
        try:
            with open(self.path, "rb+") as file:
                file.close()
                return True
        except:
            return False
    
    def arreglar_Directorio(self):
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
                list_dir.insert(2,"cecic")
                list_dir.remove(list_dir[0])
                for l in list_dir:
                    palabra = palabra +"/"+ l
                self.path = palabra

    def obtener_mbr(self):
        mbr = MBR(0,0,0,' ')
        bytes = mbr.get_bytes()
        mbr_aux = MBR(0,0,0,' ')
        with open(self.path, "rb+") as file:
            bytes_obtenidos = file.read(len(bytes))
            mbr_aux.set_bytes(bytes_obtenidos)
        return mbr_aux
    
    def buscar_particion(self, nombre, mbr):
        nombre = nombre.replace("\"","")
        nombre = self.ajustar_cadena(16,nombre)
        for part in mbr.partitions:
            if(part.name == nombre):
                return True
        return False
  
    def obtener_position(self, mbr, nombre):
        part_position = 0
        nombre = nombre.replace("\"","")
        nombre = self.ajustar_cadena(16,nombre)
        self.name = nombre
        for part in mbr.partitions:
            if(part.name == nombre):
                break
            part_position+=1
        return part_position
    
    def ajustar_cadena(self,tam,cadena):
        if(len(cadena)<tam):
            dif = tam-len(cadena)
            for i in range(0,dif):
                cadena = cadena + " "
        if(len(cadena)>tam):
            new_cadena = ""
            for i in range(0,tam):
                new_cadena = new_cadena + cadena[i]
            cadena = new_cadena
        return cadena
    
    def recorrer(self):
        if(singleton.objL.list_Mounts):
            for m in singleton.objL.list_Mounts:
                singleton.objL.respuesta['mensaje']+= m.idmount+"-->"
            singleton.objL.respuesta['mensaje']+= ""+"\n"
        else:
            singleton.objL.respuesta['mensaje']+= "sin ids mount"+"\n"
    

