
import json
from multiprocessing.connection import Client
from typing import List
from Models.Cliente import Cliente
from Models.Prestamo import Prestamo

class JsonProcessor(): #Procesador de data persistency (Para guardar datos)
    def __init__(self) -> None: 
        self.ClientesJson = "Data/Clientes.json" #Archivo
        self.Clientes = []                       #Clientes registrados (Esto es un JSON)
        self.LoadData()                          #Cargar Datos. ir a LoadData()

    def LoadData(self): #Lee los datos de los clientes
        with open(self.ClientesJson, 'rb') as clientes:
            self.Clientes = json.load(clientes)


    def getAllClients(self) -> List[Cliente]: #Obtiene todos los clientes del JSON y los transforma a objetos de Python
        Clientes = []
        if self.Clientes['Clientes']:
            for clientes in self.Clientes['Clientes']:
                client = Cliente()
                client.id = clientes['ID']
                client.Nombre = clientes['Nombre']
                for prestamos in clientes['Prestamos']:
                    prestamo = Prestamo()
                    prestamo.Cliente = client
                    prestamo.Estado = prestamos['Estado']
                    prestamo.FechaCreacion = prestamos['fecha_creacion']
                    prestamo.Id = prestamos['ID']
                    prestamo.Monto = prestamos['Monto']
                    prestamo.MontoRestante = prestamos['Monto_Restante']
                    prestamo.Plazo = prestamos['Plazo']
                    prestamo.Historial = prestamos['Historial']
                    prestamo.TazaDeInteres = prestamos['TazaDeInteres']
                    client.Prestamos.append(prestamo)
                Clientes.append(client)
        return Clientes


    def SaveClient(self, cliente: Cliente): #Guarda un nuevo cliente, y si existe lo actualiza
        self.LoadData() #Carga los datos actuales
        if not self.Clientes['Clientes']: #Si no hay clientes
            self.Clientes['Clientes'].append(cliente.clienteToJson()) #Crea un nuevo cliente
            with open(self.ClientesJson, 'w') as clientes:
                clientes.write(json.dumps(self.Clientes, indent = 4)) #Guarda los datos
                return 

        for enum, x in enumerate(self.Clientes['Clientes']): #Si hay clientes. enum: Numerador del iterador. x: dato del cliente
            if x['ID'] == cliente.id: #Si el cliente existe
                self.UpdateClient(enum, cliente) #Actualizar cliente
                break
            else:
                self.Clientes['Clientes'].append(cliente.clienteToJson()) #Si no existe, crear nuevo cliente
                with open(self.ClientesJson, 'w') as clientes:
                    clientes.write(json.dumps(self.Clientes, indent = 4))#Guardar los datos
                break

    def UpdateClient(self, index, Client: Cliente): #Actualiza el cliente
        self.Clientes['Clientes'][index] = Client.clienteToJson() #Actualiza el cliente por el index

        with open('Data/Clientes.json', 'w') as file:
            json.dump(self.Clientes, file, indent = 4)
            
        
    

