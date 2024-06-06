
from tkinter import *

ventana = Tk()
ventana.geometry("500x400")
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

# Cinfiguracion de canvas y scrollbar
canvas.configure(yscrollcommand=scrollbar.set, xscrollcommand=scrollbar.set)

# Se crea un marco y lo ponemos dentro del canvas
marco_lista = Frame(canvas)
canvas.create_window((1, 1), window=marco_lista, anchor=NW)

# Estos nomas son de prueba
elementos = [
    {"titulo": "Elemento 1", "descripcion": "Descripción del elemento 1"},
    {"titulo": "Elemento 2", "descripcion": "Descripción del elemento 2"},
    {"titulo": "Elemento 3", "descripcion": "Descripción del elemento 3"},
    {"titulo": "Elemento 3", "descripcion": "Descripción del elemento 3"},
    {"titulo": "Elemento 3", "descripcion": "Descripción del elemento 3"},
    {"titulo": "Elemento 3", "descripcion": "Descripción del elemento 3"},
    {"titulo": "Elemento 3", "descripcion": "Descripción del elemento 3"},
    {"titulo": "Elemento 3", "descripcion": "Descripción del elemento 3"},
    # Agrega más elementos aquí
]


def imprimir(titulo):
    print(f"Imprimiendo {titulo}...")

# Generar labels y botones para cada elemento de la lista
for i, elemento in enumerate(elementos):
    # Crear un marco para cada elemento
    marco_elemento = Frame(marco_lista, bd=1, relief=SOLID)
    marco_elemento.grid(row=i, column=0, padx=20, pady=10, sticky=W+E)

    # Label para el título
    label_titulo = Label(marco_elemento, text=elemento["titulo"], font=("Arial", 12, "bold"))
    label_titulo.grid(row=0, column=0, padx=10, pady=10, sticky=W)

    # Label para la descripción
    label_descripcion = Label(marco_elemento, text=elemento["descripcion"], font=("Arial", 10))
    label_descripcion.grid(row=1, column=0, padx=10, pady=10, sticky=W)

    # Botón "Imprimir" para cada elemento
    boton_imprimir = Button(marco_elemento, text="Imprimir", command=lambda titulo=elemento["titulo"]: imprimir(titulo))
    boton_imprimir.grid(row=0, column=1, rowspan=2, padx=10, pady=10)
    boton_imprimir.config(bg="black", fg="white")

# Configurar el tamaño del canvas y hacer que el marco_lista se ajuste al tamaño del canvas
marco_lista.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

ventana.mainloop()