#GUIA

#Para correr el programa hay que tener Python 3.9+ y pip. 
#Debes instalar todos los paquetes mediante pip. Esto se hace en la consola usando el comando pip install -r requirements.txt
#Todos los modulos usados estan en requirements.txt

#PrestamosSistema: Se encarga de toda la logica de menus e interactividad
#Processors.JsonProcessor: Se encarga de cargar y guardar los datos.
#Models.Prestamo, Models.Cliente: Se encargan de todo lo relacionado con cada tipo de dato.
#Data.Clientes: Se encarga de almacenar los datos.

from PrestamosSistema import SistemaPrestamo

Sistema = SistemaPrestamo()

Sistema.Start() #Inicia el sistema











