import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os
import mysql.connector
from RPCServer import RPCServer
from TicketGenerator import TicketGenerator
from dotenv import load_dotenv
import requests #Este es para jalar la data del endpoint
import json #este es para manipular el json


data = []

load_dotenv()

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

    # Se crea un diccionario para la correcta transformación de datos
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
        "vendedor_id": vendedor_id,
        "zona_id": zona_id,
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

    try:
        url = "https://n8nptor10.terio.xyz/webhook/ordersGetByDealerPhone"
        response = requests.get(url)

        if response.status_code == 200:
            json_data = response.text
            array = json.loads(json_data)
            lista = array['orders']
            for order in lista:
                #print(f"ID: {order['id']}, Nombre: {order['nombre']}, Total: {order['total']}")
                data.append(order)
            #print("arreglo"+str(data))
        else:
            print(f"Error: {response.status_code}")
        return data
    except Exception as e:
        print(f"Error: {str(e)}")
        messagebox.showinfo("Error", "Error al conectar")

def imprimir(datos):
    try:
        print(f"Imprimiendo {datos['id']}...")
        ticket_generator = TicketGenerator(
            id_pedido=str(datos["id"]),
            cliente=str(datos["nombre"]),
            monto=str(datos["total"]),
            direccion=str(datos["calle"]) + ", " + str(datos["numero_exterior"]),
            colonia=str(datos["colonia"])
            
        )
       
        ticket_generator.generar_ticket("ticket.pdf")
        messagebox.showinfo("Información", "Pdf creado correctamente")
    except Exception as e:
        print(f"Error: {str(e)}")
        messagebox.showinfo("Error", "Error al crear pdf")

def actualizar_labels():
    obtenerRegistros()
    for widget in marco_lista.winfo_children():
        widget.destroy()

    for i, elemento in enumerate(data):
        # Crear un marco para cada elemento con fondo #0D1A68
        marco_elemento = tk.Frame(marco_lista, bd=1, relief=tk.SOLID, bg="#0D1A68")
        marco_elemento.grid(row=i, column=0, padx=30, pady=10, sticky=tk.W + tk.E)

        # Ancho fijo para los labels
        ancho_fijo = 50

        # Color de fondo para los labels
        label_bg_color = "#0D1A68"
        label_fg_color = "white"

        # Label para el ID
        label_id = tk.Label(marco_elemento, text="ID: " + str(elemento["id"]), font=("Arial", 12, "bold"), width=ancho_fijo, anchor=tk.W, bg=label_bg_color, fg=label_fg_color)
        label_id.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        
        # Label para el nombre del cliente
        label_cliente = tk.Label(marco_elemento, text="Cliente: " + str(elemento["nombre"]), font=("Arial", 10, "bold"), width=ancho_fijo, anchor=tk.W, bg=label_bg_color, fg=label_fg_color)
        label_cliente.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        
        # Label para el total
        label_total = tk.Label(marco_elemento, text="Total: $" + str(elemento["total"]), font=("Arial", 14, "bold"), width=ancho_fijo, anchor=tk.W, bg=label_bg_color, fg=label_fg_color)
        label_total.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

        # Label para la descripción
        label_descripcion = tk.Label(marco_elemento, text=elemento["referencia"], font=("Arial", 10), width=ancho_fijo, anchor=tk.W, bg=label_bg_color, fg=label_fg_color)
        label_descripcion.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)

        # Botón para cada elemento
        boton_imprimir = tk.Button(marco_elemento, text="Imprimir", command=lambda datos=elemento: imprimir(datos), bg="#00CB5C", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5)
        boton_imprimir.grid(row=0, column=1, rowspan=2, padx=10, pady=10)

    # Actualizar el área de scroll del canvas
    marco_lista.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

ventana = tk.Tk()
ventana.geometry("900x500")
ventana.title("12Desk")
#ventana.iconbitmap("logo.png")

# Este marco es para meter la scrollbar
marco_principal = tk.Frame(ventana)
marco_principal.pack(fill=tk.BOTH, expand=1)

# El canvas es donde va a ir el frame con toda la info
canvas = tk.Canvas(marco_principal)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# Se crea la scrollbar y luego al canvas se le asocia
scrollbar = tk.Scrollbar(marco_principal, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configuración de canvas y scrollbar
canvas.configure(yscrollcommand=scrollbar.set, xscrollcommand=scrollbar.set)

# Se crea un marco y lo ponemos dentro del canvas
marco_lista = tk.Frame(canvas)
canvas.create_window((0, 0), window=marco_lista, anchor=tk.NW)

# Cambiar el color de la scrollbar
style = ttk.Style()
style.configure("TScrollbar", troughcolor="#00CB5C", background="#00CB5C", arrowcolor="white", bordercolor="#00CB5C")

boton_refresh = tk.Button(ventana, text="Recargar", command=actualizar_labels, bg="#00CB5C", fg="white", font=("Arial", 14, "bold"), padx=8, pady=4)
boton_refresh.pack(side=tk.TOP, anchor=tk.NE, padx=8, pady=4)

# Función para iniciar el servidor RPC en un hilo separado
def iniciar_rpc():
 try:
    rpc_server = RPCServer()
    rpc_thread = threading.Thread(target=rpc_server.run, daemon=True)
    rpc_thread.start()
 except Exception as e:
     print(f"Error: {str(e)}")
     messagebox.showinfo("Error", "Error de conexion") 
     
     

# Iniciar el servidor RPC
iniciar_rpc()

# Cargar datos iniciales
actualizar_labels()

ventana.mainloop()
