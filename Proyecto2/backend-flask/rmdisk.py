from os import remove
import os
import singleton

class rmdisk:

    def __init__(self):
        self.path = "" #string
        self.resp = "" #string

    def make_rmdisk(self):
        #SI EL PARAMETRO NO ESTA VACIO
        if(self.path != ""):
            # VERIFICAR EXISTENCIA DE PATH
            if(self.verificarDirectorio()):
                #CONFIRMAR ELIMINACION
                self.confirmar_eliminacion()
            else:
                singleton.objL.respuesta['mensaje']+= ">>>>Error: No se encontró el disco>>>>\n"
                print("*****************************************************************************")
        else:
            singleton.objL.respuesta['mensaje']+= ">>>>Error: parámetro obligatorio: path>>>>\n"
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
                list_dir[2] = "ubuntu"
                list_dir.remove(list_dir[0])
                for l in list_dir:
                    palabra = palabra +"/"+ l
                self.path = palabra
                palabra = ""
        list_dir = self.path.split('/')
        if(list_dir[1]  == "home"):
            if(list_dir[2] != "ubuntu"):
                list_dir.insert(2,"ubuntu")
                list_dir.remove(list_dir[0])
                for l in list_dir:
                    palabra = palabra +"/"+ l
                self.path = palabra

    def confirmar_eliminacion(self):
        if(self.resp == ""):
            singleton.objL.respuesta['estado']= "201"
            singleton.objL.respuesta['mensaje']+= " Alerta!!, se necesita confirmación para eliminar disco..."+"\n"
        else:
            self.ejecutar_resp()
        
        
    def ejecutar_resp(self):
        if(self.resp == 'si'):
            os.remove(self.path)
            singleton.objL.respuesta['estado'] = "202"
            singleton.objL.respuesta['mensaje']+= ">>>>Disco eliminado exitosamente!>>>>\n"
            print("*****************************************************************************")
        elif(self.resp == 'no'):
            singleton.objL.respuesta['mensaje']+= ">>>>Eliminación del disco cancelada>>>>\n"
            print("*****************************************************************************")