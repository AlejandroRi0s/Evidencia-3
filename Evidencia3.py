import os
from collections import namedtuple
import csv
import pandas as pd
import datetime
import sqlite3
from sqlite3 import Error

#creacion de la base de datos
conexion = sqlite3.connect("BdEvidencia.db")

def menu():
     print('**BIENVENIDO**')
     print('1.Registrar una Venta')
     print('2.Consultar una venta')
     print('3.Reporte de Ventas')
     print('4.Salir')
Diccionario_Ventas = {}
#Diccionario vacio
articulo = namedtuple("articulo","descripcion, piezas, precio")
while True:
    menu()
    opcion = input("SELECCIONE UNA OPCION\n*** ")
    if    opcion == '1':
            print('*Ha seleccionado Registrar una venta:**')
            decision = "1"
            while decision == "1":
                  Folio = int(input("Introduzca su Folio: "))
                  #se verifica que la clave del registro/Folio este en existencia
                  if Folio in Diccionario_Ventas.keys():
                      print("**CLAVE EN EXISTENCIA**")
                      break 
                  else:
                      print("Su clave de registro:{Folio}")
                  Descripcion = input('Caracteristica del articulo:\n')
                  Cantidad_Piezas = input('Numero de piezas deseadas:\n') 
                  Cantidad_Piezas = (int(Cantidad_Piezas))
                  Precio_venta = int(input('Precio de venta del articulo:\n'))
                  print("Procesando registro, espere")
                  Info_Venta = articulo(Descripcion,Cantidad_Piezas,Precio_venta)
                  Diccionario_Ventas[Folio] = Info_Venta
                  #Llenado de informacion al diccionario
                  monto_total = Cantidad_Piezas * Precio_venta
                  IVA = Precio_venta * 0.16
                  print(f'Su monto total a pagar en esta venta es de {monto_total} pesos')
                  print(f"El IVA total del articulo es de {IVA} pesos")
                  #creacion de la tabla asi como su posterior llenado con los datos
                  try:
                      with sqlite3.connect("BdEvidencia.db") as conn:
                          DataBase = conn.cursor()
                          DataBase.execute("CREATE TABLE IF NOT EXISTS COSMETICOS(Descripcion VARCHAR PRIMARY KEY, Cantidad_Piezas Precio_Venta INT );")
                          DataBase.execute("insert into COSMETICOS(descripcion, Cantidad, Precio) values(Descripcion, Cantidad_Piezas,Precio_Venta)")
                  except Error as e:
                      print(e)
                  #primer guardado a un csv
                  with open('articulo.csv', "w", newline='') as archivo:
                      guardado = csv.writer(archivo)
                      guardado.writerow(('Folio','piezas','precio'))
                      guardado.writerows([(Folio, Info_Venta.piezas, Info_Venta.precio) for Folio, Info_Venta in Diccionario_Ventas.items()])
                  decision=input("¿Quiere regsitrar otro articulo? S/N: ")
                  if decision == 'S':
                      Descripcion2 = input('Caracteristica del articulo:\n')
                      Cantidad_Piezas2 = input('Numero de piezas deseadas:\n') 
                      Cantidad_Piezas2 = (int(Cantidad_Piezas2))
                      Precio_venta2 = int(input('Precio de venta del articulo:\n'))
                      Segundo_Registro = articulo(Descripcion2, Cantidad_Piezas2, Precio_venta2)
                      Diccionario_Ventas[Folio] = Segundo_Registro
                      #Segundo llenado de informacion al registro en el diccionario
                      monto_secundario = Cantidad_Piezas2 * Precio_venta2
                      IVA2 = Precio_venta2 * 0.16
                      print("El costo del segundo articulo es", monto_secundario, "Y el Iva respectivamente ", IVA2 )
                      monto_definitivo = monto_secundario + monto_total
                      IVA_definitivo = IVA2 + IVA
                      print("La cantidad a pagar por ambos articulos es de", monto_definitivo, "y el iva de ambos", IVA_definitivo)
                      archivo2 = open('articulo.csv', 'w')
                      #segundo guardado en csv
                      with archivo2:
                          writer = csv.writer(archivo2)
                          writer.writerows(Segundo_Registro)  
                  elif decision == 'N':
                      pass
                
                
    elif  opcion == '2':   
             print('Ha escogido consultar una venta:')
             print("Consultando el registro, espere")
             print(Diccionario_Ventas)
             pass
             #mostrar informacion del diccionario al usuario
    elif opcion == '3':
        ventas_df = pd.read_csv('articulo.csv')
        print(ventas_df)
        print(f"El iva en total es {IVA}")
        fecha = datetime.date.today()
        print(fecha)
        #mostrar la informacion en su totalidad
        pass
        
    elif  opcion == '4':
             print('Has elegido, Salir del programa')
             break
    else:
           print("No es una opcion valida, intente de nuevo")