class singleton(object):
    # DICCIONARIO PARA MENSAJES
    respuesta = {
        'estado': '200',
        'mensaje': ""
    }
    # LISTA DE PATHS REPORTES
    list_pathsReports = []
    # LISTA DE MOUNTS: PARTICIONES
    list_Mounts = []
    # LISTA DE MOUNTS: DISCOS (FORMATEADOS)
    list_discos_mounts = []
    # LISTA PARA REPORTES
    list_idsRep = []
    # VARIABLE DE TAMAÑO DE APUNTADORES DE INODOS, ESTE NO CAMBIA
    tam_bloques_inodos = 15
    # CREAR AQUI VARIABLE PARA LA SESION DE USUARIO LOGUEADO, ESTADO: PENDIENTE
    # VALIRABLE INSTANCE
    __instance = None


    # SINGLETON
    def __new__(cls):
        if singleton.__instance is None:
            singleton._instance = object.__new__(cls)
        return cls._instance
    


objL = singleton()

