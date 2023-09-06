Ejercicio de Django Admin 
-

Modelos de Django
-
* **LogEntry**: Se configuro para ser accesible solo de lectura desde el administrador de django, tiene buscador por usuario, exportacion de registros mediante una accion, filtros por tipo de accion y tipo de contenido.

Modelos Propios : Parametros
-
* **Type**: Tipo de Vehículo
* **Location**: Ubicacion del Vehículo
* **Brand**: Marca del Vehículo
* **State**: Estado del Vehículo

En todos los casos permisos estandar, buscador por la descripcion del registro, accion de exportar y eliminar.

Modelos Propios : Personas
-
* **Customer**: Clientes con permisos estandar, buscador por nombre, apellido y documentos de identidad, accion de exportar y eliminar.
* **Employee**: Extension del modelo de Usuario para colocar informacion del funcionario para el ejemplo un campo relacional indicando a que sucursal pertenece. Buscador por nombre de usuario y accion de exportar, la adicion de registros es con la señal post save al crear un usuario y solo es editable.

Modelos Propios : Transacciones
-
* **Vehicle**: Contiene los datos del vehiculo, buscador por chasis, filtro por todos los modelos de parametros, accion solo de exportacion, cuando es consultado desde movimiento o venta devuelve solo los vehiculos disponibles.
* **Move**: Transaccion que actualiza la ubicacion de uno o varios vehiculos, la actualizacion se realiza en un señal post save del modelo MoveDetail. Buscador por Ubicacion destino Filtro por fecha.
* **Sale**: Registro de venta del vehiculo, una señal post save de este modelo marca como indisponible el vehiculo y le asigna un propietario (cliente), filtro por vendedor o numero de chasis del vehiculo


Aplicaciones de Tercero
-
+ [Django Import/Export](https://django-import-export.readthedocs.io/en/latest/index.html)
+ [Django Admin Autocomplete Filter](https://github.com/farhan0581/django-admin-autocomplete-filter)
+ [Django Range Filter](https://pypi.org/project/django-admin-rangefilter/)
