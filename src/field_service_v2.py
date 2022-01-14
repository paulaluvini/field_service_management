#BENEFICIO --> ORDENES CUMPLIDOS Ok, funciona.
#COSTO --> COSTO No estamos asignando trabajadores

#Estas dos cosas tienen que interactuar entre si porque la orden no puede cumplirse si no se le asignan la cantidad de trabajadores exactos
#1- Hay que asignar los trabajadores.
#2- Restringir que la orden solo se haga si se satisfacen los trabajadores (lo que intentamos hacer).

#for j in range(len(data.ordenes)):
#        auxiliar2 = 0
#        for i in range(0,data.cantidad_trabajadores):
#            auxiliar2 = auxiliar2 + data.trabajadores[i].torden()[j]
#        if data.ordenes[j].ctrabajadores_necesarios() == auxiliar2:
#            data.ordenes[j].csatisfecha(1)
#        else:
#            data.ordenes[j].csatisfecha(0)

#3- Esto no es prioritario. Funcion a trozos ?? 




import sys
import cplex
import numpy as np

TOLERANCE =10e-6 
# i cantidad de trabajadores
# j orden
# d dia
# t turno



## --- Facundo -- Busco una forma de plasmar el overleaf en una expresiòn, què necesitarìa? què estructura de datos responde a la flexibilidad de datos que requiero?

#for i in range(0,9)
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
        
    def cssatisfecha(self):
        return self.satisfecha

class FieldWorkAssignment:
    def __init__(self):
        self.cantidad_trabajadores = 0
        self.cantidad_ordenes = 0
        self.ordenes = []
        self.conflictos_trabajadores = []
        self.ordenes_correlativas = []
        self.ordenes_conflictivas = []
        self.ordenes_repetitivas = []
        self.turnos = []
        self.dias = []
        
    

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
            
        print(self.ordenes[1].cid())
        print(self.ordenes[1].cbeneficio())
        for i in range(len(self.ordenes)):
            print(str(i)+'----'+str(self.ordenes[i].ctrabajadores_necesarios()))
        print(self.ordenes[1].ctrabajadores_necesarios())
        print("linea 49")
        
        print(self.trabajadores[1].tturno()[1]) # me dice si el tabajador 2 se encuentra asignado al turno 2
        
        
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
        
        print(self.trabajadores[1].tdia())
        print(self.trabajadores[1].torden()) 
        print("linea 99")
        
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

        self.turnos = [0,0,0,0,0]
        self.dias = [0,0,0,0,0,0]
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
    
    #Voy a crear un array para alojar a mis trabajadores: t_ijtd donde:
    # i = 1,...T (id del trabajador)
    # j = 1,... O (id de la orden)
    # t = 1, 2, 3, 4, 5 (id del turno)
    # d = 1, 2, 3, 4, 5, 6 (id del día)

    turnos = np.arange(1,6)
    dias =  np.arange(1,7)
 
    trabajadores = np.zeros((data.cantidad_trabajadores, data.cantidad_ordenes, len(turnos), len(dias)))
  

    # EJEMPLO CLASE Agregamos restriccion de capacidad.
    #indices = list(range(data.n))
    #values = []
    #for item in data.items:
    #    values.append(item.weight)

    #row = [indices,values]
    #my_problem.linear_constraints.add(lin_expr=[row], senses=['L'], rhs=[data.b])

    #1- No toda orden de trabajo debe ser resuelta

    #2-Ningun trabajador puede trabajar los 6 dias de la planificacion
    indices = list(range(trabajadores.shape[0]*trabajadores.shape[3]))
    values = []
    for trabajador in range(data.cantidad_trabajadores): #Itero por los trabajadores
        for dia in range(len(dias)): #Itero por los dias
            values.append(trabajadores[trabajador,:,:,dia].sum()) #Sumo todas las ocurrencias
    row = [indices,values]
    my_problem.linear_constraints.add(lin_expr=[row], senses=['L'], rhs= [5]) #aca determino que la suma de values tiene que ser menor o igual a 5


    #
    T0 = []
    for orden in data.ordenes:
        T0.append(vars(orden)['trabajadores_necesarios'])
    print(T0)    
    indices = list(range(vars(orden)['trabajadores_necesarios']))
    values = []
    
    #Voy a crear un array para alojar a mis trabajadores: t_ijtd donde:
    # i = 1,...T (id del trabajador)
    # j = 1,... O (id de la orden)
    # t = 1, 2, 3, 4, 5 (id del turno)
    # d = 1, 2, 3, 4, 5, 6 (id del día)
    
    for orden in range(len(data.ordenes)): #Itero por las ordenes
        for trabajador in range(data.cantidad_trabajadores): #Itero por los trabajadores
            values.append(int(trabajadores[trabajador,orden,:,:].sum()==data.ordenes[orden].ctrabajadores_necesarios())) #Sumo todas las ocurrencias para saber qué ordenes se cumplieron            
    row = [indices,values]
    # Facundo 16/12 Cómo cargar correctamente la restricción? Pametro Senses  y Rhs
    my_problem.linear_constraints.add(lin_expr=[row], senses=['L'], rhs= [1])
    
    '''
    indices = list(range(data.cantidad_ordenes))
    values = []
    
    for orden in range(data.cantidad_ordenes): #Itero por los dias
        values.append(data.trabajadores[:,orden,:,:].sum()) # 
        my_problem.linear_constraints.add(lin_expr=[row], senses=['G'], rhs=[T0[orden]])
            #if t == 5 => orden == 1 #Sumo todas las ocurrencias
    row = [indices,values]
    '''

    # EJemplo
    ## SI ordenes[i].ctrabajadores_necesarios()== sumo trabajadores que tengan mismo turno dia y esta orden
    ## ENTONCES ordenes[i].csatisfecha(1) la orden està satisfecha
    
    #my_problem.linear_constraings.add(lin_expr=[row], senses['G'], rhs=
    print("lasad")
    for j in range(len(data.ordenes)):
        auxiliar2 = 0
        for i in range(0,data.cantidad_trabajadores):
            auxiliar2 = auxiliar2 + data.trabajadores[i].torden()[j]
            #print(data.trabajadores[i].torden()[j])
        if data.ordenes[j].ctrabajadores_necesarios() == auxiliar2:
            data.ordenes[j].csatisfecha(1)
        else:
            data.ordenes[j].csatisfecha(0)

    print(data.ordenes[1].cssatisfecha())
    
    for j in range(len(data.ordenes)):
        print(data.ordenes[i].cssatisfecha())
        
    #print(data.ordenes)
    #print(data.ordenes[:].csatisfecha())
    print("linea 147") 

def populate_by_row(my_problem, data):

    # Definimos y agregamos las variables.
    #self.trabajadores = np.zeros((self.cantidad_trabajadores, self.cantidad_ordenes, len(self.turnos), len(self.dias)))   
    # Beneficio
    # o_j * b_j = 50
    # Ordenes son las primeras en el vector, del indice 0 al 9
    coeficientes_funcion_objetivo = []
    nombres=[]
    
    for orden in data.ordenes:
        coeficientes_funcion_objetivo.append(vars(orden)['beneficio'])
        nombres.append('orden'+str(vars(orden)['id']))
    my_problem.variables.add(obj = coeficientes_funcion_objetivo, lb = [0]*data.cantidad_ordenes, ub = [1]*data.cantidad_ordenes, types=['B']*data.cantidad_ordenes, names = nombres) 

    #print("linea 285")
    #print(my_problem.variables.get_names())
    
    nombres=[]
    
    
    #Agregamos a los trabajadores. Del indice 10 al 3009
    ## i  = trabajador
    ## j  = orden
    ## t  = turno
    ## d  = dia
    
    ##print(range(1,data.cantidad_trabajadores))
    
    for i in  range(0,data.cantidad_trabajadores):
        for j in range(0,data.cantidad_ordenes): 
            for t in range(0,len(data.turnos)):
                for d in range(0,len(data.dias)):
                    nombres.append('T'+str(i)+'-'+str(j)+'-'+str(t)+'-'+str(d))

    #print("linea285")                
    #print(nombres)
    #print("linea285")
    my_problem.variables.add(obj = [-1]*(data.cantidad_trabajadores*data.cantidad_ordenes*len(data.turnos)*len(data.dias)),lb = [0]*(data.cantidad_trabajadores*data.cantidad_ordenes*len(data.turnos)*len(data.dias)), ub = [1]*(data.cantidad_trabajadores*data.cantidad_ordenes*len(data.turnos)*len(data.dias)),types=['B']*(data.cantidad_trabajadores*data.cantidad_ordenes*len(data.turnos)*len(data.dias)),names = nombres)
    #print(my_problem.variables.get_names())
    
    # Costos: trabajadores
    #\item $t_{ijtd}^1$ órdenes entre 0 y 5, remuneración de 1000
    #\item $t_{ijtd}^2$ órdenes entre 6 y 10 remuneración de 1200 
    #\item $t_{ijtd}^3$ órdenes entre 11 y 15 remuneración de 1400
    #\item $t_{ijtd}^4$ órdenes de más de 15 remuneración de 1500
    coeficientes_funcion_objetivo_1 = []
    coeficientes_funcion_objetivo_2 = []
    coeficientes_funcion_objetivo_3 = []
    coeficientes_funcion_objetivo_4 = []
    indices = []
    
    ##for trabajador in range(data.cantidad_trabajadores): #Itero por los trabajadores
      ##  for orden in range(data.cantidad_ordenes): #Itero por ordenes
             ## -- Facundo -- 
        ## al tenerlo instanciado como un array de clases, puedo ingresar a cada trabajador con un indice
        ## i-esimo como se plantea en el modelo matemàtico, para leer sus atributos siendo
        ## trabajadores[i].torden()[j] la j-esima  orden   a la cuàl està asignado 
        ## trabajadores[i].tdia()[d] el   d-esimo  dia       al cuàl està asignado
        ## trabajadores[i].tturno()[t]el  t-esimo  turno     al cuàl està asignado
        
            ## -- Facundo -- 
          
          #indices.append(data.trabajadores[trabajador],orden,:,:])
          
          # print(data.trabajadores[0][1])
            #[trabajador])
            # print(data.trabajadores[1])
            #[orden])
            # print(data.trabajadores[2])
            # print(data.trabajadores[3])
            # print("ciclo")
            #if data.trabajadores[trabajador,orden,:,:].sum() in range(0,6):
            #    coeficientes_funcion_objetivo_1.append(data.trabajadores[trabajador,orden,:,:].sum())
            #    coeficientes_funcion_objetivo_2.append(0)
            #    coeficientes_funcion_objetivo_3.append(0)
            #    coeficientes_funcion_objetivo_4.append(0)
            #if data.trabajadores[trabajador,orden,:,:].sum() in range(6,11):
            #    coeficientes_funcion_objetivo_2.append(data.trabajadores[trabajador,orden,:,:].sum()-5)
             #   coeficientes_funcion_objetivo_1.append(5)
              #  coeficientes_funcion_objetivo_3.append(0)
              #  coeficientes_funcion_objetivo_4.append(0)
            #if data.trabajadores[trabajador,orden,:,:].sum() in range(11,16):
            #    coeficientes_funcion_objetivo_3.append(data.trabajadores[trabajador,orden,:,:].sum()-10)
            #    coeficientes_funcion_objetivo_1.append(5)
            #    coeficientes_funcion_objetivo_2.append(5)
            #    coeficientes_funcion_objetivo_4.append(0)
            #if data.trabajadores[trabajador,orden,:,:].sum() in range(16,21):
            #    coeficientes_funcion_objetivo_4.append(data.trabajadores[trabajador,orden,:,:].sum()-15)
            #    coeficientes_funcion_objetivo_3.append(5)
            #    coeficientes_funcion_objetivo_2.append(5)
            #    coeficientes_funcion_objetivo_1.append(5)
    # print(indices)

    my_problem.variables.add(obj = [x * (-1000) for x in coeficientes_funcion_objetivo_1], lb = [0]*data.cantidad_trabajadores*data.cantidad_ordenes, ub = [1]*data.cantidad_trabajadores*data.cantidad_ordenes, types=['B']*data.cantidad_ordenes*data.cantidad_trabajadores) 
    my_problem.variables.add(obj = [x * (-1200) for x in coeficientes_funcion_objetivo_2], lb = [0]*data.cantidad_trabajadores*data.cantidad_ordenes, ub = [1]*data.cantidad_trabajadores*data.cantidad_ordenes, types=['B']*data.cantidad_ordenes*data.cantidad_trabajadores) 
    my_problem.variables.add(obj = [x * (-1400) for x in coeficientes_funcion_objetivo_3], lb = [0]*data.cantidad_trabajadores*data.cantidad_ordenes, ub = [1]*data.cantidad_trabajadores*data.cantidad_ordenes, types=['B']*data.cantidad_ordenes*data.cantidad_trabajadores) 
    my_problem.variables.add(obj = [x * (-1500) for x in coeficientes_funcion_objetivo_4], lb = [0]*data.cantidad_trabajadores*data.cantidad_ordenes, ub = [1]*data.cantidad_trabajadores*data.cantidad_ordenes, types=['B']*data.cantidad_ordenes*data.cantidad_trabajadores)

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
