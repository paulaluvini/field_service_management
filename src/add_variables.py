''' Código para agregar todas las variables al modelo '''

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