import sys
import cplex
import numpy as np

TOLERANCE =10e-6 

## --- Facundo -- Busco una forma de plasmar el overleaf en una expresiòn, què necesitarìa? què estructura de datos responde a la flexibilidad de datos que requiero?

##for i in range(0,9)
#	for j in range(0,9)
#          suma=trabajador[i].auxj[0]*1000+trabajador[i].auxj[1]*1200+trabajador[i].auxj[2]*1400+trabajador[i].auxj[3]*1500
          
#trabajador[0,0,0,0,0]


## --- Facundo --- Opto por hacer una clase Trabajador con atributos y mètodos, para poder indexar tanto los trabajadores
## como las òrdenes con 1 solo ìndice y acceder como necesite  a sus atributos mediante mètodos


class Trabajador:
    def __init__(self):
    # ---Facundo asigna turno 2 a trabajadores
    #    self.turno = [0,1,0,0,0] #de 0 a 4
    # ---Facundo    
    # Paula 13-01: esto es necesario tenerlo así? creo que no hace falta crear estas listas
        self.turno = [0,0,0,0,0] #de 0 a 4
        self.dia = [0,0,0,0,0,0] #de 0 a 5
        self.orden = [0,0,0,0,0,0,0,0,0,0] #de 0 a 9 
        self.auxj = [0,0,0,0] #de 0 a 3 si esta en el rango 0  entre 0 y 5, rango 1 entre 6 y 10

    def torden(self):
    	return self.orden 
    	
    def tdia(self):
    	return self.dia
    	
    def tturno(self):
    	return self.turno
    
    def tauxj(self):
    	return self.auxj
    	
class Orden:
    def __init__(self):
        self.id = 0
        self.beneficio = 0
        self.trabajadores_necesarios = 0
        
        ## ---Facundo--  Agrego una variable binaria que indica si la Orden se encuentra satisfecha o no, para que sea interpetable por Cplex?
        
        self.satisfecha = 0
    
    def load(self, row):
        self.id = int(row[0])
        self.beneficio = int(row[1])
        self.trabajadores_necesarios = int(row[2])
        
        
      ## --Facundo-- Agrego mètodos para poder acceder a los atributos de cada una de las òrdenes.
    def cid(self):
    	return self.id 
    	
    def cbeneficio(self):
    	return self.beneficio
    	
    def ctrabajadores_necesarios(self):
    	return self.trabajadores_necesarios
    
    def csatisfecha(self, v):
        self.satisfecha=v
        

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
        self.trabajadores = []
        for i in range(self.cantidad_trabajadores): 
            trab = Trabajador()
            self.trabajadores.append(trab)
        
        # Leemos la cantidad de ordenes
        self.cantidad_ordenes = int(f.readline())
        
        # Leemos cada una de las ordenes.
        self.ordenes = []
        for i in range(self.cantidad_ordenes):
            row = f.readline().replace("\n",'').split(' ')
            ## Facundo --  limpiado el \n print(row)
            orden = Orden()
            orden.load(row)
            self.ordenes.append(orden)
            
        # -- Facundo -- Pruebas y prints para corroborar que la estructura se comporte de acuerdo a los pensado   
            
        #print(self.ordenes[1].cid())
        #print(self.ordenes[1].cbeneficio())
        #print(self.ordenes[1].ctrabajadores_necesarios())
        #print("linea 49")
        
        #print(self.trabajadores[1].tturno()[1]) # me dice si el tabajador 2 se encuentra asignado al turno 2
        
        
        ## -- Facundo -- 
        ## al tenerlo instanciado como un array de clases, puedo ingresar a cada trabajador con un indice
        ## i-esimo como se plantea en el modelo matemàtico, para leer sus atributos siendo
        ## trabajadores[i].torden()[j] la j-esima  orden   a la cuàl està asignado 
        ## trabajadores[i].tdia()[d] el   d-esimo  dia       al cuàl està asignado
        ## trabajadores[i].tturno()[t]el  t-esimo  turno     al cuàl està asignado
        
        ## -- Facundo -- 
        
        
        # imagino que para cargar cada una de las restricciones lineales se podrà hacer de la forma bucle+ indice+acceso a atributo +  càlculo/restricciòn, guardando esto en donde corresponda (sea modificar el estado de una orden o si el trabajador se encuentra en uno de los rangos de òrdenes)
        
        # EJemplo
        ## SI ordenes[i].ctrabajadores_necesarios()== sumo trabajadores que tengan mismo turno dia y esta orden
        ## ENTONCES ordenes[i].csatisfecha(1) la orden està satisfecha
        
        #print(self.trabajadores[1].tdia())
        #print(self.trabajadores[1].torden()) 
        #print("linea 99")
        
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
    
    for j in data.ordenes:
        indices = []
        values = []
        for i in range(data.cantidad_trabajadores):
            for t in range(data.turnos):
                for d in range(data.dias):
                    indices.append(data.indices['T'+str(i)+'-'+str(vars(j)['id'])+'-'+str(t)+'-'+str(d)])
                    values.append(1)
        #Hasta acá tengo todos los trabajadores, ahora tengo que agregarle el id de la orden y la cantidad de trabajadores necesarios restando (porque está del otro lado de la igualdad)
        indices.append(data.indices['O'+str(vars(j)['id'])])
        values.append(vars(j)['trabajadores_necesarios'] * -1)
        row = [indices,values]
        my_problem.linear_constraints.add(lin_expr=[row], senses=['E'], rhs= [0])
    
    # Una orden se debe realizar en un solo horario.
    
    for t in range(data.turnos):
        for d in range(data.dias):
            indices = []
            values = []
            for j in data.ordenes:
                indices.append(data.indices['H'+str(vars(j)['id'])+'-'+str(t)+'-'+str(d)])
                values.append(1)
            row = [indices,values]
            my_problem.linear_constraints.add(lin_expr=[row], senses=['L'], rhs= [1.0]) #aca determino que la suma de values tiene que ser menor o igual a 1 trabajador. 
    
    # Se asume que cada orden de trabajo se puede realizar utilizando un turno, y no se pueden realizar varias ordenes en un mismo turno 
    # si comparten trabajadores. 
    
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
    
    # Esto me ayudo a entender la restriccion
    #print(row[0])
    #print(data.nombres[indices[299]])
    #print(data.nombres[indices[300]])
    
    # Ahora necesito asignar salarios a los trabajadores: si hay un turno y horas trabajadas --> cobran un salario
    # Intenté hacerlo directamente en el populate_by_row cuando creo las variables pero no me funcionaba. De nuevo, lo que comentaba Wen:
    # crear primero todas las variables (con append 0) y después si tienen un valor agregarlo: es un graaan vector con todas variables multiplicadas por valores o ceros según sea necesario.
    # Pruebo hacerlo como la 1er restriccion, creo una variable de salarios: es por trabajador pero granularidad de jtd.

    for i in range(0,data.cantidad_trabajadores):
        indices = []
        values = []
        for j in data.ordenes:    
            for t in range(0,data.turnos):
                for d in range(0,data.dias):
                    indices.append(data.indices['T'+str(i)+'-'+str(vars(j)['id'])+'-'+str(t)+'-'+str(d)])
                    values.append(1)
        indices.append(data.indices['W'+'-'+str(i)])
        values.append(-1)
        row = [indices,values]
        my_problem.linear_constraints.add(lin_expr=[row], senses=['E'], rhs= [0.0])
    
    # Ningun trabajador puede trabajar los 6 dıas de la planificacion. Creamos una variable que sea 1 cuando el trabajador trabaje en ese día.
   
    for i in range(0,data.cantidad_trabajadores):
        indices = []
        values = []
        for d in range(0,data.dias):
            indices.append(data.indices['d'+str(i)+'-'+str(d)])
            values.append(1)
        row = [indices,values]
        my_problem.linear_constraints.add(lin_expr=[row], senses=['L'], rhs= [5.0])

    # Ningún trabajador puede trabajar los 5 turnos de un día.
    for i in range(0,data.cantidad_trabajadores):
        indices = []
        values = []
        for t in range(0,data.turnos):
            indices.append(data.indices['t'+str(i)+'-'+str(t)])
            values.append(1)
        row = [indices,values]
        my_problem.linear_constraints.add(lin_expr=[row], senses=['L'], rhs= [4.0])


def populate_by_row(my_problem, data):

    ### Definimos las variables.

    # Ordenes son las primeras en el vector, del indice 0 al 9
    coeficientes_funcion_objetivo = []
    
    for orden in data.ordenes:
        coeficientes_funcion_objetivo.append(vars(orden)['beneficio'])
        data.nombres.append('O'+str(vars(orden)['id']))  #Agrego los nombres
        data.indices['O'+str(vars(orden)['id'])]=len(coeficientes_funcion_objetivo)-1  #Agrego la posición (resto 1 para comenzar dde el 0)
    
    # Agregamos a los trabajadores. Del indice 10 al 3009
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

    # Días de trabajo
    for i in range(0,data.cantidad_trabajadores):
        for d in range(0,data.dias):
            coeficientes_funcion_objetivo.append(0) 
            data.nombres.append('d'+str(i)+'-'+str(d))
            data.indices['d'+str(i)+'-'+str(d)] = len(coeficientes_funcion_objetivo)-1
    
    # Turnos de trabajo
    for i in range(0,data.cantidad_trabajadores):
        for t in range(0,data.turnos):
            coeficientes_funcion_objetivo.append(0)
            data.nombres.append('t'+str(i)+'-'+str(t))
            data.indices['t'+str(i)+'-'+str(t)] = len(coeficientes_funcion_objetivo)-1
    
    #print("Todas las variables que cree:")              
    #print(data.nombres)
    
    ### Agregar todas las variables cargadas en coeficientes_funcion_objetivo
    
    # Agrego momentáneamente a los trabajadores como si todos ganaran lo mismo, 10.
    print(len(coeficientes_funcion_objetivo))
    
    for trabajador in range(data.cantidad_trabajadores):
        coeficientes_funcion_objetivo.append(-1)
        data.nombres.append('W'+'-'+str(trabajador))
        data.indices['W'+'-'+str(trabajador)] = len(coeficientes_funcion_objetivo)-1

    # Creo esta variable auxiliar para usar después en el add de my_problem
    # Las variables de órdenes, trabajadores son binarias
    largo_binarias = len(coeficientes_funcion_objetivo)
    lower_bound = [0]*largo_binarias 
    upper_bound = [1]*largo_binarias 

    my_problem.variables.add(obj = coeficientes_funcion_objetivo,lb = lower_bound, ub = upper_bound,types=['B']*len(coeficientes_funcion_objetivo))#,names = data.nombres)
    
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
            print(data.indices[data.nombres[int(item)]])
    
    print('Funcion objetivo: ',objective_value)
    print('Status solucion: ',status_string,'(' + str(status) + ')')

    #Imprimimos las variables usadas.
    #for i in range(len(x_variables)):
         #Tomamos esto como valor de tolerancia, por cuestiones numericas.
        #if x_variables[i] > TOLERANCE:
           #print('x_' + str(data.ordenes[i].index) + ':' , x_variables[i])

def main():
    
    # Obtenemos los datos de la instancia.
    data = get_instance_data()
    #print("mydata")
    #print(vars(data)) 
    
    # Definimos el problema de cplex.
    prob_lp = cplex.Cplex()
    
    
        #--Facundo-- Acà està cagado
    # Armamos el modelo.
    populate_by_row(prob_lp,data)

    # Resolvemos el modelo.
    solve_lp(prob_lp,data)

if __name__ == '__main__':
    main()
