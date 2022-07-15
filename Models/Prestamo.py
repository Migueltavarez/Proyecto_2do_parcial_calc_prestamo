from .Cliente import Cliente
import datetime


class Prestamo(): #Modelo del Prestamo

    def __init__(self, Monto = 0, TazaDeInteres = 0, Plazo = 0): #Constructor del Prestamo
        self.Id             : int           #Id del prestamo
        self.Cliente        : Cliente       #Cliente dueño del prestamo
        self.Estado         = "ACTIVO"      #Estado del prestamo
        
        self.FechaCreacion  = datetime.date.today()                     #Fecha de creacion del prestamo
        self.Historial      = []                                        #Historial de movimientos del prestamo
        self.Monto          : float = (Monto * TazaDeInteres) + Monto   #Monto total del prestamo
        self.MontoPreTaza   = self.Monto                                #Monto sin taza de interes
        self.Interes        : float                                     #Interes 
        self.TazaDeInteres  : float = TazaDeInteres                     #Taza de interes. % de Interes
        self.Mensualidad    : float                                     #Mensualidad a pagar
        self.Plazo          : int = Plazo                               #Plazo en años a pagar
        self.InteresXCuota  : float                                     #Interes por Cuota
        self.MontoRestante  : float = (Monto * TazaDeInteres) + Monto   #Monto restante a pagar
        
    def Abonar(self, cantidad: float): # Abonar al prestamo
        self.MontoRestante -= cantidad #Quitar cantidad del Monto restante
        if self.MontoRestante < 0:     #Si el monto restante es menor que cero
            self.MontoRestante = 0     #Ponerlo en 0
            self.Estado = "PAGADO"     #Cambiar el estado del pedido a pagado
        self.Historial.append(f"El {datetime.date.today()} {self.Cliente.Nombre} abono {cantidad}") #Agregar al historial el pago

    def ObtenerHistorial(self): #Obtener todo el historial de pagos
        for x in self.Historial:
            print(x)
              
    def PrestamoToJson(self): #Convertir el prestamo a formato JSON para guardar
        prestamo = {
            "ID": self.Id,
            "Estado": self.Estado,
            "Monto": self.Monto,
            "Monto_Restante": self.MontoRestante,
            "Historial": [],
            "Plazo": self.Plazo,
            'fecha_creacion': str(self.FechaCreacion),    
            'TazaDeInteres': self.TazaDeInteres
        }
        for x in self.Historial:
            prestamo['Historial'].append(x)
        return prestamo
    
    def MostrarPrestamo(self): #Mostrar prestamo completo
        print(f"Prestamo: {self.Id}")
        print(f"    Estado: {self.Estado}")
        print(f"    Monto: {self.Monto}")
        print(f"    Monto Restante: {self.MontoRestante}")
        print(f"    Plazo: {self.Plazo}")
        print(f"    Fecha de creacion: {self.FechaCreacion}")
        print(f"    Taza de interes: {self.TazaDeInteres}")
        print(f"                    Historial")
        self.ObtenerHistorial()
        print("===================================================")

    def CancelarPrestamo(self): #Cambiar estado del prestamo
        self.Estado = "CANCELADO"  

    def ImprimirTablaAmortizacion(self): #Imprimir toda la tabla de amortizacion 
        import numpy_financial as npf
        import tabulate as tab

        

        capital = self.Monto
        tasa = self.TazaDeInteres
        plazo = self.Plazo
        cuota = round(npf.pmt(tasa, plazo, -capital, 0), 0)
        datos = []
        datos_num = []
        saldo = capital
        tot_int = 0

        for i in range(1, plazo+1):
            pago_capital = npf.ppmt(tasa, i, plazo, -capital, 0)
            pago_int = cuota - pago_capital
            tot_int += pago_int
            saldo -= pago_capital
            linea = [i, format(cuota, '0,.0f'), format(pago_capital, '0,.0f'), format(pago_int, '0,.0f'), format(saldo, '0,.0f')]
            datos.append(linea)
            linea_num = [i, cuota, pago_capital, pago_int, saldo]
            datos_num.append(linea_num)

        print(tab.tabulate(datos, headers=['Periodo', 'Cuota', 'Capital', 'Intereses', 'saldo'], tablefmt='orgtbl'))
        print('Valor del préstamo:', format(capital, '0,.0f'))
        print('Total intereses a pagar:', format(tot_int, '0,.0f'))
        
