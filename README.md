# Optimización
 ## Problema 

Muchas empresas ofrecen productos y servicios que se utilizan en una locación ajena a la misma. Muchas veces, estos productos o servicios dependen de ciertos trabajos como instalación, mantenimiento o inspección que deben ser realizados por cuadrillas que son asignadas especiﬁcamente a los diferentes trabajos. En las empresas donde este tipo de necesidades es moneda corriente (telcos, proveedores de energía o gas, entre otros) suele existir un área, Field Service Management, que enmarca todas estas actividades.
En particular en este trabajo nos interesa la planiﬁcación semanal de las cuadrillas de trabajo a las diferentes órdenes enlistadas. En este problema vamos a contar con una lista de trabajadores y una lista de trabajos a realizar. El objetivo es maximizar la ganancia total, teniendo el cuenta el beneﬁcio que nos otorga resolver un trabajo y considerando los pagos a los trabajadores.
El problema formalmente es el siguiente. Contamos con una cantidad T de trabajadores para realizar los trabajos. Por otro lado, tenemos una lista de O órdenes de trabajo a realizar. Cada orden requiere de una cantidad preﬁjada de trabajadores, denominada To. La semana a planiﬁcar tiene 6 días, ya que planiﬁcaremos de Lunes a Sábado. Cada día tiene 5 Turnos de 2 horas. Se asume que cada órden de trabajo se puede realizar utilizando un turno, y no se pueden realizar varias órdenes en un mismo turno si comparten trabajadores. La solución debe indicar cómo asignar los trabajadores a las órdenes, y a su vez cómo asignar las órdenes a los turnos, cumpliendo las siguientes restricciones necesarias para que la asignación sea factible:


No toda orden de trabajo tiene que ser resuelta.
- Ningú trabajador puede trabajar los 6 días de la planiﬁcación.
- Ningún trabajador puede trabajar los 5 turnos de un día.
- Hay pares de órdenes de trabajo que no pueden ser satisfechas en turnos consecutivos de un trabajador (Si bien en este problema no nos preocupamos por el ruteo sino solo por la asignación, hay órdenes tan lejanas geográficamente que no se podrían satisfacer consecutivamente).
- Una órden de trabajo debe tener asignada sus To trabajadores en un mismo turno para poder ser resuelta.
