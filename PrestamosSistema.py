from Models.Cliente import Cliente
import sys
import os
from Processors.JsonProcessor import JsonProcessor

from Models.Prestamo import Prestamo


class SistemaPrestamo(): #Sistema principal de prestamos. Maneja toda la logica del programa
    def __init__(self):
        self.clientes = [] #Clientes actuales
        self.prestamos = [] #Prestamos actuales
        self.opciones = { #Diccionario de opciones. Cada numero referencia a un texto para mostrar
            1: "Realizar solicitud de prestamos",
            2: "Imprimir solicitud de prestamo",
            3: "Pagar prestamo",
            4: "Consultar clientes",
            5: "Cancelar solicitud de Prestamo",
            6: "Salir"
        }

        self.JsonProcessor = JsonProcessor() #Procesador de DataPersistency.

    def Start(self): #Inicio del programa
        self.Limpiar() #Limpia la consola
        self.JsonProcessor.LoadData() #Carga los datos actuales
        if not self.clientes: #Si no hay clientes
            self.clientes = self.JsonProcessor.getAllClients() #Obtiene todos los clientes guardados
            for x in self.clientes: #Por cada cliente
                for y in x.Prestamos: #Por cada prestamo de cada cliente
                    self.prestamos.append(y) #Agregar los prestamos
        print("Seleccione una opcion")
        for keys, values in self.opciones.items(): #Por cada valor en opciones
            print(keys, values)
        opcion = int(input("Opcion: "))

        handlers = { #Diccionario para manejar las opciones. Cada numero hace referencia a un metodo
            1: self.SolicitudDePrestamo,
            2: self.ImprimirSolicitudDePrestamo,
            3: self.PagarPrestamo,
            4: self.ConsultarClientes,
            5: self.CancelarPrestamo,
            6: self.Salir
        }
        try:
            handlers[opcion]() #Ejecuta el metodo de la opcion elegida
        except Exception as e:
            print(f"Opcion no valida : {e}")

    def SolicitudDePrestamo(self): #Opcion: Imprimir solicitud de prestamo
        self.Limpiar() #Limpia consola
        clienteValido = False 
        self.MostrarClientes() #Muestra todos los clientes disponibles

        print("ID del Cliente solicitante")
        clientId = int(input("ID: "))
        if self.clientes:
            for cliente in self.clientes:
                if cliente.id == clientId:
                    clienteValido = True   #Valida si el cliente existe
     
        if clienteValido: #Si el cliente existe
            self.Limpiar() #Limpia consola
            cliente: Cliente = self.clientes[clientId] #Obtiene el cliente por su id, usando indexers
            print(f"Cliente: {cliente.Nombre}")  
            print("=================== PRESTAMO ===================")
            try:
                #Crea nuevo prestamo
                monto = float(input("Monto: $"))
                tazaDeInteres = float(input("Taza de interes: %"))
                plazo = int(input("Plazo (Años): "))
                prestamo = Prestamo(monto, tazaDeInteres, plazo)
                prestamo.Id = len(self.prestamos)
                prestamo.Cliente = cliente
                self.prestamos.append(prestamo)
                cliente.Prestamos.append(prestamo)
                self.JsonProcessor.SaveClient(cliente) #Guarda el cliente
                print(f"Se ha creado el prestamo con el ID {prestamo.Id}")
                input()
                self.Start()
            except Exception as e:
                print(f"Error: {e}")         
        else: #Si el cliente no existe
            print("Cliente no existe. ¿Desea clearlo? (Y/N)") 
            response = input("(Y/N): ")
            self.Limpiar()
            if response.lower() == "n":
                self.Start()
            elif response.lower() == "y":
                self.crearCliente() #Metodo para crear cliente
             
    def crearCliente(self): #Crea el cliente
        print(" ================ CLIENTE ================")
        try:
            nombre = input("Nombre: ")
            clienteId = len(self.clientes)
            cliente = Cliente()
            cliente.Nombre = nombre
            cliente.id = clienteId
            self.clientes.append(cliente) # Guarda el cliente en la lista de clientes
            print(f"Cliente {cliente.Nombre} creado con el ID {cliente.id}")
            input()
            self.Start()
        except Exception as e:
            print(e)
    
    def ImprimirSolicitudDePrestamo(self): #Opcion: Imprimir solicitud de prestamo
        self.Limpiar() #Limpia la consola
        self.MostrarPrestamos() #Muestra los prestamos
        try:
            prestamo = int(input("ID del prestamo a imprimir: ")) 
            for x in self.prestamos:
                if x.Id == prestamo:
                    self.Limpiar()
                    print("================ TAZA DE AMORTIZACION ================")
                    print(f"==================== ID: {x.Id} ====================")
                    x.ImprimirTablaAmortizacion() #Imprime la taza de amortizacion de el prestamo
                    input()
                    self.Start()
        except:
            print("ID invalido")
            input()
            self.Start()
        input()
        self.Start()

    def PagarPrestamo(self): #Opcion: Pagar prestamo
        self.Limpiar()
        self.MostrarPrestamos() #Muestra los prestamos
        try:
            prestamoId = int(input("ID del prestamo: "))
            for prestamo in self.prestamos:
                if prestamo.Id == prestamoId:
                    prst: Prestamo = prestamo
                    try:
                        #Abona al prestamo
                        monto = float(input("Valor a abonar: $"))
                        prst.Abonar(monto)
                        print(f"Has abonado {monto}. Cantidad restante a pagar: {prst.MontoRestante}")
                        self.JsonProcessor.SaveClient(prst.Cliente)
                        input()
                        self.Start()
                    except Exception as e:
                        print(f"Monto invalido {e}")
                        input()
                        self.Start()

        except: 
            print("Error al obtener el prestamo.")
            input()
            self.Start()

    def ConsultarClientes(self): #Opcion: Consultar clientes
        self.Limpiar()
        self.MostrarClientes() #Muestra todos los clientes
        try:
            consulta = int(input("ID del cliente que desea consultar: ")) #Selecciona un cliente
            self.Limpiar()
            for cliente in self.clientes:
                if cliente.id == consulta:
                    print(f"================== [{cliente.id}] : {cliente.Nombre} ==================")
                    print(f"================== PRESTAMOS ==================")
                    for prestamos in cliente.Prestamos:
                        prestamos.MostrarPrestamo() #Muestra los prestamos del cliente seleccionado
            input()
            self.Start()
        except:
            print("Cliente invalido")
            self.Start()

    def CancelarPrestamo(self): #Opcion: Cancelar solicitud de Prestamo
        self.Limpiar()
        self.MostrarPrestamos() #Muestra todos los prestamos
        try:
            prestamo = int(input("ID del prestamo que desea cancelar: "))
            for x in self.prestamos:
                if x.Id == prestamo:
                    x.Estado = "CANCELADO" #Cambia el estado del prestamo. Aqui no se vuelve a mostrar ese prestamo, pero queda guardado en los datos como cancelado
                    print(f"El prestamo con el ID {x.Id} fue cancelado")
                    self.JsonProcessor.SaveClient(x.Cliente)
                    input()
                    self.Start()
        
        
        except:
            print("ID del prestamo invalido")
            input()
            self.Start()

    def Salir(self): #Opcion: Salir
        sys.exit()
    #Helpers         


    def Limpiar(self): #Limpiar la consola
        clear = lambda: os.system('cls')
        clear()
    
    def MostrarClientes(self): #Muestra todos los clientes
        print("====================== Clientes ======================")
        if self.clientes:
            for cliente in self.clientes:
                print(cliente.id, cliente.Nombre)
        print("======================================================")
    
    def MostrarPrestamos(self): #Muestra todos los prestamos a excepcion de los cancelados
        print("====================== Prestamos ======================")
        for prestamo in self.prestamos:
            if prestamo.Estado == "CANCELADO":
                continue
            prst: Prestamo = prestamo
            print(f"ID: {prst.Id} Cliente: {prst.Cliente.Nombre} Cantidad: {prst.Monto} Por pagar: {prst.MontoRestante}")
        print("=======================================================")





