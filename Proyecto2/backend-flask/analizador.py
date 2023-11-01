from mkdisk import mkdisk
from rmdisk import rmdisk
from fdisk import fdisk
from rep import rep
from mount import mount
from unmount import unmount
from mkfs import mkfs
import singleton

class analizador:

    def analizar_mkdisk(self, parametros):
        parametros.remove(parametros[0])
        #INICIALIZA EL DISCRO
        disco = mkdisk() 
        for p in parametros:
             #SE OBTIENE EL TIPO Y EL PARAMETRO ACTUAL
            param = p.split('=')
            tipo = param[0]
            valor = param[1]
             #VERIFICA CUAL PARAMETRO ES PARA INICIALIZAR EL OBTJETO (LOS PARAMETROS YA VIENEN EN LOWERCASE)
            if (tipo == "size"):
                disco.size = int(valor)
            elif (tipo == "path"):
                disco.path = valor 
            elif (tipo == "unit"):
                disco.unit = valor 
            elif (tipo == "fit"):
                disco.fit = valor 
            else:
                singleton.objL.respuesta['mensaje']+= ">>>>Error: parámetro no aceptado en 'mkdisk': "+valor.upper()+">>>>\n"
                print("*****************************************************************************")
         #SE CREA EL DISCO
        disco.make_mkdisk()

    def analizar_rmdisk(self, parametros):
        parametros.remove(parametros[0])
        #INICIALIZA EL DISCRO
        disco = rmdisk() 
        for p in parametros:
             #SE OBTIENE EL TIPO Y EL PARAMETRO ACTUAL
            param = p.split('=')
            tipo = param[0]
            valor = param[1]
             #VERIFICA CUAL PARAMETRO ES PARA INICIALIZAR EL OBTJETO (LOS PARAMETROS YA VIENEN EN LOWERCASE)
            if (tipo == "path"):
                disco.path = valor 
            else:
                singleton.objL.respuesta['mensaje']+= ">>>>Error: parámetro no aceptado en 'rmdisk': "+valor.upper()+">>>>\n"
                print("*****************************************************************************")
         #SE CREA EL DISCO
        disco.make_rmdisk()

    def analizar_fdisk(self, parametros):
        parametros.remove(parametros[0])
        #INICIALIZA LA PARTICION
        particion = fdisk() 
        try:
            for p in parametros:
                #SE OBTIENE EL TIPO Y EL PARAMETRO ACTUAL
                param = p.split('=')
                tipo = param[0]
                valor = param[1]
                #VERIFICA CUAL PARAMETRO ES PARA INICIALIZAR EL OBJETO (LOS PARAMETROS YA VIENEN EN LOWERCASE)
                if (tipo == "size"):
                    particion.size = int(valor)
                elif (tipo == "path"):
                    particion.path = valor 
                elif (tipo == "name"):
                    particion.name = valor 
                elif (tipo == "unit"):
                    particion.unit = valor
                elif (tipo == "type"):
                    particion.type = valor
                elif (tipo == "fit"):
                    particion.fit = valor 
                elif (tipo == "delete"):
                    particion.delete = valor 
                elif (tipo == "add"):
                    if(valor == ''):
                        valor = '0'
                    particion.add = int(valor)
                else:
                    singleton.objL.respuesta['mensaje']+= ">>>>Error: parámetro no aceptado en 'fdisk': "+valor.upper()+">>>>\n"
                    print("*****************************************************************************")
        except:
            singleton.objL.respuesta['mensaje']+= ">>>>Error: Recuperandose..>>>>\n"
            print("*****************************************************************************")
         #SE CREA LA PARTICION
        particion.make_fdisk()

    def analizar_rep(self, parametros):
        parametros.remove(parametros[0])
        #INICIALIZA EL REPORTE
        reporte = rep() 
        for p in parametros:
             #SE OBTIENE EL TIPO Y EL PARAMETRO ACTUAL
            param = p.split('=')
            tipo = param[0]
            valor = param[1]
             #VERIFICA CUAL PARAMETRO ES PARA INICIALIZAR EL OBTJETO (LOS PARAMETROS YA VIENEN EN LOWERCASE)
            if (tipo == "name"):
                reporte.name = valor
            elif (tipo == "path"):
                reporte.path = valor 
            elif (tipo == "id"):
                reporte.ids = valor 
            elif (tipo == "ruta"):
                reporte.ruta = valor 
            else:
                singleton.objL.respuesta['mensaje']+= ">>>>Error: parámetro no aceptado en 'rep': "+valor.upper()+">>>>\n"
                print("*****************************************************************************")
         #SE CREA EL REPORTE
        reporte.make_rep()

    def analizar_mount(self, parametros):
        parametros.remove(parametros[0])
        #INICIALIZA
        mo = mount()
        #IMPRIME LOS IDS SI NO VIENEN PARAMETROS
        if(parametros):
            for p in parametros:
                #SE OBTIENE EL TIPO Y EL PARAMETRO ACTUAL
                param = p.split('=')
                tipo = param[0]
                valor = param[1]
                #VERIFICA CUAL PARAMETRO ES PARA INICIALIZAR EL OBTJETO (LOS PARAMETROS YA VIENEN EN LOWERCASE)
                if (tipo == "path"):
                    mo.path = valor 
                elif (tipo == "name"):
                    mo.name = valor 
                else:
                    singleton.objL.respuesta['mensaje']+= ">>>>Error: parámetro no aceptado en 'mount': "+valor.upper()+">>>>\n"
                    print("*****************************************************************************")
            #SE CREA EL MOUNT
            mo.make_mount()
        else:
            #RECORRE EL MOUNT
            mo.recorrer()
            print("*****************************************************************************")

    def analizar_unmount(self, parametros):
        parametros.remove(parametros[0])
        #INICIALIZA EL DISCRO
        mo = unmount() 
        for p in parametros:
             #SE OBTIENE EL TIPO Y EL PARAMETRO ACTUAL
            param = p.split('=')
            tipo = param[0]
            valor = param[1]
             #VERIFICA CUAL PARAMETRO ES PARA INICIALIZAR EL OBTJETO (LOS PARAMETROS YA VIENEN EN LOWERCASE)
            if (tipo == "id"):
                mo.idm = valor 
            else:
                singleton.objL.respuesta['mensaje']+= ">>>>Error: parámetro no aceptado en 'unmount': "+valor.upper()+">>>>\n"
                print("*****************************************************************************")
         #SE CREA EL DISCO
        mo.make_unmount()
    
    def analizar_pause(self):
        response = str(input("PAUSE [c]:  ")).lower()
        if(response == 'c'):
            print("", end='')
        else:
            self.analizar_pause()

    def analizar_mkfs(self, parametros):
        parametros.remove(parametros[0])
        #INICIA
        mk = mkfs() 
        for p in parametros:
             #SE OBTIENE EL TIPO Y EL PARAMETRO ACTUAL
            param = p.split('=')
            tipo = param[0]
            valor = param[1]
             #VERIFICA CUAL PARAMETRO ES PARA INICIALIZAR EL OBTJETO (LOS PARAMETROS YA VIENEN EN LOWERCASE)
            if (tipo == "id"):
                mk.ids = valor
            elif (tipo == "type"):
                mk.type = valor 
            elif (tipo == "fs"):
                mk.fs = valor 
            else:
                singleton.objL.respuesta['mensaje']+= ">>>>Error: parámetro no aceptado en 'mkfs': "+valor.upper()+">>>>\n"
                print("*****************************************************************************")
         #SE CREA 
        mk.make_mkfs()

    def analizar(self, linea):
        nueva_linea = linea.replace(" ","")
        try:
            comandos = nueva_linea.split('-')
        except:
            print(linea)
        token = comandos[0]
        if (token == "execute"):
            singleton.objL.respuesta['mensaje']+= "COMANDO EXECUTE\n"
            #self.analizar_rep()
        elif (token == "mkdisk"):
            singleton.objL.respuesta['mensaje']+= "COMANDO MKDISK\n"
            self.analizar_mkdisk(comandos)
        elif (token == "rmdisk"):
            singleton.objL.respuesta['mensaje']+= "COMANDO RMDISK\n"
            self.analizar_rmdisk(comandos)
        elif (token == "fdisk"):
            singleton.objL.respuesta['mensaje']+= "COMANDO FDISK\n"
            self.analizar_fdisk(comandos)
        elif (token == "rep"):
            singleton.objL.respuesta['mensaje']+= "COMANDO REP\n"
            self.analizar_rep(comandos)
        elif (token == "mount"):
            singleton.objL.respuesta['mensaje']+= "COMANDO MOUNT\n"
            self.analizar_mount(comandos)
        elif (token == "unmount"):
            singleton.objL.respuesta['mensaje']+= "COMANDO UNMOUNT\n"
            self.analizar_unmount(comandos)
        elif (token == "pause"):
            self.analizar_pause()
        elif (token == "mkfs"):
            singleton.objL.respuesta['mensaje']+= "COMANDO MKFS\n"
            self.analizar_mkfs(comandos)
        elif (token == ""):
            print("", end='')
        else:
            if(token[0]=="#"):
                singleton.objL.respuesta['mensaje']+= ""
            else:
                singleton.objL.respuesta['mensaje']+= ">>>>Error: comando no aceptado.."+token.upper()+">>>>\n"
                print("*****************************************************************************")