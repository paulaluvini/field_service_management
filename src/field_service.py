import sys
import cplex
import numpy as np
from restriction_tools import *

TOLERANCE =10e-6 
   
class Orden:
    def __init__(self):
        self.id = 0
        self.beneficio = 0
        self.trabajadores_necesarios = 0
        
    def load(self, row):
        self.id = int(row[0])
        self.beneficio = int(row[1])
        self.trabajadores_necesarios = int(row[2])
        
class FieldWorkAssignment:
    def __init__(self):
        self.cantidad_trabajadores = 0
        self.cantidad_ordenes = 0
        self.ordenes = []
        self.conflictos_trabajadores = []
        self.ordenes_correlativas = []
        self.ordenes_conflictivas = []
        self.ordenes_repetitivas = []

        self.turnos = 5 #Esto no cambia así que los dejo creados así.
        self.dias = 6
        
        self.nombres = [] #Esto no es necesario para la resolución del problema pero en la función solve_lp hago un print donde verifico qué variables están en uso y me sirve tener una lista con nombres.
        self.indices = {} #Para saber en qué posición están mis variables creo un diccionario que los guarde
        
    def load(self,filename):
        # Abrimos el archivo.
        f = open(filename)

        # Leemos la cantidad de trabajadores
        self.cantidad_trabajadores = int(f.readline())
      
        # Leemos la cantidad de ordenes
        self.cantidad_ordenes = int(f.readline())
        
        # Leemos cada una de las ordenes.
        self.ordenes = []
        for i in range(self.cantidad_ordenes):
            row = f.readline().replace("\n",'').split(' ')
            orden = Orden()
            orden.load(row)
            self.ordenes.append(orden)
            
        # Leemos la cantidad de conflictos entre los trabajadores
        cantidad_conflictos_trabajadores = int(f.readline())
        
        # Leemos los conflictos entre los trabajadores
        self.conflictos_trabajadores = []
        for i in range(cantidad_conflictos_trabajadores):
            row = f.readline().split(' ')
            self.conflictos_trabajadores.append(list(map(int,row)))
            
        # Leemos la cantidad de ordenes correlativas
        cantidad_ordenes_correlativas = int(f.readline())
        
        # Leemos las ordenes correlativas
        self.ordenes_correlativas = []
        for i in range(cantidad_ordenes_correlativas):
            row = f.readline().split(' ')
            self.ordenes_correlativas.append(list(map(int,row)))
            
        # Leemos la cantidad de ordenes conflictivas
        cantidad_ordenes_conflictivas = int(f.readline())
        
        # Leemos las ordenes conflictivas
        self.ordenes_conflictivas = []
        for i in range(cantidad_ordenes_conflictivas):
            row = f.readline().split(' ')
            self.ordenes_conflictivas.append(list(map(int,row)))
        
        # Leemos la cantidad de ordenes repetitivas
        cantidad_ordenes_repetitivas = int(f.readline())
        
        # Leemos las ordenes repetitivas
        self.ordenes_repetitivas = []
        for i in range(cantidad_ordenes_repetitivas):
            row = f.readline().split(' ')
            self.ordenes_repetitivas.append(list(map(int,row)))

        # Cerramos el archivo.
        f.close()
     
def cartesian(arrays, out=None):
    arrays = [np.asarray(x) for x in arrays]
    dtype = arrays[0].dtype
    
    n = np.prod([x.size for x in arrays])
    
    if out is None:
        out = np.zeros([n, len(arrays)], dtype=dtype)
    
    m = n / arrays[0].size
    out[:,0] = np.repeat(arrays[0], m)
    if arrays[1:]:
        cartesian(arrays[1:], out=out[0:m,1:])
        for j in xrange(1, arrays[0].size):
            out[j*m:(j+1)*m,1:] = out[0:m,1:]
    return out  

def get_instance_data():
    file_location = sys.argv[1].strip()
    instance = FieldWorkAssignment()
    instance.load(file_location)
    return instance

def populate_by_row(my_problem, data):

    ### Definimos las variables.
    coeficientes_funcion_objetivo = []

    # Agrego las ordenes
    for orden in data.ordenes:
        coeficientes_funcion_objetivo.append(vars(orden)['beneficio'])
        data.nombres.append('O'+str(vars(orden)['id']))  #Agrego los nombres
        data.indices['O'+str(vars(orden)['id'])]=len(coeficientes_funcion_objetivo)-1  #Agrego la posición (resto 1 para comenzar dde el 0)
    
    # Agregamos a los trabajadores.
    ## i  = trabajador
    ## j  = orden
    ## t  = turno
    ## d  = dia
    for i in range(0,data.cantidad_trabajadores):
        for j in data.ordenes: 
            for t in range(0,data.turnos):
                for d in range(0,data.dias):
                    coeficientes_funcion_objetivo.append(0) #Creo la variable con coeficiente 0: sólo la necesito para "tenerla" pero en la función objetivo no interviene
                    data.nombres.append('T'+str(i)+'-'+str(vars(j)['id'])+'-'+str(t)+'-'+str(d))
                    data.indices['T'+str(i)+'-'+str(vars(j)['id'])+'-'+str(t)+'-'+str(d)] = len(coeficientes_funcion_objetivo)-1
    
    # Creo la variable que relaciona las ordenes con cada turno y día
    for t in range(data.turnos):
        for d in range(data.dias):
            for j in data.ordenes:
                coeficientes_funcion_objetivo.append(0) #Creo la variable con coeficiente 0: sólo la necesito para "tenerla" pero en la función objetivo no interviene
                data.nombres.append('H'+str(vars(j)['id'])+'-'+str(t)+'-'+str(d))
                data.indices['H'+str(vars(j)['id'])+'-'+str(t)+'-'+str(d)] = len(coeficientes_funcion_objetivo)-1
    
    # Creo las variables auxiliares que uso para el salario
    for trabajador in range(data.cantidad_trabajadores):
        for tramo in range(1,4):
            coeficientes_funcion_objetivo.append(0)
            name = 'A'+str(tramo)+str(trabajador)
            data.nombres.append(name)
            data.indices[name]=len(coeficientes_funcion_objetivo)-1

    # Creo esta variable auxiliar para usar después en el add de my_problem
    # Las variables de órdenes, trabajadores son binarias
    largo_binarias = len(coeficientes_funcion_objetivo)
    lower_bound = [0]*largo_binarias 
    upper_bound = [1]*largo_binarias
    types = ['B']*largo_binarias

    # Definimos las variables W1t, W2t, W3t, W4t que nos dan salario de tramos
    salario = [1000, 1200, 1400, 1500]
    
    for trabajador in range(data.cantidad_trabajadores):
        for tramo in range(1,5):
            coeficientes_funcion_objetivo.append(salario[tramo-1]*(-1))
            name = 'W'+str(tramo)+'-'+str(trabajador)
            data.nombres.append(name)
            data.indices[name]=len(coeficientes_funcion_objetivo)-1

    t = my_problem.variables.type
    
    lower_bound = lower_bound + [0] * (data.cantidad_trabajadores * 4)
    upper_bound = upper_bound + [5] * (data.cantidad_trabajadores * 4)
    types = types + [t.integer]*(data.cantidad_trabajadores * 4)
    
    # Añadimos las variables Wt
    for trabajador in range(data.cantidad_trabajadores):
        coeficientes_funcion_objetivo.append(0)
        name = 'R'+str(trabajador)
        data.nombres.append(name)
        data.indices[name]=len(coeficientes_funcion_objetivo)-1
    
    lower_bound = lower_bound + [0] * (data.cantidad_trabajadores)
    upper_bound = upper_bound + [20] * (data.cantidad_trabajadores)
    types = types + [t.integer]*(data.cantidad_trabajadores)

    my_problem.variables.add(obj = coeficientes_funcion_objetivo, lb = lower_bound , ub = upper_bound, types = types, names = data.nombres) 

    # Seteamos direccion del problema
    my_problem.objective.set_sense(my_problem.objective.sense.maximize)
    
    # Definimos las restricciones del modelo. Encapsulamos esto en una funcion. 
    add_constraint_matrix(my_problem, data)

    # Exportamos el LP cargado en myprob con formato .lp. 
    # Util para debug.
    my_problem.write('balanced_assignment.lp')

def solve_lp(my_problem, data):
    
    # Resolvemos el ILP.
    
    my_problem.solve()

    # Obtenemos informacion de la solucion. Esto lo hacemos a traves de 'solution'. 
    x_variables = my_problem.solution.get_values()
    objective_value = my_problem.solution.get_objective_value()
    status = my_problem.solution.get_status()
    status_string = my_problem.solution.get_status_string(status_code = status)
    
    for item in range(len(x_variables)):
        if x_variables[item] == 1:
            print(data.nombres[int(item)])
    
    print('Funcion objetivo: ',objective_value)
    print('Status solucion: ',status_string,'(' + str(status) + ')')

    #Imprimimos las variables usadas.
    with open("final_variables.txt","w") as file:
        for i in range(len(x_variables)):
            #Tomamos esto como valor de tolerancia, por cuestiones numericas.
            if x_variables[i] > TOLERANCE:
                file.write("%s : %s\n" % (data.nombres[int(i)], x_variables[i]))
                
def main():
    
    # Obtenemos los datos de la instancia.
    data = get_instance_data()
    
    # Definimos el problema de cplex.
    prob_lp = cplex.Cplex()
    
    # Armamos el modelo.
    populate_by_row(prob_lp,data)

    # Resolvemos el modelo.
    solve_lp(prob_lp,data)

if __name__ == '__main__':
    main()