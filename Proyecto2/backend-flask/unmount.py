from singleton import singleton
import singleton

class unmount:

    def __init__(self):
        self.idm = "" #string

    def make_unmount(self):
        #SI EL PARAMETRO NO ESTA VACIO
        if(self.idm != ""):
            #METODO VERIFICA LA EXISTENCIA DE IDMOUNT Y ELIMINA
            if(singleton.objL.list_Mounts):
                est = 0
                n = 0
                for m in singleton.objL.list_Mounts:
                    #VALIDA QUE NO ESTE EN LA LISTA
                    if(m.idmount == self.idm):
                        est = 1
                        singleton.objL.list_Mounts.pop(n)
                        self.recorrer()
                        singleton.objL.respuesta['mensaje']+= ">>>>Particion desmontada exitosamente!>>>>"+"\n"
                        print("*****************************************************************************")
                        break
                    n += 1
                if(est == 0):
                    singleton.objL.respuesta['mensaje']+= ">>>>Error: Esta Particion No esta montada, Id no existe.>>>>"+"\n"
                    print("*****************************************************************************")
            else:
                singleton.objL.respuesta['mensaje']+= ">>>>Error: Esta Particion No esta montada, Id no existe.>>>>"+"\n"
                print("*****************************************************************************")
        else:
            singleton.objL.respuesta['mensaje']+= ">>>>Error: parámetro obligatorio: id>>>>"+"\n"
            print("*****************************************************************************")
 
    def recorrer(self):
        if(singleton.objL.list_Mounts):
            for m in singleton.objL.list_Mounts:
                singleton.objL.respuesta['mensaje']+= m.idmount+"-->"
            singleton.objL.respuesta['mensaje']+= ""+"\n"
        else:
            singleton.objL.respuesta['mensaje']+= "sin ids mount"+"\n"
    