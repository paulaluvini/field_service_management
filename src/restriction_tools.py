''' This code is going to define all the restrictions necessary to run the field service problem '''

def add_constraint_matrix(my_problem, data):
    
    # Restricciones
    # Una orden necesita sus T0 trabajadores para ser resuelta.
    for j in data.ordenes: #Por cada orden:
        indices = [] 
        values = []
        for i in range(data.cantidad_trabajadores): #Y cada trabajador
            for t in range(data.turnos): #Y cada turno
                for d in range(data.dias): # Y cada día
                    indices.append(data.indices['T'+str(i)+'-'+str(vars(j)['id'])+'-'+str(t)+'-'+str(d)]) #En el indice anoto, trabajador, orden id, turno y día
                    values.append(1)
        #Hasta acá tengo todos los trabajadores, ahora tengo que agregarle el id de la orden y la cantidad de trabajadores necesarios restando (porque está del otro lado de la igualdad)
        indices.append(data.indices['O'+str(vars(j)['id'])])
        values.append(vars(j)['trabajadores_necesarios'] * -1) 
        row = [indices,values]
        #En la restricción debe cumplirse por igualda. Si es negativa no alcancé la cantidad de trabajadores necesarios, si es positiva estaría usando más trabajadores de los necesarios, dado que los trabajadores son un costo para la empresa voy a tratar de utilizar los menos posible, eso se logra con la igualdad.
        my_problem.linear_constraints.add(lin_expr=[row], senses=['E'], rhs= [0.0])
    
    # Una orden se debe realizar en un solo horario. Creo una variable que relacione a las órdenes con el día y el horario.
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

    # Los trabajadores están linkeados al horario de la orden.

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
        indices.append(data.indices['R'+str(trabajador)])
        values.append(-1)
        row = [indices,values]
        my_problem.linear_constraints.add(lin_expr=[row], senses=["E"], rhs=[0.0])
    
    #todos los salarios de los tramos tienen que ser igual al total
    for trabajador in range(data.cantidad_trabajadores):
        indices = []
        values = []
        for W in (range(1,5)):
            indices.append(data.indices['W'+str(W)+'-'+str(trabajador)])
            values.append(1)
        indices.append(data.indices['R'+str(trabajador)])
        values.append(-1)
        row = [indices,values]
        my_problem.linear_constraints.add(lin_expr=[row], senses=["E"], rhs=[0.0])

    for trabajador in range(data.cantidad_trabajadores):
        indices = []
        values = []
        indices.append(data.indices['A2'+str(trabajador)])
        values.append(1)
        indices.append(data.indices['A1'+str(trabajador)])
        values.append(-1)
        row = [indices,values]
        my_problem.linear_constraints.add(lin_expr=[row], senses=["L"], rhs=[0.0]) 
            
    for trabajador in range(data.cantidad_trabajadores):
        indices = []
        values = []
        indices.append(data.indices['W1'+'-'+str(trabajador)])
        values.append(1)
        row = [indices,values]
        my_problem.linear_constraints.add(lin_expr=[row], senses=["L"], rhs=[5.0])
        
        indices = []
        values = []
        indices.append(data.indices['W1'+'-'+str(trabajador)])
        values.append(1)
        indices.append(data.indices['A1'+str(trabajador)])
        values.append(-5)
        row = [indices,values]
        my_problem.linear_constraints.add(lin_expr=[row], senses=["G"], rhs=[0.0])
        #
        indices = []
        values = []
        indices.append(data.indices['W2'+'-'+str(trabajador)])
        values.append(1)
        indices.append(data.indices['A1'+str(trabajador)])
        values.append(-5)
        row = [indices,values]
        my_problem.linear_constraints.add(lin_expr=[row], senses=["L"], rhs=[0.0])
        
        indices = []
        values = []
        indices.append(data.indices['W2'+'-'+str(trabajador)])
        values.append(1)
        indices.append(data.indices['A2'+str(trabajador)])
        values.append(-5)
        row = [indices,values]
        my_problem.linear_constraints.add(lin_expr=[row], senses=["G"], rhs=[0.0])
        
        
        indices = []
        values = []
        indices.append(data.indices['W3'+'-'+str(trabajador)])
        values.append(1)
        indices.append(data.indices['A2'+str(trabajador)])
        values.append(-5)
        row = [indices,values]
        my_problem.linear_constraints.add(lin_expr=[row], senses=["L"], rhs=[0.0])
     
        indices = []
        values = []
        indices.append(data.indices['W3'+'-'+str(trabajador)])
        values.append(1)
        indices.append(data.indices['A3'+str(trabajador)])
        values.append(-5)
        row = [indices,values]
        my_problem.linear_constraints.add(lin_expr=[row], senses=["G"], rhs=[0.0])    
        
        indices = []
        values = []
        indices.append(data.indices['W4'+'-'+str(trabajador)])
        values.append(1)
        indices.append(data.indices['A3'+str(trabajador)])
        values.append(-5)
        row = [indices,values]
        my_problem.linear_constraints.add(lin_expr=[row], senses=["L"], rhs=[0.0])
                 
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
                my_problem.linear_constraints.add(lin_expr=[row], senses=["L"], rhs=[10.0])             

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