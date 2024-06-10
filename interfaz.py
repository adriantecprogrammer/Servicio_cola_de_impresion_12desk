from email._header_value_parser import ContentTransferEncoding
from tkinter import *

import mysql.connector
from dotenv import load_dotenv
import os
import re
from TicketGenerator import TicketGenerator


# Aqui cargamos los datos del .env
load_dotenv()
data = []



def process_row(row):
    # Acceder a los elementos de la tupla por índice
    id = row[0]
    folio = row[1]
    cliente = row[2]
    nombre = row[3]
    descuento = float(row[5]) if row[5] else 0.0
    cantidad = row[6]
    forma_pago = row[7]
    total = float(row[8]) if row[8] else 0.0
    estatus = row[10]
    observaciones = row[11]
    fecha_hora_creacion = row[12]
    fecha_hora_modificacion = row[13]
    vendedor_id = row[14]
    zona_id = row[15]
    direccion = row[16]
    numero_interior = row[17]
    referencia = row[18]
    colonia = row[19]
    descripcion = row[20]
    latitud = row[21]
    longitud = row[22]

    # Se crea un diccionario para la correcta transformacion de datos
    row_data = {
        "id": id,
        "folio": folio,
        "cliente": cliente,
        "nombre": nombre,
        "descuento": descuento,
        "cantidad": cantidad,
        "forma_pago": forma_pago,
        "total": total,
        "estatus": estatus,
        "observaciones": observaciones,
        "fecha_hora_creacion": fecha_hora_creacion,
        "fecha_hora_modificacion": fecha_hora_modificacion,
        "vendedor_id": vendedor_id,        "zona_id": zona_id,
        "direccion": direccion,
        "numero_interior": numero_interior,
        "referencia": referencia,
        "colonia": colonia,
        "descripcion": descripcion,
        "latitud": latitud,
        "longitud": longitud
    }

    return row_data

def obtenerRegistros():
# Establecer la conexión a la base de datos
 db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    port=int(os.getenv("DB_PORT"))
 )

 # Aqui hacemos la consulta y almacenamos el resultado en una variable, se guardan en tuplas
 cursor = db.cursor()
 cursor.execute("SELECT o.*, d.* FROM Orders o JOIN Direcciones d ON o.address_id = d.iddireccion;")
 resultados = cursor.fetchall()

 # Cerrar la conexión
 cursor.close()
 db.close()
 
 

 # Aqui se almacena la informacion que se transformo de duplas a array
 data.clear()
 for row in resultados:
    row_data = process_row(row)
    data.append(row_data)



ventana = Tk()
ventana.geometry("700x400")
ventana.title("12Desk")

# Este marco es para meter la scrollbar
marco_principal = Frame(ventana)
marco_principal.pack(fill=BOTH, expand=1)

# El canvas es donde va ir el frame con toda la info
canvas = Canvas(marco_principal)
canvas.pack(side=LEFT, fill=BOTH, expand=1)

# Se crea la scrollbar y luego al canvas se le asocia
scrollbar = Scrollbar(marco_principal, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)

# Configuración de canvas y scrollbar
canvas.configure(yscrollcommand=scrollbar.set, xscrollcommand=scrollbar.set)

# Se crea un marco y lo ponemos dentro del canvas
marco_lista = Frame(canvas)
canvas.create_window((0, 0), window=marco_lista, anchor=NW)

def imprimir(datos):
    
    try:
        
     print(f"Imprimiendo {datos["id"]}...")
     ticket_generator = TicketGenerator(
     id_pedido =str(datos["id"]),
     cliente= str(datos["nombre"]),
     monto=str(datos["total"]),
     direccion=str(datos["direccion"])+", "+str(datos["numero_interior"])+", "+str(datos["colonia"]),
     )
     ticket_generator.generar_ticket("ticket.pdf")
    except Exception as e:
        print(f"Error: {str(e)}")
    
def actualizar_labels():
    
    obtenerRegistros()
   
    
    for widget in marco_lista.winfo_children():
        widget.destroy()

    for i, elemento in enumerate(data):
        # Crear un marco para cada elemento
        marco_elemento = Frame(marco_lista, bd=1, relief=SOLID)
        marco_elemento.grid(row=i, column=0, padx=30, pady=10, sticky=W+E)

        # Ancho fijo para los labels
        ancho_fijo = 50

        # Label para el título
        label_titulo = Label(marco_elemento, text="ID: " + str(elemento["id"]), font=("Arial", 12, "bold"), width=ancho_fijo, anchor=W)
        label_titulo.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        
         # Label para el título
        label_titulo = Label(marco_elemento, text="Cliente: " + str(elemento["nombre"]), font=("Arial", 12, "bold"), width=ancho_fijo, anchor=W)
        label_titulo.grid(row=1, column=0, padx=10, pady=10, sticky=W)

        # Label para la descripción
        label_descripcion = Label(marco_elemento, text=elemento["descripcion"], font=("Arial", 10), width=ancho_fijo, anchor=W)
        label_descripcion.grid(row=2, column=0, padx=10, pady=10, sticky=W)

        # Botón para cada elemento
        boton_imprimir = Button(marco_elemento, text="Imprimir", command=lambda datos=elemento: imprimir(datos))
        boton_imprimir.grid(row=0, column=1, rowspan=2, padx=10, pady=10)
        boton_imprimir.config(bg="black", fg="white")

    # Actualizar el área de scroll del canvas
    marco_lista.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

# Crear el botón de Refresh en la parte superior derecha
boton_refresh = Button(ventana, text="Recargar", command=actualizar_labels)
boton_refresh.pack(side=TOP, anchor=NE, padx=10, pady=10)

# Llamar a la función para inicializar los labels
actualizar_labels()

ventana.mainloop()