''' Código para generar escenarios que testeen el modelo '''
''' Como inputs debemos ingresar: #trabajadores, #ordenes, rangos de beneficio, de trabajadores y #de ordenes y trabajadores
    conflictivos, correlativos y repetitivos. 
    Como outputs recibiremos un .txt con el que correremos el field_service.py '''

import random
import numpy as np

class datos():
    def __init__(self, trabajadores, ordenes, conflictos_trabajadores, ordenes_correlativas, ordenes_conflictivas, ordenes_repetitivas):
        with open("input_field_service_new.txt","w") as file:
            file.write("%s \n" % trabajadores)
            file.write("%s \n" % ordenes)
            for orden in range(0,ordenes):
                beneficio = random.choice(np.arange(100,10000))
                trabajadores_necesarios = random.choice(np.arange(1,10))
                file.write("%s %s %s\n" % (orden, beneficio, trabajadores_necesarios) )
            file.write("%s \n" % conflictos_trabajadores)
            lista_trabajadores = np.arange(0,trabajadores)
            for conflicto in range(0,conflictos_trabajadores):
                trabajador_1 = random.choice(lista_trabajadores)
                lista_trabajadores = np.delete(lista_trabajadores, np.where(lista_trabajadores == trabajador_1)[0][0])
                trabajador_2 = random.choice(lista_trabajadores)
                file.write("%s %s\n" % (trabajador_1, trabajador_2))
            lista_ordenes = np.arange(0,ordenes)
            file.write("%s \n" % ordenes_correlativas)
            for orden in range(0, ordenes_correlativas):
                orden_1 = random.choice(lista_ordenes)
                lista_trabajadores = np.delete(lista_ordenes, np.where(lista_ordenes == orden_1)[0][0])
                orden_2 = random.choice(lista_ordenes)
                file.write("%s %s\n" % (orden_1, orden_2))
            file.write("%s \n" % ordenes_conflictivas)
            for orden in range(0, ordenes_conflictivas):
                orden_1 = random.choice(lista_ordenes)
                lista_trabajadores = np.delete(lista_ordenes, np.where(lista_ordenes == orden_1)[0][0])
                orden_2 = random.choice(lista_ordenes)
                file.write("%s %s\n" % (orden_1, orden_2))
            file.write("%s \n" % ordenes_repetitivas)  
            for orden in range(0, ordenes_repetitivas):
                orden_1 = random.choice(lista_ordenes)
                lista_trabajadores = np.delete(lista_ordenes, np.where(lista_ordenes == orden_1)[0][0])
                orden_2 = random.choice(lista_ordenes)
                file.write("%s %s\n" % (orden_1, orden_2))

datos(trabajadores=15,ordenes=30,conflictos_trabajadores = 3, ordenes_correlativas=3, ordenes_conflictivas=3, ordenes_repetitivas=3)