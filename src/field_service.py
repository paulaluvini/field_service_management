import sys
import cplex
import numpy as np

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

        self.turnos = 5 #Esto no cambia así que los dejo creados así. P.
        self.dias = 6
        
        self.nombres = [] #Para conocer el nombre de mis variables. No sé si es 100% necesario aún, Wen me comentó que habían hecho así: un diccionario para guardar el indice y una lista para guardar nombres. P.
        self.indices = {} #Para saber en qué posición están mis variables creo una matriz. P.
        
    
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

def add_constraint_matrix(my_problem, data):
    
    # Restricciones

    # Una orden necesita sus T0 trabajadores para ser resuelta.
    # Acá lo pienso como que la suma de los trabajadores que pertenezcan a la orden j tienen que ser exactamente iguales a trabajadores_necesarios
    # Ej:   X_111J + X_211J + X_311J + ... = Zj * trabajadores_necesarios
    # Si Zj = 1 --> orden resuelta porque no tiene ni más ni menos trabajadores. 
    #Por cada orden:
    for j in data.ordenes:
        indices = [] 
        values = []
        #Y cada trabajador
        for i in range(data.cantidad_trabajadores):
            #Y cada turno
            for t in range(data.turnos):
                # Y cada día
                for d in range(data.dias): 
                    #En el indice anoto, trabajador, orden id, turno y día
                    indices.append(data.indices['T'+str(i)+'-'+str(vars(j)['id'])+'-'+str(t)+'-'+str(d)])
                    values.append(1)
        #Hasta acá tengo todos los trabajadores, ahora tengo que agregarle el id de la orden y la cantidad de trabajadores necesarios restando (porque está del otro lado de la igualdad)
        indices.append(data.indices['O'+str(vars(j)['id'])])
        #Trabajadores necesarios
        values.append(vars(j)['trabajadores_necesarios'] * -1)
        row = [indices,values]
        #En la restricción debe cumplirse por igualda. Si es negativa no alcancé la cantidad de trabajadores necesarios, si es positiva estaría usando más trabajadores de los necesarios, dado que los trabajadores son un costo para la empresa voy a tratar de utilizar los menos posible, eso se logra con la igualdad.
        my_problem.linear_constraints.add(lin_expr=[row], senses=['E'], rhs= [0.0])
    
    # Una orden se debe realizar en un solo horario. Creo una variable que relacione a las órdenes con el día y el horario.
    # O1: H111, H121, H131, H141... 
    for j in data.ordenes:
        indices = []
        values = []
        for t in range(data.turnos):
            for d in range(data.dias):

                indices.append(data.indices['H'+str(vars(j)['id'])+'-'+str(t)+'-'+str(d)])
                values.append(1)
            row = [indices,values]

            #Solo puede ser realizada en un día y horario
            my_problem.linear_constraints.add(lin_expr=[row], senses=['L'], rhs= [1.0]) 

    # los trabajadores están linkeados al horario de la orden.

    for t in range(data.turnos):
        for d in range(data.dias):
            for j in data.ordenes:
                indices = []
                values = []
                for i in range(data.cantidad_trabajadores):
                    indices.append(data.indices['T'+str(i)+'-'+str(vars(j)['id'])+'-'+str(t)+'-'+str(d)])
                    values.append(1)
                indices.append(data.indices['H'+str(vars(j)['id'])+'-'+str(t)+'-'+str(d)])
                values.append(vars(j)['trabajadores_necesarios'] * -1)
                row = [indices,values]
                my_problem.linear_constraints.add(lin_expr=[row], senses=['E'], rhs= [0.0])

    # Un trabajador en 1 turno solo puede ir a 1 orden
    
    for i in range(data.cantidad_trabajadores):
        for t in range(data.turnos):
            for d in range(data.dias):
                indices = []
                values = []
                for j in data.ordenes:
                    indices.append(data.indices['T'+str(i)+'-'+str(vars(j)['id'])+'-'+str(t)+'-'+str(d)])
                    values.append(1)
                row = [indices,values]
                my_problem.linear_constraints.add(lin_expr=[row], senses=['L'], rhs= [1.0]) #aca determino que la suma de values tiene que ser menor o igual a 1 trabajador. 
        
    # Ningun trabajador puede trabajar los 6 dıas de la planificacion. 
   
    for i in range(0,data.cantidad_trabajadores):     
        for t in range(0,data.turnos):
            indices = []
            values = []  
            for j in data.ordenes:
                for d in range(0,data.dias):
                    indices.append(data.indices['T'+str(i)+'-'+str(vars(j)['id'])+'-'+str(t)+'-'+str(d)])
                    values.append(1)
            row = [indices,values]
            my_problem.linear_constraints.add(lin_expr=[row], senses=['L'], rhs= [5.0])

            
    #El salario de los trabajadores depende de las cantidad de horas trabajadas
    #  De 0  a  5 ordenes: el salario 1000
    #  De 5  a 10 ordenes: el salario  1200
    # De 10 a 15 ordenes: el salario 1400
    # De 15 ordenes: el salario 1500
    
    for trabajador in range(data.cantidad_trabajadores):
        indices = []
        values = []
        for turno in range(data.turnos):
            for dia in range(data.dias):
                for orden in data.ordenes:
                    indices.append(data.indices['T'+str(trabajador)+'-'+str(vars(orden)['id'])+'-'+str(turno)+'-'+str(dia)])
                    values.append(1)
        indices.append(data.indices['W'+str(trabajador)])
        values.append(-1)
        row = [indices,values]
        my_problem.linear_constraints.add(lin_expr=[row], senses=["E"], rhs=[0])
    
    #todos los salarios de los tramos tienen que ser igual al total
    for trabajador in range(data.cantidad_trabajadores):
        indices = []
        values = []
        for W in (range(1,5)):
            indices.append(data.indices['W'+str(W)+'-'+str(trabajador)])
            values.append(1)
        indices.append(data.indices['W'+str(trabajador)])
        values.append(-1)
        row = [indices,values]
        my_problem.linear_constraints.add(lin_expr=[row], senses=["E"], rhs=[0])

    for trabajador in range(data.cantidad_trabajadores):
        
        indices = []
        values = []
        indices.append(data.indices['A2'+str(trabajador)])
        values.append(1)
        indices.append(data.indices['A1'+str(trabajador)])
        values.append(-1)
        row = [indices,values]
        my_problem.linear_constraints.add(lin_expr=[row], senses=["L"], rhs=[0]) 
            
            
    for trabajador in range(data.cantidad_trabajadores):
        
        indices = []
        values = []
        indices.append(data.indices['W1'+'-'+str(trabajador)])
        values.append(1)
        row = [indices,values]
        my_problem.linear_constraints.add(lin_expr=[row], senses=["L"], rhs=[5])
        
        indices = []
        values = []
        indices.append(data.indices['W1'+'-'+str(trabajador)])
        values.append(1)
        indices.append(data.indices['A1'+str(trabajador)])
        values.append(-5)
        row = [indices,values]
        my_problem.linear_constraints.add(lin_expr=[row], senses=["G"], rhs=[0])
        #
        indices = []
        values = []
        indices.append(data.indices['W2'+'-'+str(trabajador)])
        values.append(1)
        indices.append(data.indices['A1'+str(trabajador)])
        values.append(-5)
        row = [indices,values]
        my_problem.linear_constraints.add(lin_expr=[row], senses=["L"], rhs=[0])
        
        indices = []
        values = []
        indices.append(data.indices['W2'+'-'+str(trabajador)])
        values.append(1)
        indices.append(data.indices['A2'+str(trabajador)])
        values.append(-5)
        row = [indices,values]
        my_problem.linear_constraints.add(lin_expr=[row], senses=["G"], rhs=[0])
        
        
        indices = []
        values = []
        indices.append(data.indices['W3'+'-'+str(trabajador)])
        values.append(1)
        indices.append(data.indices['A2'+str(trabajador)])
        values.append(-5)
        row = [indices,values]
        my_problem.linear_constraints.add(lin_expr=[row], senses=["L"], rhs=[0])
     
        indices = []
        values = []
        indices.append(data.indices['W3'+'-'+str(trabajador)])
        values.append(1)
        indices.append(data.indices['A3'+str(trabajador)])
        values.append(-5)
        row = [indices,values]
        my_problem.linear_constraints.add(lin_expr=[row], senses=["G"], rhs=[0])    
        
        indices = []
        values = []
        indices.append(data.indices['W4'+'-'+str(trabajador)])
        values.append(1)
        indices.append(data.indices['A3'+str(trabajador)])
        values.append(-5)
        row = [indices,values]
        my_problem.linear_constraints.add(lin_expr=[row], senses=["L"], rhs=[0])
            
            
    # Ningún trabajador puede trabajar los 5 turnos de un día.

    for i in range(0,data.cantidad_trabajadores):    
        for t in range(0,data.dias):
            indices = []
            values = []
            for j in data.ordenes:
                for t in range(0,data.turnos):
                    indices.append(data.indices['T'+str(i)+'-'+str(vars(j)['id'])+'-'+str(t)+'-'+str(d)])
                    values.append(1)
            row = [indices,values]
            my_problem.linear_constraints.add(lin_expr=[row], senses=['L'], rhs= [4.0])

    # Hay pares de ordenes de trabajo que no pueden ser satisfechas en turnos consecutivos de un trabajador
    
    turnos_conflictivos = [[0,1],[1,2],[2,3],[3,4],[1,0],[2,1],[3,2],[4,3]] #Creamos esta lista con los turnos consecutivos (ida y vuelta)
    for i in range(0,data.cantidad_trabajadores):
        for d in range(data.dias):
            for conflictivas in data.ordenes_conflictivas:
                for tu in turnos_conflictivos:
                    indices = []
                    indices.append(data.indices['T'+str(i)+'-'+str(conflictivas[0])+'-'+str(tu[0])+'-'+str(d)])
                    indices.append(data.indices['T'+str(i)+'-'+str(conflictivas[1])+'-'+str(tu[1])+'-'+str(d)])
                    values=[1,1]
                    row = [indices, values]
                    my_problem.linear_constraints.add(lin_expr=[row], senses=['L'], rhs=[1.0])
    
    # Existen algunos pares de ordenes de trabajo correlativas. 
    # Un par ordenado de ordenes correlativas A y B, indica que si se satisface A, entonces debe satisfacerse B ese mismo dia en el turno consecutivo.
    
    turnos_correlativos = [[0,1],[1,2],[2,3],[3,4]] #Creamos esta lista con los turnos consecutivos
    for d in range(data.dias):
        for correlativas in data.ordenes_correlativas:
            for tu in turnos_correlativos:
                indices = []
                indices.append(data.indices['H'+str(correlativas[0])+'-'+str(tu[0])+'-'+str(d)])
                indices.append(data.indices['H'+str(correlativas[1])+'-'+str(tu[1])+'-'+str(d)])
                values=[1.0,1.0* -1]
                row = [indices, values]
                my_problem.linear_constraints.add(lin_expr=[row], senses=['L'], rhs=[0.0])

    # Tengo que restringir que la primera orden no puede ocurrir en el ultimo turno y la segunda no puede ocurrir en el primero.

    turnos_imposibles = [4,0]
    for d in range(data.dias):
        for correlativas in data.ordenes_correlativas:
            indices = []
            indices.append(data.indices['H'+str(correlativas[0])+'-'+str(turnos_imposibles[0])+'-'+str(d)])
            indices.append(data.indices['H'+str(correlativas[1])+'-'+str(turnos_imposibles[1])+'-'+str(d)])
            values=[1.0,1.0]
            row = [indices, values]
            my_problem.linear_constraints.add(lin_expr=[row], senses=['L'], rhs=[0.0])
            
    #La diferencia en la cantidad de ordenes asignadas al trabajador con más horas y el de menor cantidad de ordenes no puede ser mayor a 10.  
    
    for i1 in range(data.cantidad_trabajadores):
        for i2 in range(data.cantidad_trabajadores):
            if i1 != i2:
                indices = []
                values = []
                indices.append(data.indices['T'+str(i1)+'-'+str(vars(j)['id'])+'-'+str(t)+'-'+str(d)])
                values.append(1)
                indices.append(data.indices['T'+str(i2)+'-'+str(vars(j)['id'])+'-'+str(t)+'-'+str(d)])
                values.append(-1)
                row = [indices,values]
                my_problem.linear_constraints.add(lin_expr=[row], senses=["L"], rhs=[10])             

    ### Restricciones deseables
    ## Hay conflictos entre algunos trabajadores que hacen que prefieran no ser asignados a una misma orden de trabajo.

    for t in range(data.turnos):
        for d in range(data.dias):
            for j in data.ordenes:
                for conflictos in data.conflictos_trabajadores:
                    indices = []
                    values = []
                    indices.append(data.indices['T'+str(conflictos[0])+'-'+str(vars(j)['id'])+'-'+str(t)+'-'+str(d)])
                    indices.append(data.indices['T'+str(conflictos[1])+'-'+str(vars(j)['id'])+'-'+str(t)+'-'+str(d)])
                    values=[1,1]
                    row = [indices,values]
                    my_problem.linear_constraints.add(lin_expr=[row], senses=['L'], rhs= [1.0])

    ## Hay pares de ´ordenes de trabajo que son repetitivas por lo que ser´ıa bueno que un mismo trabajador no sea asignado a ambas.
    #ordenes_repetitivas

    for i in range(0,data.cantidad_trabajadores):
        for repetitivas in data.ordenes_repetitivas:
            indices = []
            values = []
            for d in range(data.dias):
                for t in range(data.turnos):
                    indices.append(data.indices['T'+str(i)+'-'+str(repetitivas[0])+'-'+str(t)+'-'+str(d)])
                    indices.append(data.indices['T'+str(i)+'-'+str(repetitivas[1])+'-'+str(t)+'-'+str(d)])
                    values.append(1)
                    values.append(1)
            row = [indices, values]
            my_problem.linear_constraints.add(lin_expr=[row], senses=['L'], rhs=[1.0])
    

def populate_by_row(my_problem, data):

    ### Definimos las variables.

    # Ordenes son las primeras en el vector, del indice 0 al 9
    coeficientes_funcion_objetivo = []
    
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
    
    for t in range(data.turnos):
        for d in range(data.dias):
            for j in data.ordenes:
                coeficientes_funcion_objetivo.append(0) #Creo la variable con coeficiente 0: sólo la necesito para "tenerla" pero en la función objetivo no interviene
                data.nombres.append('H'+str(vars(j)['id'])+'-'+str(t)+'-'+str(d))
                data.indices['H'+str(vars(j)['id'])+'-'+str(t)+'-'+str(d)] = len(coeficientes_funcion_objetivo)-1
    

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
        name = 'W'+str(trabajador)
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
    # for i in range(len(x_variables)):
    #      #Tomamos esto como valor de tolerancia, por cuestiones numericas.
    #     if x_variables[i] > TOLERANCE:
    #        print('x_' + str(data.ordenes[i].index) + ':' , x_variables[i])

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
