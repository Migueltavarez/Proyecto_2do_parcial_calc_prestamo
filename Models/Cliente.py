##Modelo del cliente

class Cliente:
    def __init__(self):
        self.Prestamos = []     #Prestamos del cliente
        self.id        : int    #Id del cliente
        self.Nombre    : str    #Nombre del cliente
    
    def clienteToJson(self):    #Convertir el cliente a formato JSON para guardarlo
        cliente = {
            "Nombre": self.Nombre,
            "ID": self.id,
            "Prestamos": []
        }

        for x in self.Prestamos:
            cliente["Prestamos"].append(x.PrestamoToJson())
        
        return cliente
    